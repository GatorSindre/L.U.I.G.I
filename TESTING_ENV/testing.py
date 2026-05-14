from piper import PiperVoice
import keyboard

voice = PiperVoice.load(
    "../piper/models/en_US-kusal-medium.onnx"
)

def speak(text):
    with open("output.wav", "wb") as f:
        voice.synthesize(text, f)

activation_keybind = "space"
print(f"Model loaded, ready to speak after ({activation_keybind}) is pressed.")
keyboard.wait(activation_keybind)
speak("Hello, I am ready to speak.")