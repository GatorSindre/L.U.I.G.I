import os
from scipy.io.wavfile import write
import threading
import sys
import traceback

## Threads
wake_event = threading.Event()

#TODO Remove keyboard after usage (from requirements too)
import keyboard

## .py Imports
from config import settings
print("[IMPORTING] config loaded")
from audio import whisper_stt
print("[IMPORTING] whisper_stt loaded")
from audio import piper_tts
print("[IMPORTING] piper_tts loaded")
from audio import recorder
print("[IMPORTING] recorder loaded")
from threads import vosk
print("[IMPORTING] vosk loaded")
from ai import memory
print("[IMPORTING] memory loaded")
from ai import brain
print("[IMPORTING] brain loaded")

## Make sure console can handle emojis and such from L.U.I.G.I's responses
sys.stdout.reconfigure(encoding='utf-8')

###     CLEANUP used after closing script

def clear_temp():
    temp_folder = "temp"

    # Make sure folder exists
    if not os.path.exists(temp_folder):
        return

    # Remove all files
    for file in os.listdir(temp_folder):
        file_path = os.path.join(temp_folder, file)

        if os.path.isfile(file_path):
            os.remove(file_path)

    print("Temp folder cleared.")

###     Create system to run checkup every __ seconds

checkup_interval = settings.checkup_interval

def checkup():
    ## Find out what user is doing TODO
    ## Evaluate if its necessary to do something
    # Her skal sjekking fungere og spørring om jeg har husket diverse ting og slik
    True

## MAIN LOOP
def main():
    # start wake word thread
    threading.Thread(
    target=vosk.wake_listener,args=(wake_event,),daemon=True).start()

    while True:

        # wait __ seconds or trigger wake event
        triggered = wake_event.wait(timeout=checkup_interval)

        if triggered:
            wake_event.clear()
            print("Running assistant")
            brain.luigi_activate()
        else:
            print("Checkup triggered")
            checkup()

# 1. Wake word i egen thread som endrer en variabel
# 2. Loop som sjekker etter checkup og om wake word variabel er aktivert som da starter AI loop
# 3. Streaming av ollama for å kunne abryte

def on_key_press(event):
    wake_event.set()
keyboard.on_press_key("space", on_key_press)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
    finally:
        clear_temp()
        print("exiting...")