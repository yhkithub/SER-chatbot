import streamlit as st

def render_sidebar():
    """사이드바 렌더링"""
    with st.sidebar:
        st.markdown("""
            <h1 style='
                color: white;
                margin-bottom: 2rem;
                font-size: 1.5rem;
            '>감정인식 챗봇 🏠</h1>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='
                background-color: #3A3B3C;
                padding: 1rem;
                border-radius: 0.5rem;
                margin-bottom: 2rem;
            '>
                <h3 style='
                    color: white;
                    margin-bottom: 1rem;
                    font-size: 1.1rem;
                '>사용 방법</h3>
                <ol style='
                    color: #E0E0E0;
                    margin-left: 1.2rem;
                    font-size: 0.9rem;
                '>
                    <li>채팅창에 현재 기분이나 상황을 입력하세요</li>
                    <li>챗봇이 감정을 분석하고 공감적인 대화를 제공합니다</li>
                    <li>필요한 경우 적절한 조언이나 위로를 받을 수 있습니다</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
        
        # 감정 상태 표시
        if 'current_emotion' in st.session_state:
            st.markdown(f"""
                <div style='
                    background-color: #3A3B3C;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-bottom: 1rem;
                '>
                    <h3 style='
                        color: white;
                        margin-bottom: 0.5rem;
                        font-size: 1.1rem;
                    '>현재 감정 상태</h3>
                    <p style='
                        color: #E0E0E0;
                        font-size: 0.9rem;
                    '>{st.session_state.current_emotion}</p>
                </div>
            """, unsafe_allow_html=True)
        
        # 대화 통계
        if 'conversation_stats' in st.session_state:
            st.markdown("""
                <div style='
                    background-color: #3A3B3C;
                    padding: 1rem;
                    border-radius: 0.5rem;
                '>
                    <h3 style='
                        color: white;
                        margin-bottom: 0.5rem;
                        font-size: 1.1rem;
                    '>대화 통계</h3>
                    <p style='color: #E0E0E0; font-size: 0.9rem;'>
                        총 대화 수: {total}<br>
                        긍정적 감정: {positive}<br>
                        부정적 감정: {negative}
                    </p>
                </div>
            """.format(
                total=st.session_state.conversation_stats.get('total', 0),
                positive=st.session_state.conversation_stats.get('positive', 0),
                negative=st.session_state.conversation_stats.get('negative', 0)
            ), unsafe_allow_html=True)