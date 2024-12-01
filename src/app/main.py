import streamlit as st
import torch
import torchaudio
import os
<<<<<<< HEAD
from transformers import AutoModelForAudioClassification, AutoProcessor
import torchaudio.transforms as T
=======
from datetime import datetime
import time
from transformers import AutoModelForAudioClassification, AutoProcessor
import torchaudio.transforms as T

>>>>>>> 7b5f7e1 (feat: 대화 통계 기능 추가 및 페르소나 전환 버그 수정)
from src.core.services.chatbot_service import ChatbotService
from src.app.config import OpenAIConfig
from src.utils.audio_handler import process_audio_file
from src.components.message_display import apply_chat_styles, display_message, get_emotion_color
from src.core.services.personas import PERSONAS
<<<<<<< HEAD

# 음성 감정 인식 모델 설정
model_name = "forwarder1121/ast-finetuned-model"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForAudioClassification.from_pretrained(model_name)

# 감정 매핑
EMOTION_MAPPING = {
    0: "Anger",
    1: "Disgust", 
    2: "Fear",
    3: "Happy",
    4: "Neutral",
    5: "Sad"
}


def get_emotion_from_gpt(prompt: str) -> str:
    """
    GPT를 통해 텍스트 감정을 추론하고 표준화된 값 반환.
    """
    predefined_emotions = ["Anger", "Disgust", "Fear", "Happy", "Neutral", "Sad"]
    emotion_prompt = (
        f"The user said: \"{prompt}\".\n"
        f"Classify the user's input into one of these emotions: {', '.join(predefined_emotions)}.\n"
        f"Respond ONLY with the emotion name (e.g., Happy, Neutral).\n"
    )

    # OpenAI API 호출
    response = st.session_state.chatbot_service.llm.invoke(emotion_prompt)
    detected_emotion = response.content.strip()  # 응답에서 감정 추출
    print(f"[DEBUG] Detected Emotion: {detected_emotion}")

    if detected_emotion not in predefined_emotions:
        print(f"[DEBUG] Unexpected emotion: {detected_emotion}")
        detected_emotion = "Neutral"  # 기본값 설정

    return detected_emotion


def process_audio(waveform, target_sample_rate=16000, target_length=16000):
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


def predict_audio_emotion(audio_path):
    """Predict emotion from audio file."""
    try:
        # 오디오 로드
        waveform, sample_rate = torchaudio.load(audio_path)
        print(f"[DEBUG] 오디오 로드 완료: Waveform Shape: {waveform.shape}, Sample Rate: {sample_rate}")

        # 오디오 전처리
        processed_waveform = process_audio(waveform, target_sample_rate=16000)
        if processed_waveform is None:
            print("[ERROR] 오디오 전처리 실패")
            return None
        print(f"[DEBUG] 전처리된 Waveform Shape: {processed_waveform.shape}")

        # 모델 입력 생성
        inputs = processor(processed_waveform.squeeze(), sampling_rate=16000, return_tensors="pt")
        print(f"[DEBUG] 모델 입력 생성 완료: {inputs.keys()}")

        # 모델 예측
        with torch.no_grad():
            outputs = model(**inputs)
        print(f"[DEBUG] 모델 출력: {outputs.logits}")

        # 예측된 감정 인덱스
        predicted_class_idx = outputs.logits.argmax(-1).item()
        print(f"[DEBUG] 감정 분석 결과 Index: {predicted_class_idx}")

        # 감정 매핑
        emotion = EMOTION_MAPPING.get(predicted_class_idx, "Unknown")
        print(f"[DEBUG] 감정 분석 결과 Emotion: {emotion}")
        return emotion

    except Exception as e:
        print(f"[ERROR] 감정 분석 중 오류 발생: {e}")
        return None


