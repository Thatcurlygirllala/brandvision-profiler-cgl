
import os
import requests
from datetime import datetime

def log_tracker_to_airtable(user_email, brand_name, month, pdf_file):
    url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/MonthlyTrackerLogs"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User Email": user_email,
            "Brand Name": brand_name,
            "Month": month,
            "PDF File": pdf_file,
            "Timestamp": datetime.now().isoformat(),
            "Source": "Monthly Brand Tracker"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)
