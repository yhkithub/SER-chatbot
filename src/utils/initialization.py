import streamlit as st
from datetime import datetime
from src.app.config import OpenAIConfig
from src.app.constants import DEFAULT_PERSONA

def initialize_chatbot_service():
    """ChatbotService 초기화"""
    from src.core.services.chatbot_service import ChatbotService
    return ChatbotService(OpenAIConfig())

def initialize_session_state(selected_persona: str = None):
    """세션 상태 초기화"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        
        # 페르소나 설정
        st.session_state.selected_persona = selected_persona or DEFAULT_PERSONA
        
        # 챗봇 서비스 초기화
        if 'chatbot_service' not in st.session_state:
            st.session_state.chatbot_service = initialize_chatbot_service()
        
        # 메시지 초기화
        if 'messages' not in st.session_state:
            st.session_state.messages = [{
                'role': 'assistant',
                'content': "안녕하세요! 오늘 하루는 어떠셨나요? 기분이나 감정을 자유롭게 이야기해주세요. 😊",
                'timestamp': datetime.now().strftime('%p %I:%M')
            }]
        
        # 감정 상태 초기화
        if 'current_emotion' not in st.session_state:
            st.session_state.current_emotion = "아직 감정이 분석되지 않았습니다"
        
        # 대화 통계 초기화
        if 'conversation_stats' not in st.session_state:
            st.session_state.conversation_stats = {
                'total': 0,
                'positive': 0,
                'negative': 0
            }