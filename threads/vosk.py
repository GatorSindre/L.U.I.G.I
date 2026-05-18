###     WAKEUP WORD LOW RAM AI THREAD
import json
import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import time

from audio import recorder
from config import settings

def speak_detection():
    global last_trigger
    
    q = queue.Queue()

    vosk_model = Model(r"vosk-models\vosk-model-small-en-us-0.15")

    print("[VOSK] Model loaded")

    recognizer = KaldiRecognizer(vosk_model, 16000)

    last_partial = ""

    def callback(indata, frames, time_value, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=1024,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        while True:
            while not settings.vosk_on:
                time.sleep(0.5)

            print("[VOSK] ENABLED")

            last_sound = False ## MAKE SURE THIS VARIABLE IS ONLY EVER FALSE OR time.time() value

            while settings.vosk_on:
                data = q.get(timeout=0.5)

                if last_sound != False and (time.time() - last_sound > 2):
                    print("------  FINISHED SPEAKING")
                    last_sound = False
                    settings.user_speaking = False
                    recorder.stop()

                    # Give a little minimun buffer for the recording to save so we dont start another recording instantly
                    time.sleep(0.4)

                # SENTENCE
                if recognizer.AcceptWaveform(data):
                    try:
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").strip()

                        if text:
                            # print(f"[VOSK] SENTENCE: {text}")
                            last_sound = time.time()
                    except Exception as e:
                        print(f"Wake JSON error: {e}")

                # WORD
                else:
                    partial = json.loads(recognizer.PartialResult())

                    text = partial.get("partial", "").strip()
                    
                    # print(f"[VOSK]: WORD: {text}")

                    if text and settings.user_speaking == False:
                        print("---------------  SPEAKING")
                        settings.user_speaking = True
                        recorder.start()

                    if text and last_sound != False:
                        last_sound = time.time()

            # CODE AFTER CLOSING VOSK