def handle_audio_upload(uploaded_audio):
    """
    음성 파일 업로드 핸들러
    """
    temp_audio_path = "temp_audio.wav"
    try:
        with open(temp_audio_path, "wb") as f:
            f.write(uploaded_audio.getbuffer())

        print(f"[DEBUG] 임시 파일 저장 완료: {temp_audio_path}")

        # 음성 -> 텍스트 변환
        with st.spinner("음성을 텍스트로 변환 중..."):
            audio_text = process_audio_file(uploaded_audio.read(), temp_audio_path)
            if not audio_text:
                st.warning("음성에서 텍스트를 감지할 수 없습니다.")
                return

        # 감정 분석
        with st.spinner("감정 분석 중..."):
            audio_emotion = predict_audio_emotion(temp_audio_path)
            if not audio_emotion:
                st.warning("음성 감정을 분석할 수 없습니다.")
                return

        # 감정 상태 업데이트
        st.session_state.current_emotion = audio_emotion
        update_conversation_stats(audio_emotion)  # 대화 통계 업데이트

        # 선택된 페르소나 가져오기
        persona_name = st.session_state.get("selected_persona", "김소연 선생님")

        # GPT 응답 생성
        with st.spinner("GPT 응답 생성 중..."):
            gpt_prompt = (
                f"The user uploaded an audio file. Here is the transcribed text: '{audio_text}'.\n"
                f"The detected emotion is '{audio_emotion}'.\n"
                f"Respond to the user in the selected persona: {persona_name}."
            )
            chatbot = st.session_state.chatbot_service
            gpt_response = chatbot.get_response(gpt_prompt, persona_name)

        # 메시지 업데이트
        current_time = datetime.now().strftime('%p %I:%M')
        st.session_state.messages.append({
            "role": "user",
            "content": f"[음성 파일] 텍스트: {audio_text}",
            "emotion": audio_emotion,
            "timestamp": current_time
        })
        st.session_state.messages.append({
            "role": "assistant",
            "content": gpt_response,
            "timestamp": current_time
        })

        print("[DEBUG] 메시지 업데이트 완료")

    except Exception as e:
        st.error(f"오류 발생: {e}")
        print(f"[ERROR] handle_audio_upload에서 오류 발생: {e}")

    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print(f"[DEBUG] 임시 파일 삭제 완료: {temp_audio_path}")

        # UI 강제 갱신
        st.rerun()


# def handle_audio_upload(uploaded_audio):
#     """
#     음성 파일 업로드 핸들러
#     """
#     temp_audio_path = "temp_audio.wav"
#     try:
#         # 임시 파일 저장
#         with open(temp_audio_path, "wb") as f:
#             f.write(uploaded_audio.getbuffer())

#         print(f"[DEBUG] 임시 파일 저장 완료: {temp_audio_path}")

#         # 텍스트 변환
#         with st.spinner("텍스트 변환 중..."):
#             audio_text = process_audio_file(uploaded_audio.read(), temp_audio_path)
#             if not audio_text:
#                 st.warning("음성에서 텍스트를 감지할 수 없습니다.")
#                 return

#         # 감정 분석
#         with st.spinner("감정 분석 중..."):
#             audio_emotion = predict_audio_emotion(temp_audio_path)
#             if not audio_emotion:
#                 st.warning("음성 감정을 분석할 수 없습니다.")
#                 return

#         # 결과 업데이트
#         current_time = datetime.now().strftime('%p %I:%M')
#         st.session_state.messages.append({
#             "role": "user",
#             "content": f"[음성 파일] 텍스트: {audio_text}",
#             "emotion": audio_emotion,
#             "timestamp": current_time
#         })
#         st.session_state.messages.append({
#             "role": "assistant",
#             "content": f"음성에서 '{audio_text}'를 감지했으며, 감정은 '{audio_emotion}'입니다.",
#             "timestamp": current_time
#         })

#         update_conversation_stats(audio_emotion)
#         print("[DEBUG] 메시지 업데이트 완료")

#     except Exception as e:
#         st.error(f"오류 발생: {e}")
#         print(f"[ERROR] handle_audio_upload에서 오류 발생: {e}")

#     finally:
#         # 모든 작업이 끝난 후 파일 삭제
#         if os.path.exists(temp_audio_path):
#             os.remove(temp_audio_path)
#             print(f"[DEBUG] 임시 파일 삭제 완료: {temp_audio_path}")



