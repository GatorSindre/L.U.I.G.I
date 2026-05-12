import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer
import numpy as np
from scipy.io.wavfile import write
import ollama
import threading
import requests
import sys
import regex as re
import traceback

print("Imports Loaded")

## .py Imports
from audio import whisper_stt
print("whisper_stt loaded")
from audio import piper_tts
print("piper_tts loaded")
from audio import recorder
print("recorder loaded")

## Make sure console can handle emojis and such from L.U.I.G.I's responses
sys.stdout.reconfigure(encoding='utf-8')


###     RECORD UNTIL SILENCE


###     Function to clear out characters for tts

def clean_tts_text(text: str) -> str:
    text = re.sub(r"\p{Emoji_Presentation}", "", text)
    text = re.sub(r"\p{Extended_Pictographic}", "", text)

    return text

###     AI memory system

system_prompt = {
    "role": "system",
    "content": """
You are L.U.I.G.I, a local voice assistant running on the user's computer.

Your responses will be spoken aloud using a text-to-speech engine.

Rules:
- Respond naturally and conversationally.
- Keep responses concise unless the user asks for detail.
- Avoid emojis, markdown, bullet points, symbols, visual formatting, internet-style expressions like "lol", "lmao", emojis, kaomojis, or excessive punctuation.
- Use clean spoken language that sounds natural when read aloud.
- Follow the user's intent carefully.
- Do not add conversational closers such as "Let me know if you need anything else", "Feel free to ask", or similar ending phrases. End responses immediately after the main answer is complete.

Examples of good responses:

User: Remember the word concrete.
Assistant: I've remembered the word "concrete".

User: What time is it?
Assistant: It's 5:30 PM.

User: Explain concrete.
Assistant: Concrete is a strong building material made from cement, sand, gravel, and water.

User: Thank you.
Assistant: You're welcome.

"""
}

MAX_MEMORY = 10

short_term_memory = []

## Example of short term memory
""" short_term_memory = [
    {"role": "user", "content": "Hey can you answer with one word, what is 2+2"},
    {"role": "assistant", "content": "four"},
    {"role": "user", "content": "Correct. Now what is 8/4"},
    {"role": "assistant", "content":"2"},
    {"role": "user", "content": "Dont overthink it, its just simple math. Now 5+4 in 1 word"},
    {"role": "assistant", "content": "nine"},
    {"role": "user", "content": "Dont stress too much, just think for 2 seconds and say the first thing that comes to mind right now"},
    {"role": "assistant", "content": "nine"},
    {"role": "user", "content": "Smart, i would have said the same thing, could you just answer 'Hello' for me without the strings"},
    {"role": "assistant", "content": "Hello"},
]   """

def short_term_memory_add(new_message):
    short_term_memory.append(new_message)

    # remove oldest messages if too long
    while len(short_term_memory) > MAX_MEMORY:
        short_term_memory.pop(0)



###     Ollama Oppstart og response systemm

url = "http://localhost:11434/api/chat"

def build_prompt(user_input):
    messages = [system_prompt] + short_term_memory + [
        {"role": "user", "content": user_input}
    ]

    return {
        "model": "qwen3:8b",
        "messages": messages,
        "stream": True
    }

def New_AI_Message(input_text):

    full_response = ""

    # Prepare payload to ollama
    payload = build_prompt(input_text)

    # Make the request
    response = requests.post(url, json=payload, stream=True)

    # Wait for response and continusly print answer
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))

            if "message" in data and "content" in data["message"]:
                token = data["message"]["content"]
                print(token, end="", flush=True)
                full_response += token

            if data.get("done"):
                break

    # Add user message to memory
    short_term_memory_add({"role": "user", "content": input_text})

    # add assistant reply to memory
    short_term_memory_add({"role": "assistant", "content": full_response})

    print("\n")

    return full_response

###     Create system to run checkup every __ seconds

checkup_interval = 60 # In Seconds

def checkup():
    ## Find out what user is doing TODO
    ## Evaluate if its necessary to do something
    # Her skal sjekking fungere og spørring om jeg har husket diverse ting og slik
    True

###     Main AI Processering

def luigi_activate():
    ## Record
    recorder.start()
    ## Audio To Text
    input_text = whisper_stt.run()
    ## Talk to AI
    print(f"Startet ai sequence med tekst: {input_text}")
    ai_response = New_AI_Message(input_text)

    # Filtrer response for dårlige ting til tts som emojier for eksempel
    filtered_response = clean_tts_text(ai_response)
    
    piper_tts.play(filtered_response)


###     WAKEUP WORD LOW RAM AI THREAD

wake_event = threading.Event()

def wake_listener():
    q = queue.Queue()

    vosk_model = Model(r"vosk-models\vosk-model-small-en-us-0.15")

    print("Vosk model loaded")

    recognizer = KaldiRecognizer(vosk_model, 16000)

    def callback(indata, frames, time, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        print("Listening for wake word...")

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):

                try:
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                except Exception as e:
                    print(f"Wake JSON error: {e}")

                if text:
                    if "luigi" in text:
                        print("- Wake Up Word")
                        sd.stop()
                        wake_event.set()

## MAIN LOOP
def main():
    # start wake word thread
    threading.Thread(target=wake_listener, daemon=True).start()

    print("Main AI system running...")

    while True:

        # wait __ seconds or trigger wake event
        triggered = wake_event.wait(timeout=checkup_interval)

        if triggered:
            wake_event.clear()
            print("Running assistant")
            luigi_activate()

        else:
            print("Checkup triggered")
            checkup()

# 1. Wake word i egen thread som endrer en variabel
# 2. Loop som sjekker etter checkup og om wake word variabel er aktivert som da starter AI loop
# 3. Streaming av ollama for å kunne abryte

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
    finally:
        print("exiting...")