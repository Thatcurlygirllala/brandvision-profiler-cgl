import os
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()
BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_TABLE_NAME = "Affiliates"

# Simulated Affiliate Data Fetcher (replace with actual logic if needed)
def fetch_affiliate_data(affiliate_email):
    # In real setup, you'd query Airtable or your database
    return {
        "Affiliate Name": "Alex Rivers",
        "Affiliate Email": affiliate_email,
        "Referrals": 28,
        "Commission Earned": "$280.00",
        "Payout Status": "Pending"
    }

# PDF Generator
def create_affiliate_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Affiliate Report", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"{datetime.now().strftime('%Y-%m-%d')} | {data['Affiliate Name']}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for key, value in data.items():
        pdf.cell(0, 10, f"{key}: {value}", ln=True)

    filename = f"affiliate_report_{data['Affiliate Name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# Airtable Logger
def log_affiliate_report(email, filename):
    url = f"https://api.airtable.com/v0/{BASE_ID}/Affiliates"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "Affiliate Email": email,
            "Report File": filename,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Airtable log status:", response.status_code)

# Main Runner
def run_affiliate_tracker(affiliate_email):
    data = fetch_affiliate_data(affiliate_email)
    pdf_file = create_affiliate_pdf(data)
    log_affiliate_report(affiliate_email, pdf_file)
    print(f"Affiliate report saved & logged for {affiliate_email}")

# Example usage
if __name__ == "__main__":
    run_affiliate_tracker("affiliate@example.com")