def update_conversation_stats(emotion: str):
    """Update conversation statistics based on the detected emotion."""
    st.session_state.conversation_stats['total'] += 1
    if emotion in ['Happy', 'Neutral']:
        st.session_state.conversation_stats['positive'] += 1
    elif emotion in ['Anger', 'Disgust', 'Fear', 'Sad']:
        st.session_state.conversation_stats['negative'] += 1

def main():
    st.set_page_config(
        page_title="감정인식 챗봇",
        page_icon="🤗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 상태 초기화
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.chatbot_service = ChatbotService(OpenAIConfig())
        st.session_state.messages = [{
            'role': 'assistant',
            'content': "안녕하세요! 오늘 하루는 어떠셨나요? 기분이나 감정을 자유롭게 이야기해주세요. 텍스트로 입력하거나 음성 파일을 업로드해주세요. 😊",
            'timestamp': datetime.now().strftime('%p %I:%M')
        }]
        st.session_state.last_uploaded_audio = None
        st.session_state.current_emotion = "Neutral"
=======
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
    EMOTION_MAPPING
)

# 음성 감정 인식 모델 설정
MODEL_NAME = "forwarder1121/ast-finetuned-model"
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)

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
    """
    오디오 데이터를 모델 입력에 맞게 전처리합니다.
    
    Args:
        waveform (torch.Tensor): 입력 오디오 데이터
        target_sample_rate (int): 목표 샘플링 레이트
        target_length (int): 목표 길이
        
    Returns:
        torch.Tensor: 전처리된 오디오 데이터
    """
    try:
        # 다채널 오디오를 모노로 변환
        if waveform.shape[0] > 1:
            waveform = torch.mean(waveform, dim=0, keepdim=True)

        # 샘플링 레이트 조정
        if waveform.shape[1] > 0:
            current_sample_rate = target_sample_rate
            if current_sample_rate != target_sample_rate:
                resampler = T.Resample(orig_freq=current_sample_rate, new_freq=target_sample_rate)
                waveform = resampler(waveform)

        # 길이 조정
        if waveform.shape[1] < target_length:
            padding_length = target_length - waveform.shape[1]
            waveform = torch.nn.functional.pad(waveform, (0, padding_length))
        else:
            start = (waveform.shape[1] - target_length) // 2
            waveform = waveform[:, start:start + target_length]

        return waveform
    except Exception as e:
        st.error(f"오디오 처리 중 오류 발생: {str(e)}")
        return None

def predict_audio_emotion(audio_path: str) -> str:
    """
    오디오 파일에서 감정을 예측합니다.
    
    Args:
        audio_path (str): 오디오 파일 경로
        
    Returns:
        str: 예측된 감정
    """
    try:
        # 오디오 로드 및 전처리
        waveform, sample_rate = torchaudio.load(audio_path)
        processed_waveform = process_audio(waveform)
        if processed_waveform is None:
            return None

        # 모델 입력 생성 및 예측
        inputs = processor(processed_waveform.squeeze(), sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)

        # 예측 결과 변환
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

def render_chat_area():
    """채팅 영역을 렌더링합니다."""
    st.title("채팅")

    # 메시지 표시
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            display_message(message, persona=st.session_state.selected_persona)

    # 채팅 입력 처리
    if prompt := st.chat_input("메시지를 입력하세요..."):
        if prompt.strip():
            try:
                # 현재 상태 저장
                current_persona = st.session_state.selected_persona
                
                # 챗봇 서비스 확인
                if 'chatbot_service' not in st.session_state:
                    initialize_session_state(current_persona)
                
                # 메시지 처리
                user_emotion, response = handle_chat_message(prompt, current_persona)
                
                # 대화 통계 업데이트
                update_conversation_stats(user_emotion)
                
                # 메시지 추가
                add_chat_message("user", prompt, user_emotion)
                add_chat_message("assistant", response)
                
                # 세션 상태에 처리 완료 표시
                st.session_state.processed = True
                
            except Exception as e:
                st.error(f"메시지 처리 중 오류가 발생했습니다: {str(e)}")
    
    # 메시지 처리 후 화면 갱신
    if st.session_state.get('processed', False):
        st.session_state.processed = False
        st.rerun()

