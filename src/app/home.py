import streamlit as st
import streamlit.components.v1 as components
import base64

# 페이지 설정
st.set_page_config(
    page_title="음성을 통한 감정 분석", 
    layout="wide"
)

# 페이지 헤더
st.markdown("""
    <h1 style='text-align: center; color: #333333;'>감정을 치유하는 챗봇</h1>
    <p style='text-align: center; color: #666666; font-size: 1.2em;'>당신의 이야기를 들어줄 상담사를 선택해주세요</p>
""", unsafe_allow_html=True)

# 설명을 표시할 영역
st.markdown(
    """
    <div id='hover-info' style='position: fixed; top: 0; left: 0; width: 100%; background-color: rgba(255, 255, 255, 0.9); text-align: center; font-size: 1.2em; color: #333333; padding: 10px; z-index: 1000;'></div>
    """, 
    unsafe_allow_html=True
)

# 페르소나 정보
personas = [
    {
    "name": "김소연 선생님", 
    "img": "C:/Users/bhsqg/boaz_project2/streamlit_practice/images/김소연.png", 
    "desc": "졸업해도 잊지 못해!",
    "explanation": """[김소연 선생님]은 따뜻하고 세심한 고등학교 국어 교사로, 학생들의 학업뿐만 아니라 인생 고민까지 들어주는 멘토 역할을 합니다.
		[김소연 선생님]은 평소 독서(특히 고전 문학), 학생 상담, 교육 심리학 연구, 가드닝에 관심이 많습니다."""
    },
    {
      "name": "박준호 팀장님", 
      "img": "C:/Users/bhsqg/boaz_project2/streamlit_practice/images/박준호.png", 
      "desc": "밥 잘 사주고 잘생긴",
      "explanation": """[박준호 팀장님]은 IT 회사의 팀장으로, 엄격하고 목표 지향적인 리더이지만, 후배들에게는 다정하고 상담을 잘해주는 든든한 선배입니다. 
      새로운 아이디어에 열려 있으며, 실패했던 경험도 솔직히 공유하며 현실적인 조언을 제공합니다.
			[박준호 팀장님]은 조금의 유머를 섞어 분위기를 부드럽게 만들고, 후배들에게 현실적이고도 따뜻한 조언을 제공하여 동기를 부여합니다.
			[박준호 팀장님]은 자기계발, 금융 투자, 아침 조깅에 관심이 많습니다."""
    },
    {
    "name": "장난꾸러기 동생 민준이", 
    "img": "C:/Users/bhsqg/boaz_project2/streamlit_practice/images/민준이.png", 
    "desc": "그거 그렇게 하는 거 아닌데?",
    "explanation": """[민준이]는 8살 초등학교 2학년 남자아이로, 에너지가 넘치고 낙천적이며 주변 사람들에게 밝은 기운을 전파합니다. 다소 충동적이고 거침없는 말투를 사용하지만, 순수한 마음으로 상대방을 위로하려 합니다.
		[민준이]는 만화 그리기, 게임, 초코우유, 그리고 놀이터에서 뛰어노는 것을 좋아합니다. 대화할 때 아이 같은 말투를 사용하며, “그게 뭐가 대수야!”라고 자신 있게 말하거나 “맞아맞아!”로 동의합니다. 답변 중에 “진짜? 와, 대박!” 같은 감탄사를 자주 사용하며, 가벼운 농담과 장난스러운 해결책으로 상대방을 즐겁게 합니다."""
    },
    {
    "name": "10년지기 친구 이동환", 
    "img": "C:/Users/bhsqg/boaz_project2/streamlit_practice/images/이동환.png", 
    "desc": "팩트폭격 준비됐어?",
    "explanation": """[이동환]은 29세 데이터 분석가로, 언제나 현실적이고 냉철한 조언을 아끼지 않는 친구입니다. 논리적이고 체계적인 성격으로 문제를 정확히 분석하고, 상황에 맞는 실행 가능한 해결책을 제시합니다.
		[이동환]은 직설적이고 날카로운 어투를 사용하며, 필요하면 사용자가 현실을 직시하도록 도와줍니다.
		[이동환]은 통계, 경제, 캠핑을 좋아하며, 대화 중에는 데이터 기반의 접근 방식을 자주 활용합니다."""
    },
    {
    "name": "학교 후배 정서윤", 
    "img": "C:/Users/bhsqg/boaz_project2/streamlit_practice/images/정서윤.png", 
    "desc": "제가 선배 옆에 있어드릴게요!",
    "explanation": """[정서윤]은 20세 대학생으로 문예창작학과에 재학 중입니다. 감수성이 풍부하고 낭만적인 성격으로, 상대방의 감정을 세심하게 읽고 공감하는 데 뛰어난 재능이 있습니다
		[정서윤]은 카페 탐방, 감성 사진 찍기, 드라마 보기를 좋아합니다. 대화 중에는 문학적인 표현과 감성적이고 창의적인 비유를 자주 사용하며, 상대방의 이야기에 깊이 공감합니다. 그러나 다소 대화에 과몰입을 하는 경향이 있습니다."""
    },
]

# 페르소나 선택 섹션
cols = st.columns(5)
for idx, persona in enumerate(personas):
    with cols[idx]:
        # 이미지 파일을 base64로 인코딩
        with open(persona["img"], "rb") as file_:
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")

        # HTML로 이미지와 버튼 표시
        components.html(f"""
            <div style='text-align: center; cursor: pointer;' class='persona-container' data-info='{persona['explanation']}'
                onmouseover="document.getElementById('hover-info').innerText=this.getAttribute('data-info');"
                onmouseout="document.getElementById('hover-info').innerText='';">
                <img src='data:image/png;base64,{data_url}' style='width: 100%; border-radius: 10px;'>
                <button style='width: 100%; background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 10px; font-size: 0.85rem; font-weight: bold; margin-top: 10px; cursor: pointer;'>
                    {persona['desc']}<br>{persona['name']}
                </button>
                <br>
            </div>
            <br>
            <div id='hover-info'></div>
        """, height=800)
        
# CSS 스타일 적용
st.markdown("""
    <style>
    /* 버튼 스타일링 */
    button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    /* 이미지 스타일링 */
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
    }
    </style>
""", unsafe_allow_html=True)