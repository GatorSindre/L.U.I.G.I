import subprocess
from scipy.io.wavfile import read
import sounddevice as sd
from config import settings 
import os
from piper import PiperVoice
import wave
import io
import numpy as np

## Check folder exists
os.makedirs("temp", exist_ok=True)

piper_exe = r"piper/piper.exe"

if (settings.language_mode == "no"):
    model = r"piper\models\no_NO-talesyntese-medium.onnx"
elif (settings.language_mode == "en"):
    model = r"piper\models\en_US-kusal-medium.onnx"
else:
    print(f"Language mode ( {settings.language_mode} ) is not valid -- Exiting script to avoid errors")
    exit()

if not os.path.exists(model):
    print(f"[ERROR] Piper Model file not found: {model}")

output_file = r"temp/output.wav"

voice = PiperVoice.load(model)

def generate(input_text): ## Uses old piper.exe via subprocess
    command = [
        piper_exe,
        "--model", model,
        "--output_file", output_file
    ]

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        text=True
    ) 

    process.communicate(input_text)

    if process.returncode != 0:
        raise RuntimeError(f"Piper exited with code {process.returncode}")

def play(input_text):

    print("Generating TTS")
    try:
        generate(input_text)
    except Exception as e:
        print(f"[PIPER TTS ERROR] TTS generation failed: {e}")
        return

    print("Loading TTS File")
    try:
        samplerate, data = read(output_file)
    except Exception as e:
        print(f"[PIPER TTS ERROR] Could not read TTS output file: {e}")
        return
    
    print("Playing TTS")
    sd.play(data, samplerate)

    print("Waiting for TTS to finish playing")
    sd.wait()

    print("TTS finished")

def test():
    sample_file = r"sample_test/output.wav"
    
    command = [
        piper_exe,
        "--model", model,
        "--output_file", sample_file
    ]

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        text=True
    ) 

    process.communicate("Tesing piper.")

    if process.returncode != 0:
        raise RuntimeError(f"Piper exited with code {process.returncode}")
