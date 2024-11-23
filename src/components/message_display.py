import streamlit as st

def display_message(message: dict):
    """채팅 메시지 표시"""
    role = message.get('role', '')
    content = message.get('content', '')
    timestamp = message.get('timestamp', '')
    emotion = message.get('emotion', '')
    
    # 챗봇 메시지 (왼쪽)
    if role == "assistant":
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                <div style="
                    background-color: white;
                    color: black;
                    padding: 12px 16px;
                    border-radius: 12px;
                    max-width: 70%;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 0.95rem;">{content}</div>
                    <div style="font-size: 0.75rem; color: #666; margin-top: 4px;">
                        {timestamp}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # 사용자 메시지 (오른쪽)
    else:
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                <div style="
                    background-color: #FEE500;
                    color: black;
                    padding: 12px 16px;
                    border-radius: 12px;
                    max-width: 70%;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                ">
                    <div style="font-size: 0.95rem;">{content}</div>
                    <div style="
                        display: flex;
                        justify-content: flex-end;
                        align-items: center;
                        gap: 8px;
                        margin-top: 4px;
                    ">
                        <span style="font-size: 0.75rem; color: #666;">{timestamp}</span>
                        {f'<span style="font-size: 0.75rem; background-color: rgba(0,0,0,0.1); padding: 2px 8px; border-radius: 10px;">{emotion}</span>' if emotion else ''}
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def get_emotion_class(emotion: str) -> str:
    """감정에 따른 스타일 클래스 반환"""
    positive_emotions = {'joy', 'love', 'surprise'}
    negative_emotions = {'anger', 'sadness', 'fear'}
    
    if emotion in positive_emotions:
        return 'positive'
    elif emotion in negative_emotions:
        return 'negative'
    return 'neutral' 
