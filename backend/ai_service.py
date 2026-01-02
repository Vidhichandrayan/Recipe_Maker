import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def ask_mistral(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        return f"AI Error: {str(e)}"
