
import os
import requests
from datetime import datetime

def log_income_blueprint_to_airtable(user_email, audience_description):
    url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/AI Reports Table"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User Email": user_email,
            "Report Type": "Audience-to-Income Blueprint",
            "Keyword": audience_description[:80],
            "Source": "Audience-to-Income Blueprint",
            "Confidence Score": 95,
            "Lead Source": "Direct Script Run"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)
    if response.status_code != 200:
        print("Error response:", response.text)
