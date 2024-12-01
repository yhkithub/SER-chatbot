import streamlit as st
from functools import wraps
from typing import Callable

def handle_streamlit_errors(func: Callable):
    """Streamlit 에러 처리 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")
            st.error("페이지를 새로고침하거나 다시 시도해주세요.")
            raise
    return wrapper 