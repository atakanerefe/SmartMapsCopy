import pytest
import requests
from unittest.mock import patch
from website.gemini_api import make_gemini_request

@patch("requests.post")
def test_make_gemini_request_success(mock_post):
    """
    Tests if `make_gemini_request` correctly parses the API response.
    """
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": "Try making pasta!"}]}}
        ]
    }

    result = make_gemini_request("What can I cook?")
    assert result == "Try making pasta!"

@patch("requests.post")
def test_make_gemini_request_error(mock_post):
    """
    Tests how `make_gemini_request` handles API failures.
    """
    mock_post.return_value.status_code = 500

    result = make_gemini_request("What can I cook?")
    assert "Error: Request failed with status 500" in result

@patch("requests.post")
def test_make_gemini_request_missing_keys(mock_post):
    """
    Tests `make_gemini_request` when the API response is missing expected keys.
    This should trigger the KeyError or IndexError exception.
    """
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {  # Missing "candidates" key
        "unexpected_key": "No valid response"
    }

    result = make_gemini_request("What can I cook?")
    assert result == "Sorry, I couldn't generate a response."

@patch("requests.post")
def test_make_gemini_request_index_error(mock_post):
    """
    Tests `make_gemini_request` when the response has an empty 'candidates' list.
    """
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        "candidates": []  # Empty list triggers IndexError
    }

    result = make_gemini_request("What can I cook?")
    assert result == "Sorry, I couldn't generate a response."