from datetime import datetime
import streamlit as st
from src.core.services.chatbot_service import ChatbotService
from src.app.config import OpenAIConfig

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
    
    # 사이드바
    with st.sidebar:
        st.title("감정인식 챗봇 🏠")
        
        st.markdown("### 사용 방법")
        st.markdown("""
        1. 채팅창에 현재 기분이나 상황을 입력하세요
        2. 챗봇이 감정을 분석하고 공감적인 대화를 제공합니다
        3. 필요한 경우 적절한 조언이나 위로를 받을 수 있습니다
        """)
        
        if 'current_emotion' in st.session_state:
            st.markdown("### 현재 감정 상태")
            st.write(st.session_state.current_emotion)
        
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
    
    # 입력창
    if prompt := st.chat_input("메시지를 입력하세요..."):
        if prompt.strip():
            # 메시지 처리
            chatbot = st.session_state.chatbot_service
            emotions = chatbot.analyze_emotion(prompt)
            dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
            response = chatbot.get_response(prompt)
            
            current_time = datetime.now().strftime('%p %I:%M')
            
            # 메시지 추가
            if 'messages' not in st.session_state:
                st.session_state.messages = []
                
            st.session_state.messages.extend([
                {
                    "role": "user",
                    "content": prompt,
                    "emotion": dominant_emotion,
                    "timestamp": current_time
                },
                {
                    "role": "assistant",
                    "content": response,
                    "timestamp": current_time
                }
            ])
            
            st.rerun()

if __name__ == "__main__":
    main()
