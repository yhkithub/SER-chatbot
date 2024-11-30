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


# def display_message(message: dict):
#     """Display chat message with emotion-based styling"""
#     role = message.get('role', '')
#     content = message.get('content', '')
#     timestamp = message.get('timestamp', '')
#     emotion = message.get('emotion', '')
    
#     # Assistant message (left side)
#     if role == "assistant":
#         st.markdown(f"""
#             <div style="display: flex; justify-content: flex-start; margin: 16px 0;">
#                 <div style="
#                     background-color: #F0F0F0;
#                     color: black;
#                     padding: 12px 18px;
#                     border-radius: 18px;
#                     border-top-left-radius: 4px;
#                     max-width: 80%;
#                     box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#                     position: relative;
#                 ">
#                     <div style="font-size: 1rem; line-height: 1.4;">{content}</div>
#                     <div style="
#                         font-size: 0.75rem;
#                         color: #666;
#                         margin-top: 6px;
#                         text-align: right;
#                     ">{timestamp}</div>
#                 </div>
#             </div>
#         """, unsafe_allow_html=True)
    
#     # User message (right side)
#     else:
#         background = get_emotion_color(emotion)
#         st.markdown(f"""
#             <div style="display: flex; justify-content: flex-end; margin: 16px 0;">
#                 <div style="
#                     background: {background};
#                     color: black;
#                     padding: 12px 18px;
#                     border-radius: 18px;
#                     border-top-right-radius: 4px;
#                     max-width: 80%;
#                     box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#                     position: relative;
#                 ">
#                     <div style="font-size: 1rem; line-height: 1.4;">{content}</div>
#                     <div style="
#                         display: flex;
#                         justify-content: flex-end;
#                         align-items: center;
#                         gap: 8px;
#                         margin-top: 6px;
#                     ">
#                         <span style="
#                             font-size: 0.75rem;
#                             background-color: rgba(0,0,0,0.1);
#                             padding: 2px 8px;
#                             border-radius: 12px;
#                             font-weight: 500;
#                         ">{emotion}</span>
#                         <span style="font-size: 0.75rem; color: #333;">{timestamp}</span>
#                     </div>
#                 </div>
#             </div>
#         """, unsafe_allow_html=True)

def apply_chat_styles():
    """Apply comprehensive and modern styles for chat interface"""
    st.markdown("""
        <style>
        /* 전체 채팅 인터페이스 스타일 */
        [data-testid="stChatMessage"] {
            display: flex;
            align-items: flex-start;
            margin-bottom: 1rem;
            max-width: 100%;
        }

        /* 사용자 메시지 스타일 */
        [data-testid="stChatMessage"][data-sender="user"] {
            flex-direction: row-reverse;
            justify-content: flex-end;
            text-align: right;
        }

        [data-testid="stChatMessage"][data-sender="user"] > div {
            margin-left: auto;
            margin-right: 0;
            background-color: #E6F2FF; /* 부드러운 파란색 배경 */
            border-radius: 15px;
            border-top-right-radius: 4px;
        }

        /* 챗봇 메시지 스타일 */
        [data-testid="stChatMessage"][data-sender="assistant"] {
            flex-direction: row;
            justify-content: flex-start;
            text-align: left;
        }

        [data-testid="stChatMessage"][data-sender="assistant"] > div {
            margin-right: auto;
            margin-left: 0;
            background-color: #F0F0F0; /* 연한 회색 배경 */
            border-radius: 15px;
            border-top-left-radius: 4px;
        }

        /* 아바타 스타일 */
        [data-testid="stChatMessageAvatar"] {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin: 0 10px;
        }

        [data-testid="stChatMessage"][data-sender="user"] [data-testid="stChatMessageAvatar"] {
            order: 2;
        }

        /* 메시지 내용 스타일 */
        [data-testid="stChatMessageContent"] {
            max-width: 75%;
            padding: 12px 16px;
            line-height: 1.4;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* 채팅 입력 영역 스타일 */
        .stTextInput > div > div > input {
            background-color: #F8F9FA;
            border: 1px solid #E9ECEF;
            border-radius: 10px;
            padding: 10px 15px;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        .stTextInput > div > div > input:focus {
            border-color: #007BFF;
            box-shadow: 0 0 0 3px rgba(0,123,255,0.25);
        }

        /* 전송 버튼 스타일 */
        .stButton > button {
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            transition: background-color 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #0056b3;
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
