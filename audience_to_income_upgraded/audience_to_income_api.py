
from flask import Flask, request, jsonify
from audience_to_income_engine import generate_income_blueprint
from generate_income_pdf import create_income_pdf
from log_income_to_airtable import log_income_blueprint_to_airtable
from send_income_email import send_email_with_attachment

app = Flask(__name__)

@app.route('/generate-income-blueprint', methods=['POST'])
def generate_income():
    try:
        data = request.get_json()
        user_email = data.get("email")
        audience_description = data.get("audience_description")
        user_strength = data.get("user_strength", "writing")

        summary = generate_income_blueprint(audience_description, user_strength)
        filename = create_income_pdf(summary, audience_description)
        log_income_blueprint_to_airtable(user_email, audience_description)

        send_email_with_attachment(
            to_email=user_email,
            subject="Your Monetization Blueprint is Ready!",
            body="Attached is your personalized Audience-to-Income Blueprint. Use it to launch smarter!",
            attachment_path=filename
        )

        return jsonify({"success": True, "message": "Blueprint generated and emailed!"})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
