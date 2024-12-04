import streamlit as st
from src.utils.initialization import initialize_session_state
from src.utils.error_handling import handle_streamlit_errors
import torch
import torchaudio
import os
from datetime import datetime
import time
from transformers import AutoModelForAudioClassification, AutoProcessor
import torchaudio.transforms as T

from src.core.services.chatbot_service import ChatbotService
from src.app.config import OpenAIConfig
from src.utils.audio_handler import process_recorded_audio, predict_audio_emotion, AudioRecorder
from src.components.message_display import apply_chat_styles, display_message, get_emotion_color
from src.core.services.personas import PERSONAS
from src.utils.state_management import (
    initialize_session_state, 
    clear_session_state, 
    ensure_state_initialization
)
from src.components.chat_components import (
    render_emotion_indicator,
    render_conversation_stats
)
from src.app.constants import (
    DEFAULT_PERSONA, 
    DEFAULT_EMOTION, 
    EMOTIONS,
    EMOTION_MAPPING,
    PERSONA_NAME_MAPPING
)

# 음성 감정 인식 모델 설정
MODEL_NAME = "forwarder1121/ast-finetuned-model"
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)

AUDIO_ENABLED = True
try:
    from src.utils.audio_handler import process_recorded_audio, predict_audio_emotion, AudioRecorder
except ImportError:
    AUDIO_ENABLED = False
    st.warning("Audio functionality is disabled. Please install required dependencies.")

def get_emotion_from_gpt(prompt: str) -> str:
    """
    GPT를 통해 텍스트의 감정을 분석합니다.
    
    Args:
        prompt (str): 분석할 텍스트
        
    Returns:
        str: 감지된 감정 (Anger, Disgust, Fear, Happy, Neutral, Sad 중 하나)
    """
    predefined_emotions = list(EMOTION_MAPPING.values())
    emotion_prompt = (
        f"The user said: \"{prompt}\".\n"
        f"Classify the user's input into one of these emotions: {', '.join(predefined_emotions)}.\n"
        f"Respond ONLY with the emotion name (e.g., Happy, Neutral).\n"
    )

    response = st.session_state.chatbot_service.llm.invoke(emotion_prompt)
    detected_emotion = response.content.strip()

    if detected_emotion not in predefined_emotions:
        detected_emotion = DEFAULT_EMOTION

    return detected_emotion

def process_audio(waveform: torch.Tensor, target_sample_rate: int = 16000, target_length: int = 16000) -> torch.Tensor:
    """Process audio to correct format."""
    try:
        if waveform.shape[0] > 1:  # 다채널 오디오인 경우 평균 처리
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        if waveform.shape[1] > 0:
            current_sample_rate = target_sample_rate
            if current_sample_rate != target_sample_rate:
                resampler = T.Resample(orig_freq=current_sample_rate, new_freq=target_sample_rate)
                waveform = resampler(waveform)

        if waveform.shape[1] < target_length:
            padding_length = target_length - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding_length))
        else:
            start = (waveform.shape[1] - target_length) // 2
            waveform = waveform[:, start:start + target_length]

        return waveform
    except Exception as e:
        st.error(f"Error in audio processing: {str(e)}")
        return None

