from flask import Blueprint, request, jsonify
import json
import re
import time
import hashlib

from services.shared import groq_client as client
from services.shared import cache_client as cache  # ✅ ADD THIS

categorise_bp = Blueprint("categorise", __name__)


def load_prompt():
    with open("prompts/categorise_prompt.txt", "r") as file:
        return file.read()


# ✅ Cache key generator
def generate_cache_key(text):
    return hashlib.sha256(text.encode()).hexdigest()


@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        input_text = data["text"]

        # 🔥 Step 1: Check cache
        key = generate_cache_key(input_text)
        cached = cache.get(key)

        if cached:
            return jsonify(json.loads(cached))

        # 🔥 Step 2: Generate prompt
        prompt_template = load_prompt()
        prompt = prompt_template.format(input_text=input_text)

        start = time.time()
        response = client.generate(prompt)
        end = time.time()

        # 🔥 Step 3: Extract JSON
        try:
            json_match = re.search(r'\{[\s\S]*?\}', response)

            if json_match:
                parsed_response = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found")

        except Exception:
            parsed_response = {
                "category": "Other",
                "confidence": 0.0,
                "reasoning": response
            }

        result = {
            "data": parsed_response,
            "meta": {
                "confidence": parsed_response.get("confidence", 0.0),
                "model_used": client.model,
                "tokens_used": len(prompt.split()),
                "response_time_ms": int((end - start) * 1000),
                "cached": False
            }
        }

        # 🔥 Step 4: Store in cache (15 min TTL handled inside client)
        cache.set(key, json.dumps(result))

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500