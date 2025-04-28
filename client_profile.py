
import os
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
from mailjet_rest import Client
import base64
import requests

# Load environment variables
load_dotenv()

# === PDF CREATOR ===
def generate_client_profile_pdf(client_name, email, brand_niche, tone, goals):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Client Profile Snapshot", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Name: {client_name}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.cell(200, 10, f"Niche: {brand_niche}", ln=True)
    pdf.cell(200, 10, f"Tone of Voice: {tone}", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Client Goals:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, goals)

    filename = f"client_profile_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# === EMAIL FUNCTION ===
def send_client_profile_email(pdf_file, recipient_email, client_name):
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
            "Subject": f"Your BrandVision Client Profile Snapshot: {client_name}",
            "TextPart": "Your personalized brand snapshot is attached.",
            "HTMLPart": f"<h3>Your Client Profile Report for <b>{client_name}</b> is ready!</h3><p>We've attached your branding insights, audience fit, and strategy snapshot in a downloadable PDF.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }

    result = mailjet.send.create(data=data)
    print("Email status:", result.status_code)

# === AIRTABLE LOGGING ===
def log_client_profile_to_airtable(name, email, niche, tone, goals, filename):
    airtable_url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/Client Profile Table"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "fields": {
            "Name": name,
            "Email": email,
            "Niche": niche,
            "Tone": tone,
            "Goals": goals,
            "PDF Filename": filename,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }

    response = requests.post(airtable_url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)

# === MAIN FUNCTION ===
def run_client_profile(name, email, niche, tone, goals):
    filename = generate_client_profile_pdf(name, email, niche, tone, goals)
    send_client_profile_email(filename, email, name)
    log_client_profile_to_airtable(name, email, niche, tone, goals, filename)
    print("Client profile report generated, emailed, and logged.")

# === TEST TRIGGER ===
if __name__ == "__main__":
    run_client_profile(
        name="Yalonda Johnson",
        email="demo@brandvision.com",
        niche="Brand Coaching",
        tone="Confident & Conversational",
        goals="Launch a scalable content system, increase audience trust, and convert more clients using AI-powered insights."
    )