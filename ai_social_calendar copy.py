import os
import openai
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
from airtable_connector import save_to_airtable

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === MAIN AI GENERATOR ===
def generate_ai_social_calendar(business_name, industry, subscription):
    """
    Generates a content calendar based on the user's subscription plan.
    """
    content_plan = []

    if subscription == "Free":
        content_plan.extend([
            "📌 Monday: Story-based engagement post",
            "📌 Wednesday: Quote graphic (Brand Identity)",
            "📌 Friday: 'Behind-the-Scenes' short-form video"
        ])
    elif subscription == "Pro":
        content_plan.extend([
            "📌 Monday: Brand storytelling post",
            "📌 Tuesday: AI-generated infographic (Industry Insights)",
            "📌 Thursday: AI-written LinkedIn post (Thought Leadership)",
            "📌 Friday: Instagram Reel (Trend-Based)"
        ])
    elif subscription == "Premium":
        content_plan.extend([
            "📌 Monday: AI-Generated Customer Testimonial Video",
            "📌 Wednesday: Live Q&A Session (AI Recommends Topics)",
            "📌 Friday: AI-Optimized Paid Ad Campaign (Social & Google)",
            "📌 Sunday: Personal Branding Blog Post (SEO-Optimized)"
        ])
    else:
        content_plan.append("⚠️ Invalid Subscription Level")

    return content_plan

# === PDF CREATION FUNCTION ===
def create_pdf_calendar(business_name, industry, calendar):
    filename = f"social_calendar_{business_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "BrandVision Profiler: AI Social Calendar", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Business: {business_name} | Industry: {industry}", ln=True)
    pdf.ln(10)

    for post in calendar:
        pdf.multi_cell(0, 10, post)

    pdf.output(filename)
    return filename

# === FULL RUNNER FUNCTION ===
def run_social_calendar(business_name, industry, subscription, user_email):
    calendar = generate_ai_social_calendar(business_name, industry, subscription)
    pdf_file = create_pdf_calendar(business_name, industry, calendar)

    # Log to Airtable
    save_to_airtable("Social Media Strategy", {
        "User Email": user_email,
        "Business Name": business_name,
        "Industry": industry,
        "Plan": subscription,
        "PDF Filename": pdf_file,
        "Date": datetime.now().isoformat()
    })

    print(f"✅ Social Calendar PDF generated & logged: {pdf_file}")

# === TEST RUN ===
if __name__ == "__main__":
    run_social_calendar(
        business_name="CGL Coaching",
        industry="personal branding",
        subscription="Pro",
        user_email="demo@brandvision.com"
    )