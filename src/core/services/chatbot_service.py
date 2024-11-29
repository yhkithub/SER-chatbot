import os
from dataclasses import dataclass
from typing import Dict
from transformers import pipeline
from langchain_openai import ChatOpenAI
from src.core.services.personas import PERSONAS

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
        persona_prompt = PERSONAS.get(persona_name, "기본 페르소나 프롬프트")
        prompt = f"""
        {persona_prompt}
    
        사용자 메시지: {user_input}
    
        [페르소나]의 답변:
        응답에 페르소나 이름을 포함하지 마세요. 단순히 대화 내용을 작성하세요.
        """
    
        # GPT 호출
        response = self.llm.invoke(prompt)
        cleaned_response = response.content.strip()  # 응답 양 끝 공백 제거
        print(f"[DEBUG] GPT Response: {cleaned_response}")
        return cleaned_response

