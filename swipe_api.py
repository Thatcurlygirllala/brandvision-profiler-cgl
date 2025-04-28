from flask import Flask, request, jsonify
from swipe_engine import generate_swipe_copy
from generate_swipe_pdf import create_swipe_copy_pdf
from log_swipe_copy_to_airtable import log_swipe_copy_to_airtable
from send_swipe_email import send_email_with_pdf

app = Flask(__name__)

@app.route('/generate-swipe-copy', methods=['POST'])
def generate_swipe():
    try:
        data = request.json
        user_email = data.get("email")
        user_name = data.get("name", "User")
        niche = data.get("niche")
        audience = data.get("audience")
        offer = data.get("offer")
        emotion_tone = data.get("emotion_tone")
        plan_tier = data.get("plan_tier", "Free")

        if not all([user_email, niche, audience, offer, emotion_tone]):
            return jsonify({"error": "Missing required fields"}), 400

        # Run the generator
        result = generate_swipe_copy(niche, audience, offer, emotion_tone, plan_tier)

        # Create the PDF
        pdf_file = create_swipe_copy_pdf(user_name, niche, emotion_tone, result)

        # Log to Airtable
        log_swipe_copy_to_airtable(user_email, niche, audience, offer, emotion_tone, plan_tier, result, pdf_file)

        # Email the result
        send_email_with_pdf(pdf_file, user_email, emotion_tone, niche)

        return jsonify({"message": "Swipe Copy Generated & Emailed!", "status": "success"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
