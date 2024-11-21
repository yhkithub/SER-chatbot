import os
from dataclasses import dataclass
from typing import Dict
from transformers import pipeline
from langchain_openai import ChatOpenAI

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

    def get_response(self, user_input: str) -> str:
        # 동기 방식으로 변경
        emotions = self.analyze_emotion(user_input)
        dominant_emotion = max(emotions.items(), key=lambda x: x[1])[0]
        
        prompt = f"""
        사용자의 감정: {dominant_emotion}
        사용자 메시지: {user_input}
        
        위 내용에 대해 공감적이고 지지적인 응답을 해주세요. 
        필요한 경우 적절한 조언이나 위로의 말을 포함해주세요.
        응답은 한국어로 해주세요.
        """
        
        response = self.llm.invoke(prompt)
        return response.content
