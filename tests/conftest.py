import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from website import create_app

@pytest.fixture(scope='module')
def test_client():
    """Creates a Flask test client for testing API endpoints."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        yield testing_client  # This is where the tests will run

@pytest.fixture(scope='function')
def gemini_api_mock(mocker):
    """Mock the Gemini API response to avoid real API calls."""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Mocking getRecipesAPI to return a static response instead of calling Gemini
    mocker.patch('website.views.get_itinerary', return_value="1. Breakfast at local café\n2. Hike at Blue Mountain\n3. Wine tasting in the afternoon")

    with flask_app.test_client() as testing_client:
        yield testing_client
    