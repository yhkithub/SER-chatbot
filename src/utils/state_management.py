import streamlit as st
from datetime import datetime
from src.app.constants import (
    DEFAULT_EMOTION,
    WELCOME_MESSAGE_TEMPLATE
)
from src.app.config import OpenAIConfig
from src.core.services.chatbot_service import ChatbotService

def initialize_session_state(selected_persona: str):
    """세션 상태 초기화"""
    st.session_state.initialized = True
    st.session_state.selected_persona = selected_persona
    st.session_state.chatbot_service = ChatbotService(OpenAIConfig())
    st.session_state.messages = [{
        'role': 'assistant',
        'content': WELCOME_MESSAGE_TEMPLATE.format(persona=selected_persona),
        'timestamp': datetime.now().strftime('%p %I:%M')
    }]
    st.session_state.last_uploaded_audio = None
    st.session_state.current_emotion = DEFAULT_EMOTION
    st.session_state.conversation_stats = {
        'total': 0,
        'positive': 0,
        'negative': 0
    }

def clear_session_state():
    """세션 상태 초기화"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def ensure_state_initialization(key: str, default_value):
    """세션 상태 키가 없으면 초기화"""
    if key not in st.session_state:
        st.session_state[key] = default_value