import streamlit as st

def get_emotion_color(emotion: str) -> str:
    """Return background color based on emotion"""
    emotion_colors = {
        # Positive emotions
        'Happy': 'linear-gradient(135deg, #90EE90, #98FB98)',  # Light green gradient
        'Neutral': 'linear-gradient(135deg, #FEE500, #FFE44D)',  # Yellow gradient
        
        # Negative emotions
        'Sad': 'linear-gradient(135deg, #ADD8E6, #87CEEB)',  # Light blue gradient
        'Anger': 'linear-gradient(135deg, #FFB6C1, #FFA07A)',  # Light red gradient
        'Fear': 'linear-gradient(135deg, #DDA0DD, #D8BFD8)',  # Light purple gradient
        'Disgust': 'linear-gradient(135deg, #F0E68C, #EEE8AA)'  # Light khaki gradient
    }
    return emotion_colors.get(emotion, 'linear-gradient(135deg, #FEE500, #FFE44D)')

def get_emotion_color(emotion: str) -> str:
    """Return background color based on emotion"""
    emotion_colors = {
        # Positive emotions
        'Happy': 'linear-gradient(135deg, #90EE90, #98FB98)',  # Light green gradient
        'Neutral': 'linear-gradient(135deg, #FEE500, #FFE44D)',  # Yellow gradient
        
        # Negative emotions
        'Sad': 'linear-gradient(135deg, #ADD8E6, #87CEEB)',  # Light blue gradient
        'Anger': 'linear-gradient(135deg, #FFB6C1, #FFA07A)',  # Light red gradient
        'Fear': 'linear-gradient(135deg, #DDA0DD, #D8BFD8)',  # Light purple gradient
        'Disgust': 'linear-gradient(135deg, #F0E68C, #EEE8AA)'  # Light khaki gradient
    }
    return emotion_colors.get(emotion, 'linear-gradient(135deg, #FEE500, #FFE44D)')

def display_message(message: dict):
    """Display chat message with emotion-based styling"""
    role = message.get('role', '')
    content = message.get('content', '')
    timestamp = message.get('timestamp', '')
    emotion = message.get('emotion', '')
    
    # Assistant message (left side)
    if role == "assistant":
        st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 16px 0;">
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
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        /* 채팅 메시지 컨테이너 기본 스타일 */
        [data-testid="stChatMessage"] {
            display: flex;
            flex-direction: row !important;
            align-items: start;
            gap: 1rem;
            padding: 0.5rem 1rem;
            width: 100%;
        }
        
        /* 사용자 메시지 컨테이너 반전 */
        [data-testid="stChatMessage"][data-role="user"] {
            flex-direction: row-reverse !important;
        }
        
        /* 메시지 내용 컨테이너 */
        [data-testid="stChatMessage"] > div {
            display: flex;
            align-items: start;
            gap: 1rem;
        }
        
        /* 사용자 메시지 내용 컨테이너 반전 */
        [data-testid="stChatMessage"][data-role="user"] > div {
            flex-direction: row-reverse;
            margin-left: auto;
        }
        
        /* 아바타 이미지 컨테이너 */
        [data-testid="stChatMessage"] div:has(img) {
            order: 1;
        }
        
        /* 사용자 메시지의 아바타 이미지 컨테이너 */
        [data-testid="stChatMessage"][data-role="user"] div:has(img) {
            order: 2;
            margin-left: 0;
            margin-right: 0;
        }
        
        /* 메시지 텍스트 컨테이너 */
        [data-testid="stMarkdownContainer"] {
            order: 2;
            margin: 0 !important;
        }
        
        /* 사용자 메시지의 텍스트 컨테이너 */
        [data-testid="stChatMessage"][data-role="user"] [data-testid="stMarkdownContainer"] {
            order: 1;
            margin-right: auto !important;
        }
        
        /* 캡션 스타일링 */
        [data-testid="stChatMessageCaption"] {
            text-align: right;
        }

        /* 메시지 내용 여백 조정 */
        [data-testid="stMarkdownContainer"] > p {
            margin-bottom: 0;
        }

        /* 스크롤바 스타일링 */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
            background-color: #1E1E1E;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #4A4A4A;
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background-color: #5A5A5A;
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
