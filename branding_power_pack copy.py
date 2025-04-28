
import os
import openai
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from airtable_connector import save_to_airtable

# Load API keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_branding_power_pack(brand_name, niche, tone="confident"):
    prompt = f"""
You are a top-tier AI branding strategist.

Create a full Branding Power Pack for:
Brand: {brand_name}
Niche: {niche}
Tone: {tone}

Include:
1. Brand Voice Overview
2. Core Messaging Pillars (3-5)
3. Offer Positioning (benefits + ideal audience)
4. 1-line Unique Value Proposition
5. Website Hero Section (Headline + Subheadline + CTA)
6. Suggested Signature Framework Name
7. Emotional Language Highlights to boost conversions
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message["content"]

def create_branding_pdf(brand_name, content):
    filename = f"branding_power_pack_{brand_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Branding Power Pack", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Brand: {brand_name} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(8)

    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Take Action", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "1. Add this copy to your website and social media profiles.\n"
        "2. Use your Signature Framework in content and offers.\n"
        "3. Book a Strategy Call – https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "4. Unlock the Full Branding Vault – https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    pdf.output(filename)
    return filename

def run_branding_power_pack(brand_name, niche, user_email):
    content = generate_branding_power_pack(brand_name, niche)
    pdf_file = create_branding_pdf(brand_name, content)

    # Log to Airtable
    save_to_airtable("Branding Power Pack", {
        "User Email": user_email,
        "Brand Name": brand_name,
        "Niche": niche,
        "AI Summary": content,
        "PDF Filename": pdf_file,
        "Timestamp": datetime.now().isoformat()
    })

    print(f"Branding Power Pack generated: {pdf_file}")

# Example run
if __name__ == "__main__":
    run_branding_power_pack("CGL Coaching", "business coaching", "demo@brandvision.com")