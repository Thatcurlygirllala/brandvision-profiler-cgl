import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
TABLE_NAME = "Payments Table"

def log_payment_to_airtable(user_email, product_name, amount, payment_type="One-Time", notes=None):
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
        "Product": product_name,
        "Amount": float(amount),
        "Payment Type": payment_type,
        "Date": datetime.utcnow().isoformat()
    }

    if notes:
        fields["Notes"] = notes

    data = { "fields": fields }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            print("Payment successfully logged to Airtable.")
        else:
            print(f"Failed to log payment. Status: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print("Error logging payment:", str(e))

# Example usage
if __name__ == "__main__":
    log_payment_to_airtable(
        user_email="client@example.com",
        product_name="AI Power Bundle",
        amount=149,
        payment_type="One-Time",
        notes="Purchased via website upsell flow."
    )