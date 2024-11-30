import streamlit as st

PERSONA_ICONS = {
    "김소연 선생님": "https://example.com/icons/teacher.png",
    "박준호 팀장님": "https://example.com/icons/manager.png",
    "민준이": "https://example.com/icons/child.png",
    "이동환": "https://example.com/icons/friend.png",
    "정서윤": "https://example.com/icons/student.png",
}

def get_emotion_color(emotion: str) -> str:
    """Return solid background color based on emotion"""
    emotion_colors = {
        # Positive emotions
        'Happy': '#90EE90',  # Light green
        'Neutral': '#FFD700',  # Gold

        # Negative emotions
        'Sad': '#ADD8E6',  # Light blue
        'Anger': '#FF6347',  # Tomato
        'Fear': '#DDA0DD',  # Plum
        'Disgust': '#F0E68C'  # Khaki
    }
    return emotion_colors.get(emotion, '#FFD700')  # Default to gold for neutral

def display_message(message: dict, persona: str = "default"):
    """Display chat message with persona-based icon styling"""
    role = message.get('role', '')
    content = message.get('content', '')
    timestamp = message.get('timestamp', '')
    emotion = message.get('emotion', '')

    # Assistant message (left side)
    if role == "assistant":
        icon_url = PERSONA_ICONS.get(persona, "https://example.com/icons/default.png")  # Default icon
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 16px 0;">
                <img src="{icon_url}" style="
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    margin-right: 10px;
                ">
                <div style="
                    background-color: #F0F0F0;
                    color: black;
                    padding: 12px 18px;
                    border-radius: 18px;
                    border-top-left-radius: 4px;
                    max-width: 80%;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    position: relative;
                ">
                    <div style="font-size: 1rem; line-height: 1.4;">{content}</div>
                    <div style="
                        font-size: 0.75rem;
                        color: #666;
                        margin-top: 6px;
                        text-align: right;
                    ">{timestamp}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # User message (right side)
    else:
        background = get_emotion_color(emotion)
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 16px 0;">
                <div style="
                    background: {background};
                    color: black;
                    padding: 12px 18px;
                    border-radius: 18px;
                    border-top-right-radius: 4px;
                    max-width: 80%;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    position: relative;
                ">
                    <div style="font-size: 1rem; line-height: 1.4;">{content}</div>
                    <div style="
                        display: flex;
                        justify-content: flex-end;
                        align-items: center;
                        gap: 8px;
                        margin-top: 6px;
                    ">
                        <span style="
                            font-size: 0.75rem;
                            background-color: rgba(0,0,0,0.1);
                            padding: 2px 8px;
                            border-radius: 12px;
                            font-weight: 500;
                        ">{emotion}</span>
                        <span style="font-size: 0.75rem; color: #333;">{timestamp}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

def apply_chat_styles():
    """Apply custom styles for chat interface"""
    st.markdown("""
        <style>
        /* User messages - move icon to the right */
        .st-emotion-container .st-chat-message-user {
            flex-direction: row-reverse !important;
            justify-content: flex-start !important;
            text-align: right;
        }

        /* Ensure user message content is aligned right */
        .st-emotion-container .st-chat-message-user .st-chat-message-content {
            margin-left: auto !important;
            margin-right: 0 !important;
        }

        /* Assistant messages - keep default left alignment */
        .st-emotion-container .st-chat-message-assistant {
            flex-direction: row !important;
            justify-content: flex-start !important;
            text-align: left;
        }

        /* Ensure assistant message content is aligned left */
        .st-emotion-container .st-chat-message-assistant .st-chat-message-content {
            margin-right: auto !important;
            margin-left: 0 !important;
        }

        /* Optional: Chat input and button styles */
        .stTextInput input {
            background-color: #2D2D2D;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.8rem;
        }
        
        .stButton button {
            background-color: #007AFF;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.8rem 1.5rem;
        }
        </style>
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
