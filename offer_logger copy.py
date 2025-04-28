import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Airtable Setup
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = "Offer Creation Logs"

def log_offer_to_airtable(email, offer_type, topic, delivery_method, price_range, value_stack, brand_emotion):
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        print("Missing API key or Base ID.")
        return

    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "User Email": email,
            "Offer Type": offer_type,
            "Offer Topic": topic,
            "Delivery Method": delivery_method,
            "Price Range": price_range,
            "Value Stack": value_stack,
            "Brand Emotion": brand_emotion,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print("Offer successfully logged to Airtable.")
    else:
        print("Failed to log offer:", response.text)

# Example use
if __name__ == "__main__":
    log_offer_to_airtable(
        email="client@example.com",
        offer_type="Signature Program",
        topic="Confident Content Strategy",
        delivery_method="Live Cohort",
        price_range="$497 - $997",
        value_stack="✓ Templates ✓ Coaching Calls ✓ Private Portal",
        brand_emotion="Empowered"
    )