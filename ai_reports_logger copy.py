
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
TABLE_NAME = "AI Reports Table"

def log_ai_report_to_airtable(user_email, report_type, keyword, pdf_filename, notes=None):
    if not BASE_ID or not AIRTABLE_API_KEY:
        print("Missing BASE_ID or AIRTABLE_API_KEY.")
        return

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    fields = {
        "User Email": user_email,
        "Report Type": report_type,
        "Keyword": keyword,
        "PDF Filename": pdf_filename,
        "Timestamp": datetime.utcnow().isoformat()
    }

    if notes:
        fields["Notes"] = notes

    data = { "fields": fields }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("AI Report successfully logged to Airtable.")
        else:
            print(f"Failed to log AI Report. Status: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print("Error logging AI Report:", str(e))

# Example usage
if __name__ == "__main__":
    log_ai_report_to_airtable(
        user_email="client@example.com",
        report_type="Audience-to-Income Blueprint",
        keyword="coaching burnout",
        pdf_filename="income_blueprint_coaching_burnout.pdf",
        notes="High interest in monetization."
    )