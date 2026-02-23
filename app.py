"""
Flask app that proxies requests to local Ollama and serves the chat UI.
Run with: python app.py
Then open http://localhost:5000
"""
import os
import requests
from flask import Flask, request, Response, send_from_directory

app = Flask(__name__, static_folder="static")
OLLAMA_BASE = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = "iKhalid/ALLaM:7b"


def stream_response(url: str, json: dict):
    """Stream a response from Ollama to the client."""
    import json as _json
    try:
        with requests.post(url, json=json, stream=True, timeout=120) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=None):
                if chunk:
                    yield chunk
    except requests.exceptions.ConnectionError:
        yield (_json.dumps({"error": "Cannot connect to Ollama. Is it running on " + OLLAMA_BASE + "?"}) + "\n").encode()
    except requests.exceptions.Timeout:
        yield (_json.dumps({"error": "Ollama took too long to respond."}) + "\n").encode()
    except requests.exceptions.HTTPError as e:
        body = e.response.text if e.response is not None else str(e)
        yield (_json.dumps({"error": body or "Ollama error"}) + "\n").encode()


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Proxy POST /api/chat to Ollama with optional streaming."""
    import json as _json
    url = f"{OLLAMA_BASE}/api/chat"
    data = request.get_json() or {}
    data.setdefault("model", DEFAULT_MODEL)
    # Ensure system prompt is in messages if provided at top level (Ollama chat uses messages[].role=system)
    system = data.pop("system", None)
    if system and isinstance(data.get("messages"), list):
        messages = data["messages"]
        if not messages or messages[0].get("role") != "system":
            data["messages"] = [{"role": "system", "content": system}] + list(messages or [])
    if data.get("stream", True):
        return Response(
            stream_response(url, data),
            mimetype="application/x-ndjson",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )
    try:
        r = requests.post(url, json=data, timeout=120)
        r.raise_for_status()
        return Response(r.content, mimetype="application/json")
    except requests.exceptions.ConnectionError:
        return Response(
            _json.dumps({"error": "Cannot connect to Ollama. Is it running on " + OLLAMA_BASE + "?"}),
            status=503,
            mimetype="application/json",
        )
    except requests.exceptions.Timeout:
        return Response(
            _json.dumps({"error": "Ollama took too long to respond."}),
            status=504,
            mimetype="application/json",
        )
    except requests.exceptions.HTTPError as e:
        try:
            err_body = e.response.text
        except Exception:
            err_body = str(e)
        return Response(
            _json.dumps({"error": err_body or f"Ollama error: {e.response.status_code}"}),
            status=e.response.status_code if e.response is not None else 502,
            mimetype="application/json",
        )


@app.route("/api/tags", methods=["GET"])
def tags():
    """Proxy GET /api/tags to list available models."""
    import json as _json
    try:
        r = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=10)
        r.raise_for_status()
        return Response(r.content, mimetype="application/json")
    except requests.exceptions.ConnectionError:
        return Response(
            _json.dumps({"error": "Cannot connect to Ollama. Is it running?"}),
            status=503,
            mimetype="application/json",
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
