import requests
from config import OLLAMA_HOST


def stream_chat(payload):
    url = f"{OLLAMA_HOST}/api/chat"

    with requests.post(url, json=payload, stream=True, timeout=120) as r:
        r.raise_for_status()

        for chunk in r.iter_content(chunk_size=None):
            if chunk:
                yield chunk


def list_models():
    url = f"{OLLAMA_HOST}/api/tags"
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.json()