import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def perguntar_llama(prompt: str):

    body = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=body
    )

    data = response.json()

    return data["response"]