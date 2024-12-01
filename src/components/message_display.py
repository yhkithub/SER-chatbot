import streamlit as st
from src.app.constants import PERSONA_IMAGES

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
    """Display chat message with persona-based styling"""
    try:
        content = message.get('content', '')
        timestamp = message.get('timestamp', '')
        emotion = message.get('emotion', '')
        
        # 사용자 메시지
        if message.get('role') == 'user':
            background = get_emotion_color(emotion)
            with st.container():
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
            
        # 챗봇 메시지
        else:
            # 페르소나 이미지 URL 가져오기
            persona_image = PERSONA_IMAGES.get(persona)
            
            with st.container():
                st.markdown(f"""
                    <div style="display: flex; align-items: flex-start; margin: 16px 0; gap: 8px;">
                        <img src="{persona_image}" style="
                            width: 40px;
                            height: 40px;
                            border-radius: 50%;
                            object-fit: cover;
                        "/>
                        <div style="
                            background-color: #F0F0F0;
                            color: black;
                            padding: 12px 18px;
                            border-radius: 18px;
                            border-top-left-radius: 4px;
                            max-width: 80%;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <div style="font-size: 1rem; line-height: 1.4;">{content}</div>
                            <div style="font-size: 0.75rem; color: #666; margin-top: 6px;">{timestamp}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"메시지 표시 중 오류 발생: {str(e)}")

def apply_chat_styles():
    """Apply custom styles for chat interface"""
    st.markdown("""
        <style>
        /* 기본 채팅 아이콘 숨기기 */
        .stChatMessage .stChatMessageAvatar {
            display: none !important;
        }
        
        /* 채팅 메시지 컨테이너 여백 조정 */
        .stChatMessage {
            padding-left: 0 !important;
            padding-right: 0 !important;
        }
        
        /* 채팅 입력창 스타일 */
        .stTextInput input {
            background-color: #2D2D2D;
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.8rem;
        }
        
        /* 버튼 스타일 */
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
