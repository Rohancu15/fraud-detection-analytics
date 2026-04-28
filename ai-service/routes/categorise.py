from flask import Blueprint, request, jsonify
import json
import re

from services.shared import groq_client as client  # ✅ FIX

categorise_bp = Blueprint("categorise", __name__)


def load_prompt():
    with open("prompts/categorise_prompt.txt", "r") as file:
        return file.read()


@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field"}), 400

        input_text = data["text"]

        prompt_template = load_prompt()
        prompt = prompt_template.format(input_text=input_text)

        response = client.generate(prompt)

        try:
            json_match = re.search(r'\{[\s\S]*?\}', response)

            if json_match:
                json_str = json_match.group()
                parsed_response = json.loads(json_str)
            else:
                raise ValueError("No JSON found")

        except Exception:
            parsed_response = {
                "category": "Unknown",
                "confidence": 0.0,
                "reasoning": response
            }

        return jsonify(parsed_response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500