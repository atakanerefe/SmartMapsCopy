"""
Handles requests to the Google Gemini API.
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def make_gemini_request(prompt):
    """
    Sends a prompt to the Gemini API and retrieves a response.

    Args:
        prompt (str): The input text to send to the Gemini API.

    Returns:
        str: The response text or an error message.
    """
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    )

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    response = requests.post(url, json=data, headers=headers, timeout=10)

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Sorry, I couldn't generate a response."

    return f"Error: Request failed with status {response.status_code}"
