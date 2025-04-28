
import os
import openai
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_monthly_tracker(brand_name, month):
    prompt = f"""
You are a branding analyst creating a monthly tracker report.

Brand: {brand_name}
Month: {month}

Include:
1. Summary of brand voice consistency (based on engagement themes)
2. Emotional tone shifts in the audience
3. Top performing content styles (e.g. video, carousels, thought-leadership)
4. Recommended hooks or themes for the upcoming month
5. Offer positioning updates or trend pivots

Make the insights smart, emotionally intelligent, and content-focused.
"""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_monthly_pdf(brand_name, month, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Monthly Brand Tracker", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Brand: {brand_name} | Month: {month}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Implementation Plan", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "To implement this:
"
        "- Adjust your next 30 days of content based on hook suggestions.
"
        "- Use emotional tone shifts to reposition your messaging.
"
        "- Apply offer tweaks based on trend insights.

"
        "Need help executing?
"
        "Book a Strategy Call â https://calendly.com/curlygirllala/30-minute-strategy-call"
    ))

    filename = f"brand_tracker_{brand_name.replace(' ', '_')}_{month.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

def run_monthly_brand_tracker(brand_name, month):
    content = generate_monthly_tracker(brand_name, month)
    filename = create_monthly_pdf(brand_name, month, content)
    print(f"Monthly Tracker PDF saved: {filename}")