from transformers import pipeline
import torchaudio
import os

# Whisper 모델 로드
whisper_model = pipeline(task="automatic-speech-recognition", model="openai/whisper-small")

def convert_audio_to_text(audio_data, language='ko'):
    """
    Whisper 모델을 사용해 음성을 텍스트로 변환
    """
    try:
        # 오디오 데이터를 메모리에서 읽어서 Torchaudio로 변환
        waveform, sample_rate = torchaudio.load(io.BytesIO(audio_data))
        print(f"[DEBUG] Audio Info: Shape={waveform.shape}, Sample Rate={sample_rate}")

        # 16kHz로 변환
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)

        # Whisper에 입력 가능한 형식으로 변환
        audio_data = waveform.squeeze().numpy()
        result = whisper_model(audio_data, language=language)
        return result['text']
    except Exception as e:
        print(f"[ERROR] Whisper STT Error: {e}")
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
