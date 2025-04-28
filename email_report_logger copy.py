import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
EMAIL_REPORTS_TABLE = "Email Reports"

def log_email_report(user_email, report_type, pdf_filename, notes=None):
    airtable_url = f"https://api.airtable.com/v0/{BASE_ID}/{EMAIL_REPORTS_TABLE}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "User Email": user_email,
            "Report Type": report_type,
            "PDF Filename": pdf_filename,
            "Date Sent": datetime.utcnow().isoformat(),
        }
    }

    if notes:
        data["fields"]["Notes"] = notes

    response = requests.post(airtable_url, headers=headers, json=data)
    print(f"Email report log status: {response.status_code}")
    return response.status_code
