import os
import openai
import datetime
from flask import Flask, request, jsonify, render_template, send_file
from pyairtable import Table
from dotenv import load_dotenv
import pdfkit

# Load environment variables
load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)
openai.api_key = OPENAI_API_KEY

# === Blueprint Routes ===
from quick_launch_ai import quick_launch_ai
app.register_blueprint(quick_launch_ai)

# === Branding Report Route ===
@app.route("/generate-branding-report", methods=["POST"])
def generate_branding_report():
    data = request.json
    client_name = data.get("client_name", "Brand Owner")
    business_type = data.get("business_type", "Business")
    industry = data.get("industry", "Industry")

    prompt = f"""
    You are a world-class branding strategist. Generate a Branding Report for {client_name}, a {business_type} in the {industry} industry.
    Include: USP, Positioning, Competitor Analysis, Social Media Plan, Content Ideas, Paid Ad Copy.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    report_content = response["choices"][0]["message"]["content"]

    record = table.create({
        "Client Name": client_name,
        "Business Type": business_type,
        "Industry": industry,
        "Report Content": report_content,
        "Generated Date": str(datetime.datetime.now())
    })

    return jsonify({
        "message": "Branding report generated!",
        "branding_report": report_content,
        "report_id": record['id']
    })

# === Social Calendar Route ===
@app.route("/generate-social-calendar", methods=["POST"])
def generate_social_calendar():
    data = request.json
    subscription_plan = data.get("subscription_plan", "Basic")
    plan_map = {
        "Basic": [
            "📌 Monday: Story-based engagement post",
            "📌 Wednesday: Quote post with CTA",
            "📌 Friday: Behind-the-scenes Reel"
        ],
        "Pro": [
            "📌 Monday: Blog summary",
            "📌 Tuesday: Engagement post",
            "📌 Thursday: LinkedIn post",
            "📌 Friday: Trend Reel"
        ],
        "Premium": [
            "📌 Monday: Testimonial video",
            "📌 Wednesday: Paid ad copy",
            "📌 Friday: Viral trend forecast",
            "📌 Sunday: Blog post"
        ]
    }
    return jsonify({
        "message": "Social Calendar Generated",
        "social_media_calendar": plan_map.get(subscription_plan, plan_map["Basic"])
    })

# === Competitor Analysis Route ===
@app.route("/competitor-analysis", methods=["POST"])
def competitor_analysis():
    data = request.json
    competitor_name = data.get("competitor_name", "Competitor Brand")
    industry = data.get("industry", "Industry")

    prompt = f"""
    Analyze {competitor_name} in the {industry} industry.
    Include: Strengths, Weaknesses, Social Media, Ads, Differentiators.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    competitor_report = response["choices"][0]["message"]["content"]

    return jsonify({
        "message": f"Analysis for {competitor_name}",
        "competitor_analysis": competitor_report
    })

# === Ad Copy Generator ===
@app.route("/generate-ad-copy", methods=["POST"])
def generate_ad_copy():
    data = request.json
    product_name = data.get("product_name", "Brand Product")
    industry = data.get("industry", "Industry")

    prompt = f"""
    Write short-form ad copy for {product_name} in {industry}.
    Include: Facebook, Instagram, LinkedIn, Google.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    ad_copy = response["choices"][0]["message"]["content"]

    return jsonify({
        "message": "Ad Copy Generated",
        "ad_copy": ad_copy
    })

# === SWOT Analysis ===
@app.route("/generate-swot-analysis", methods=["POST"])
def generate_swot_analysis():
    data = request.json
    business_name = data.get("business_name", "Brand")
    industry = data.get("industry", "Industry")

    prompt = f"""
    Generate a SWOT for {business_name} in {industry}.
    Include: Strengths, Weaknesses, Opportunities, Threats, Recommendations.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    swot_report = response["choices"][0]["message"]["content"]

    return jsonify({
        "message": "SWOT Analysis Generated",
        "swot_analysis": swot_report
    })

# === Launch Timeline Route ===
from launch_timeline import generate_launch_timeline

@app.route('/generate_timeline', methods=['POST'])
def generate_timeline():
    data = request.get_json()
    plan_length = int(data.get('plan_length', 7))
    client_name = data.get('client_name', 'BrandVision User')

    html_output = generate_launch_timeline(plan_length=plan_length, client_name=client_name)
    return jsonify({"html": html_output})

# === Swipe Copy Route ===
from swipe_copy_generator import generate_swipe_copy, log_swipe_copy_to_airtable

@app.route('/generate_swipe_copy', methods=['POST'])
def generate_swipe_copy_route():
    data = request.get_json()
    user = data.get("user_name", "Guest User")
    niche = data.get("niche", "coaching")
    audience = data.get("audience", "women entrepreneurs")
    offer = data.get("offer", "signature program")
    emotion = data.get("emotion_tone", "empowering")
    plan = data.get("plan_tier", "free")

    result = generate_swipe_copy(niche, audience, offer, emotion, plan)
    log_swipe_copy_to_airtable(user, niche, audience, offer, emotion, plan, result)

    return jsonify(result)

# === Offer Blueprint Generator Route ===
from offer_matchmaker import generate_offer_blueprint

@app.route('/generate_blueprint', methods=['POST'])
def generate_blueprint():
    user_path = request.form.get('user_path')
    client_type = request.form.get('client_type')
    audience_type = request.form.get('audience_type')
    emotion_summary = request.form.get('emotion_summary')
    content_topics = request.form.get('content_topics')
    inquiry_summary = request.form.get('inquiry_summary')
    niche = request.form.get('niche')
    trend_keywords = request.form.get('trend_keywords')

    html_output = generate_offer_blueprint(
        user_path, client_type, audience_type,
        emotion_summary, content_topics,
        inquiry_summary, niche, trend_keywords
    )

    output_path = f"static/blueprints/blueprint_{datetime.datetime.now().timestamp()}.pdf"
    pdfkit.from_string(html_output, output_path)

    return render_template("blueprint_result.html", html_output=html_output, pdf_url='/' + output_path)

# === New Offer Summary Intake Route (for Tally integration) ===
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

# === Run the Flask App ===
if __name__ == "__main__":
    app.run(debug=True)