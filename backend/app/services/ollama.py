import json
import requests
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "mistral"

def analyze_event_from_text(input: str) -> dict:
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")

    prompt = f"""
    You are an intelligent calendar assistant.
    The current time is {current_time}.

    Check if the user's input contains an EVENT (something to attend, has location and duration) or a TASK (something to do, has deadline).
    
    If it contains an event description, extract the event details from the user's input and return only a valid JSON object with the following structure:
    {{
        "type": "event",
        "name" : "Short title of the event (string)",
        "datetime" : "Date and time in 'YYYY-MM-DD HH:MM' format (string)",
        "location" : "Location of the event (string, leave empty if not provided)",
        "duration" : "Duration of the event in minutes (integer)",
        "description" : "Any additional details about the event (string, leave empty if not provided)",
        "repeats" : True if the event repeats, otherwise False (boolean),
        "repeat_interval" : "If the event repeats, specify the interval in days (integer, 0 if not repeating)",
        "repeats_until" : "If the event repeats, specify the end date in 'YYYY-MM-DD' format (string, leave empty if not repeating)"
    }}

    If the user's input contains a task description, extract the task details and return only a valid JSON object with the following structure:
    {{
        "type": "task",
        "name" : "Short title of the task (string)",
        "deadline" : "Date and time in 'YYYY-MM-DD HH:MM' format (string)",
        "description" : "Any additional details about the task (string, leave empty if not provided)"
    }}
    
    User input: "{input}"
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
        ai_response_dict = json.loads(ai_response_text)
        return ai_response_dict
        
    except requests.exceptions.ConnectionError:
        raise Exception("Ollama is not running. Please start Ollama locally.")
    except json.JSONDecodeError:
        raise Exception("AI failed to return a valid JSON.")
    except Exception as e:
        raise Exception(f"An error occurred with AI processing: {str(e)}")