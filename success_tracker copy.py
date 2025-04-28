
import os
import base64
import requests
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
from mailjet_rest import Client

# Load environment variables
load_dotenv()

# === PDF CREATOR ===
def generate_success_tracker_pdf(business_name, email, highlights, lessons, metrics, next_steps):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Social Media Success Tracker", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Business: {business_name}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.ln(10)

    sections = {
        "Wins / Highlights": highlights,
        "Lessons Learned": lessons,
        "Top Metrics Tracked": metrics,
        "Next Steps & Focus": next_steps
    }

    for title, text in sections.items():
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, text)
        pdf.ln(5)

    filename = f"success_tracker_{business_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# === EMAIL DELIVERY ===
def send_success_tracker_email(pdf_file, recipient_email, business_name):
    mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_SECRET_KEY")))
    with open(pdf_file, "rb") as file:
        pdf_data = file.read()

    data = {
        'Messages': [{
            "From": {
                "Email": os.getenv("MAILJET_SENDER"),
                "Name": "BrandVision Profiler"
            },
            "To": [{"Email": recipient_email}],
            "Subject": f"Social Media Success Tracker for {business_name}",
            "TextPart": "Your monthly success report is attached.",
            "HTMLPart": f"<h3>Here's your success tracker PDF for <b>{business_name}</b></h3><p>Use this to reflect, plan and scale smarter.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }

    result = mailjet.send.create(data=data)
    print("Email sent:", result.status_code)

# === AIRTABLE LOGGING ===
def log_success_tracker_to_airtable(business_name, email, filename):
    airtable_url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/Social Media Success"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "Business Name": business_name,
            "Email": email,
            "PDF Filename": filename,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }

    response = requests.post(airtable_url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)

# === MAIN RUN FUNCTION ===
def run_success_tracker(business_name, email, highlights, lessons, metrics, next_steps):
    pdf_file = generate_success_tracker_pdf(business_name, email, highlights, lessons, metrics, next_steps)
    send_success_tracker_email(pdf_file, email, business_name)
    log_success_tracker_to_airtable(business_name, email, pdf_file)
    print(f"Success tracker report saved and sent for {business_name}.")

# === EXAMPLE USAGE ===
if __name__ == "__main__":
    run_success_tracker(
        business_name="CGL Coaching",
        email="demo@brandvision.com",
        highlights="Increased reach by 25%, first viral Reel, 3 new inbound leads.",
        lessons="Posts with emotional storytelling converted best. Educational posts underperformed.",
        metrics="Reach: 40.2k | Engagement Rate: 5.6% | Followers: +127",
        next_steps="Focus on emotional content, schedule Reels 3x/week, test new CTA formats."
    )