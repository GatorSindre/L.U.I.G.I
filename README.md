UNDER CONSTRUCTION

J.A.R.V.I.S version called L.U.I.G.I

<----------> Extra Requirements
Python -- 3.12.10
OLLAMA -- Check config model
vosk-models -- (on track to be removed)
    Make a folder called vosk-models and add this file AFTER UNZIPPING into the folder https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
Piper -- Download this file and extract the zip into this directory
    https://github.com/rhasspy/piper/releases
    Download the two onyx files and create and put them in these folders piper/models
    https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/kusal/medium
FFMPEG -- Install and add to path

Functions:
- Trigger a chat if you call its name
- Continously check up on what your doing on your computer and see if it is a good time to say something
    Lets say your tired it might notice that on the webcam and tell you its a good time to take a break
- Have its own face and while talking being capable of tracking where your eyes are and your emotions to look at you through the screen
- Check stuff on your pc and do stuff too
- Have a AI decicion and Windows Functions loop so it can do stuff on your pc or check something
    Functions might include, use tesseract to try and understand what app your in or check what music your listening too and ask you about it.
- I want to include an emotional mode where it seems a bit real and imitate human feelings


def generate(input_text):
    voice.synthesize(
        input_text,
        output_file
    )



def generate(input_text):
    with wave.open(output_file, "wb") as wav_file:
        voice.synthesize(input_text, wav_file)