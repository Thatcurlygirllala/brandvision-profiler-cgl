import os
import openai
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from airtable_connector import save_to_airtable  # Assumes you have this helper

# === Load API keys ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Text Cleaner (for emojis / weird symbols) ===
def clean_text(text):
    replacements = {
        "â": "—", "â": "✓", "â¢": "•", "â¦": "...", "â": '"', "â": '"',
        "â": "'", "â": "'", "â": "-", "\u200b": "", "\u2019": "'", "\u2013": "-"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# === AI Calendar Generator ===
def generate_ai_social_calendar(niche, plan_type):
    plan_days = {"Free": 5, "Pro": 7, "Premium": 30}
    num_days = plan_days.get(plan_type, 5)

    prompt = f"""
You are an elite AI branding strategist.

Niche: {niche}
Plan Type: {plan_type}

Generate a {num_days}-day AI-powered content calendar. Include:
- Short-form videos (Reels/TikToks)
- Long-form content (LinkedIn/YouTube)
- Best posting times
- Pain point-based hooks
- CTA prompts
- Bonus: Add an AI Brand Audit Score (1-100) with feedback
Format it cleanly for easy use.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response["choices"][0]["message"]["content"]

# === PDF Generator ===
def create_pdf(business_name, niche, calendar_text):
    filename = f"social_calendar_{business_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "BrandVision Profiler: AI Social Calendar", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Business: {business_name} | Niche: {niche}", ln=True)
    pdf.ln(10)
    pdf.multi_cell(0, 10, clean_text(calendar_text))

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your Next Move", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, 
        "Now that you have your calendar:\n"
        "- Schedule using Buffer, Later, or Metricool.\n"
        "- Add emotional storytelling.\n"
        "- Need help launching?\n"
        "✓ Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "✓ Get the Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149"
    )

    pdf.output(filename)
    return filename

# === Main Runner ===
def run_social_calendar(business_name, niche, plan, user_email):
    print(f"Generating calendar for {business_name} ({niche}) — Plan: {plan}")
    calendar = generate_ai_social_calendar(niche, plan)
    pdf_file = create_pdf(business_name, niche, calendar)

    save_to_airtable("Social Media Strategy", {
        "User Email": user_email,
        "Business Name": business_name,
        "Industry": niche,
        "Plan": plan,
        "PDF Filename": pdf_file,
        "Date": datetime.now().isoformat()
    })

    print(f"✅ PDF saved: {pdf_file}")
    return calendar, pdf_file

# === Test Run ===
if __name__ == "__main__":
    run_social_calendar(
        business_name="CGL Coaching",
        niche="personal branding",
        plan="Pro",
        user_email="demo@brandvision.com"
    )