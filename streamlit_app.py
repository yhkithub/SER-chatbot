import os
from dotenv import load_dotenv
import streamlit as st
from datetime import datetime
from chatbot_logic import initialize_conversation, initialize_pinecone

# .env 파일에서 환경 변수 로드
load_dotenv()

# 필요한 환경 변수 불러오기
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Streamlit 설정
st.set_page_config(page_title="EnvPolicyChat", page_icon="🌍", layout="centered")
st.title("🌍 **환경 정책 소개 챗봇**")
st.divider()

# 사이드바에 디버그 모드 설정 추가
st.sidebar.title("설정")
st.sidebar.subheader("옵션")
st.sidebar.checkbox("참조된 문서 확인하기", key="show_docs")

# Pinecone 설정 및 초기화
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = initialize_pinecone()

# 대화 기록 초기화
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{
        'role': 'assistant',
        'content': "안녕하세요! 환경 정책에 대해 무엇을 도와드릴까요?",
        'timestamp': datetime.now().strftime('%p %I:%M')
    }]

# 대화 초기화
if 'conversation' not in st.session_state:
    st.session_state.conversation = initialize_conversation(st.session_state.vectorstore)

# 메시지 표시 함수
def display_message(role, content, timestamp):
    alignment = 'flex-end' if role == "user" else 'flex-start'
    bg_color = '#dcf8c6' if role == "user" else '#f1f0f0'  # 카카오톡 스타일 색상 적용
    text_align = 'right' if role == "user" else 'left'
    label = "🙋 사용자" if role == "user" else "🤖 챗봇"
    timestamp_position = 'left: -60px;' if role == "user" else 'right: -60px;'

    return f"""
        <div style='display: flex; justify-content: {alignment}; margin-bottom: 10px;'>
            <div style='max-width: 60%; position: relative;'>
                <div style='text-align: {text_align}; color: #888;'>{label}</div>
                <div style='background-color: {bg_color}; padding: 10px; border-radius: 10px; color: black; border: 1px solid #C0C0C0;'>
                    {content}
                </div>
                <div style='font-size: 0.8em; color: #555; position: absolute; {timestamp_position} bottom: 0; margin: 0 5px;'>{timestamp}</div>
            </div>
        </div>
    """

# 이전 대화 기록 표시
chat_container = st.container()
with chat_container:
    for message in st.session_state['messages']:
        st.markdown(display_message(message['role'], message['content'], message['timestamp']), unsafe_allow_html=True)

# 사용자 입력 받기
input_container = st.container()

# 사용자 입력 필드와 전송 버튼
with st.form(key='user_input_form', clear_on_submit=True):
    user_input = st.text_input(
        "💬 질문을 입력해주세요:",
        placeholder="환경 정책에 대해 궁금한 점을 입력하세요...",
        key="user_input"
    )
    submit_button = st.form_submit_button(label='전송')

if submit_button and user_input:
    # 대화 내역에 사용자 입력 추가
    st.session_state['messages'].append({
        'role': 'user',
        'content': user_input,
        'timestamp': datetime.now().strftime('%p %I:%M')
    })

    # 챗봇 응답 생성
    response = st.session_state.conversation.invoke(
        {'input': user_input},
        config={'configurable': {'session_id': 'default'}}
    )

    # 대화 내역에 챗봇 응답 추가
    st.session_state['messages'].append({
        'role': 'assistant',
        'content': response['answer'],
        'timestamp': datetime.now().strftime('%p %I:%M')
    })

    # 대화 내역 갱신
    for message in st.session_state['messages'][-2:]:
        st.markdown(display_message(message['role'], message['content'], message['timestamp']), unsafe_allow_html=True)

# 스타일 추가 (기본 스타일 유지, 심플하게)
st.markdown(
    """
    <style>
    .stTextInput, .stAlert {
        border-radius: 10px;
        margin-left: 20px;
    }
    .css-1gkdjib.e1yohnl3 {
        height: 70vh;
        overflow-y: auto;
    }
    .css-1gkdjib.e1ewe7hr3 {
        margin-top: auto;
    }
    .stTextInput {
        display: flex;
        align-items: center;
    }
    .stButton > button {
        width: 60px;
        height: 40px;
        margin-left: 10px;
        border-radius: 8px;
        align-items: center;
        font-size: 16px;
    }
    .sidebar-content {
        padding: 20px;
    }
    .sidebar-content .stCheckbox {
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
