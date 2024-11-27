import speech_recognition as sr
from transformers import pipeline
import torchaudio
import io
import os

# Whisper 모델 로드
whisper_model = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

def convert_audio_with_google(audio_path):
    """
    Google Speech Recognition API를 사용해 오디오를 텍스트로 변환
    """
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        # Google Speech Recognition API로 변환
        text = recognizer.recognize_google(audio_data)
        print(f"[DEBUG] Google Speech Recognition 결과: {text}")
        return text
    except sr.UnknownValueError:
        print("[DEBUG] Google Speech Recognition이 음성을 이해하지 못했습니다.")
        return None
    except Exception as e:
        print(f"[ERROR] Google API 처리 중 오류 발생: {e}")
        return None


def process_audio_with_whisper(audio_path):
    """
    Whisper 모델을 사용해 오디오를 텍스트로 변환
    """
    try:
        waveform, sample_rate = torchaudio.load(audio_path)
        print(f"[DEBUG] Waveform Shape: {waveform.shape}, Sample Rate: {sample_rate}")

        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        result = whisper_model(waveform.squeeze().numpy())
        text = result.get("text", "").strip()
        print(f"[DEBUG] Whisper 모델 결과: {text}")
        return text
    except Exception as e:
        print(f"[ERROR] Whisper 처리 중 오류 발생: {e}")
        return None


def process_audio_input(audio_bytes):
    """
    Google API와 Whisper 모델을 병행하여 오디오를 텍스트로 변환
    """
    try:
        # 파일을 임시 저장
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        print("[DEBUG] 임시 파일 저장 완료. Google API로 변환 시도 중...")
        # 1. Google Speech Recognition으로 텍스트 변환 시도
        google_text = convert_audio_with_google(temp_audio_path)

        if google_text:
            print(f"[DEBUG] Google 변환 성공: {google_text}")
            return google_text

        print("[DEBUG] Google 변환 실패. Whisper로 대체 시도 중...")
        # 2. Google API가 실패하면 Whisper로 폴백
        whisper_text = process_audio_with_whisper(temp_audio_path)
        if whisper_text:
            print(f"[DEBUG] Whisper 변환 성공: {whisper_text}")
        return whisper_text
    finally:
        # 임시 파일 삭제
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print("[DEBUG] 임시 파일 삭제 완료.")
