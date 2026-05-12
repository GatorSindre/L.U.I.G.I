# WHISPER AUDIO TO TEXT

import whisper
from config import settings 

whisper_model = "medium"
created_whisper_model = whisper.load_model(whisper_model)

print(f"Loaded Whisper Model: {whisper_model}")

def whisper():
    result = created_whisper_model.transcribe(r"AUDIO\recording.wav", language=settings.language_mode)

    print("-- Transcribed audio")

    text = result["text"]

    print(text)
    print("")

    return text