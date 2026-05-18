class Settings:
    def __init__(self):
        self.language_mode = "en"
        self.whisper_model = "medium"
        self.memory_limit = 10 # How many messages to remember
        self.silence_threshold = 500
        self.checkup_interval = 60  # In Seconds
        self.show_mic_volume = True
        self.vosk_on = True
        self.user_speaking = False
        self.recording_ready = False
        self.ollama_model = "llama3.2:3b"
        self.vosk_silence_wait = 1 # In Seconds
settings = Settings()

## CURRENT GOAL
# Working in testing_env to make openwakeword work

## TODO Legg til slik at alt av ai som whisper, piper og ollama kjører en gang slikt at det går raskere neste gang.


## TODO ADD THRESHOLD CALIBRATION   DESKTOP-HYBEL 20, LAPTOP 100
## Have checkup listen to noise and set threshold accordingly

#TODO
#FORTSETTE Å LAGE FLERE PY FILER FOR STRUKTUR -Neste er ollama.py i ai/

#TODO
## Målet er egentlig at wakeword skal starte første sequence og 
# imens skal også vosk starte i bakgrunnen, den skal brukes for å se om brukeren 
# fortsatt snakker eller begynner å snakke istedet for silence, også for å avbryte AI-en

## Veldig viktig å optimalizere AI sequence's raskhet og mulighet til å avbryte når som helst
# Egentlig burde for eksempel vosk deteksjon av ord med en gang skru på recording, mens 
# resten av funksjoner fullfører og avbryter.

# La vosk kjøre i bakgrunnen i kanskje 15 sekunder for å se om brukeren fortsetter å snakke
# Hvis den merker at brukeren gjør det

#TODO
## Make whisper run with my gpu and not cpu


""" # USE This to check for event as a variable instead of waiting for x seconds
if wake_event.is_set():
        wake_event.clear()
        print("Running assistant")
        luigi_activate()
"""



## TODO
# Add en funksjon slik at AI-en kan bli spurt om å huske noe. Deretter generer den mange kanskje sånn 20 keywords 
# om den tingen og legger det i minnet sånn at senere automatisk hver gang jeg spør om noe vil mitt program mate ai-en med
# De viktigste minnene ettersom hva jeg spurte om var via søking av keyword.

## TODO
# Make the recording audio in memory and only save to a file when the ai is ready to process.


## TODO
# Add en funksjon til å bare kjenne igjen min stemme