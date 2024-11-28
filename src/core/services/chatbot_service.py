import os
from dataclasses import dataclass
from typing import Dict
from transformers import pipeline
from langchain_openai import ChatOpenAI
from src.core.services import PERSONAS

os.environ["TOKENIZERS_PARALLELISM"] = "false"

@dataclass
class ChatbotService:
    def __init__(self, openai_config):
        self.llm = ChatOpenAI(
            api_key=openai_config.api_key,
            model_name=openai_config.chat_model,
            temperature=openai_config.temperature
        )
        self.emotion_classifier = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=None,
            device=-1
        )

    def analyze_emotion(self, text: str) -> Dict[str, float]:
        results = self.emotion_classifier(text)
        return {score['label']: score['score'] for score in results[0]}

    def get_response(self, user_input: str, persona_name: str) -> str:
        """
        사용자 입력과 선택된 페르소나를 기반으로 GPT 응답 생성.
        """
        # 페르소나 프롬프트 가져오기
        persona_prompt = PERSONAS.get(persona_name, "기본 페르소나 프롬프트")
        
        # 감정 분석
        emotions = self.analyze_emotion(user_input)
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]

        # 프롬프트 생성
        prompt = f"""
        {persona_prompt}

        사용자 메시지: {user_input}
        사용자의 감정: {dominant_emotion}

        [페르소나]의 답변:
        """

        # GPT 호출
        response = self.llm.invoke(prompt)
        return response.content
