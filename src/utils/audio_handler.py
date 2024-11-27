from transformers import pipeline
import torchaudio
import io

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