def render_chat_page():
    """채팅 페이지를 렌더링합니다."""
    selected_persona = st.query_params.get("persona")
    
    # 세션 상태 초기화가 필요한 경우
    if ('initialized' not in st.session_state or 
        'selected_persona' not in st.session_state or 
        st.session_state.selected_persona != selected_persona):
        clear_session_state()
        initialize_session_state(selected_persona)
    
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
            st.query_params.clear()
            st.query_params["page"] = "home"  # 홈 페이지로 이동
            st.rerun()

        st.markdown("### 사용 방법")
        st.markdown("""
        1. 채팅창에 현재 기분이나 상황을 입력하세요.
        2. 음성 파일을 업로드하여 감정을 분석할 수 있습니다.
        3. 챗봇이 감정을 분석하고 공감적인 대화를 제공합니다.
        4. 필요한 경우 적절한 조언이나 위로를 받을 수 있습니다.
        """)

        # 현재 페르소나 표시
        current_persona = st.session_state.get('selected_persona', st.query_params.get("persona"))
        st.markdown(f"### 현재 대화 상대: {current_persona}")

        # 상태 초기화 및 표시
        ensure_state_initialization('current_emotion', DEFAULT_EMOTION)
        ensure_state_initialization('conversation_stats', {'total': 0, 'positive': 0, 'negative': 0})
        render_emotion_indicator(st.session_state.current_emotion)
        render_conversation_stats(st.session_state.conversation_stats)

        # 음성 파일 업로드
        st.markdown("### 음성 파일 업로드")
        uploaded_audio = st.file_uploader("지원 형식: WAV", type=["wav"])
        if uploaded_audio is not None and uploaded_audio != st.session_state.get('last_uploaded_audio'):
            st.session_state.last_uploaded_audio = uploaded_audio
            handle_audio_upload(uploaded_audio)

def update_conversation_stats(emotion: str):
    """
    대화 통계를 업데이트합니다.
    
    Args:
        emotion (str): 감지된 감정
    """
    if 'conversation_stats' not in st.session_state:
>>>>>>> 7b5f7e1 (feat: 대화 통계 기능 추가 및 페르소나 전환 버그 수정)
        st.session_state.conversation_stats = {
            'total': 0,
            'positive': 0,
            'negative': 0
        }
