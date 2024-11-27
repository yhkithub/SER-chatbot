from transformers import pipeline
import torchaudio
import io

# Whisper 모델 초기화
whisper_model = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

def convert_audio_to_text(audio_bytes):
    """
    Whisper 모델을 사용하여 음성을 텍스트로 변환
    """
    try:
        # 오디오 파일 로드
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))

        # 16kHz로 리샘플링
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # Whisper 모델 입력 형식으로 변환
        audio_data = waveform.squeeze().numpy()

        # Whisper 모델로 텍스트 변환
        result = whisper_model(audio_data)
        text = result.get("text", "").strip()

        if not text:
            print("[DEBUG] Whisper 모델이 텍스트를 반환하지 않았습니다.")
            return None
        return text
    except Exception as e:
        print(f"[ERROR] Whisper STT Error: {e}")
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
