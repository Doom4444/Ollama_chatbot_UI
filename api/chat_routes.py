import json
from flask import Blueprint, request, Response
from services.llm_service import stream_chat, list_models
from config import DEFAULT_MODEL

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}

    data.setdefault("model", DEFAULT_MODEL)

    if data.get("stream", True):
        return Response(
            stream_chat(data),
            mimetype="application/x-ndjson",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    return Response(stream_chat(data), mimetype="application/json")


@chat_bp.route("/api/tags", methods=["GET"])
def tags():
    try:
        data = list_models()
        return data
    except Exception as e:
        return {"error": str(e)}, 500