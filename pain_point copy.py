import os
import openai
from pyairtable import Table
from datetime import datetime
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from fpdf import FPDF

load_dotenv()

pain_point_bp = Blueprint('pain_point_profiler', __name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
airtable = Table(os.getenv("AIRTABLE_API_KEY"), os.getenv("AIRTABLE_BASE_ID"), "AI Reports Table")

def generate_pain_point_analysis(niche):
    prompt = f"""
You are an AI trained in branding psychology, market behavior, and content strategy.

Target Niche: {niche}

Step 1: Identify top 5 emotional pain points users are experiencing in this niche.
Step 2: Label each pain with its emotional root (e.g. fear, doubt, confusion, overwhelm).
Step 3: Suggest marketing messages that neutralize that emotion (calming phrases, empowering CTAs).
Step 4: Create 3 social media hook examples per pain point.
Step 5: Recommend a high-converting offer that would solve 2+ of these pain points.

Format clearly and use bullet points.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_pdf_report(content, niche):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Pain Point Profiler", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Niche: {niche} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your Next Step", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "Your brand strategy starts here.

"
        "â Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call
"
        "â Unlock AI Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149

"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    filename = f"pain_point_report_{niche.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

@pain_point_bp.route('/generate-pain-point', methods=['POST'])
def generate_pain_point():
    data = request.get_json()
    email = data.get("email")
    niche = data.get("niche")

    try:
        insights = generate_pain_point_analysis(niche)
        filename = generate_pdf_report(insights, niche)

        airtable.create({
            "User Email": email,
            "Niche": niche,
            "Insights": insights,
            "PDF File": filename,
            "Timestamp": datetime.now().isoformat()
        })

        return jsonify({
            "success": True,
            "niche": niche,
            "insights": insights,
            "pdf_file": filename
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
