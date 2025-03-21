import pytest
from unittest.mock import patch

def test_home_page_mock_api(gemini_api_mock):
    """
    GIVEN the itinerary planner app
    WHEN the home page is requested
    THEN it should return a 200 status code and show the app title
    """
    response = gemini_api_mock.get("/")
    assert response.status_code == 200
    assert b"Travel Planner" in response.data  # Adjust based on your actual homepage content


def test_get_itinerary_missing_name(gemini_api_mock):
    """
    Test when 'name' is missing from the POST body
    """
    response = gemini_api_mock.post("/get_itinerary", json={"time": "2025-05-10"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input. Expected location name as a text string."}

def test_get_itinerary_invalid_name(gemini_api_mock):
    """
    Test when 'name' is missing from the POST body
    """
    response = gemini_api_mock.post("/get_itinerary", json={"name":"Waterville, ME, US, 04901", 
                                                            "time": "2025-05-10"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input. Expected location in the format 'city, state, country'."}

def test_get_itinerary_with_state(gemini_api_mock):
    """
    Test when 'state' is present in the POST body
    """
    response = gemini_api_mock.post("/get_itinerary", json={"name":"Waterville, ME, US", 
                                                            "time": "2025-05-10"})
    assert response.status_code == 200
    data = response.get_json()
    assert "itinerary" in data
    assert data["itinerary"].startswith("Here is an itinerary for your trip:")

def test_get_itinerary_missing_time(gemini_api_mock):
    """
    Test when 'time' is missing from the POST body
    """
    response = gemini_api_mock.post("/get_itinerary", json={"name": "Rome, Italy"})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid input. Expected time as a text string."}


@patch("website.views.make_gemini_request", return_value="Here is an itinerary for your trip:\n1. Eiffel Tower at 9 AM\n2. Louvre Museum at 11 AM\n3. Seine River cruise at 2 PM")
def test_get_itinerary_success(mock_gemini, gemini_api_mock):
    """
    GIVEN valid location and time
    WHEN /get_itinerary is POSTed to
    THEN it should return a generated itinerary
    """
    response = gemini_api_mock.post("/get_itinerary", json={
        "name": "Paris, France",
        "time": "2025-05-10"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "itinerary" in data
    assert data["itinerary"].startswith("Here is an itinerary for your trip:")