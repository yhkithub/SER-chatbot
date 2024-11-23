from datetime import datetime
import streamlit as st
from src.core.services.chatbot_service import ChatbotService
from src.app.config import OpenAIConfig

def add_message(role, content, emotion=None):
    """세션 상태에 메시지를 추가."""
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
            'content': "안녕하세요! 오늘 하루는 어떠셨나요? 기분이나 감정을 자유롭게 이야기해주세요. 😊",
            'timestamp': datetime.now().strftime('%p %I:%M')
        }]
        st.session_state.current_emotion = "아직 감정이 분석되지 않았습니다"
        st.session_state.conversation_stats = {
            'total': 0,
            'positive': 0,
            'negative': 0
        }
        st.session_state.audio_uploaded = False  # 오디오 업로드 상태 초기화

    # 추가 방어 코드
    if 'audio_uploaded' not in st.session_state:
        st.session_state.audio_uploaded = False

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

        # 오디오 파일 업로더 추가
        st.markdown("### 음성 감정 분석")
        uploaded_audio = st.file_uploader("음성 파일 업로드", type=["wav", "mp3", "ogg"])
        
        if uploaded_audio is not None and not st.session_state.audio_uploaded:
            try:
                # 임시 파일로 저장
                with open("temp_audio.wav", "wb") as f:
                    f.write(uploaded_audio.getbuffer())

                # 음성 감정 분석
                with st.spinner('음성 분석 중...'):
                    audio_emotion = "Happy"  # Dummy emotion, replace with prediction logic
                    st.session_state.messages.append({
                        "role": "user",
                        "content": "[음성 파일이 업로드됨]",
                        "emotion": audio_emotion,
                        "timestamp": datetime.now().strftime('%p %I:%M')
                    })
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"음성에서 감지된 감정은 {audio_emotion}입니다. 더 자세히 이야기해주시겠어요?",
                        "timestamp": datetime.now().strftime('%p %I:%M')
                    })
                    
                    # 통계 업데이트
                    st.session_state.conversation_stats['total'] += 1
                    if audio_emotion in ['Happy', 'Neutral']:
                        st.session_state.conversation_stats['positive'] += 1
                    elif audio_emotion in ['Anger', 'Disgust', 'Fear', 'Sad']:
                        st.session_state.conversation_stats['negative'] += 1

                # 임시 파일 삭제
                if os.path.exists("temp_audio.wav"):
                    os.remove("temp_audio.wav")

                # 오디오 업로드 상태 업데이트
                st.session_state.audio_uploaded = True

            except Exception as e:
                st.error(f"음성 처리 중 오류가 발생했습니다: {str(e)}")


        # 현재 감정 상태 표시
        if 'current_emotion' in st.session_state:
            st.markdown("### 현재 감정 상태")
            st.write(st.session_state.current_emotion)
        
        # 대화 통계 표시
        if 'conversation_stats' in st.session_state:
            st.markdown("### 대화 통계")
            st.write(f"총 대화 수: {st.session_state.conversation_stats.get('total', 0)}")
            st.write(f"긍정적 감정: {st.session_state.conversation_stats.get('positive', 0)}")
            st.write(f"부정적 감정: {st.session_state.conversation_stats.get('negative', 0)}")
    
    # 메인 채팅 영역
    st.title("채팅")
    
    # 메시지 표시
    for message in st.session_state.get('messages', []):
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "emotion" in message:
                st.caption(f"감정: {message['emotion']}")
            st.caption(f"시간: {message['timestamp']}")
    
    # 텍스트 입력 처리
    if prompt := st.chat_input("메시지를 입력하세요..."):
        if prompt.strip():
            chatbot = st.session_state.chatbot_service
            emotions = chatbot.analyze_emotion(prompt)
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            response = chatbot.get_response(prompt)

            add_message("user", prompt, emotion=dominant_emotion)
            add_message("assistant", response)

            # 리렌더링
            st.session_state.audio_uploaded = False  # 텍스트 입력 후 오디오 상태 초기화
            st.rerun()

if __name__ == "__main__":
    main()
