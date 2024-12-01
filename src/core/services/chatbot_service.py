import os
from dataclasses import dataclass
from typing import Dict, Optional
from transformers import pipeline
from langchain_openai import ChatOpenAI
from src.app.constants import DEFAULT_PERSONA, PERSONA_PROMPTS
from src.utils.error_handling import handle_streamlit_errors

@dataclass
class ChatbotService:
    def __init__(self, openai_config):
        self.llm = ChatOpenAI(
            api_key=openai_config.api_key,
            model_name=openai_config.chat_model,
            temperature=openai_config.temperature
        )
        self._initialize_emotion_classifier()

    def _initialize_emotion_classifier(self):
        """감정 분석 모델 초기화"""
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        self.emotion_classifier = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,
            device=-1
        )

    @handle_streamlit_errors
    def analyze_emotion(self, text: str) -> Dict[str, float]:
        """텍스트의 감정을 분석하여 감정별 점수를 반환"""
        results = self.emotion_classifier(text)
        return {score['label']: score['score'] for score in results[0]}

    @handle_streamlit_errors
    def get_response(self, user_input: str, persona_name: str) -> str:
        """사용자 입력에 대한 페르소나 기반 응답 생성"""
        print(f"\n=== GPT 응답 생성 디버그 ===")
        print(f"요청된 페르소나: {persona_name}")
        
        persona_prompt = PERSONA_PROMPTS.get(persona_name, PERSONA_PROMPTS[DEFAULT_PERSONA])
        print(f"선택된 페르소나: {persona_name}")
        
        prompt = f"""
        {persona_prompt}
        
        사용자의 메시지: {user_input}
        
        위 페르소나 설정을 바탕으로 사용자의 메시지에 공감하고 적절한 응답을 해주세요.
        응답은 반드시 한국어로 해주세요.
        응답에는 페르소나의 특징이 잘 드러나야 합니다.
        응답에는 '페르소나의 메시지:', '챗봇의 메시지:' 등의 접두어를 포함하지 마세요.
        """
    
        response = self.llm.invoke(prompt)
        return response.content.strip()

