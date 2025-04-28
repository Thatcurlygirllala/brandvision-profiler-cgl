import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
TABLE_NAME = "Payments Table"

def log_payment_to_airtable(user_email, product_name, amount, payment_method, transaction_id, status="Completed"):
    if not BASE_ID or not AIRTABLE_API_KEY:
        print("Missing BASE_ID or AIRTABLE_API_KEY in environment.")
        return

    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "User Email": user_email,
            "Product": product_name,
            "Amount": float(amount),
            "Payment Method": payment_method,
            "Transaction ID": transaction_id,
            "Status": status,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200 or response.status_code == 201:
            print("Payment successfully logged to Airtable.")
        else:
            print(f"Failed to log payment. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print("Error logging payment to Airtable:", str(e))

# Example usage
if __name__ == "__main__":
    log_payment_to_airtable(
        user_email="client@example.com",
        product_name="AI Branding Accelerator",
        amount=999,
        payment_method="Stripe",
        transaction_id="txn_demo_999"
    )