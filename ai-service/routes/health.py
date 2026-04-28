from flask import Blueprint, jsonify
import time

from services.groq_client import GroqClient
from services.chroma_client import ChromaClient
from services.metrics import start_time  # ✅ FIXED

health_bp = Blueprint("health", __name__)

groq = GroqClient()
chroma = ChromaClient()


@health_bp.route("/health", methods=["GET"])
def health():
    uptime = int(time.time() - start_time)

    return jsonify({
        "status": "healthy",
        "model": "llama-3.3-70b-versatile",
        "avg_response_time_ms": round(groq.get_avg_response_time(), 2),
        "chroma_doc_count": chroma.collection.count(),
        "uptime_seconds": uptime
    })