import speech_recognition as sr
from pydub import AudioSegment
import io

def convert_audio_to_text(wav_audio_data, language='ko-KR'):
    """음성 데이터를 텍스트로 변환하는 함수"""
    try:
        # AudioSegment로 변환
        audio = AudioSegment.from_file(io.BytesIO(wav_audio_data), format="wav")

        # 파일 정보 디버깅
        print(f"[DEBUG] Audio Info: Channels={audio.channels}, Frame Rate={audio.frame_rate}, Duration={len(audio)}ms")

        # 16kHz, 단일 채널로 변환
        audio = audio.set_frame_rate(16000).set_channels(1)

        # 짧은 오디오 패딩 추가
        if len(audio) < 1000:  # 1초 미만
            silence = AudioSegment.silent(duration=1000 - len(audio))
            audio = audio + silence

        # 변환된 오디오를 Google API가 처리할 수 있는 WAV 형식으로 저장
        audio_file = io.BytesIO()
        audio.export(audio_file, format="wav")
        audio_file.seek(0)

        # Google Speech Recognition API 호출
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
        return text
    except sr.UnknownValueError:
        print("[DEBUG] Google Speech Recognition could not understand audio.")
        return None
    except Exception as e:
        print(f"[ERROR] Error in speech recognition: {e}")
        return None

def process_audio_input(wav_audio_data, language_options=('ko-KR', 'en-US')):
    """음성 입력을 처리하고 텍스트를 반환"""
    if wav_audio_data is not None:
        for language in language_options:
            try:
                # 언어별로 STT 시도
                audio_text = convert_audio_to_text(wav_audio_data, language=language)
                if audio_text:
                    print(f"[DEBUG] Detected Language: {language}, Text: {audio_text}")
                    return audio_text, language
            except Exception as e:
                print(f"[ERROR] Error processing language {language}: {e}")
                continue  # 다음 언어로 시도

        # 실패 시 None 반환
        return None, None
