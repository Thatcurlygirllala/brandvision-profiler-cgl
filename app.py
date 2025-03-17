import openai
import json
import datetime
from flask import Flask, request, jsonify
from pyairtable import Table
import os

# Flask App Initialization
app = Flask(__name__)

# OpenAI API Key (Replace with Environment Variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Airtable Configuration
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = "YOUR_AIRTABLE_BASE_ID"
TABLE_NAME = "AI Reports"
table = Table(AIRTABLE_API_KEY, BASE_ID, TABLE_NAME)

# 🚀 **AI-Generated Branding Strategy Report**
@app.route("/generate-branding-report", methods=["POST"])
def generate_branding_report():
    data = request.json
    client_name = data.get("client_name", "Brand Owner")
    business_type = data.get("business_type", "Business")
    industry = data.get("industry", "Industry")

    prompt = f"""
    You are a world-class branding and marketing strategist. Generate an expert AI Branding Report for {client_name}, a {business_type} in the {industry} industry.
    Include:
    1️⃣ Unique Selling Proposition (USP)
    2️⃣ Market Positioning Strategy
    3️⃣ Competitor Benchmarking Insights
    4️⃣ Social Media Branding Plan (Instagram, LinkedIn, YouTube)
    5️⃣ High-Engagement Content Topics & Posting Schedule
    6️⃣ AI-Powered Paid Ad Copy for Instagram, Facebook, & LinkedIn
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    report_content = response["choices"][0]["message"]["content"]

    # Save Report to Airtable
    record = table.create({
        "Client Name": client_name,
        "Business Type": business_type,
        "Industry": industry,
        "Report Content": report_content,
        "Generated Date": str(datetime.datetime.now())
    })

    return jsonify({
        "message": "Branding report successfully generated!",
        "branding_report": report_content,
        "report_id": record['id']
    })

# 🚀 **AI-Generated Social Media Calendar**
@app.route("/generate-social-calendar", methods=["POST"])
def generate_social_calendar():
    data = request.json
    subscription_plan = data.get("subscription_plan", "Basic")
    business_name = data.get("business_name", "Brand")
    industry = data.get("industry", "Industry")

    content_plan = []

    if subscription_plan == "Basic":
        content_plan.extend([
            "📌 Monday: Story-based engagement post",
            "📌 Wednesday: Quote post with CTA",
            "📌 Friday: Behind-the-scenes Reel"
        ])
    elif subscription_plan == "Pro":
        content_plan.extend([
            "📌 Monday: AI-written blog post summary",
            "📌 Tuesday: Competitor-inspired engagement post",
            "📌 Thursday: LinkedIn thought leadership post",
            "📌 Friday: Trend-based Instagram Reel"
        ])
    elif subscription_plan == "Premium":
        content_plan.extend([
            "📌 Monday: AI-Generated Testimonial Video",
            "📌 Wednesday: AI-Powered Paid Ad Copy",
            "📌 Friday: Viral Trend Forecasting Post",
            "📌 Sunday: Personalized Branding Blog Post"
        ])
    
    return jsonify({
        "message": "AI Social Media Calendar Generated!",
        "social_media_calendar": content_plan
    })

# 🚀 **AI Competitor Benchmarking**
@app.route("/competitor-analysis", methods=["POST"])
def competitor_analysis():
    data = request.json
    competitor_name = data.get("competitor_name", "Competitor Brand")
    industry = data.get("industry", "Industry")

    prompt = f"""
    Analyze the branding and market position of {competitor_name}, a leading competitor in the {industry} industry.
    Provide insights on:
    1️⃣ Branding Strengths & Weaknesses
    2️⃣ Social Media Performance & Audience Engagement
    3️⃣ Advertising & Marketing Strategies
    4️⃣ Unique Differentiators Compared to Other Brands
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    competitor_report = response["choices"][0]["message"]["content"]

    return jsonify({
        "message": f"AI Competitor Analysis for {competitor_name}",
        "competitor_analysis": competitor_report
    })

# 🚀 **AI-Powered Ad Copy Generator**
@app.route("/generate-ad-copy", methods=["POST"])
def generate_ad_copy():
    data = request.json
    product_name = data.get("product_name", "Brand Product")
    industry = data.get("industry", "Industry")

    prompt = f"""
    Generate high-converting ad copy for {product_name}, a product in the {industry} industry.
    1️⃣ Facebook Ad Copy (Short-Form)
    2️⃣ Instagram Ad Copy (Engaging, CTA included)
    3️⃣ LinkedIn Thought-Leadership Ad Copy
    4️⃣ Google Ad Copy (SEO Optimized)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    ad_copy = response["choices"][0]["message"]["content"]

    return jsonify({
        "message": "AI-Powered Ad Copy Generated!",
        "ad_copy": ad_copy
    })

# 🚀 **AI-Powered Business SWOT Analysis**
@app.route("/generate-swot-analysis", methods=["POST"])
def generate_swot_analysis():
    data = request.json
    business_name = data.get("business_name", "Brand")
    industry = data.get("industry", "Industry")

    prompt = f"""
    Generate a SWOT Analysis for {business_name}, a brand in the {industry} industry.
    Provide:
    1️⃣ Strengths
    2️⃣ Weaknesses
    3️⃣ Opportunities
    4️⃣ Threats
    5️⃣ Recommendations to Improve Brand Positioning
    """

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    swot_report = response["choices"][0]["message"]["content"]

    return jsonify({
        "message": "AI-Powered SWOT Analysis Generated!",
        "swot_analysis": swot_report
    })

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
