import json
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "mistral"

def analyze_event_from_text(input: str) -> dict:
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")

    prompt = f"""
    You are an intellgent calendar assistant.
    The current time is {current_time}.

    Your task is to extract event details from the user's input and return only a valid JSON object with the following structure:
    {{
        "name" : "Short title of the event (string)",
        "datetime" : "Date and time in 'YYYY-MM-DD HH:MM' format (string)",
        "duration" : "Duration of the event in minutes (integer)",
        "description" : "Any additional details about the event (string, leave empty if not provided)",
        "repeats" : True if the event repeats, otherwise False (boolean),
        "repeat_interval" : "If the event repeats, specify the interval in days (integer, 0 if not repeating)"
    }}

    User message: "{input}"
    """

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "format": "json",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        ai_response_text = data.get("response", "{}")
        event_dict = json.loads(ai_response_text)
        return event_dict
        
    except requests.exceptions.ConnectionError:
        raise Exception("Ollama is not running. Please start Ollama locally.")
    except json.JSONDecodeError:
        raise Exception("AI failed to return a valid JSON.")
    except Exception as e:
        raise Exception(f"An error occurred with AI processing: {str(e)}")