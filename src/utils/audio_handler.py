import torchaudio
import torch
import os
from transformers import pipeline
from pydub import AudioSegment
import speech_recognition as sr

# Whisper 모델 로드
whisper_model = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

def convert_with_google(audio_path):
    """
    Google Speech Recognition API를 사용하여 오디오를 텍스트로 변환
    """
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        print(f"[DEBUG] Google Speech Recognition 결과: {text}")
        return text
    except sr.UnknownValueError:
        print("[DEBUG] Google Speech Recognition이 텍스트를 감지하지 못했습니다.")
        return None
    except Exception as e:
        print(f"[ERROR] Google Speech Recognition 오류: {e}")
        return None

def convert_with_whisper(audio_path):
    """
    Whisper 모델을 사용하여 오디오를 텍스트로 변환
    """
    try:
        waveform, sample_rate = torchaudio.load(audio_path)
        print(f"[DEBUG] Waveform Shape: {waveform.shape}, Sample Rate: {sample_rate}")

        # 16kHz로 리샘플링
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        result = whisper_model(waveform.squeeze().numpy())
        text = result.get("text", "").strip()
        print(f"[DEBUG] Whisper 결과: {text}")
        return text
    except Exception as e:
        print(f"[ERROR] Whisper 처리 중 오류 발생: {e}")
        return None

def process_audio_file(audio_bytes, temp_audio_path="temp_audio.wav"):
    """
    Google API와 Whisper를 병행하여 오디오를 텍스트로 변환
    """
    try:
        # 임시 파일 저장
        with open(temp_audio_path, "wb") as f:
            f.write(audio_bytes)

        print(f"[DEBUG] 임시 파일 저장 완료: {temp_audio_path}")

        # Google API 시도
        google_text = convert_with_google(temp_audio_path)
        if google_text:
            return google_text  # Google API 성공

        # Google 실패 시 Whisper 시도
        print("[DEBUG] Google 실패, Whisper로 대체 시도...")
        whisper_text = convert_with_whisper(temp_audio_path)
        return whisper_text

    except Exception as e:
        print(f"[ERROR] Audio Processing Error: {e}")
        return None
    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
            print(f"[DEBUG] 임시 파일 삭제 완료: {temp_audio_path}")
