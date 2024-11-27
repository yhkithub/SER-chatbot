from transformers import pipeline
import torchaudio
import os
import streamlit as st
from datetime import datetime

# Whisper 모델 로드
whisper_model = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

def process_audio_with_whisper(audio_file_path):
    """
    Whisper 모델을 사용해 오디오를 텍스트로 변환
    """
    try:
        # 오디오 로드
        waveform, sample_rate = torchaudio.load(audio_file_path)
        print(f"[DEBUG] Waveform Shape: {waveform.shape}, Sample Rate: {sample_rate}")

        # 16kHz로 샘플링 레이트 변경
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # Whisper 모델 입력
        print(f"[DEBUG] Passing data to Whisper model: {waveform.shape}")
        result = whisper_model(waveform.squeeze().numpy())
        print(f"[DEBUG] Whisper Result: {result}")
        return result['text']
    except Exception as e:
        print(f"[ERROR] Whisper 처리 중 오류 발생: {e}")
        return None

def process_audio_input(audio_bytes):
    """
    오디오 입력을 처리하여 텍스트 변환 결과 반환
    """
    try:
        text = convert_audio_to_text(audio_bytes)
        return text
    except Exception as e:
        print(f"[ERROR] Audio Processing Error: {e}")
        return None
