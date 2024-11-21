# 감정인식 챗봇 (Emotion-Aware Chatbot) 🤖

## 📌 프로젝트 소개

이 프로젝트는 **사용자의 감정을 인식**하고 **공감적인 대화**를 나눌 수 있는 AI 챗봇입니다. **GPT-4**와 **감정 분석 모델**을 활용하여 사용자의 감정 상태를 파악하고 적절한 응답을 제공합니다.

## 🌟 주요 기능

-   🎯 **실시간 감정 분석**
-   💬 **맥락을 이해하는 대화**
-   📊 **대화 통계 추적**
-   🤝 **공감적인 응답 생성**

## 🛠 기술 스택

-   **Frontend**: Streamlit
-   **Backend**: Python
-   **AI Models**:
    -   OpenAI GPT-4
    -   DistilRoBERTa (감정 분석)
-   **Dependencies**: PyTorch, Transformers, Langchain

## 🚀 설치 방법

1. ### **저장소 클론**

    ```bash
    git clone https://github.com/your-username/emotion-aware-chatbot.git
    cd emotion-aware-chatbot
    ```

2. ### **가상환경 생성 및 활성화**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. ### **필요한 패키지 설치**

    ```bash
    pip install -r requirements.txt
    ```

4. ### **환경 변수 설정**

    `.env` 파일을 생성하고 다음 내용을 추가합니다:

    ```env
    OPENAI_API_KEY=your_openai_api_key
    HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
    ```

## 🏃‍♀️ 실행 방법

```bash
streamlit run run.py
```

## 📂 프로젝트 구조

```plaintext
emotion-aware-chatbot/
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── config.py
│   ├── core/
│   │   ├── models/
│   │   │   └── document.py
│   │   └── services/
│   │       └── chatbot_service.py
│   ├── components/
│   │   ├── chat_interface.py
│   │   ├── message_display.py
│   │   └── sidebar.py
│   └── utils/
│       ├── initialization.py
│       └── message_handler.py
├── .env
├── requirements.txt
├── run.py
└── README.md
```

### 📁 디렉토리 및 파일 설명

-   **src/** - 소스 코드의 메인 디렉토리
    -   **app/** - 애플리케이션 설정 및 실행 코드
        -   **main.py** - 앱의 메인 실행 파일
        -   **config.py** - 설정 관리 (API 키, 모델 설정 등)
    -   **core/** - 핵심 비즈니스 로직
        -   **models/** - 데이터 모델 정의
        -   **services/** - 챗봇 서비스 로직 (감정 분석, 응답 생성 등)
    -   **components/** - UI 컴포넌트
        -   **chat_interface.py** - 채팅 인터페이스 구현
        -   **message_display.py** - 메시지 표시 로직
        -   **sidebar.py** - 사이드바 구현
    -   **utils/** - 유틸리티 함수 모음
        -   **initialization.py** - 초기화 함수
        -   **message_handler.py** - 메시지 처리 유틸리티
-   **.env** - 환경 변수 파일 (API 키 등)
-   **requirements.txt** - 필요한 패키지 목록
-   **run.py** - 애플리케이션 실행 파일
-   **README.md** - 프로젝트 설명서

> **Note**: 코드의 역할과 책임이 명확하게 분리되어 있어 유지보수와 확장이 용이합니다.

## 🔍 주요 컴포넌트 설명

### **1. ChatbotService**

-   **사용자 입력 처리**
-   **감정 분석 수행**
-   **GPT-4를 통한 응답 생성**

### **2. 감정 분석**

-   **DistilRoBERTa 기반 감정 분석 모델 사용**
-   **7가지 감정 분류**: 기쁨, 슬픔, 분노, 공포, 혐오, 놀람, 중립

### **3. 사용자 인터페이스**

-   **Streamlit 기반의 직관적인 채팅 인터페이스**
-   **실시간 감정 상태 표시**
-   **대화 이력 관리 기능**

## ⚙️ 환경 요구사항

-   **Python 3.8 이상**
-   **CUDA 지원** (선택 사항)
-   **최소 4GB RAM**
-   **OpenAI API 키**
-   **Hugging Face API 토큰**

## 📄 라이선스

이 프로젝트는 **MIT 라이선스**를 따릅니다.

## 🤝 기여 방법

1. **저장소 포크**

2. **기능 브랜치 생성**

    ```bash
    git checkout -b feature/새로운기능
    ```

3. **변경 사항 커밋**

    ```bash
    git commit -m '새로운 기능 추가'
    ```

4. **브랜치에 푸시**

    ```bash
    git push origin feature/새로운기능
    ```

5. **Pull Request 생성**

## 📬 문의사항

프로젝트에 대한 문의는 **Issues** 탭에 등록해 주세요.
