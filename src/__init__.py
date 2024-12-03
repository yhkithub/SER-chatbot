from dotenv import load_dotenv
import os

# 환경변수 로드
load_dotenv()

# SSL 검증 비활성화
os.environ['CURL_CA_BUNDLE'] = ''

# 환경변수 확인
print("\n=== Global Environment Variables ===")
print(f"PINECONE_API_KEY: {os.getenv('PINECONE_API_KEY')}")
print(f"PINECONE_ENVIRONMENT: {os.getenv('PINECONE_ENVIRONMENT')}")
print(f"PINECONE_INDEX_NAME: {os.getenv('PINECONE_INDEX_NAME')}")
print("=== End Global Environment Variables ===\n") 