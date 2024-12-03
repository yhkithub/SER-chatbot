import streamlit as st
import os

# 환경변수 확인
print("\n=== Checking Streamlit Environment Variables ===")
required_vars = [
    "OPENAI_API_KEY",
    "PINECONE_API_KEY",
    "PINECONE_ENVIRONMENT",
    "PINECONE_INDEX_NAME"
]

for var in required_vars:
    value = os.getenv(var)
    is_present = "✓" if value else "✗"
    print(f"{is_present} {var}: {'Present' if value else 'Missing'}")
print("=== End Environment Variables Check ===\n")

from src.app.main import main

if __name__ == "__main__":
    main() 