import torchaudio
import torch
import os
from transformers import AutoModelForAudioClassification, AutoProcessor
from pydub import AudioSegment
import whisper
import streamlit as st
from streamlit_audio_recorder import audio_recorder  # 추가된 부분

# 음성 감정 인식 모델 설정
MODEL_NAME = "forwarder1121/ast-finetuned-model"
processor = AutoProcessor.from_pretrained(MODEL_NAME)
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)

def predict_audio_emotion(audio_path: str) -> str:
    """음성 파일의 감정을 예측합니다."""
    try:
        # 기본 감정을 'Neutral'로 설정
        default_emotion = "Neutral"

        # 음성 파일 로드
        waveform, sample_rate = torchaudio.load(
            audio_path,
            backend="soundfile"  # 백엔드 명시
        )

        # 리샘플링 (필요한 경우)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # 모델 입력 준비
        inputs = processor(waveform.squeeze().numpy(), sampling_rate=16000, return_tensors="pt")

        # 예측
        with torch.no_grad():
            outputs = model(**inputs)
            predicted_label = torch.argmax(outputs.logits, dim=1).item()

        # 감정 매핑
        emotion_mapping = {
            0: "Anger",
            1: "Disgust",
            2: "Fear",
            3: "Happy",
            4: "Neutral",
            5: "Sad"
        }

        predicted_emotion = emotion_mapping.get(predicted_label, default_emotion)
        print(f"[DEBUG] 예측된 음성 감정: {predicted_emotion}")
        return predicted_emotion

    except Exception as e:
        print(f"[ERROR] 음성 감정 분석 중 오류 발생: {str(e)}")
        return default_emotion

def transcribe_audio(audio_path: str) -> str:
    """오디오 파일을 텍스트로 변환합니다."""
    try:
        # Whisper 모델 로드
        model = whisper.load_model("base")
        result = model.transcribe(audio_path, language='ko')
        text = result["text"].strip()
        print(f"[Whisper] 변환 결과: {text}")
        return text

    except Exception as e:
        print(f"[ERROR] 음성 변환 중 오류 발생: {str(e)}")
        return None

def process_recorded_audio(audio_bytes):
    """녹음된 오디오 바이트를 처리합니다."""
    try:
        # 오디오 바이트를 임시 파일로 저장
        temp_audio_path = "temp_audio.wav"
        with open(temp_audio_path, 'wb') as f:
            f.write(audio_bytes)

        if not os.path.exists(temp_audio_path):
            print("[ERROR] 오디오 파일이 생성되지 않았습니다.")
            return None, "Neutral"

        # 텍스트 변환 및 감정 분석
        text = transcribe_audio(temp_audio_path)
        if text:
            emotion = predict_audio_emotion(temp_audio_path)
        else:
            emotion = "Neutral"

        # 임시 파일 삭제
        try:
            os.remove(temp_audio_path)
        except Exception as e:
            print(f"[WARNING] 임시 파일 삭제 실패: {str(e)}")

        return text, emotion

    except Exception as e:
        print(f"[ERROR] 전체 처리 중 오류 발생: {str(e)}")
        return None, "Neutral"

# Streamlit 앱 메인 함수
def main():
    st.title("음성 감정 분석 및 텍스트 변환")

    # 오디오 녹음 위젯 표시
    audio_bytes = audio_recorder(
        pause_threshold=3.0,
        sample_rate=16000,
        text="음성을 녹음하려면 클릭하세요",
        icon_size="4x"
    )

    if audio_bytes:
        # 녹음된 오디오 재생
        st.audio(audio_bytes, format='audio/wav')

        # 녹음된 오디오 처리
        text, emotion = process_recorded_audio(audio_bytes)

        # 결과 출력
        if text:
            st.subheader("변환된 텍스트:")
            st.write(text)
        else:
            st.write("음성 인식에 실패했습니다.")

        st.subheader("예측된 감정:")
        st.write(emotion)

if __name__ == "__main__":
    main()
