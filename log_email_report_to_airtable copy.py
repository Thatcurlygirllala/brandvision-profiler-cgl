import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
TABLE_NAME = "Email Reports"

def log_email_report(user_email, report_type, file_name, delivery_status="Sent"):
    if not BASE_ID or not AIRTABLE_API_KEY:
        print("Missing BASE_ID or AIRTABLE_API_KEY.")
        return

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "User Email": user_email,
            "Report Type": report_type,
            "PDF Filename": file_name,
            "Delivery Status": delivery_status,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("Email report successfully logged to Airtable.")
        else:
            print(f"Failed to log email report. Status: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print("Error logging email report:", str(e))

# Example usage
if __name__ == "__main__":
    log_email_report(
        user_email="client@example.com",
        report_type="TrendSync Insights",
        file_name="trend_sync_insight_confidence_content_20250416.pdf"
    )