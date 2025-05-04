# === BrandVision Profiler - Final Launch Version app.py ===

from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "BrandVision_!2025_SuperSecure_Key_XYZ4729")

# === Initialize Flask app ===
app = Flask(__name__)

# === Authorization Check ===
def check_authorization(request):
    auth_header = request.headers.get('Authorization')
    return auth_header == SECRET_KEY

# === Import Feature Scripts ===
from offer_summary import generate_offer_summary
from audience_to_income import create_audience_to_income
from quick_launch_ai import generate_quick_launch
from swipe_copy_generator import generate_swipe_copy
from emotion_engine import run_emotion_engine
from reddit_scanner_enhanced_19star import run_enhanced_reddit_scanner
from trendsync_engine import generate_trend_insights
from vip_bulk_report import generate_vip_bulk_reports
from brand_tracker import generate_monthly_pulse_report
from affiliate_tracking import register_affiliate

# === ROUTES ===

@app.route('/run-offer-summary', methods=['POST'])
def run_offer_summary_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(generate_offer_summary(request.get_json()))

@app.route('/run-audience-blueprint', methods=['POST'])
def run_audience_blueprint_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(create_audience_to_income(request.get_json()))

@app.route('/run-quick-launch', methods=['POST'])
def run_quick_launch_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(generate_quick_launch(request.get_json()))

@app.route('/run-swipe-copy', methods=['POST'])
def run_swipe_copy_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(generate_swipe_copy(request.get_json()))

@app.route('/run-emotion-engine', methods=['POST'])
def run_emotion_engine_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    keyword = data.get("keyword", "brand strategy")
    user_email = data.get("user_email", "test@brandvision.com")
    try:
        run_emotion_engine(keyword, user_email)
        return jsonify({
            "status": "success",
            "message": f"Emotion Engine report generated for: {keyword}",
            "email": user_email
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Emotion Engine failed: {str(e)}"
        }), 500

@app.route('/run-reddit-scanner', methods=['POST'])
def run_reddit_scanner_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    keyword = data.get("keyword", "default keyword")
    user_email = data.get("user_email", "demo@brandvision.com")
    run_enhanced_reddit_scanner(keyword, user_email)
    return jsonify({
        "status": "success",
        "message": f"Reddit Scanner completed for: {keyword}",
        "user_email": user_email
    })

@app.route('/run-trendsync', methods=['POST'])
def run_trendsync():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    keyword = data.get("keyword", "brand strategy")
    platform = data.get("platform", "multi")
    result = generate_trend_insights(keyword, platform)
    return jsonify({
        "status": "success",
        "keyword": keyword,
        "platform": platform,
        "insight": result
    })

@app.route('/run-vip-bulk', methods=['POST'])
def run_vip_bulk_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(generate_vip_bulk_reports(request.get_json()))

@app.route('/run-brand-tracker', methods=['POST'])
def run_brand_tracker_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(generate_monthly_pulse_report(request.get_json()))

@app.route('/register-affiliate', methods=['POST'])
def register_affiliate_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(register_affiliate(request.get_json()))

# === Run Locally ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
