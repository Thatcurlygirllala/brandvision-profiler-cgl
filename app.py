from flask import Flask, request, jsonify
from ai_engine import generate_branding_strategy
from email_service import send_branding_report
from database import store_report, get_report

app = Flask(__name__)

# ✅ Home Route (To Prevent 404 Errors)
@app.route("/")
def home():
    return "BrandVision API is Running!"

# ✅ Generate Branding Strategy Route
@app.route("/generate-branding-strategy", methods=["POST"])
def branding_strategy():
    data = request.json
    user_input = data.get("user_input", "")
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    report = generate_branding_strategy(user_input)
    store_report(data["user_id"], report)
    return jsonify({"branding_report": report})

# ✅ Fetch Existing Branding Reports
@app.route("/get-report/<user_id>", methods=["GET"])
def get_branding_report(user_id):
    report = get_report(user_id)
    if report:
        return jsonify({"branding_report": report})
    else:
        return jsonify({"error": "No report found for this user"}), 404

# ✅ Ensure App Runs Properly
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
from flask import Flask, request, jsonify
from ai_engine import generate_ai_social_calendar

app = Flask(__name__)

@app.route("/generate-social-calendar", methods=["POST"])
def social_calendar():
    data = request.json
    niche = data.get("niche", "general")
    plan_type = data.get("plan_type", "basic")
    competitor_analysis = data.get("competitor_analysis", False)
    regenerate = data.get("regenerate", False)

    # Call AI function to generate the content calendar
    calendar = generate_ai_social_calendar(niche, plan_type, competitor_analysis, regenerate)

    return jsonify({"social_media_calendar": calendar})

if __name__ == "__main__":
    app.run(debug=True)
