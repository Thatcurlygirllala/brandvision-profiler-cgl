import os
from openai import OpenAI
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
import requests

# === Load Environment Variables ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_id = os.getenv("BASE_ID")
airtable_key = os.getenv("AIRTABLE_API_KEY")
table_name = os.getenv("OFFER_GENERATOR_TABLE")

client = OpenAI(api_key=api_key)

# === AI Offer Generator ===
def generate_offer_summary(title, offer_type, description):
    prompt = f"""
You are a master offer strategist and launch copywriter.

Create a high-converting Offer Summary for:

Title: {title}
Type: {offer_type}
What it includes: {description}

Respond with:
1. Summary of what it is and who it's for
2. Emotional trigger (what pain or desire it solves)
3. Tangible outcomes they'll get
4. Bonuses or fast-action incentives
5. Suggested pricing model (one-time, recurring, etc.)
6. Recommended CTA phrase
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === PDF Generator ===
def create_offer_pdf(title, offer_type, description, summary):
    summary = summary.encode('latin-1', 'replace').decode('latin-1')
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Offer Summary", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Offer: {title} | Type: {offer_type}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Description: {description}")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Offer Strategy:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, summary)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Step:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "Want help launching this offer?\n"
        "- Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Explore Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    )

    filename = f"offer_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
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
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)

# === Run Offer Generator ===
def run_offer_summary(title, offer_type, description, user_email="demo@brandvision.com"):
    print(f"Generating AI Offer Summary for: {title}")
    summary = generate_offer_summary(title, offer_type, description)
    pdf_file = create_offer_pdf(title, offer_type, description, summary)
    log_offer_to_airtable(user_email, title, offer_type, description, summary, pdf_file)
    print(f"Offer Summary PDF saved as: {pdf_file}")

# === Test Trigger ===
if __name__ == "__main__":
    run_offer_summary(
        title="Emotional Marketing Mastery",
        offer_type="Coaching",
        description="4-part video series to teach coaches how to create emotionally magnetic content that sells.",
        user_email="demo@brandvision.com"
    )