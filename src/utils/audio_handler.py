import speech_recognition as sr
from pydub import AudioSegment
import io
import streamlit as st

def convert_audio_to_text(wav_audio_data, language='ko-KR'):
    """음성 데이터를 텍스트로 변환하는 함수"""
    try:
        # WAV 데이터를 AudioSegment로 변환
        audio = AudioSegment.from_file(io.BytesIO(wav_audio_data), format="wav")

        # 파일 정보 출력 (디버깅용)
        st.write(f"Audio Info: Channels={audio.channels}, Frame Rate={audio.frame_rate}, Duration={len(audio)}ms")

        # 오디오를 16kHz, 모노로 표준화
        audio = audio.set_frame_rate(16000).set_channels(1)

        # 음성이 너무 짧은 경우 패딩 추가
        if len(audio) < 1000:  # 1초 미만인 경우
            silence = AudioSegment.silent(duration=1000 - len(audio))
            audio = audio + silence

        # Google API가 처리할 수 있는 형식으로 변환
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

def process_audio_input(wav_audio_data, language_options=('ko-KR', 'en-US')):
    """음성 입력을 처리하고 결과를 반환하는 함수"""
    if wav_audio_data is not None:
        # 음성 재생 가능하도록 표시
        st.sidebar.audio(wav_audio_data, format='audio/wav')

        # 음성을 텍스트로 변환 (다중 언어 지원)
        for language in language_options:
            st.write(f"Trying language: {language}")  # 시도 중인 언어 표시
            text = convert_audio_to_text(wav_audio_data, language=language)
            if text:
                st.sidebar.success(f"인식된 텍스트: {text} (언어: {language})")
                return text, language

        # 모든 언어 변환 실패
        st.sidebar.error("음성을 텍스트로 변환하지 못했습니다.")
        return None, None

