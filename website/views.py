from flask import Blueprint, request, jsonify, render_template
from website.gemini_api import make_gemini_request  # Use the AI function

views_blueprint = Blueprint("views", __name__)

@views_blueprint.route('/', methods=['GET'])
def main_page():
    """
    Renders the homepage.
    """
    return render_template('index.html')

@views_blueprint.route('/get_itinerary', methods=['POST'])
def get_itinerary():
    """
    Handles itinerary generation requests via the Gemini API.

    This endpoint accepts a JSON request containing a full paragraph of travel details.
    It calls the `make_gemini_request` function to generate a suggested itinerary.

    Returns:
        JSON response with the generated itinerary or an error message.
    """
    data = request.get_json()
    
    # Ensure the expected JSON structure is present
    if 'travel_details' not in data or not isinstance(data['travel_details'], str):
        return jsonify({"error": "Invalid input. Expected travel details as a text string."}), 400

    # Extract the full travel description
    travel_details = data['travel_details']

    prompt = (f"Here is a description of a trip: {travel_details}. "
              "Based on this information, can you generate a short itinerary with top activities and places to visit?")

    # Call the AI function
    itinerary = make_gemini_request(prompt)

    return jsonify({"itinerary": itinerary})