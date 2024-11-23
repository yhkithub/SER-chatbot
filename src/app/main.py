from datetime import datetime
import streamlit as st
import torch
import torchaudio
import os
from transformers import AutoModelForAudioClassification, AutoProcessor
import torchaudio.transforms as T
from src.core.services.chatbot_service import ChatbotService
from src.app.config import OpenAIConfig

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

def process_audio(waveform, target_sample_rate=16000, target_length=16000):
    """Process audio to correct format."""
    try:
        if waveform.shape[0] > 1:
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
        waveform, sample_rate = torchaudio.load(audio_path)
        processed_waveform = process_audio(waveform, target_sample_rate=16000)
        
        if processed_waveform is None:
            return None
        
        inputs = processor(processed_waveform.squeeze(), sampling_rate=16000, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        predicted_class_idx = outputs.logits.argmax(-1).item()
        
        if predicted_class_idx in EMOTION_MAPPING:
            return EMOTION_MAPPING[predicted_class_idx]
        return None
            
    except Exception as e:
        st.error(f"Error in emotion prediction: {str(e)}")
        return None

def add_message(role, content, emotion=None):
    """Add a new message to the chat."""
    current_time = datetime.now().strftime('%p %I:%M')
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "emotion": emotion,
        "timestamp": current_time
    })

def main():
    st.set_page_config(
        page_title="감정인식 챗봇",
        page_icon="🤗",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 세션 상태 초기화
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.chatbot_service = ChatbotService(OpenAIConfig())
        st.session_state.messages = [{
            'role': 'assistant',
            'content': "안녕하세요! 오늘 하루는 어떠셨나요? 기분이나 감정을 자유롭게 이야기해주세요. 텍스트로 입력하거나 음성 파일을 업로드해주세요. 😊",
            'timestamp': datetime.now().strftime('%p %I:%M')
        }]
        st.session_state.audio_processing = False  # 음성 처리 상태 초기화
        st.session_state.audio_message = None  # 음성 메시지 초기화

    # 사이드바
    with st.sidebar:
        st.title("감정인식 챗봇 🏠")
        st.markdown("### 사용 방법")
        st.markdown("""
        1. 채팅창에 현재 기분이나 상황을 입력하세요
        2. 또는 음성 파일을 업로드하여 감정을 분석할 수 있습니다
        3. 챗봇이 감정을 분석하고 공감적인 대화를 제공합니다
        4. 필요한 경우 적절한 조언이나 위로를 받을 수 있습니다
        """)

        # 음성 파일 업로더
        uploaded_audio = st.file_uploader("음성 파일 업로드", type=["wav", "mp3", "ogg"])
        if uploaded_audio is not None and not st.session_state.audio_processing:
            try:
                # 음성 처리 시작 플래그
                st.session_state.audio_processing = True

                # 임시 파일로 저장
                with open("temp_audio.wav", "wb") as f:
                    f.write(uploaded_audio.getbuffer())

                # 음성 분석
                with st.spinner('음성 분석 중...'):
                    audio_emotion = predict_audio_emotion("temp_audio.wav")

                if audio_emotion:
                    # 음성 메시지 저장
                    st.session_state.audio_message = [
                        {
                            "role": "user",
                            "content": "[음성 파일이 업로드됨]",
                            "emotion": audio_emotion,
                            "timestamp": datetime.now().strftime('%p %I:%M')
                        },
                        {
                            "role": "assistant",
                            "content": f"음성에서 감지된 감정은 {audio_emotion}입니다. 더 자세히 이야기해주시겠어요?",
                            "timestamp": datetime.now().strftime('%p %I:%M')
                        }
                    ]
            except Exception as e:
                st.error(f"음성 처리 중 오류가 발생했습니다: {str(e)}")
            finally:
                # 음성 처리 완료 후 파일 삭제
                if os.path.exists("temp_audio.wav"):
                    os.remove("temp_audio.wav")

    # 메인 채팅 영역
    st.title("채팅")

    # 기존 메시지 출력
    for message in st.session_state.get('messages', []):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "emotion" in message:
                st.caption(f"감정: {message['emotion']}")
            st.caption(f"시간: {message['timestamp']}")

    # 새로 업로드된 음성 메시지 출력
    if st.session_state.audio_message:
        for audio_msg in st.session_state.audio_message:
            with st.chat_message(audio_msg["role"]):
                st.write(audio_msg["content"])
                if "emotion" in audio_msg:
                    st.caption(f"감정: {audio_msg['emotion']}")
                st.caption(f"시간: {audio_msg['timestamp']}")

    # 텍스트 입력창
    if prompt := st.chat_input("메시지를 입력하세요..."):
        if prompt.strip():
            # 텍스트 메시지 분석 및 응답
            chatbot = st.session_state.chatbot_service
            emotions = chatbot.analyze_emotion(prompt)
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            response = chatbot.get_response(prompt)

            current_time = datetime.now().strftime('%p %I:%M')

            # 메시지 저장
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "emotion": dominant_emotion,
                "timestamp": current_time
            })
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": current_time
            })

            # 음성 상태 초기화
            st.session_state.audio_processing = False
            st.session_state.audio_message = None

            # 새 메시지 렌더링
            st.rerun()

if __name__ == "__main__":
    main()
