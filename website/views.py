"""
This module defines the Flask routes for the AI Recipe Generator.

It includes:
- Rendering the homepage (`/`).
- Handling API requests for recipe generation (`/get_recipes`).
"""

from flask import Blueprint, request, jsonify, render_template
from website.gemini_api import make_gemini_request  # Use the new function

views_blueprint = Blueprint("views", __name__)

@views_blueprint.route('/', methods=['GET'])
def main_page():
    """
    Renders the homepage.
    """
    return render_template('index.html')

@views_blueprint.route('/get_recipes', methods=['POST'])
def get_recipes():
    """
    Handles recipe generation requests via the Gemini API.

    This endpoint accepts a JSON request containing a list of ingredients.
    It calls the `make_gemini_request` function to generate a short recipe.

    Returns:
        JSON response with the generated recipe or an error message.
    """
    data = request.get_json()
    if 'ingredients' not in data or not isinstance(data['ingredients'], list):
        return jsonify({"error": "Invalid input. Expected a list of ingredients."}), 400

    recipes = make_gemini_request(f"I have these ingredients: {', '.join(data['ingredients'])}. "
                                  "What recipes can I make?")

    return jsonify({"recipes": recipes})
