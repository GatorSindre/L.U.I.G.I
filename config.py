class Settings:
    def __init__(self):
        self.language_mode = "en"
        self.whisper_model = "medium"
        self.memory_limit = 10
        self.silence_threshold= 500
        self.checkup_interval = 60  # In Seconds
        self.show_mic_volume = True
settings = Settings()

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