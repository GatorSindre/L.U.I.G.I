# WHISPER AUDIO TO TEXT

import whisper
from config import settings 

whisper_model = "medium"
created_whisper_model = whisper.load_model(whisper_model)

def run():
    result = created_whisper_model.transcribe(r"temp/recording.wav", language=settings.language_mode)

    text = result["text"]

    return text

def test(): 
    ## FORCES ENGLISH BECAUSE OF SAMPLED TEST 
    #TODO Make two sample files and let it switch between depending on language mode
    result = created_whisper_model.transcribe(r"sample_test/test_recording.wav", language="en")

    text = result["text"]

    return text