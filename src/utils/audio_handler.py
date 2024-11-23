import speech_recognition as sr
from pydub import AudioSegment
import io
import streamlit as st

def convert_audio_to_text(wav_audio_data, language):
    """음성 데이터를 텍스트로 변환하는 함수"""
    try:
        # WAV 데이터를 AudioSegment로 변환 및 표준화
        audio = AudioSegment.from_file(io.BytesIO(wav_audio_data), format="wav")
        audio = audio.set_channels(1)  # 단일 채널 (모노)
        audio = audio.set_frame_rate(16000)  # 16kHz 샘플링 레이트

        # Google API가 처리 가능한 형식으로 변환
        audio_file = io.BytesIO()
        audio.export(audio_file, format="wav")
        audio_file.seek(0)

        # 음성 인식
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        st.error("음성을 텍스트로 변환할 수 없습니다. 음성이 명확하지 않을 수 있습니다.")
        return None
    except Exception as e:
        st.error(f"음성 인식 중 오류가 발생했습니다: {str(e)}")
        return None

def process_audio_input(wav_audio_data, language):
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
