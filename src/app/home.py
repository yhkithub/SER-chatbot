import streamlit as st
import streamlit.components.v1 as components
from src.utils.state_management import clear_session_state, initialize_session_state
from src.app.constants import PERSONA_IMAGES, PERSONA_URL_MAPPING

# 페르소나 정보를 상수로 정의
PERSONAS = [
    {
        "name": "김소연 선생님", 
        "img": PERSONA_IMAGES["김소연 선생님"],
        "desc": "졸업해도 잊지 못해!",
        "explanation": """[김소연 선생님]은 따뜻하고 세심한 고등학교 국어 교사로, 학생들의 학업뿐만 아니라 인생 고민까지 들어주는 멘토 역할을 합니다.
        [김소연 선생님]은 평소 독서(특히 고전 문학), 학생 상담, 교육 심리학 연구, 가드닝에 관심이 많습니다."""
    },
    {
        "name": "박준호 팀장님", 
        "img": PERSONA_IMAGES["박준호 팀장님"],
        "desc": "밥 잘 사주고 잘생긴",
        "explanation": """[박준호 팀장님]은 IT 회사의 팀장으로, 엄격하고 목표 지향적인 리더이지만, 후배들에게는 다정하고 상담을 잘해주는 든든한 선배입니다."""
    },
    {
        "name": "장난꾸러기 동생 민준이", 
        "img": PERSONA_IMAGES["장난꾸러기 동생 민준이"],
        "desc": "그거 그렇게 하는 거 아닌데?",
        "explanation": """[민준이]는 8살 초등학교 2학년 남자아이로, 에너지가 넘치고 낙천적이며 주변 사람들에게 밝은 기운을 전파합니다."""
    },
    {
        "name": "10년지기 친구 이동환", 
        "img": PERSONA_IMAGES["10년지기 친구 이동환"],
        "desc": "팩트폭격 준비됐어?",
        "explanation": """[이동환]은 29세 데이터 분석가로, 언제나 현실적이고 냉철한 조언을 아끼지 않는 친구입니다."""
    },
    {
        "name": "학교 후배 정서윤", 
        "img": PERSONA_IMAGES["학교 후배 정서윤"],
        "desc": "제가 선배 옆에 있어드릴게요!",
        "explanation": """[정서윤]은 20세 대학생으로 문예창작학과에 재학 중입니다. 감수성이 풍부하고 낭만적인 성격으로, 상대방의 감정을 세심하게 읽고 공감하는 데 뛰어난 재능이 있습니다"""
    },
]

def get_page_styles() -> str:
    """페이지 스타일 CSS를 반환하는 함수"""
    return """
        <style>
        .persona-button {
            width: 100%;
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 10px;
            font-size: 0.85rem;
            font-weight: bold;
            margin-top: 10px;
            cursor: pointer;
        }
        
        .persona-button:hover {
            background-color: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        img {
            transition: transform 0.3s;
        }
        
        img:hover {
            transform: scale(1.05);
        }
                
        .persona-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: auto; 
        }
                
        #hover-info {
            font-size: 1.2em;
            color: #333333;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.9);
            text-align: center;
            padding: 10px;
            z-index: 1000;
        }
        </style>
    """

def render_home():
    """홈페이지 렌더���"""
    # 페이지 헤더
    st.markdown("""
        <h1 style='text-align: center; color: white;'>감정을 치유하는 챗봇</h1>
        <p style='text-align: center; color: rgba(255, 255, 255, 0.8); font-size: 1.2em;'>
            당신의 이야기를 들어줄 상담사를 선택해주세요
        </p>
    """, unsafe_allow_html=True)

    # 스타일 적용
    st.markdown(get_page_styles(), unsafe_allow_html=True)

    # 페르소나 선택 섹션
    cols = st.columns(5)
    for idx, persona in enumerate(PERSONAS):
        with cols[idx]:
            container = st.container()
            
            # 이미지 표시
            container.image(
                persona["img"],
                use_column_width=True,
                caption=persona["desc"]
            )
            
            # 디튼 클릭으로 페르소나 선택
            if container.button(
                f"{persona['desc']}\n{persona['name']}", 
                key=f"persona_button_{idx}",
                use_container_width=True
            ):
                # 세션 상태 초기화
                clear_session_state()
                
                # 새로운 페르소나로 초기화
                initialize_session_state(persona['name'])
                
                # URL 파라미터 설정
                persona_url = PERSONA_URL_MAPPING[persona['name']]
                st.query_params["page"] = "chat"
                st.query_params["persona"] = persona_url
                
                # 페이지 새로고침
                st.rerun()

    # 세션 상태 초기화
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
