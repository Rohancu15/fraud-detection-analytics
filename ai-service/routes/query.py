from flask import Blueprint, request, jsonify
from services.groq_client import GroqClient
from services.chroma_client import ChromaClient
from services.cache_client import CacheClient
from services.shared import groq_client as groq
from services.shared import cache_client as cache
from services.shared import chroma_client as chroma
import hashlib
import json

query_bp = Blueprint("query", __name__)




def load_prompt():
    with open("prompts/query_prompt.txt", "r") as f:
        return f.read()


# ✅ Generate SHA256 cache key
def generate_cache_key(question):
    return hashlib.sha256(question.encode()).hexdigest()


@query_bp.route("/query", methods=["POST"])
def query():
    try:
        data = request.get_json()

        if not data or "question" not in data:
            return jsonify({"error": "Missing 'question'"}), 400

        question = data["question"]

        # 🔥 Step 1: Check cache
        key = generate_cache_key(question)
        cached = cache.get(key)

        if cached:
            return jsonify(json.loads(cached))

        # 🔥 Step 2: Normal pipeline
        docs = chroma.query(question)
        sources = docs[0] if docs else []

        context = "\n".join([f"- {doc}" for doc in sources])

        prompt_template = load_prompt()

        prompt = prompt_template.format(
            context=context,
            question=question
        )

        answer = groq.generate(prompt)

        response = {
            "answer": answer,
            "sources": sources,
            "confidence": round(len(sources) / 3, 2)
        }

        # 🔥 Step 3: Store in cache (15 min TTL handled in client)
        cache.set(key, json.dumps(response))

        return jsonify(response)

    except Exception:
        return jsonify({"error": "Internal server error"}), 500