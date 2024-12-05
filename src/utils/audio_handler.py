import torchaudio
import torch
import os
from transformers import AutoModelForAudioClassification, AutoProcessor
from pydub import AudioSegment
import sounddevice as sd
import numpy as np
import wave
import streamlit as st
import whisper
import speech_recognition as sr

# 음성 감정 인식 모델 설정
MODEL_NAME = "forwarder1121/ast-finetuned-model"
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)


class AudioRecorder:
    def __init__(self):
        self.frames = []
        self.samplerate = 16000  # 샘플링 레이트
        self.channels = 1  # 채널 수
        self.is_recording = False

    def start_recording(self):
        """녹음을 시작합니다."""
        print("[DEBUG] 녹음 시작")
        self.frames = []
        self.is_recording = True

        def callback(indata, frames, time, status):
            if self.is_recording:
                self.frames.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=self.samplerate,
            channels=self.channels,
            callback=callback
        )
        self.stream.start()
        print("[DEBUG] 스트림 시작 완료")

    def stop_recording(self):
        """녹음을 중지하고 WAV 파일로 저장합니다."""
        print("[DEBUG] 녹음 중지")
        self.is_recording = False
        self.stream.stop()
        self.stream.close()

        # WAV 파일로 저장
        temp_path = "temp_recording.wav"
        print(f"[DEBUG] WAV 파일 저장 중: {temp_path}")
        with wave.open(temp_path, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(sd.default.samplerate.bit_length() // 8)
            wf.setframerate(self.samplerate)
            wf.writeframes(b''.join([frame.tobytes() for frame in self.frames]))
        print("[DEBUG] WAV 파일 저장 완료")

        return temp_path


def transcribe_audio(audio_path: str) -> str:
    """오디오 파일을 텍스트로 변환합니다."""
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language='ko-KR')
            except:
                model = whisper.load_model("base")
                result = model.transcribe(audio_path, language='ko')
                return result.get("text", "").strip()
    except Exception as e:
        print(f"[ERROR] 음성 변환 오류: {e}")
        return None


def predict_audio_emotion(audio_path: str) -> str:
    """오디오 파일의 감정을 예측합니다."""
    try:
        waveform, sample_rate = torchaudio.load(audio_path, backend="soundfile")
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
        inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
        emotion_mapping = {
            0: "Anger", 1: "Disgust", 2: "Fear",
            3: "Happy", 4: "Neutral", 5: "Sad"
        }
        return emotion_mapping[torch.argmax(outputs.logits, dim=1).item()]
    except Exception as e:
        print(f"[ERROR] 감정 분석 오류: {e}")
        return "Neutral"


def process_recorded_audio():
    """실시간 녹음된 오디오를 처리합니다."""
    try:
        if not hasattr(st.session_state, 'audio_recorder'):
            print("[ERROR] AudioRecorder가 초기화되지 않았습니다.")
            return None, "Neutral"

        recorder = st.session_state.audio_recorder
        audio_path = recorder.stop_recording()
        if not audio_path or not os.path.exists(audio_path):
            return None, "Neutral"

        text = transcribe_audio(audio_path)
        emotion = predict_audio_emotion(audio_path)
        os.remove(audio_path)  # 임시 파일 삭제
        return text, emotion
    except Exception as e:
        print(f"[ERROR] 오디오 처리 오류: {e}")
        return None, "Neutral"
