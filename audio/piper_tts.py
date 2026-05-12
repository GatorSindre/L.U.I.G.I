import subprocess
from scipy.io.wavfile import read
import sounddevice as sd
from config import settings 

piper_exe = r"piper\piper.exe"

if (settings.language_mode == "no"):
    model = r"piper\models\no_NO-talesyntese-medium.onnx"
elif (settings.language_mode == "en"):
    model = r"piper\models\en_US-ryan-high.onnx"
else:
    print(f"Language mode ( {settings.language_mode} ) is not valid -- Exiting script to avoid errors")
    exit()

output_file = r"TTS\output.wav"

def tts_generate(input_text):
    command = [
        piper_exe,
        "-m", model,
        "-f", output_file
    ]

    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        text=True
    )  

    process.communicate(input_text)

def play(text):

    print("Generating TTS")
    tts_generate(text)

    print("Loading TTS File")
    samplerate, data = read(output_file)

    print("Playing TTS")
    sd.play(data, samplerate)

    print("Waiting for TTS to finish playing")
    sd.wait()

    print("TTS finished")

print("Started TTS Engine")
