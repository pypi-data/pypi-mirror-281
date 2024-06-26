# app1/decorators.py
import requests
from functools import wraps
import os

def load_api_key():
    api_key_file = "api_key.txt"
    if os.path.exists(api_key_file):
        with open(api_key_file, "r") as file:
            api_key = file.read().strip()
            print(f"Loaded API key from file: {api_key}")  # Debug print
            return api_key
    print("API key file not found")  # Debug print
    return None

def validate_api_key(api_key):
    url = "https://demo-cr.twinhome.online/chatbot/api/validate-key/"  # Change to your actual domain
    response = requests.post(url, json={"api_key": api_key})
    print(f"Validation response status: {response.status_code}")  # Debug print
    print(f"Validation response body: {response.text}")  # Debug print
    return response.status_code == 200

def api_key_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        api_key = load_api_key()
        if not api_key:
            raise ValueError("API key is required and not found in the local file")

        if not validate_api_key(api_key):
            raise ValueError("Invalid or inactive API key")

        # Proceed with the function call
        return func(*args, **kwargs)
    
    return wrapper
