import streamlit as st
import streamlit.components.v1 as components
from src.utils.state_management import clear_session_state, initialize_session_state
from src.app.constants import PERSONA_IMAGES, PERSONA_URL_MAPPING

# 페르소나 정보를 상수로 정의
PERSONAS = [
    {
        "name": "김서연 교수", 
        "img": PERSONA_IMAGES["김서연 교수"],
        "desc": "심리학과 교수 | 상담심리전문가",
        "explanation": "20년 이상의 상담 경험을 보유한 심리학 전문가입니다. 따뜻하면서도 전문적인 관점에서 당신의 이야기를 경청하고 통찰력 있는 조언을 제공합니다."
    },
    {
        "name": "박준영 멘토", 
        "img": PERSONA_IMAGES["박준영 멘토"],
        "desc": "리더십 코치 | 커리어 멘토",
        "explanation": "실용적이고 체계적인 분석을 통해 당신의 성장을 돕습니다. 리더십 개발과 경력 관리에 대한 전문적인 조언을 제공합니다."
    },
    {
        "name": "민지원 친구", 
        "img": PERSONA_IMAGES["민지원 친구"],
        "desc": "또래 상담사 | 공감 전문가",
        "explanation": "편안하고 친근한 대화를 통해 당신의 고민을 함께 나누고 해결책을 모색합니다. 젊은 세대의 고민을 깊이 이해합니다."
    },
    {
        "name": "이현우 상담가", 
        "img": PERSONA_IMAGES["이현우 상담가"],
        "desc": "임상심리전문가 | CBT 전문가",
        "explanation": "객관적이고 분석적인 관점에서 문제 해결을 돕습니다. 인지행동치료와 해결중심치료 전문가입니다."
    },
    {
        "name": "정유진 카운셀러", 
        "img": PERSONA_IMAGES["정유진 카운셀러"],
        "desc": "예술치료사 | 감정코칭 전문가",
        "explanation": "창의적이고 감성적인 접근으로 당신의 내면을 탐색합니다. 예술치료와 감정 표현 전문가입니다."
    },
]

def get_page_styles() -> str:
    """페이지 스타일 CSS를 반환하는 함수"""
    return """
        <style>
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            margin: -1rem -1rem 2rem -1rem;
            color: white;
        }
        
        .main-header h1 {
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            background: linear-gradient(120deg, #b3d9ff, #80bfff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .main-header p {
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.8);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .persona-container {
            display: flex;
            flex-direction: row;
            justify-content: center;
            gap: 1.5rem;
            padding: 0 2rem;
            margin-top: 2rem;
            flex-wrap: nowrap;
            overflow-x: auto;
        }
        
        .persona-card {
            background: #2d2d2d;
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
            min-width: 280px;
            max-width: 280px;
            height: 400px;
            display: flex;
            flex-direction: column;
        }
        
        .persona-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .persona-image {
            width: 100%;
            height: 200px;
            border-radius: 8px;
            margin-bottom: 1rem;
            object-fit: cover;
        }
        
        .persona-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: white;
            margin-bottom: 0.5rem;
        }
        
        .persona-desc {
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 1rem;
        }
        
        .persona-explanation {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.6);
            margin: 0.5rem 0;
            flex-grow: 1;
        }
        </style>
    """

def render_home():
    """홈페이지 렌더링"""
    # 페이지 헤더
    st.markdown("""
        <div class="main-header">
            <h1>AI 감정 케어 서비스</h1>
            <p>당신의 이야기에 귀 기울여줄 상담 파트너를 선택해주세요</p>
        </div>
    """, unsafe_allow_html=True)

    # 스타일 적용
    st.markdown(get_page_styles(), unsafe_allow_html=True)

    # 페르소나 선택 섹션을 가로로 배치
    cols = st.columns(5)
    
    for idx, persona in enumerate(PERSONAS):
        with cols[idx]:
            st.markdown(f"""
                <div class="persona-card">
                    <img src="{persona['img']}" class="persona-image" alt="{persona['name']}"/>
                    <div class="persona-title">{persona['name']}</div>
                    <div class="persona-desc">{persona['desc']}</div>
                    <div class="persona-explanation">{persona['explanation']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Streamlit 버튼으로 변경
            if st.button("대화 시작하기", key=f"persona_button_{idx}"):
                # 세션 상태 초기화
                clear_session_state()
                
                # 새로운 페르소나로 초기화
                initialize_session_state(persona['name'])
                
                # URL 파라미터 설정
                st.query_params["page"] = "chat"
                st.query_params["persona"] = PERSONA_URL_MAPPING[persona['name']]
                
                # 페이지 새로고침
                st.rerun()
