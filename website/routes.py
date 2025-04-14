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
    Endpoint to generate a Gemini API response from a user-provided prompt.

    Expects:
        JSON payload with a key `"input"` containing the user's prompt as a string.

    Returns:
        Response: JSON object containing the Gemini API response, or an error message
        if input is missing.
    """
    data = request.get_json()
    prompt = data.get("input", "")

    if not prompt:
        return jsonify({"error": "No input provided"}), 400

    response = make_gemini_request(prompt)
    return jsonify({"response": response})
