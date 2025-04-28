
import os
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF
import requests
from openai import OpenAI

# === Load Environment Variables ===
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# === 1. AI Offer Generator ===
def generate_offer_summary(title, offer_type, description):
    prompt = f"""
You are a 19-star AI Branding Strategist. Create a smart, emotionally engaging **Offer Summary**.

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

Use strong language, insight-based marketing, and confidence-boosting tone.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

# === 2. PDF Generator ===
def create_offer_pdf(title, offer_type, description, summary):
    filename = f"offer_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    # Cover Page
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "BrandVision Profiler", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "AI-Powered Offer Summary", ln=True, align="C")
    pdf.ln(10)

    # Offer Details
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Offer Title: {title}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Type: {offer_type}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Description: {description}")
    pdf.ln(5)

    # AI Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Strategy Summary:", ln=True)
    pdf.set_font("Arial", "", 12)
    clean_summary = summary.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_summary)

    # Monetization CTA
    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "Need help launching?\n"
        "- Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Upgrade with Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    )

    pdf.output(filename)
    return filename

# === 3. Airtable Logging ===
def log_to_airtable(user_email, title, offer_type, description, summary, pdf_filename):
    airtable_url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/{os.getenv('OFFER_GENERATOR_TABLE')}"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }

    fields = {
        "User Email": user_email,
        "Offer Title": title,
        "Offer Type": offer_type,
        "Description": description,
        "AI Summary": summary,
        "PDF Filename": pdf_filename,
        "Status": "Generated",
        "Confidence Score": "Auto",
        "Lead Source": "Offer Generator",
        "Next Step": "Client Review"
    }

    response = requests.post(airtable_url, headers=headers, json={"fields": fields})
    print("Airtable log status:", response.status_code)

# === 4. Main Function ===
def run_offer_summary(title, offer_type, description, user_email="demo@brandvision.com"):
    print(f"Generating AI Offer Summary for: {title}")
    summary = generate_offer_summary(title, offer_type, description)
    pdf_file = create_offer_pdf(title, offer_type, description, summary)
    log_to_airtable(user_email, title, offer_type, description, summary, pdf_file)
    print(f"Offer Summary PDF saved as: {pdf_file}")

# === 5. Test Execution ===
if __name__ == "__main__":
    run_offer_summary(
        title="Emotional Marketing Mastery",
        offer_type="Coaching Program",
        description="A 4-week coaching experience for creators & coaches to master storytelling, emotional hooks, and offer clarity.",
        user_email="brandvisionprofiler@gmail.com"
    )