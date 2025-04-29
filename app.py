# === BrandVision Profiler - Final Launch Version app.py ===

from flask import Flask, request, jsonify
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
from reddit_scanner import generate_reddit_report
from trendsync_engine import generate_trendsync_insights
from vip_bulk_report import generate_vip_bulk_reports
from brand_tracker import generate_monthly_pulse_report
from affiliate_tracking import register_affiliate

# === App Routes ===

@app.route('/run-offer-summary', methods=['POST'])
def run_offer_summary():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_offer_summary(data)
    return jsonify(result)

@app.route('/run-audience-blueprint', methods=['POST'])
def run_audience_blueprint():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = create_audience_to_income(data)
    return jsonify(result)

@app.route('/run-quick-launch', methods=['POST'])
def run_quick_launch():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_quick_launch(data)
    return jsonify(result)

@app.route('/run-swipe-copy', methods=['POST'])
def run_swipe_copy():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_swipe_copy(data)
    return jsonify(result)

@app.route('/run-emotion-engine', methods=['POST'])
def run_emotion_engine():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_emotion_report(data)
    return jsonify(result)

@app.route('/run-reddit-scanner', methods=['POST'])
def run_reddit_scanner():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_reddit_report(data)
    return jsonify(result)

@app.route('/run-trendsync', methods=['POST'])
def run_trendsync():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_trendsync_insights(data)
    return jsonify(result)

@app.route('/run-vip-bulk', methods=['POST'])
def run_vip_bulk():
    if not check_authorization(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.get_json()
    result = generate_vip_bulk_reports(data)
    return jsonify(result)

@app.route('/run-brand-tracker', methods=['POST'])
def run_brand_tracker():
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