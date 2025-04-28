import os
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
import openai
import requests

# Load environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
BASE_ID = os.getenv("BASE_ID")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
TABLE_NAME = "Branding Accelerator (VIP)"

# === AI Strategy Generator ===
def generate_vip_branding_bundle(brand_name, industry, goal):
    prompt = f"""
You are a senior AI brand strategist. Create a complete branding accelerator report for:

Brand: {brand_name}
Industry: {industry}
Goal: {goal}

Include:
1. Emotional brand positioning
2. Competitor gap and strategic edge
3. Top 3 pain points and unmet emotional needs
4. Messaging & voice guide
5. Offer structure (main, bonus, upsell)
6. Content strategy (short-form, long-form, CTA strategy)
7. Launch funnel flow (lead magnet → nurture → offer)
8. Final confidence-boosting monetization moves

Use emotional intelligence, brand psychology, and high-converting frameworks.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# === PDF Generator ===
def create_vip_pdf(brand_name, industry, goal, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: VIP Branding Accelerator", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"{brand_name} | Industry: {industry} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "VIP Action Plan", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "Next Steps:\n"
        "- Translate this strategy into a 30-day launch roadmap.\n"
        "- Book a VIP Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Access your Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    filename = f"vip_branding_report_{brand_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# === Airtable Logger ===
def log_vip_to_airtable(user_email, brand_name, industry, filename):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User Email": user_email,
            "Brand Name": brand_name,
            "Niche": industry,
            "PDF Filename": filename,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)

# === Run the Full Flow ===
def run_vip_branding_accelerator(user_email, brand_name, industry, goal):
    content = generate_vip_branding_bundle(brand_name, industry, goal)
    filename = create_vip_pdf(brand_name, industry, goal, content)
    log_vip_to_airtable(user_email, brand_name, industry, filename)
    print(f"VIP Branding Accelerator PDF saved: {filename}")

# === Test ===
if __name__ == "__main__":
    run_vip_branding_accelerator(
        user_email="demo@brandvision.com",
        brand_name="CGL Coaching",
        industry="personal branding",
        goal="Attract premium coaching clients"
    )