def predict_audio_emotion(audio_path: str) -> str:
    """Predict emotion from audio file."""
    try:
        waveform, sample_rate = torchaudio.load(audio_path)
        processed_waveform = process_audio(waveform)
        if processed_waveform is None:
            return None

        inputs = processor(processed_waveform.squeeze(), sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        predicted_class_idx = outputs.logits.argmax(-1).item()
        return EMOTION_MAPPING.get(predicted_class_idx, DEFAULT_EMOTION)

    except Exception as e:
        st.error(f"감정 분석 중 오류 발생: {str(e)}")
        return None

def handle_chat_message(prompt: str, current_persona: str) -> tuple:
    """
    채팅 메시지를 처리하고 응답을 생성합니다.
    """
    # 감정 분석
    user_emotion = get_emotion_from_gpt(prompt)
    st.session_state.current_emotion = user_emotion
    
    # GPT 응답 생성
    response = st.session_state.chatbot_service.get_response(prompt, current_persona)
    
    return user_emotion, response

def add_chat_message(role: str, content: str, emotion: str = None):
    """
    채팅 메시지를 대화 기록에 추가합니다.
    """
    current_time = datetime.now().strftime('%p %I:%M')
    message = {
        "role": role,
        "content": content,
        "timestamp": current_time
    }
    if emotion:
        message["emotion"] = emotion
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.append(message)

def update_conversation_stats(emotion: str):
    """
    대화 통계를 업데이트합니다.
    
    Args:
        emotion (str): 감지된 감정
    """
    if 'conversation_stats' not in st.session_state:
        st.session_state.conversation_stats = {
            'total': 0,
            'positive': 0,
            'negative': 0
        }
    
    # 전체 대화 수 증가
    st.session_state.conversation_stats['total'] += 1
    
    # 감정에 따른 통계 업데이트
    positive_emotions = ['Happy']
    negative_emotions = ['Anger', 'Disgust', 'Fear', 'Sad']
    
    if emotion in positive_emotions:
        st.session_state.conversation_stats['positive'] += 1
    elif emotion in negative_emotions:
        st.session_state.conversation_stats['negative'] += 1

def render_chat_area():
    """채팅 영역을 렌더링합니다."""
    st.title("채팅")

    # 세션 상태 확인
    if not st.session_state.get('initialized') or 'selected_persona' not in st.session_state:
        return

    # 메시지 표시
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # 스타일 적용
    apply_chat_styles()
    
    # 메시지 컨테이너
    messages_container = st.container()
    with messages_container:
        for message in st.session_state.messages:
            display_message(message, persona=st.session_state.selected_persona)

    # 채팅 입력 처리
    col1, col2, col3 = st.columns([8, 1.2, 1.2])
    
    with col1:
        chat_input = st.text_input("메시지를 입력하세요...", key="chat_input", label_visibility="collapsed")
    
    with col2:
        if AUDIO_ENABLED:
            # 녹음 상태 초기화
            if 'is_recording' not in st.session_state:
                st.session_state.is_recording = False
                
            # 마이크 버튼
            mic_clicked = st.button(
                "⏺️ 녹음 중지" if st.session_state.is_recording else "🎤 음성 입력",
                help="클릭하여 녹음 시작/중지",
                key="mic_button"
            )
            
            if mic_clicked:
                if not st.session_state.is_recording:
                    # 녹음 시작
                    st.session_state.is_recording = True
                    st.session_state.audio_recorder = AudioRecorder()
                    st.session_state.audio_recorder.start_recording()
                    st.rerun()
                else:
                    # 녹음 중지 및 처리
                    st.session_state.is_recording = False
                    audio_text, audio_emotion = process_recorded_audio()
                    
                    if audio_text:
                        # 현재 상태 저장
                        current_persona = st.session_state.selected_persona
                        
                        # GPT 응답 생성
                        response = st.session_state.chatbot_service.get_response(audio_text, current_persona)
                        
                        # 대화 통계 업데이트
                        update_conversation_stats(audio_emotion)
                        
                        # 메시지 추가
                        add_chat_message("user", f"[음성] {audio_text}", audio_emotion)
                        add_chat_message("assistant", response)
                        
                        # 상태 업데이트
                        st.session_state.current_emotion = audio_emotion
                        st.session_state.last_message = audio_text
                        st.rerun()
                    else:
                        st.error("음성을 인식할 수 없습니다. 다시 시도해주세요.")
                        st.session_state.is_recording = False
                        st.rerun()
        else:
            # 오디오 기능이 비활성화된 경우 버튼을 비활성화 상태로 표시
            st.button("🎤 음성 입력", disabled=True, help="음성 입력 기능을 사용할 수 없습니다")
    
    with col3:
        send_clicked = st.button("전송", use_container_width=True)
    
    # 새 메시지가 있고 아직 처리되지 않았다면
    if (send_clicked or chat_input) and chat_input.strip() and chat_input != st.session_state.get('last_message'):
        try:
            # 현재 상태 저장
            current_persona = st.session_state.selected_persona
            
            # 챗봇 서비스 확인
            if 'chatbot_service' not in st.session_state:
                initialize_session_state(current_persona)
            
            # 메시지 처리
            user_emotion, response = handle_chat_message(chat_input, current_persona)
            
            # 대화 통계 업데이트
            update_conversation_stats(user_emotion)
            
            # 메시지 추가
            add_chat_message("user", chat_input, user_emotion)
            add_chat_message("assistant", response)
            
            # 상태 업데이트
            st.session_state.messages = st.session_state.messages
            st.session_state.current_emotion = user_emotion
            st.session_state.last_message = chat_input
            
            # 화면 갱신을 위한 플래그 설정
            st.session_state.needs_rerun = True
            
        except Exception as e:
            st.error(f"메시지 처리 중 오류가 발생했습니다: {str(e)}")

    # 화면 갱신이 필요한 경우
    if st.session_state.get('needs_rerun', False):
        st.session_state.needs_rerun = False
        time.sleep(0.1)  # 약간의 지연을 추가하여 상태 업데이트 보장
        st.rerun()

def render_chat_page():
    """채팅 페이지를 렌더링합니다."""
    # URL에서 영어 페르소나 이름 가져오기
    persona_url = st.query_params.get("persona")
    
    # 페르소나가 없으면 홈으로 리다이렉트
    if not persona_url:
        st.query_params["page"] = "home"
        st.rerun()
        return
    
    # URL의 영어 이름을 한글 페르소나 이름으로 변환
    selected_persona = PERSONA_NAME_MAPPING.get(persona_url, DEFAULT_PERSONA)
    
    # 페르소나가 변경되었거나 초기화되지 않은 경우에만 상태 초기화
    if (not st.session_state.get('initialized') or 
        st.session_state.get('selected_persona') != selected_persona):
        # 채팅 기록 유지를 위한 임시 저장
        old_messages = st.session_state.get('messages', [])
        
        # 상태 초기화
        clear_session_state()
        
        # 새로운 페르소나로 초기화
        initialize_session_state(selected_persona)
        
        # 이전 채팅 기록 복원 (필요한 경우)
        if old_messages and st.session_state.get('selected_persona') == selected_persona:
            st.session_state.messages = old_messages
    
    # URL 파라미터 설정
    st.query_params["page"] = "chat"
    st.query_params["persona"] = persona_url
    
    render_sidebar()
    render_chat_area()

def render_sidebar():
    """사이드바를 렌더링합니다."""
    with st.sidebar:
        st.title("감정인식 챗봇 🏠")
        
        # 홈으로 돌아가기 버튼
        if st.button("← 다른 페르소나 선택하기", key="change_persona_button"):
            # 세션 상태 완전 초기화
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            
            # URL 파라미터 초기화
            for param in list(st.query_params.keys()):
                del st.query_params[param]
            
            # 홈 페이지로 이동하기 위한 파라미터 설정
            st.query_params["page"] = "home"
            st.rerun()
            return

        st.markdown("### 사용 방법")
        st.markdown("""
        1. 채팅창에 현재 기분이나 상황을 입력하세요.
        2. 마이크 버튼을 눌러 음성으로 대화할 수 있습니다.
        3. 챗봇이 감정을 분석하고 공감적인 대화를 제공합니다.
        4. 필요한 경우 적절한 조언이나 위로를 받을 수 있습니다.
        """)

        # 현재 페르소나 표시
        current_persona = st.session_state.get('selected_persona', st.query_params.get("persona"))
        st.markdown(f"### 현재 대 상대: {current_persona}")

        # 상태 초기화 및 표시
        ensure_state_initialization('current_emotion', DEFAULT_EMOTION)
        ensure_state_initialization('conversation_stats', {'total': 0, 'positive': 0, 'negative': 0})
        render_emotion_indicator(st.session_state.current_emotion)
        render_conversation_stats(st.session_state.conversation_stats)

def main():
    """메인 애플리케이션을 실행합니다."""
    # 페이지 설정
    st.set_page_config(
        page_title="감정인식 챗봇",
        page_icon="🤗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 페재 페이지 확인
    current_page = st.query_params.get("page", "home")
    
    # 페이지 라우팅
    if current_page == "chat":
        render_chat_page()
    else:
        from src.app.home import render_home
        render_home()

if __name__ == "__main__":
    main()
