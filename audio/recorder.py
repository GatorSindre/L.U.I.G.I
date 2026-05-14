import os
import time
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from config import settings

def start(
    filename="recording.wav",
    samplerate=16000,
    threshold=settings.silence_threshold,
    silence_duration=1.0,
    min_record_time=3.0,
    chunk_size=1024
):
    ## Check the file exists
    os.makedirs("temp", exist_ok=True)

    # Full file path
    filepath = os.path.join("temp", filename)

    print("Listening...")

    recording = []
    silent_chunks = 0

    start_time = time.time()

    with sd.InputStream(
        samplerate=samplerate,
        channels=1,
        dtype='int16'
    ) as stream:

        while True:
            audio_chunk, overflowed = stream.read(chunk_size)

            recording.append(audio_chunk)

            volume = np.abs(audio_chunk).mean()

            if volume < threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            silence_time = (silent_chunks * chunk_size) / samplerate

            if min_record_time > time.time() - start_time:
                continue

            if silence_time > silence_duration:
                print("Silence detected, stopping.")
                break

    audio = np.concatenate(recording)

    write(filepath, samplerate, audio)

    print(f"Saved {filepath}")

    return
