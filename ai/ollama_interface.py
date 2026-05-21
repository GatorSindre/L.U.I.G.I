import ollama
import requests
from ai import memory
import json

from config import settings


###     Ollama Oppstart og response systemm

url = "http://localhost:11434/api/chat"

MODEL = settings.ollama_model

## TODO Check here that ollama model exists
if True:
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

    response.raise_for_status()

    # Wait for response and continusly print answer
    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode("utf-8"))
        except json.JSONDecodeError:
            continue

        if "error" in data:
            print("[OLLAMA ERROR]", data["error"])
            return ""

        msg = data.get("message", {})
        token = msg.get("content", "")

        if token:
            full_response += token

        if data.get("done"):
            break

    full_response = full_response.strip()

    if not full_response:
        print("[OLLAMA] Empty response received")
        return ""

    # Add user message to memory
    memory.short_term_add({"role": "user", "content": input_text})

    # add assistant reply to memory
    memory.short_term_add({"role": "assistant", "content": full_response})

    print("\n")

    return full_response


def test():
    test_prompt = "Say 'Ollama is working' and nothing else."

    response = requests.post(
        url,
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": test_prompt
                }
            ],
            "stream": True
        },
        stream=True
    )

    full_response = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))

            if "message" in data and "content" in data["message"]:
                full_response += data["message"]["content"]

            if data.get("done"):
                break

    return full_response