import os
from dotenv import load_dotenv
import requests

# Load .env file and debug it
env_loaded = load_dotenv()
print("DEBUG - .env loaded:", env_loaded)

# Check current working directory
print("DEBUG - Current Directory:", os.getcwd())
print("DEBUG - Files in this directory:", os.listdir())

# Read variables
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("TABLE_NAME")

# Show what we're reading from .env
print("DEBUG - AIRTABLE_API_KEY:", bool(AIRTABLE_API_KEY))
print("DEBUG - BASE_ID:", BASE_ID)
print("DEBUG - TABLE_NAME:", TABLE_NAME)

# Make request
url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)
