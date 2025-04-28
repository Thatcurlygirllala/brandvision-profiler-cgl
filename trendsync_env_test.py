import os
import requests
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Read directly from "TABLE_NAME" since that's what the .env uses
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("TABLE_NAME")

print("Using table:", TABLE_NAME)

# Build Airtable request
url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
headers = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

response = requests.get(url, headers=headers)
print("Status Code:", response.status_code)
print("Response:", response.text)
