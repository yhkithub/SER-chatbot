import streamlit as st
from datetime import datetime
from src.app.constants import (
    DEFAULT_PERSONA,
    DEFAULT_EMOTION,
    WELCOME_MESSAGE_TEMPLATE
)
from src.app.config import OpenAIConfig
from src.core.services.chatbot_service import ChatbotService

def initialize_session_state(selected_persona: str = DEFAULT_PERSONA):
    """세션 상태 초기화"""
    print(f"Initializing state for: {selected_persona}")  # 디버깅용
    
    # 기존 상태가 다른 페르소나면 초기화
    if ('selected_persona' in st.session_state and 
        st.session_state.selected_persona != selected_persona):
        clear_session_state()
    
    # 새로운 상태 설정
    st.session_state.initialized = True
    st.session_state.selected_persona = selected_persona
    
    # 챗봇 서비스 초기화
    if 'chatbot_service' not in st.session_state:
        st.session_state.chatbot_service = ChatbotService(OpenAIConfig())
    
    # 메시지 초기화 - 페르소나가 변경되었을 때만
    if ('messages' not in st.session_state or 
        st.session_state.get('selected_persona') != selected_persona):
        st.session_state.messages = [{
            'role': 'assistant',
            'content': WELCOME_MESSAGE_TEMPLATE.format(persona=selected_persona),
            'timestamp': datetime.now().strftime('%p %I:%M')
        }]
    
    # 기타 상태 초기화
    if 'last_uploaded_audio' not in st.session_state:
        st.session_state.last_uploaded_audio = None
    if 'current_emotion' not in st.session_state:
        st.session_state.current_emotion = DEFAULT_EMOTION
    if 'conversation_stats' not in st.session_state:
        st.session_state.conversation_stats = {
            'total': 0,
            'positive': 0,
            'negative': 0
        }

def clear_session_state():
    """세션 상태를 완전히 초기화"""
    # 현재 URL 파라미터 저장
    current_params = dict(st.query_params.items())
    
    # 모든 세션 상태 삭제
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # URL 파라미터 복원
    for key, value in current_params.items():
        st.query_params[key] = value

def ensure_state_initialization(key: str, default_value):
    """세션 상태 키가 없으면 초기화"""
    if key not in st.session_state:
        st.session_state[key] = default_value