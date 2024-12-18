import speech_recognition as sr
from pydub import AudioSegment
import io
import streamlit as st

def convert_audio_to_text(wav_audio_data, language='ko-KR'):
    """음성 데이터를 텍스트로 변환하는 함수"""
    try:
        # WAV 데이터를 AudioSegment로 변환
        audio = AudioSegment.from_wav(io.BytesIO(wav_audio_data))
        
        # 음성 인식기 초기화
        recognizer = sr.Recognizer()
        
        # AudioSegment를 speech_recognition에서 사용할 수 있는 형식으로 변환
        audio_file = audio.export(format="wav")
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            
        # 음성을 텍스트로 변환
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except Exception as e:
        st.error(f"음성 인식 중 오류가 발생했습니다: {str(e)}")
        return None

def process_audio_input(wav_audio_data, language='ko-KR'):
    """음성 입력을 처리하고 결과를 반환하는 함수"""
    if wav_audio_data is not None:
        # 음성 재생 가능하도록 표시
        st.sidebar.audio(wav_audio_data, format='audio/wav')
        
        # 음성을 텍스트로 변환
        text = convert_audio_to_text(wav_audio_data, language)
        
        if text:
            st.sidebar.success(f"인식된 텍스트: {text}")
            return text
        else:
            st.sidebar.error("음성을 텍스트로 변환하지 못했습니다.")
            return None
    return None