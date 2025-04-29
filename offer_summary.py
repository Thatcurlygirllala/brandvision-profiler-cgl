# === Offer Summary Generator: Unified 19-Star Version ===

import os
import openai

from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
import requests
import smtplib
from email.message import EmailMessage

# === Load Environment Variables ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_id = os.getenv("BASE_ID")
airtable_key = os.getenv("AIRTABLE_API_KEY")
table_name = os.getenv("OFFER_GENERATOR_TABLE")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_APP_PASSWORD")

# === Set OpenAI API key ===
openai.api_key = api_key

# === AI Offer Generator ===
def generate_offer_summary(title, offer_type, description):
    prompt = f"""
You are a 19-star AI Branding Strategist. Create a smart, emotionally engaging Offer Summary.

Details:
- Title: {title}
- Type: {offer_type}
- Description: {description}

Include:
1. Who it’s for
2. Emotional pain/desire it solves
3. Tangible outcomes
4. Bonuses or urgency triggers
5. Suggested pricing model (with confidence score)
6. Launch funnel path (lead magnet → upsell)
7. CTA phrase to trigger action
8. Instant Upgrade Offer (Power Bundle or Strategy Call)
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# === PDF Generator ===
def create_offer_pdf(title, offer_type, description, summary):
    summary_cleaned = summary.encode('latin-1', 'replace').decode('latin-1')
    filename = f"offer_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "BrandVision Profiler: Offer Summary", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Title: {title}\nType: {offer_type}\n\nDescription: {description}")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Strategy:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, summary_cleaned)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "✓ Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "✓ Upgrade with Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    )

    pdf.output(filename)
    return filename

# === Airtable Logger ===
def log_offer_to_airtable(user_email, title, offer_type, description, summary, pdf_filename):
    url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
    headers = {
        "Authorization": f"Bearer {airtable_key}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User Email": user_email,
            "Offer Title": title,
            "Offer Type": offer_type,
            "Offer Description": description,
            "Offer Summary": summary,
            "PDF Filename": pdf_filename,
            "Status": "Generated",
            "Confidence Score": "Auto",
            "Lead Source": "Offer Generator",
            "Next Step": "Client Review"
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)

# === Email Sender ===
def send_offer_email(to_email, subject, body, attachment_path):
    msg = EmailMessage()
    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with open(attachment_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(attachment_path))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

    print(f"Email sent to {to_email}")

# === Run Everything ===
def run_offer_summary(title, offer_type, description, user_email="demo@brandvision.com"):
    print(f"Generating AI Offer Summary for: {title}")
    summary = generate_offer_summary(title, offer_type, description)
    pdf_file = create_offer_pdf(title, offer_type, description, summary)
    log_offer_to_airtable(user_email, title, offer_type, description, summary, pdf_file)
    send_offer_email(user_email, f"Your Offer Summary: {title}", "See your AI-generated offer summary attached.", pdf_file)
    print(f"✅ Offer Summary generated and emailed.")

# === Test Run (Optional) ===
if __name__ == "__main__":
    run_offer_summary(
        title="Emotional Marketing Mastery",
        offer_type="Coaching Program",
        description="4-week experience for creators & coaches to master storytelling, emotional hooks, and content that converts.",
        user_email="brandvisionprofiler@gmail.com"
    )