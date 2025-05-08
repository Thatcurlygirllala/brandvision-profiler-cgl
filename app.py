# === BrandVision Profiler - Final Launch Version app.py ===

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "BrandVision_!2025_SuperSecure_Key_XYZ4729")

# === Initialize Flask App ===
app = Flask(__name__)

# === Authorization Check ===
def check_authorization(request):
    return request.headers.get('Authorization') == SECRET_KEY

# === Feature Script Imports ===
from offer_summary import generate_offer_summary
from audience_to_income import create_audience_to_income
from quick_launch_ai import generate_quick_launch
from swipe_copy_generator import generate_swipe_copy
from emotion_engine import analyze_emotional_tone
from reddit_scanner_enhanced_19star import run_enhanced_reddit_scanner
from trendsync_engine import generate_trend_insights
from vip_bulk_launcher import run_vip_bulk_launcher
from brand_tracker import generate_monthly_pulse_report
from affiliate_tracking import register_affiliate

# === Health Check Route ===
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "ok", "message": "BrandVision Profiler API is running."})

# === Routes ===

@app.route('/run-offer-summary', methods=['POST'])
def run_offer_summary_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        result = generate_offer_summary(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-audience-blueprint', methods=['POST'])
def run_audience_blueprint_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        result = create_audience_to_income(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-quick-launch', methods=['POST'])
def run_quick_launch_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        result = generate_quick_launch(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-swipe-copy', methods=['POST'])
def run_swipe_copy_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        result = generate_swipe_copy(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-emotion-engine', methods=['POST'])
def run_emotion_engine_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        input_text = data.get("text", "")
        result = analyze_emotional_tone(input_text)
        return jsonify({
            "status": "success",
            "input": input_text,
            "emotional_analysis": result
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-reddit-scanner', methods=['POST'])
def run_reddit_scanner_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        keyword = data.get("keyword", "default keyword")
        user_email = data.get("user_email", "demo@brandvision.com")
        run_enhanced_reddit_scanner(keyword, user_email)
        return jsonify({
            "status": "success",
            "message": f"Enhanced Reddit Scanner completed for: {keyword}",
            "user_email": user_email
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-trendsync', methods=['POST'])
def run_trendsync():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        keyword = data.get("keyword", "brand strategy")
        platform = data.get("platform", "multi")
        insight = generate_trend_insights(keyword, platform)
        return jsonify({
            "status": "success",
            "keyword": keyword,
            "platform": platform,
            "insight": insight
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-vip-bulk', methods=['POST'])
def run_vip_bulk_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        client_name = data.get("client_name", "")
        industry = data.get("industry", "")
        goals = data.get("goals", "")
        pdf_filename = run_vip_bulk_launcher(client_name, industry, goals)
        return jsonify({
            "status": "success",
            "message": f"VIP Report generated for {client_name}",
            "filename": pdf_filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/run-brand-tracker', methods=['POST'])
def run_brand_tracker_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        result = generate_monthly_pulse_report(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/register-affiliate', methods=['POST'])
def register_affiliate_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.get_json()
        result = register_affiliate(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Run Locally ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
