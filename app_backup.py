import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pyairtable import Base

# Load environment variables
load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")

airtable_base = Base(AIRTABLE_API_KEY, AIRTABLE_BASE_ID)
openai.api_key = OPENAI_API_KEY

# === Offer Summary Route Only ===
from offer_summary_generator import run_offer_summary as run_offer_summary_logic

@app.route("/run-offer-summary", methods=["POST"])
def offer_summary_webhook():
    try:
        data = request.json
        email = data.get("email")
        offer_title = data.get("offer_title")
        offer_type = data.get("offer_type")
        offer_description = data.get("offer_description")

        if not all([email, offer_title, offer_type, offer_description]):
            return jsonify({"error": "Missing fields"}), 400

        run_offer_summary_logic(
            title=offer_title,
            offer_type=offer_type,
            description=offer_description,
            user_email=email
        )

        return jsonify({"success": True, "message": "Offer summary created successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run Flask ===
if __name__ == "__main__":
    app.run(debug=True)