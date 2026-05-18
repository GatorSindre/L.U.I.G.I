import regex as re
from audio import recorder
from audio import whisper_stt
import time

from ai import ollama_interface
from audio import piper_tts

from config import settings

def clean_tts_text(text: str) -> str:           ##TODO Add manual filtering where it runs through text and if L.U.I.G.I is written transform it to Luigi.
    text = re.sub(r"\p{Emoji_Presentation}", "", text)
    text = re.sub(r"\p{Extended_Pictographic}", "", text)

    return text

def luigi_activate():
    ## Audio To Text
    input_text = whisper_stt.run()
    ## Talk to AI
    print(f"[USER INPUT]: {input_text}")
    ai_response = ollama_interface.New_AI_Message(input_text)
    print(f"[AI OUTPUT] {ai_response}")

    # Filtrer response for dårlige ting til tts som emojier for eksempel
    filtered_response = clean_tts_text(ai_response)
    
    piper_tts.play(filtered_response)