<<<<<<< HEAD
        st.session_state.selected_persona = "김소연 선생님"  # 기본 페르소나

    # 사이드바
    with st.sidebar:
        st.title("감정인식 챗봇 🏠")

        st.markdown("### 사용 방법")
        st.markdown("""
        1. 채팅창에 현재 기분이나 상황을 입력하세요.
        2. 음성 파일을 업로드하여 감정을 분석할 수 있습니다.
        3. 챗봇이 감정을 분석하고 공감적인 대화를 제공합니다.
        4. 필요한 경우 적절한 조언이나 위로를 받을 수 있습니다.
        """)

        st.markdown("### 페르소나 선택")
        selected_persona = st.selectbox("페르소나를 선택하세요:", list(PERSONAS.keys()))
        st.session_state.selected_persona = selected_persona

        # 현재 감정 상태 표시
        st.markdown("### 현재 감정 상태")
        emotion = st.session_state.current_emotion
        emotion_color = get_emotion_color(emotion)
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            margin-top: 16px;
        ">
            <span style="
                background-color: {emotion_color};
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: 600;
            ">{emotion}</span>
        </div>
        """, unsafe_allow_html=True)

        # 대화 통계
        stats = st.session_state.conversation_stats
        st.markdown("### 대화 통계")
        st.write(f"- 총 대화 수: {stats.get('total', 0)}")
        st.write(f"- 긍정적 감정: {stats.get('positive', 0)}")
        st.write(f"- 부정적 감정: {stats.get('negative', 0)}")

        # 음성 파일 업로드
        st.markdown("### 음성 파일 업로드")
        uploaded_audio = st.file_uploader("지원 형식: WAV", type=["wav"])
        if uploaded_audio is not None and uploaded_audio != st.session_state.last_uploaded_audio:
            st.session_state.last_uploaded_audio = uploaded_audio
            handle_audio_upload(uploaded_audio)

    # 메인 채팅 영역
    st.title("채팅")

    # 메시지 표시
    for message in st.session_state.get('messages', []):
        with st.chat_message(message["role"]):
            display_message(message, persona=selected_persona)

    # 텍스트 입력 처리
    if prompt := st.chat_input("메시지를 입력하세요..."):
        if prompt.strip():
            chatbot = st.session_state.chatbot_service
            persona_name = st.session_state.get("selected_persona", "김소연 선생님")
    
            # 감정 분석
            user_emotion = get_emotion_from_gpt(prompt)
            st.session_state.current_emotion = user_emotion  # 현재 감정 상태 업데이트
    
            # 대화 통계 업데이트
            update_conversation_stats(user_emotion)
    
            # GPT 응답 생성
            response = chatbot.get_response(prompt, persona_name)
    
            # 메시지 저장
            current_time = datetime.now().strftime('%p %I:%M')
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "emotion": user_emotion,
                "timestamp": current_time
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": current_time
            })
    
            # 화면 갱신
=======
    
    # 전체 대화 수 증가
    st.session_state.conversation_stats['total'] += 1
    
    # 감정에 따른 통계 업데이트
    positive_emotions = ['Happy']
    negative_emotions = ['Anger', 'Disgust', 'Fear', 'Sad']
    
    if emotion in positive_emotions:
        st.session_state.conversation_stats['positive'] += 1
    elif emotion in negative_emotions:
        st.session_state.conversation_stats['negative'] += 1

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
        # 페르소나 확인
        selected_persona = st.query_params.get("persona")
        if not selected_persona:
            st.query_params.clear()
            st.query_params["page"] = "home"
>>>>>>> 7b5f7e1 (feat: 대화 통계 기능 추가 및 페르소나 전환 버그 수정)
            st.rerun()
        else:
            # URL 파라미터 유지
            st.query_params["page"] = "chat"
            st.query_params["persona"] = selected_persona
            render_chat_page()
    else:
        from src.app.home import render_home
        render_home()


if __name__ == "__main__":
    main()


    # if prompt := st.chat_input("메시지를 입력하세요..."):
    #     if prompt.strip():
    #         chatbot = st.session_state.chatbot_service
    
    #         # GPT를 통해 감정 분석
    #         dominant_emotion = get_emotion_from_gpt(prompt)
    
    #         # GPT로부터 응답 생성
    #         response = chatbot.get_response(prompt)
    
    #         # 현재 시간 기록
    #         current_time = datetime.now().strftime('%p %I:%M')
    
    #         # 사용자 메시지 저장
    #         st.session_state.messages.append({
    #             "role": "user",
    #             "content": prompt,
    #             "emotion": dominant_emotion,
    #             "timestamp": current_time
    #         })
    
    #         # GPT 응답 메시지 저장
    #         st.session_state.messages.append({
    #             "role": "assistant",
    #             "content": response,
    #             "timestamp": current_time
    #         })
    
    #         # 통계 업데이트
    #         update_conversation_stats(dominant_emotion)
    
    #         # 화면 갱신
    #         st.rerun()


    # # 텍스트 입력창
    # if prompt := st.chat_input("메시지를 입력하세요..."):
    #     if prompt.strip():
    #         chatbot = st.session_state.chatbot_service
    #         emotions = chatbot.analyze_emotion(prompt)
    #         dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
    #         response = chatbot.get_response(prompt)

    #         current_time = datetime.now().strftime('%p %I:%M')
    #         st.session_state.messages.append({
    #             "role": "user",
    #             "content": prompt,
    #             "emotion": dominant_emotion,
    #             "timestamp": current_time
    #         })
    #         st.session_state.messages.append({
    #             "role": "assistant",
    #             "content": response,
    #             "timestamp": current_time
    #         })

    #         # 통계 업데이트
    #         update_conversation_stats(dominant_emotion)

    #         st.rerun()
