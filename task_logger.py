import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
TABLE_NAME = "Task Table"

def log_task_to_airtable(user_email, task_name, assigned_by="System", status="Pending", category=None, due_date=None, notes=None):
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
        "Task Name": task_name,
        "Assigned By": assigned_by,
        "Status": status,
        "Timestamp": datetime.utcnow().isoformat()
    }

    if category:
        fields["Task Category"] = category
    if due_date:
        fields["Due Date"] = due_date
    if notes:
        fields["Notes"] = notes

    data = { "fields": fields }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("Task successfully logged to Airtable.")
        else:
            print(f"Failed to log task. Status: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print("Error logging task:", str(e))

# Example usage
if __name__ == "__main__":
    log_task_to_airtable(
        user_email="client@example.com",
        task_name="Review AI Strategy PDF",
        assigned_by="Admin",
        status="In Progress",
        category="AI Reports",
        due_date="2025-04-20",
        notes="Send follow-up after review."
    )