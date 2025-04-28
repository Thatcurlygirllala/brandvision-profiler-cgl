
import os
import requests
from datetime import datetime

def log_to_airtable(user_email, keyword, emotions, pdf_file):
    url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/TrendDominationLogs"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User Email": user_email,
            "Keyword": keyword,
            "Emotional Summary": emotions,
            "PDF File": pdf_file,
            "Timestamp": datetime.now().isoformat(),
            "Source": "Trend Domination Engine"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)
