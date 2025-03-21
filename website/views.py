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
        return jsonify({"error": "Invalid input. Expected location in the format 'city, state, country'."}), 400

    date = data['time']

    # Get weather prompt
    weather_info = get_weather_details(city, country, state)

    prompt = (f"I am traveling to {location} on {date}. "
              f"Based on this information and {weather_info} can you generate a one-day itinerary with top activities and places to visit?"
              "Prioritize activities that are suitable for the weather conditions, priotizing outdoor activities with nice weather and indoor ones in bad weather. "
              "Do not include a description of the weather at the beginning of the itinerary. Start with Here is an itinerary for your trip:"
              )

    # Call the AI function
    itinerary = make_gemini_request(prompt)

    return {"itinerary": itinerary}

def get_weather_details(city, country, state):
    weather_data = get_weather(city, country, state)
    
    weather_data = weather_data[0]

    test_weather_data = weather_data = {'coord': {'lon': -74.006, 'lat': 40.7143}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 12.2, 'feels_like': 10.05, 'temp_min': 12.2, 'temp_max': 12.2, 'pressure': 1007, 'humidity': 22, 'sea_level': 1007, 'grnd_level': 1007}, 'visibility': 10000, 'wind': {'speed': 13.38, 'deg': 310, 'gust': 18.01}, 'clouds': {'all': 0}, 'dt': 1742592380, 'sys': {'type': 2, 'id': 2008776, 'country': 'US', 'sunrise': 1742554642, 'sunset': 1742598528}, 'timezone': -14400, 'id': 5128581, 'name': 'New York', 'cod': 200}

    if weather_data is None:
        weather_data = test_weather_data
    
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

    return weather_data, error_message