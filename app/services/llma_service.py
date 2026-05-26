import gc
import os

import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_CHAT_URL = os.getenv("OLLAMA_CHAT_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")


def perguntar_llama(prompt: str):

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "keep_alive": 0,
        "options": {
            "num_ctx": 1024,
            "temperature": 0.2,
            "num_predict": 200
        }
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        return f"Nao foi possivel consultar o modelo agora: {exc}"
    finally:
        try:
            requests.post(
                OLLAMA_CHAT_URL,
                json={
                    "model": MODEL,
                    "messages": [],
                    "keep_alive": 0
                },
                timeout=10
            )
        except requests.RequestException:
            pass

        gc.collect()

    resposta = data.get("response")

    if resposta:
        return resposta

    erro = data.get("error", "Resposta inesperada do Ollama")
    return f"Nao foi possivel gerar a resposta: {erro}"