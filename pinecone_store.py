import os
from dotenv import load_dotenv
import time
from tqdm import tqdm
from uuid import uuid4

from pinecone import Pinecone,ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from PyPDF2 import PdfReader

# .env 파일에서 환경 변수 로드
load_dotenv()

# 필요한 환경 변수 불러오기
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API 키와 환경 변수 확인
if not PINECONE_API_KEY or not OPENAI_API_KEY or not PINECONE_ENVIRONMENT:
    raise ValueError("PINECONE_API_KEY, OPENAI_API_KEY, PINECONE_ENVIRONMENT 환경 변수를 설정해주세요.")

EMBEDDING_DIMENSION = 1536

def load_pdf_documents(pdf_path):
    documents = []
    pdf_reader = PdfReader(pdf_path)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    metadata = {'source': pdf_path}
    documents.append(Document(page_content=text, metadata=metadata))
    return documents

def create_embeddings_and_db(documents):
    # 문서 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    split_docs = text_splitter.split_documents(documents)

    # OpenAI 임베딩 생성
    embeddings = OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=OPENAI_API_KEY
    )

    # Pinecone 초기화 및 인덱스 생성
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "law-index"

    # 인덱스가 없으면 생성
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric='cosine',
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        # 인덱스가 준비될 때까지 대기
        while True:
            if pc.describe_index(index_name).status['ready']:
                break
            time.sleep(1)

    # 인덱스 연결
    index = pc.Index(index_name)

    # PineconeVectorStore 생성
    vectorstore = PineconeVectorStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )

    # 문서에 UUID 할당 및 추가
    uuids = [str(uuid4()) for _ in range(len(split_docs))]
    for doc, uuid in tqdm(zip(split_docs, uuids), total=len(split_docs), desc="Pinecone에 문서 추가 중"):
        vectorstore.add_documents(documents=[doc], ids=[uuid])

    print("문서 저장이 완료되었습니다.")
    return vectorstore

if __name__ == "__main__":
    pdf_path = "test.pdf"
    documents = load_pdf_documents(pdf_path)
    create_embeddings_and_db(documents)