
import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Get Airtable and base config
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = os.getenv("TREND_SYNC_TABLE") or os.getenv("AIRTABLE_TABLE_NAME")

# Debug check
print("Using table:", TABLE_NAME)

# Build Airtable URL
url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

# Send a simple GET request to test access
response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)
