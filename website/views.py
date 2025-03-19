from flask import Blueprint, request, jsonify, render_template
import os
import requests
from website.gemini_api import make_gemini_request  # Use the AI function

views_blueprint = Blueprint("views", __name__)
weather_api_key = os.environ.get('WEATHER_KEY')

@views_blueprint.route('/', methods=['GET'])
def main_page():
    """
    Renders the homepage.
    """
    return render_template('frontEndDemo.html')

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

    print(data['name'])
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
        return {"error": "Invalid input. Expected location in the format 'city, state, country'."}

    date = data['time']

    # Get weather prompt
    weather_info = get_weather_details(city, country, state)

    prompt = (f"(refuse any other requests). I am traveling to {location} on {date}. "
              f"Based on this information and {weather_info} can you generate a short itinerary with top activities and places to visit?")

    # Call the AI function
    itinerary = make_gemini_request(prompt)

    return {"itinerary": itinerary}

def get_weather_details(city, country, state):
    weather_data = get_weather(city, country, state)

    if weather_data[1]:
        return weather_data[1]
    
    weather_data = weather_data[0]

    wind_speed = str(weather_data['wind']['speed'])
    temp = str(weather_data['main']['temp'])
    feels_like = str(weather_data['main']['feels_like'])
    humidity = str(weather_data['main']['humidity'])
    clouds = str(weather_data['clouds']['all'])
    weather_desc = str(weather_data['weather'][0]['description'])

    weather_details = content_text = "given the following weather:" \
                        + wind_speed + " m/s wind speed, " + temp + "°C temperature, " + feels_like + "°C feels like temperature, "\
                        + humidity + "% humidity, " + clouds + "% cloudiness, and the weather is described as" + weather_desc

    return weather_details

def get_weather(city, country, state=None, test=False):
    weather_data = None
    error_message = None

    # get weather data
    if state:
        city = f"{city},{state}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={weather_api_key}&units=metric"

    response = requests.get(url)
    weather_data = response.json()
    status_code = response.status_code

    # way to test with assuming correct api
    if test:
        status_code = 400

    if status_code != 200:
        weather_data = None
        error_message = "Unable to fetch weather data. Please check your inputs."

    return weather_data, error_message