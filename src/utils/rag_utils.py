from typing import List, Dict, Any, Tuple
from pinecone import Pinecone, ServerlessSpec
from langchain.vectorstores import Pinecone as LangchainPinecone
from sentence_transformers import SentenceTransformer
from langchain.embeddings import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv, find_dotenv
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 환경변수 로드
env_path = find_dotenv(raise_error_if_not_found=True)
load_dotenv(env_path, override=True)

class RAGUtils:
    def __init__(self):
        # API 키 직접 가져오기
        api_key = os.getenv("PINECONE_API_KEY")
        environment = os.getenv("PINECONE_ENVIRONMENT")
        self.index_name = os.getenv("PINECONE_INDEX_NAME")

        # 환경변수 확인
        print("\n=== RAGUtils Initialization ===")
        print(f"API Key length: {len(api_key) if api_key else 'None'}")
        print(f"Environment: {environment}")
        print(f"Index Name: {self.index_name}")
        
        if not all([api_key, environment, self.index_name]):
            raise ValueError("Missing required environment variables")

        # 384차원 임베딩 모델 초기화
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"  # 384차원 임베딩
        )
        
        # Pinecone 초기화
        try:
            self.pc = Pinecone(
                api_key=api_key,
                environment=environment
            )
            print("Pinecone client initialized successfully")
            
            # 새 인덱스 생성 (기존 인덱스가 없는 경우)
            try:
                indexes = self.pc.list_indexes()
                if self.index_name not in indexes.names():
                    print(f"\nCreating new index: {self.index_name}")
                    self.pc.create_index(
                        name=self.index_name,
                        dimension=384,  # MiniLM 모델의 임베딩 차원
                        metric='cosine',
                        spec=ServerlessSpec(
                            cloud="aws",
                            region="us-east-1"
                        )
                    )
                    print("Index created successfully")
                else:
                    print(f"\nUsing existing index: {self.index_name}")
            except Exception as e:
                print(f"Error with index operations: {str(e)}")
                raise
            
            # Langchain Pinecone 벡터스토어 초기화
            self.vectorstore = LangchainPinecone.from_existing_index(
                index_name=self.index_name,
                embedding=self.embeddings,
                namespace=""
            )
            print("Vectorstore initialized successfully")
            
        except Exception as e:
            print(f"\nError in RAGUtils initialization: {str(e)}")
            raise

    def retrieve_relevant_context(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        주어진 쿼리와 관련된 문서를 검색합니다.
        """
        try:
            print(f"\n=== Searching for relevant documents ===")
            print(f"Query: {query}")
            
            # 쿼리를 벡터로 변환
            vector = self.embeddings.embed_query(query)  # encode 대신 embed_query 사용
            
            # Pinecone 인덱스에서 검색
            results = self.pc.Index(self.index_name).query(
                vector=vector,  # 이미 리스트 형태로 반환됨
                top_k=k,
                include_metadata=True
            )
            
            # 결과 처리
            processed_results = []
            for match in results.matches:
                metadata = match.metadata
                if metadata and 'content' in metadata:  # content 필드가 있는 경우
                    processed_results.append({
                        'content': metadata['content'],
                        'metadata': {
                            'disease': metadata.get('disease', ''),
                            'tab': metadata.get('tab', '')
                        }
                    })
                    print(f"Found document: {metadata.get('disease', '')} - {metadata.get('tab', '')}")
            
            print(f"Found {len(processed_results)} relevant documents")
            return processed_results
            
        except Exception as e:
            print(f"Error in retrieve_relevant_context: {str(e)}")
            print(f"Error details: {type(e).__name__}")
            return []

    def get_augmented_prompt(self, query: str, persona: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        검색 결과를 포함한 증강된 프롬프트를 생성합니다.
        """
        # 관련 문서 검색
        relevant_docs = self.retrieve_relevant_context(query)
        
        # 컨텍스트 구성
        context = "\n\n".join([
            f"문서 {i+1}:\n{doc['content']}" 
            for i, doc in enumerate(relevant_docs)
        ])
        
        # 프르소나별 맞춤 프롬프트 생성
        prompt = f"""
        다음 정보를 참고하여 사용자의 질문에 답변해주세요.
        
        참고할 정보:
        {context if context.strip() else "관련 정보가 없습니다."}
        
        사용자 질문: {query}
        
        답변 시 주의사항:
        1. 위 참고 정보의 내용을 반드시 활용하되, 페르소나의 특성에 맞게 자연스럽게 설명해주세요.
        2. 의학 용어나 전문적인 설명은 페르소나의 성격에 맞게 쉽게 풀어서 설명해주세요.
        3. 각 페르소나의 특징을 살려주세요:
           - 김소연 선생님: 따뜻하고 세심한 설명, 이해하기 쉬운 비유 사용
           - 박준호 팀장님: 논리적이고 체계적인 설명, 실용적인 조언
           - 민준이: 단순하고 직관적인 설명, 재미있는 비유
           - 이동환: 팩트 위주의 명확한 설명, 현실적인 조언
           - 정서윤: 감성적이고 공감적인 설명, 문학적 표현
        4. 참고 정보에 있는 구체적인 수치나 기관명 등은 자연스럽게 언급해주세요.
        5. 마지막에는 페르소나 특성에 맞는 위로나 격려의 말을 덧붙여주세요.
        
        위 내용을 {persona}의 성격과 말투로 자연스럽게 답변해주세요.
        """
        
        return prompt, relevant_docs