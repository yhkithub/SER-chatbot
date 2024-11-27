import io
from transformers import pipeline
import torchaudio

whisper_model = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

def process_audio_with_whisper(audio_bytes):
    """Process audio bytes with Whisper model."""
    try:
        # 파일 메모리에서 로드
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
        print(f"[DEBUG] Waveform Shape: {waveform.shape}, Sample Rate: {sample_rate}")

        # 샘플링 레이트 16kHz로 변경
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # Whisper 모델 입력 처리
        result = whisper_model(waveform.squeeze().numpy())
        return result['text']
    except Exception as e:
        print(f"[ERROR] Whisper Error: {e}")
        return None

def process_audio_input(audio_bytes, language_options=('ko', 'en')):
    """
    Whisper를 사용하여 오디오 데이터를 텍스트로 변환
    """
    for language in language_options:
        try:
            text = convert_audio_to_text(audio_bytes, language=language)
            if text:
                return text, language
        except Exception as e:
            print(f"[ERROR] Error processing audio for language '{language}': {e}")
            continue
    return None, None
