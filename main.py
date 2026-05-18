import os
from scipy.io.wavfile import write
import threading
import sys
import traceback
import time

## FROM AUDIO
from audio import whisper_stt
print("[IMPORTING] whisper_stt loaded")
from audio import piper_tts
print("[IMPORTING] piper_tts loaded")
from audio import recorder
print("[IMPORTING] recorder loaded")

## FROM AI
from ai import memory
print("[IMPORTING] memory loaded")
from ai import ollama_interface
print("[IMPORTING] ollama loaded")
from ai import brain
print("[IMPORTING] brain loaded")

## FROM THREADS
from threads import vosk
print("[IMPORTING] vosk loaded")

## FROM MISCELLANEOUS
from config import settings
print("[IMPORTING] config loaded")


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

    print("[CLEANUP] Temp folder wiped")

###     Create system to run checkup every __ seconds

checkup_interval = settings.checkup_interval

def checkup():
    ## Find out what user is doing TODO
    ## Evaluate if its necessary to do something
    # Her skal sjekking fungere og spørring om jeg har husket diverse ting og slik
    pass

## MAIN LOOP
def main():
    # start speech detection thread
    threading.Thread(
    target=vosk.speak_detection,args=(),daemon=True).start()

    ## Run a Systems Test
    print(f"[SYSTEM TEST - OLLAMA] {ollama_interface.test()}")
    print(f"[SYSTEM TEST - WHISPER] {whisper_stt.test()}")
    piper_tts.test()
    print(f"[SYSTEM TEST - PIPER] Done")

    ## Keybind loop to activate AI
    import keyboard
    while True:
        start_keybind = "d"
        print(f"------------ Enable AI by pressing {start_keybind}")
        keyboard.wait(start_keybind)

        ## ACTIVATION EVENT
        settings.vosk_on = True
        while not settings.recording_ready:
            time.sleep(0.05)
        brain.luigi_activate()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
    finally:
        clear_temp()
        print("exiting...")