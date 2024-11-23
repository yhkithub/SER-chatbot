import speech_recognition as sr
from pydub import AudioSegment
import io
import streamlit as st

def convert_audio_to_text(wav_audio_data, languages=('ko-KR', 'en-US')):
    """음성 데이터를 텍스트로 변환하는 함수 (다중 언어 지원)"""
    try:
        # WAV 데이터를 AudioSegment로 변환 및 표준화
        audio = AudioSegment.from_file(io.BytesIO(wav_audio_data), format="wav")
        audio = audio.set_channels(1).set_frame_rate(16000)
        
        # Google API가 처리할 수 있는 형식으로 변환
        audio_file = io.BytesIO()
        audio.export(audio_file, format="wav")
        audio_file.seek(0)

        # 음성 인식
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        # 여러 언어로 변환 시도
        for language in languages:
            try:
                text = recognizer.recognize_google(audio_data, language=language)
                return text, language  # 성공 시 텍스트와 언어 반환
            except sr.UnknownValueError:
                continue  # 언어 실패 시 다음 언어로 진행

        # 모든 언어에서 실패한 경우
        st.error("음성을 텍스트로 변환할 수 없습니다. 음성이 명확하지 않을 수 있습니다.")
        return None, None
    except Exception as e:
        st.error(f"음성 인식 중 오류가 발생했습니다: {str(e)}")
        return None, None


def process_audio_input(wav_audio_data, language_options=('ko-KR', 'en-US')):
    """음성 입력을 처리하고 결과를 반환하는 함수"""
    if wav_audio_data is not None:
        # 음성 재생 가능하도록 표시
        st.sidebar.audio(wav_audio_data, format='audio/wav')
        
        # 음성을 텍스트로 변환
        text, detected_language = convert_audio_to_text(wav_audio_data, languages=language_options)
        
        if text:
            st.sidebar.success(f"인식된 텍스트: {text} (언어: {detected_language})")
            return text, detected_language
        else:
            st.sidebar.error("음성을 텍스트로 변환하지 못했습니다.")
            return None, None
    return None, None
