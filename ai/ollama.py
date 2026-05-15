import ollama
import requests
from ai import memory
import json


###     Ollama Oppstart og response systemm

url = "http://localhost:11434/api/chat"

#   Finding Ollama Model
PREFERRED_MODELS = [
    "qwen3:8b",
    "llama3.2:3b",
]

def get_best_model():
    try:
        installed = [m.model for m in ollama.list().models]
    except Exception as e:
        print(f"[OLLAMA ERROR] Could not connect to Ollama API: {e}")
        print("[OLLAMA ERROR] Make sure Ollama is running")
        exit()

    for model in PREFERRED_MODELS:
        if model in installed:
            return model

    return None

MODEL = get_best_model()

if MODEL:
    print(f"[OLLAMA] Using {MODEL}")
else:
    print("[OLLAMA] No compatible model installed")

def build_prompt(user_input):
    messages = [memory.system_prompt] + memory.short_term + [
        {"role": "user", "content": user_input}
    ]

    return {
        "model": MODEL,
        "messages": messages,
        "stream": True
    }

def New_AI_Message(input_text):

    full_response = ""

    # Prepare payload to ollama
    payload = build_prompt(input_text)

    # Make the request
    response = requests.post(url, json=payload, stream=True)

    # Wait for response and continusly print answer
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))

            if "message" in data and "content" in data["message"]:
                token = data["message"]["content"]
                # print(token, end="", flush=True)
                full_response += token

            if data.get("done"):
                break

    # Add user message to memory
    memory.short_term_add({"role": "user", "content": input_text})

    # add assistant reply to memory
    memory.short_term_add({"role": "assistant", "content": full_response})

    print("\n")

    return full_response
