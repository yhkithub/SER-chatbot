import streamlit as st
import os

# Streamlit secrets를 환경변수로 설정
print("\n=== Loading Streamlit Secrets ===")
if 'secrets' in st.__dict__:
    for key, value in st.secrets.items():
        os.environ[key] = value
        print(f"Loaded secret: {key}")
else:
    print("No secrets found in Streamlit configuration")

# 환경변수 확인
print("\n=== Checking Environment Variables ===")
required_vars = [
    "OPENAI_API_KEY",
    "PINECONE_API_KEY",
    "PINECONE_ENVIRONMENT",
    "PINECONE_INDEX_NAME"
]

missing_vars = []
for var in required_vars:
    value = os.getenv(var)
    is_present = "✓" if value else "✗"
    print(f"{is_present} {var}: {'Present' if value else 'Missing'}")
    if not value:
        missing_vars.append(var)

if missing_vars:
    st.error(f"Missing required environment variables: {', '.join(missing_vars)}")
    st.info("Please set these variables in Streamlit's secrets management")
    st.stop()

print("=== End Environment Variables Check ===\n")

from src.app.main import main

if __name__ == "__main__":
    main() 