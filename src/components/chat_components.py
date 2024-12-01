import streamlit as st
from src.app.constants import EMOTION_COLORS, PERSONA_IMAGES

def render_emotion_indicator(emotion: str):
    """감정 상태 표시 컴포넌트"""
    emotion_color = EMOTION_COLORS.get(emotion, EMOTION_COLORS['Neutral'])
    return st.markdown(f"""
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

def render_conversation_stats(stats: dict):
    """대화 통계 표시 컴포넌트"""
    st.markdown("### 대화 통계")
    st.write(f"- 총 대화 수: {stats.get('total', 0)}")
    st.write(f"- 긍정적 감정: {stats.get('positive', 0)}")
    st.write(f"- 부정적 감정: {stats.get('negative', 0)}")

def display_message(message: str, is_user: bool, persona_name: str = None):
    if is_user:
        st.chat_message("user").write(message)
    else:
        with st.chat_message("assistant", avatar=PERSONA_IMAGES.get(persona_name)):
            st.write(message) 