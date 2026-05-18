### WAKEUP WORD LOW RAM AI THREAD

import json
import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import time

last_trigger = 0

def wake_listener(wake_event):
    global last_trigger

    q = queue.Queue()

    vosk_model = Model(r"vosk-models\vosk-model-small-en-us-0.15")

    print("[VOSK] Model loaded")

    recognizer = KaldiRecognizer(vosk_model, 16000)

    last_partial = ""

    def callback(indata, frames, time_info, status):
        if status:
            print(status)

        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=1024,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        print("Listening for wake word...")

        while True:
            data = q.get()

            # FINALIZED SENTENCE
            if recognizer.AcceptWaveform(data):

                try:
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()

                    if text:
                        print(f"[FINAL] {text}")

                except Exception as e:
                    print(f"Wake JSON error: {e}")

            # LIVE STREAMING WORDS
            else:

                try:
                    partial = json.loads(recognizer.PartialResult())
                    text = partial.get("partial", "").strip()

                    # Only print if changed
                    if text and text != last_partial:
                        last_partial = text

                        print(f"[PARTIAL] {text}")

                        # Wake word detection
                        if "luigi" in text:
                            if time.time() - last_trigger > 2:

                                print("[WAKE WORD DETECTED]")

                                wake_event.set()
                                last_trigger = time.time()

                except Exception as e:
                    print(f"Partial JSON error: {e}")