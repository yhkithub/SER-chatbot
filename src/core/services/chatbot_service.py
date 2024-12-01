import os
from dataclasses import dataclass
from typing import Dict
from transformers import pipeline
from langchain_openai import ChatOpenAI
from src.core.services.personas import PERSONAS
<<<<<<< HEAD
=======
from src.app.constants import DEFAULT_PERSONA, PERSONA_PROMPTS
>>>>>>> 7b5f7e1 (feat: 대화 통계 기능 추가 및 페르소나 전환 버그 수정)

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
<<<<<<< HEAD
        persona_prompt = PERSONAS.get(persona_name, "기본 페르소나 프롬프트")
        prompt = f"""
        {persona_prompt}
    
        사용자 메시지: {user_input}
    
        [페르소나]의 답변:
        응답에 페르소나 이름을 포함하지 마세요. 단순히 대화 내용을 작성하세요.
=======
        """GPT 응답 생성"""
        print("\n=== GPT 응답 생성 디버그 ===")
        print(f"요청된 페르소나: {persona_name}")
        print(f"사용 가능한 페르소나: {list(PERSONA_PROMPTS.keys())}")
        
        # 페르소나 프롬프트 가져오기
        if persona_name not in PERSONA_PROMPTS:
            print(f"경고: 페르소나 '{persona_name}'를 찾을 수 없음")
            persona_name = DEFAULT_PERSONA
            print(f"기본 페르소나로 대체: {persona_name}")
        
        persona_prompt = PERSONA_PROMPTS[persona_name]
        print(f"선택된 페르소나: {persona_name}")
        
        prompt = f"""
        {persona_prompt}
        
        사용자의 메시지: {user_input}
        
        위 페르소나 설정을 바탕으로 사용자의 메시지에 공감하고 적절한 응답을 해주세요.
        응답은 반드시 한국어로 해주세요.
        응답에는 페르소나의 특징이 잘 드러나야 합니다.
>>>>>>> 7b5f7e1 (feat: 대화 통계 기능 추가 및 페르소나 전환 버그 수정)
        """
    
        # GPT 호출
        response = self.llm.invoke(prompt)
<<<<<<< HEAD
        cleaned_response = response.content.strip()  # 응답 양 끝 공백 제거
        print(f"[DEBUG] GPT Response: {cleaned_response}")
        return cleaned_response
=======
        return response.content.strip()
>>>>>>> 7b5f7e1 (feat: 대화 통계 기능 추가 및 페르소나 전환 버그 수정)

