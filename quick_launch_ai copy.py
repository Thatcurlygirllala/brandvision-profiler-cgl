from flask import Blueprint, request, jsonify
import openai
import os
from datetime import datetime
from pyairtable import Api
from pytrends.request import TrendReq
from fpdf import FPDF
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import traceback

load_dotenv()

quick_launch_ai = Blueprint('quick_launch_ai', __name__)
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = os.getenv("QUICK_LAUNCH_TABLE")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "•": "*", "…": "...",
        "→": "->", "®": "", "©": "", "™": "", "\u200b": "", "â": "✓", "â": "-", "â": "-"
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def export_to_pdf(ideas_text, keyword):
    cleaned_ideas = clean_text(ideas_text)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Quick Launch Vault", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Industry: {keyword} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cleaned_ideas)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "CTA + Bonus", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "Love one of these business ideas?\n"
        "✓ Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "✓ Get the AI Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    filename = f"vault_report_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def send_email(to_email, subject, body, attachment_path):
    try:
        msg = EmailMessage()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(body)

        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"Email sent to {to_email} with attachment {file_name}")
    except Exception as e:
        print("Email failed:", e)

@quick_launch_ai.route('/generate-quick-launch', methods=['POST'])
def generate_quick_launch():
    data = request.get_json()

    user_email = data.get('email')
    budget = data.get('budget', 'any')
    skill_level = data.get('skill_level', 'beginner')
    preferred_industry = data.get('industry', 'any')
    time_commitment = data.get('time_commitment', 'part-time')
    export_pdf = data.get('export_pdf', True)

    trend_keyword = preferred_industry if preferred_industry != 'any' else 'online business'

    try:
        pytrends = TrendReq()
        pytrends.build_payload([trend_keyword], timeframe='today 3-m')
        trend_data = pytrends.interest_over_time()
        trend_score = int(trend_data[trend_keyword].mean()) if not trend_data.empty else "No data"
    except Exception:
        trend_score = "Unavailable"

    prompt = (
        f"You are a premium AI business strategist and trend researcher.\n\n"
        f"Google Trends Insight: Interest in '{trend_keyword}' has an average score of {trend_score}/100 over the last 90 days.\n\n"
        f"Generate 3 low-competition business ideas someone can start this week based on:\n"
        f"- Budget: {budget}\n- Skill Level: {skill_level}\n- Industry: {preferred_industry}\n- Time Commitment: {time_commitment}\n\n"
        f"For each idea, include:\n"
        f"1. Business Name\n2. Emotional Trigger\n3. Audience Fit\n4. Offer or Service\n5. Pricing Strategy\n"
        f"6. Client Acquisition Tips\n7. Tools or Platforms Needed\n8. Startup Cost Estimate\n9. Next 3 Steps to Launch\n"
        f"10. Branding Hook or Slogan\n11. Launch Power Score (Rate 1–100)\n12. Score Breakdown\n13. Emotion Match Tag\n"
        f"14. Real Business Inspiration\n15. Suggested Instagram Caption\n\n"
        f"Format everything in clean markdown."
    )

    try:
        client = openai.OpenAI(api_key=OPENAI_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a startup strategist trained in monetization and current social trends."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2200,
            temperature=0.85
        )
        ideas = response.choices[0].message.content
        ideas_cleaned = clean_text(ideas)

        api = Api(AIRTABLE_KEY)
        table = api.table(BASE_ID, TABLE_NAME)

        airtable_data = {
            "Email": user_email,
            "Generated At": datetime.utcnow().isoformat(),
            "Industry": preferred_industry,
            "Trend Score": str(trend_score),
            "AI Output": ideas_cleaned
        }

        filename = None
        if export_pdf:
            filename = export_to_pdf(ideas_cleaned, preferred_industry)
            airtable_data["PDF Filename"] = filename
            send_email(
                to_email=user_email,
                subject="Your Quick Launch Vault Report is Ready!",
                body="See your custom business ideas attached and take action fast.",
                attachment_path=filename
            )

        table.create(airtable_data)

        return jsonify({
            "success": True,
            "ideas": ideas_cleaned,
            "pdf_file": filename,
            "email": user_email
        })

    except Exception as e:
        print("ERROR:", traceback.format_exc())
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500