import sounddevice as sd
from scipy.io.wavfile import write
import os
import numpy as np

from config import settings

stream = None
recording = []

def callback(indata, frames, time, status):
    recording.append(indata.copy())

def start():
    global stream, recording
    recording = []
    
    stream = sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype='int16',
        callback=callback
    )
    stream.start()

def stop(filename="recording.wav"):
    global stream, recording
    stream.stop()
    audio = np.concatenate(recording)
    write(os.path.join("temp", filename), 16000, audio)
    settings.recording_ready = True