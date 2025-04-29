# === BrandVision Profiler - Final Launch Version app.py (Fixed) ===

from flask import Flask, request, jsonify
from trendsync_engine import generate_trend_insights
import os

# === Load Environment Variables ===
from dotenv import load_dotenv
load_dotenv()

# === Initialize Flask app ===
app = Flask(__name__)

# === Load Secret Key ===
SECRET_KEY = os.getenv("SECRET_KEY", "BrandVision_!2025_SuperSecure_Key_XYZ4729")

# === Authorization Check ===
def check_authorization(request):
    auth_header = request.headers.get('Authorization')
    if auth_header != SECRET_KEY:
        return False
    return True

# === Import Feature Scripts ===
from offer_summary import generate_offer_summary
from audience_to_income import create_audience_to_income
from quick_launch_ai import generate_quick_launch
from swipe_copy_generator import generate_swipe_copy
from emotion_engine import generate_emotion_report
from reddit_scanner_enhanced_19star import run_enhanced_reddit_scanner
from trendsync_engine import run_trend_insights
from vip_bulk_report import generate_vip_bulk_reports
from brand_tracker import generate_monthly_pulse_report
from affiliate_tracking import register_affiliate

# === App Routes ===

@app.route('/run-offer-summary', methods=['POST'])
def run_offer_summary_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_offer_summary(data)
    return jsonify(result)

@app.route('/run-audience-blueprint', methods=['POST'])
def run_audience_blueprint_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = create_audience_to_income(data)
    return jsonify(result)

@app.route('/run-quick-launch', methods=['POST'])
def run_quick_launch_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_quick_launch(data)
    return jsonify(result)

@app.route('/run-swipe-copy', methods=['POST'])
def run_swipe_copy_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_swipe_copy(data)
    return jsonify(result)

@app.route('/run-emotion-engine', methods=['POST'])
def run_emotion_engine_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_emotion_report(data)
    return jsonify(result)

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
        "message": f"Enhanced Reddit Scanner completed for keyword: {keyword}",
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
    data = request.get_json()
    result = generate_vip_bulk_reports(data)
    return jsonify(result)

@app.route('/run-brand-tracker', methods=['POST'])
def run_brand_tracker_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_monthly_pulse_report(data)
    return jsonify(result)

@app.route('/register-affiliate', methods=['POST'])
def register_affiliate_route():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = register_affiliate(data)
    return jsonify(result)

# === Run App Locally for Testing ===
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
