"""
This module defines the Flask routes for SmartMaps.

It includes:
- Rendering the homepage (`/`).
- Handling API requests for task breakdown (`/get_itinerary`).
"""

import os
import json
import re
from datetime import datetime

from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_login import current_user, login_required
import requests

from website import db
from website.gemini_api import make_gemini_request
from .models import Event

views_blueprint = Blueprint("views", __name__)

weather_api_key = os.environ.get('WEATHER_KEY')
mapbox_api_key = os.environ.get('MAPBOX_KEY')

admin_emails = ['obraym25@colby.edu']

@views_blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    """
    Renders the homepage.
    """
    return redirect(url_for('views.landing_page'))


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
    if 'name' not in data or not isinstance(data['name'], str):
        return jsonify({"error": "Invalid input. Expected location name as a text string."}), 400
    if 'time' not in data or not isinstance(data['time'], str):
        return jsonify({"error": "Invalid input. Expected time as a text string."}), 400

    name_data = data['name'].split(',')
    city = name_data[0].strip()

    if len(name_data) == 2:
        country = name_data[1].strip()
        state = None
        location = f"{city}, {country}"
    elif len(name_data) == 3:
        state = name_data[1].strip()
        country = name_data[2].strip()
        location = f"{city}, {state}, {country}"
    else:
        return jsonify({
            "error": (
                "Invalid input. Expected location in the format "
                "'city, state, country'."
            )
        }), 400

    date = data['time']

    # Get weather prompt
    weather_info = get_weather_details(city, country, state)

    prompt = (
        f"I am traveling to {location} on {date}. "
        f"Based on this information and {weather_info}, can you generate a one-day itinerary "
        "with top activities and places to visit? "
        "Prioritize activities that are suitable for the weather conditions, prioritizing "
        "outdoor activities with nice weather and indoor ones in bad weather. "
        "Do not include a description of the weather at the beginning of the itinerary. "
        "Start with: Here is an itinerary for your trip:"
    )

    # Call the AI function
    itinerary = make_gemini_request(prompt)

    return {"itinerary": itinerary}


def get_weather_details(city, country, state):
    """
    Generates a human-readable weather description based on the given location.

    Args:
        city (str): The name of the city.
        country (str): The country where the city is located.
        state (str): The state or region (optional depending on the country).

    Returns:
        str: A formatted weather description string for use in itinerary generation.
    """
    weather_data = get_weather(city, country, state)[0]

    # Fallback test data in case real data is unavailable (debug/development use)
    test_weather_data = {
        'coord': {'lon': -74.006, 'lat': 40.7143},
        'weather': [{
            'id': 800,
            'main': 'Clear',
            'description': 'clear sky',
            'icon': '01d'
        }],
        'base': 'stations',
        'main': {
            'temp': 12.2,
            'feels_like': 10.05,
            'temp_min': 12.2,
            'temp_max': 12.2,
            'pressure': 1007,
            'humidity': 22,
            'sea_level': 1007,
            'grnd_level': 1007
        },
        'visibility': 10000,
        'wind': {
            'speed': 13.38,
            'deg': 310,
            'gust': 18.01
        },
        'clouds': {'all': 0},
        'dt': 1742592380,
        'sys': {
            'type': 2,
            'id': 2008776,
            'country': 'US',
            'sunrise': 1742554642,
            'sunset': 1742598528
        },
        'timezone': -14400,
        'id': 5128581,
        'name': 'New York',
        'cod': 200
    }

    if weather_data is None:
        weather_data = test_weather_data

    wind_speed = str(weather_data['wind']['speed'])
    temp = str(weather_data['main']['temp'])
    feels_like = str(weather_data['main']['feels_like'])
    humidity = str(weather_data['main']['humidity'])
    clouds = str(weather_data['clouds']['all'])
    weather_desc = str(weather_data['weather'][0]['description'])

    weather_details = (
        "given the following weather: "
        f"{wind_speed} m/s wind speed, "
        f"{temp}°C temperature, "
        f"{feels_like}°C feels like temperature, "
        f"{humidity}% humidity, "
        f"{clouds}% cloudiness, and the weather is described as {weather_desc}"
    )

    return weather_details


