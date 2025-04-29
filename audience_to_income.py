import os
import openai
import requests
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# === Load environment variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
AIRTABLE_BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = "AI Reports Table"

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# === AI Strategy Generator ===
def create_audience_to_income(audience_description, user_strength="writing"):
    prompt = f"""
You are a 19-star AI monetization strategist helping brands turn their audience into income.

Audience: {audience_description}
User Strength: {user_strength}

Create an Audience-to-Income Blueprint:
1. Analyze emotional signals & engagement stage
2. Recommend 2 monetizable offers (aligned with emotions + strengths)
3. Suggest 3 soft-sell CTA post ideas
4. Funnel path (DM prompt → lead magnet → upsell)
5. Confidence-boosting language to reduce doubt
6. Quick win timeline (7-day warm-up)
7. Add a VIP upgrade suggestion with call-to-action
"""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === PDF Generator (with encoding fix) ===
def create_income_pdf(content, audience_description):
    def clean_text(text):
        replacements = {
            "’": "'", "‘": "'", "“": '"', "”": '"',
            "–": "-", "—": "-", "•": "*", "…": "...",
            "→": "->", "®": "", "©": "", "™": "", "\u200b": "", "\u2019": "'"
        }
        for bad, good in replacements.items():
            text = text.replace(bad, good)
        return text

    cleaned_content = clean_text(content)
    cleaned_input = clean_text(audience_description)

    filename = f"income_blueprint_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Monetization Blueprint", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Input: {cleaned_input[:50]}... | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cleaned_content)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "- Turn this into a launch plan.\n"
        "- Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Unlock the Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    )

    pdf.output(filename)
    return filename

# === Airtable Logger (Updated) ===
def log_income_blueprint_to_airtable(user_email, audience_description):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User Email": user_email,
            "Report Type": "Audience-to-Income Blueprint",
            "Keyword": audience_description[:80],
            "Source": "Audience-to-Income Blueprint",
            "Confidence Score": 95,
            "Lead Source": "Direct Script Run"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)
    if response.status_code != 200:
        print("Error response:", response.text)

# === Gmail Auto Email Sender ===
def send_email_with_attachment(to_email, subject, body, attachment_path):
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
        print("EMAIL_ADDRESS:", EMAIL_ADDRESS)
        print("EMAIL_PASSWORD:", EMAIL_PASSWORD)
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print(f"Email sent to {to_email} with attachment {file_name}")

# === Run Everything ===
def run_audience_to_income_blueprint(audience_description, user_strength="writing", user_email="demo@brandvision.com"):
    print(f"Generating 19-star Monetization Blueprint for: {audience_description}")
    summary = create_audience_to_income(audience_description, user_strength)
    filename = create_income_pdf(summary, audience_description)
    log_income_blueprint_to_airtable(user_email, audience_description)

    email_subject = "Your Monetization Blueprint is Ready!"
    email_body = (
        f"Hi there,\n\nYour personalized Audience-to-Income Blueprint is ready.\n"
        f"Use it to launch confidently and convert your audience.\n\n"
        f"Book your strategy call here: https://calendly.com/curlygirllala/30-minute-strategy-call\n\n"
        f"– Team BrandVision Profiler"
    )
    send_email_with_attachment(user_email, email_subject, email_body, filename)
    print("✅ All steps completed successfully.")

# === Test Run ===
if __name__ == "__main__":
    run_audience_to_income_blueprint(
        audience_description="People love my content but I don’t know what to sell",
        user_strength="speaking",
        user_email="demo@brandvision.com"
    )
