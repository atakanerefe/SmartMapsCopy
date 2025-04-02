"""
This module defines the Flask routes for handling text generation requests via the Gemini API.

Routes:
- `/generate` (POST): Accepts user input and returns 
AI-generated text using `make_gemini_request()`.
"""

from flask import Blueprint, request, jsonify
from website.gemini_api import make_gemini_request

routes_blueprint = Blueprint("routes", __name__)

@routes_blueprint.route('/generate', methods=['POST'])
def generate():
    """
    Handles POST requests to generate text using the Gemini API.

    This endpoint receives a JSON request containing an input prompt.
    It calls `make_gemini_request` to generate a response.

    Returns:
        JSON response with the generated text or an error message.
    """
    data = request.get_json()
    prompt = data.get("input", "")

    if not prompt:
        return jsonify({"error": "No input provided"}), 400

    response = make_gemini_request(prompt)
    return jsonify({"response": response})