def get_weather(city, country, state=None, test=False):
    """
    Fetches weather data for the specified location using the OpenWeatherMap API.

    Args:
        city (str): The name of the city.
        country (str): The country where the city is located.
        state (str, optional): The state or region, if applicable.
        test (bool): If True, simulates a failed response (used for testing).

    Returns:
        tuple: A tuple containing:
            - dict or None: The weather data if available, else None.
            - str or None: An error message if the request failed.
    """
    weather_data = None
    error_message = None

    # Append state to city if available
    if state:
        city = f"{city},{state}"

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}"
        f"&appid={weather_api_key}&units=metric"
    )
    response = requests.get(url, timeout=30)
    weather_data = response.json()
    status_code = response.status_code

    # Simulate API failure in test mode
    if test:
        status_code = 400

    if status_code != 200:
        weather_data = None
        error_message = "Unable to fetch weather data. Please check your inputs."

    return weather_data, error_message


@views_blueprint.route('/demo')
def frontend_demo():
    """
    Renders the front-end demo page for testing UI components.
    """
    return render_template('frontEndDemo.html')


@views_blueprint.route('/landing')
def landing_page():
    """
    Renders the landing page of the SmartMaps application.
    """
    return render_template('landing-page.html')


@views_blueprint.route('/itinerary')
@login_required
def itinerary_page():
    """
    Renders the schedule view page for the user's itinerary.
    Requires user to be logged in.
    """
    return render_template('schedule.html')

@views_blueprint.route('/analytics')
@login_required
def analytics_page():
    """
    Renders the analytics page for the user's itinerary.
    Requires user to be logged in.
    """
    # if current_user
    return render_template('analytics.html')


@views_blueprint.route('/planning')
def planning_page():
    """
    Renders the planning interface with recommendation cards.
    Requires user to be logged in.
    """
    return render_template('index.html', cards=[], mapbox_key=mapbox_api_key)


def fetch_unsplash_image(query):
    """
    Fetches an image URL from Unsplash based on the given query.

    Args:
        query (str): Search term to look for relevant images.

    Returns:
        str or None: A direct URL to the image if found, otherwise None.
    """
    unsplash_access_key = os.environ.get('UNSPLASH_KEY')
    url = (
        f"https://api.unsplash.com/search/photos?query={query}"
        f"&client_id={unsplash_access_key}&per_page=1"
    )
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["regular"]
    except requests.RequestException as e:
        print(f"Unsplash request error for {query}: {e}")

    # print("Status Code:", response.status_code)
    # print("X-Ratelimit-Limit:", response.headers.get("X-Ratelimit-Limit"))
    # print("X-Ratelimit-Remaining:", response.headers.get("X-Ratelimit-Remaining"))
    # print("X-Ratelimit-Reset:", response.headers.get("X-Ratelimit-Reset"))

    return None


