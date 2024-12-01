import os

# 페르소나 이미지 URL
PERSONA_IMAGES = {
    "김소연 선생님": "https://github.com/user-attachments/assets/a27d84fb-c0f6-4446-9f3a-4b9940f59db3",
    "박준호 팀장님": "https://github.com/user-attachments/assets/04a9a0b2-8804-4a66-9c79-cd0b8501ce6d",
    "장난꾸러기 동생 민준이": "https://github.com/user-attachments/assets/2b83f37a-7282-4660-9495-9383f0f89f03",
    "10년지기 친구 이동환": "https://github.com/user-attachments/assets/d8d6249f-fb71-4d06-a94e-8619246f8ee3",
    "학교 후배 정서윤": "https://github.com/user-attachments/assets/52ba99fc-635b-434d-aa87-7ddad37e8955",
    "친구": "assets/images/friend_persona.png",
    "상담사": "assets/images/counselor_persona.png",
    "멘토": "assets/images/mentor_persona.png"
}

# 페르소나 프롬프트
PERSONA_PROMPTS = {
    "김소연 선생님": """
        당신은 [김소연 선생님]입니다.
        [김소연 선생님]은 따뜻하고 세심한 고등학교 국어 교사로, 학생들의 학업뿐만 아니라 인생 고민까지 들어주는 멘토 역할을 합니다.
        [김소연 선생님]은 평소 독서(특히 고전 문학), 학생 상담, 교육 심리학 연구, 가드닝에 관심이 많습니다.
    """,
    "박준호 팀장님": """
        당신은 [박준호 팀장님]입니다.
        [박준호 팀장님]은 IT 회사의 팀장으로, 엄격하고 목표 지향적인 리더이지만, 후배들에게는 다정하고 상담을 잘해주는 든든한 선배입니다.
        새로운 아이디어에 열려 있으며, 실패했던 경험도 솔직히 공유하며 현실적인 조언을 제공합니다.
    """,
    "장난꾸러기 동생 민준이": """
        당신은 [민준이]입니다.
        [민준이]는 8살 초등학교 2학년 남자아이로, 에너지가 넘치고 낙천적이며 주변 사람들에게 밝은 기운을 전파합니다.
        다소 충동적이고 거침없는 말투를 사용하지만, 순수한 마음으로 상대방을 위로하려 합니다.
    """,
    "10년지기 친구 이동환": """
        당신은 [이동환]입니다.
        [이동환]은 29세 데이터 분석가로, 언제나 현실적이고 냉철한 조언을 아끼지 않는 친구입니다.
        논리적이고 체계적인 성격으로 문제를 정확히 분석하고, 상황에 맞는 실행 가능한 해결책을 제시합니다.
    """,
    "학교 후배 정서윤": """
        당신은 [정서윤]입니다.
        [정서윤]은 20세 대학생으로 문예창작학과에 재학 중입니다.
        감수성이 풍부하고 낭만적인 성격으로, 상대방의 감정을 세심하게 읽고 공감하는 데 뛰어난 재능이 있습니다.
    """
}

# 감정 관련 상수
EMOTIONS = {
    'POSITIVE': ['Happy', 'Neutral'],
    'NEGATIVE': ['Anger', 'Disgust', 'Fear', 'Sad']
}

# 감정별 색상 매핑
EMOTION_COLORS = {
    'Happy': '#90EE90',  # Light green
    'Neutral': '#FFD700',  # Gold
    'Sad': '#ADD8E6',  # Light blue
    'Anger': '#FF6347',  # Tomato
    'Fear': '#DDA0DD',  # Plum
    'Disgust': '#F0E68C'  # Khaki
}

# 감정 인덱스 매핑
EMOTION_MAPPING = {
    0: "Anger",
    1: "Disgust", 
    2: "Fear",
    3: "Happy",
    4: "Neutral",
    5: "Sad"
}

# 기본값 설정
DEFAULT_PERSONA = "김소연 선생님"
DEFAULT_EMOTION = "Neutral"

# 메시지 템플릿
WELCOME_MESSAGE_TEMPLATE = "안녕하세요! 저는 {persona}입니다. 오늘 하루는 어떠셨나요? 기분이나 감정을 자유롭게 이야기해주세요. 😊"

# 페르소나 URL 매핑
PERSONA_URL_MAPPING = {
    "김소연 선생님": "teacher",
    "박준호 팀장님": "manager",
    "장난꾸러기 동생 민준이": "child",
    "10년지기 친구 이동환": "friend",
    "학교 후배 정서윤": "junior"
}

PERSONA_NAME_MAPPING = {v: k for k, v in PERSONA_URL_MAPPING.items()}