###     WAKEUP WORD LOW RAM AI THREAD
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
                        if time.time() - last_trigger > 2:
                            wake_event.set()
                            last_trigger = time.time()