def generate_cards_from_responses(data):
    """
    Generates travel recommendation cards using the Gemini API 
    and enriches each with an Unsplash image.

    Args:
        data (dict): Dictionary of user preferences.

    Returns:
        dict: A dictionary with a "cards" key containing a list of cards.
    """
    destination = data.get("destination", "a destination")
    environment = data.get("environment", "any")
    budget = data.get("budget", "any")
    vibe = data.get("vibe", "any vibe")
    diet = data.get("diet", "no dietary restrictions")
    notes = data.get("notes", "")
    tags = data.get("tags", [])

    tag_str = ", ".join(tags) if tags else "no additional preferences"

    prompt = (
        f"I'm planning a trip to {destination}. I prefer {environment.lower()} activities,"
        f" my budget is {budget}, and I enjoy places that feel {vibe.lower()}."
        f" I have the following dietary restrictions: {diet}."
        f" Additional preferences: {tag_str}."
        f" {notes if notes else ''} "
        "Based on that, suggest the top 1-15 travel spots or experiences that match my preferences. Only generate items that match my preferences exactly."
        " Return them as JSON with:"
        " - location"
        " - stars (1–5)"
        " - tags (as an array)"
        " - a short description."
        " Do NOT wrap the output in markdown or ```."
    )

    try:
        raw_response = make_gemini_request(prompt)
        cleaned = re.sub(r"```(?:json)?\s*|```", "", raw_response).strip()
        cards = json.loads(cleaned)

        if isinstance(cards, list):
            for card in cards:
                location = card.get("location")
                image_url = fetch_unsplash_image(location)
                card["image"] = image_url or "/static/img/no-image-available.png"
            return {"cards": cards}

        if isinstance(cards, dict) and "cards" in cards:
            for card in cards["cards"]:
                location = card.get("location")
                image_url = fetch_unsplash_image(location)
                card["image"] = image_url or "/static/img/no-image-available.png"
            return cards

        print("Error parsing Gemini response structure")
        return fallback_card()

    except (json.JSONDecodeError, TypeError, KeyError) as e:
        print("Error parsing Gemini response:", e)
        return fallback_card()


def fallback_card():
    return {
        "cards": [{
            "location": "Error generating cards",
            "stars": 3,
            "tags": ["fallback"],
            "description": (
                "We couldn't generate recommendations right now. "
                "Please try again later."
            ),
            "image": "/static/default-image.jpg",
        }]
    }


@views_blueprint.route("/submit_survey", methods=["POST"])
def submit_survey():
    """
    Handles survey submission from the frontend.

    Expects:
        JSON payload with user preferences including:
        - destination, environment, budget, vibe, diet, notes (optional)

    Returns:
        JSON: A dictionary with a "cards" key containing a list of recommendation cards.
              If an error occurs, returns an appropriate error message and status code.
    """
    try:
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({"error": "Invalid input format. Expected a JSON object."}), 400

        print("Survey data received:", data)
        cards = generate_cards_from_responses(data)
        return jsonify(cards)

    except Exception as e:
        print("Unhandled error in /submit_survey:", e)
        return jsonify({"error": "An unexpected error occurred. Please try again later."}), 500


@views_blueprint.route("/save_itinerary", methods=["POST"])
# @login_required # add back with login prompt later
def save_itinerary_to_database():
    """
    Endpoint to save the itinerary.
    """
    print("Saving itinerary to database...")
    events = request.get_json().get("events", [])
    if not events:
        return jsonify({"error": "No events provided"}), 400

    print("Events received:", events)

    for event in events:
        title = event["title"]
        start = datetime.strptime(event["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
        print("event start saving:", start)
        end = datetime.strptime(
            event["start"], "%Y-%m-%dT%H:%M:%S.%fZ") if event["end"] else None
        all_day = event["allDay"]

        # Create a new Event instance
        new_event = Event(
            title=title,
            start=start,
            end=end,
            all_day=all_day,
            user_id=current_user.id
        )

        # Add the event to the calendar
        db.session.add(new_event)

    db.session.commit()

    return jsonify({"message": "Itinerary saved successfully!"}), 200


@views_blueprint.route("/get_itinerary", methods=["GET"])
# add version to return empty when not logged in
def get_itinerary_from_database():
    """
    Endpoint to get the itinerary.
    """
    print("Fetching itinerary from database...")
    user_id = current_user.id
    events = Event.query.filter_by(user_id=user_id).all()

    itinerary = []
    for event in events:
        print("event start fetching:", event.start)
        itinerary.append({
            "title": event.title,
            "start": f'{event.start.isoformat()}Z',
            "end": f'{event.end.isoformat()}Z' if event.end else None,
            "allDay": event.all_day
        })

    return jsonify({'events': itinerary}), 200

@views_blueprint.route('/old-survey')
def old_survey_page():
    return render_template('old-survey.html', cards=[], mapbox_key=mapbox_api_key)