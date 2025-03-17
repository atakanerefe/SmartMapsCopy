import pytest

def test_generate_endpoint(gemini_api_mock):
    """
    Tests the `/generate` endpoint to ensure it returns AI-generated responses.
    """
    response = gemini_api_mock.post("/generate", json={"input": "Tell me a joke."})
    
    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
    assert isinstance(data["response"], str)

def test_generate_endpoint_missing_input(gemini_api_mock):
    """
    Tests `/generate` when no input is provided.
    It should return a 400 error with a relevant message.
    """
    response = gemini_api_mock.post("/generate", json={})  # No "input" key
    assert response.status_code == 400
    assert response.get_json() == {"error": "No input provided"}

def test_generate_endpoint_empty_input(gemini_api_mock):
    """
    Tests `/generate` when input is an empty string.
    It should return a 400 error with a relevant message.
    """
    response = gemini_api_mock.post("/generate", json={"input": ""})  # Empty input
    assert response.status_code == 400
    assert response.get_json() == {"error": "No input provided"}
