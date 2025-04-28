from fpdf import FPDF
from datetime import datetime
from airtable_connector import save_to_airtable

def run_social_calendar(business_name, industry, subscription, user_email):
    calendar = generate_ai_social_calendar(business_name, industry, subscription)

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
    print(f"PDF Saved: {filename}")

    # Save to Airtable
    save_to_airtable("Social Media Strategy", {
        "User Email": user_email,
        "Business Name": business_name,
        "Industry": industry,
        "Plan": subscription,
        "PDF Filename": filename,
        "Date": datetime.now().isoformat()
    return content_calendar

ai_role = """
You are an AI-powered Branding & Social Media Marketing expert. Your expertise includes:
- Brand positioning & audience engagement.
- Competitor analysis & differentiation strategies.
- Viral social media content creation.
- AI-powered paid ads for Instagram, Facebook, and LinkedIn.
"""

def generate_branding_strategy(user_input):
    prompt = f"""
    Branding Request: {user_input}
    - Unique brand positioning strategy
    - Top 3 audience pain points
    - Competitor weaknesses & how to differentiate
    - Viral content strategy for LinkedIn & Instagram
    - CTA-driven messaging approach
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": ai_role}, {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]
import openai
import datetime

# ✅ AI Social Media Calendar Function (DO NOT DELETE OLD FUNCTIONS)
def generate_ai_social_calendar(niche, plan_type, competitor_analysis=True, regenerate=False):
    """
    Generates an AI-powered social media content calendar with trends & brand audits.
    
    :param niche: The industry or business niche.
    :param plan_type: 'basic', 'pro', or 'premium' (5, 7, or 30-day plan).
    :param competitor_analysis: Whether to include competitor-based insights.
    :param regenerate: Whether the user is regenerating an existing calendar.
    :return: A structured social media content plan (dict).
    """

    # Define the number of days based on the plan
    plan_days = {"basic": 5, "pro": 7, "premium": 30}
    num_days = plan_days.get(plan_type, 5)

    # AI Prompt for Branding & Social Media Strategy
    prompt = f"""
    You are an expert branding and social media marketing strategist. 
    Generate a {num_days}-day **social media content calendar** for a business in the **{niche}** niche.

    The calendar must:
    ✅ Solve audience problems & pain points.
    ✅ Include **short-form video ideas** (Reels, TikToks, Shorts).
    ✅ Include **long-form video ideas** (YouTube, LinkedIn Webinars).
    ✅ Suggest the **best posting times** for maximum engagement.
    ✅ Provide expert **branding insights** and engagement strategies.
    ✅ Offer **niche competitor trend insights** (if competitor_analysis=True).
    ✅ If regenerate=True, improve the strategy based on past content.

    Structure the response like this:
    - **Day X: [Post Type]**
    - **Content Idea:**
    - **Best Posting Time:**
    - **Hashtags:**
    - **Call-To-Action (CTA):**
    - **Competitor Insight (if applicable):**

    Also, generate an **AI-powered Brand Audit Score** (out of 100), analyzing:
    ✅ **Social presence & engagement levels**
    ✅ **Content consistency & branding effectiveness**
    ✅ **Audience interaction & growth rate**
    
    Finally, provide a **1-Click Scheduling Recommendation** (Buffer, Later, Metricool).
    """

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract AI response
    content_calendar = response["choices"][0]["message"]["content"]

    return content_calendar
def generate_ai_social_calendar(business_name, industry, subscription):
    """
    🚀 AI-Generated Social Media Strategy:
    - AI must create content that solves **audience pain points**.
    - AI must use the latest **social media engagement trends**.
    - AI should include **both short-form & long-form content**.
    - AI must integrate **video post ideas** into every calendar.
    - AI should optimize **posting times & engagement strategies**.
    """

    content_plan = []

    if subscription == "Free":
        content_plan.append("📌 Monday: Story-based engagement post")
        content_plan.append("📌 Wednesday: Quote graphic (Brand Identity)")
        content_plan.append("📌 Friday: 'Behind-the-Scenes' short-form video")
        return content_plan

    elif subscription == "Pro":
        content_plan.append("📌 Monday: Brand storytelling post")
        content_plan.append("📌 Tuesday: AI-generated infographic (Industry Insights)")
        content_plan.append("📌 Thursday: AI-written LinkedIn post (Thought Leadership)")
        content_plan.append("📌 Friday: Instagram Reel (Trend-Based)")
        return content_plan

    elif subscription == "Premium":
        content_plan.append("📌 Monday: AI-Generated Customer Testimonial Video")
        content_plan.append("📌 Wednesday: Live Q&A Session (AI Recommends Topics)")
        content_plan.append("📌 Friday: AI-Optimized Paid Ad Campaign (Social & Google)")
        content_plan.append("📌 Sunday: Personal Branding Blog Post (SEO-Optimized)")
        return content_plan

    return ["⚠️ Invalid Subscription Level"]
def run_social_calendar(business_name, industry, subscription, user_email):
    calendar = generate_ai_social_calendar(business_name, industry, subscription)
from fpdf import FPDF
from datetime import datetime
from airtable_connector import save_to_airtable

def run_social_calendar(business_name, industry, subscription, user_email):
    calendar = generate_ai_social_calendar(business_name, industry, subscription)

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
    print(f"PDF Saved: {filename}")

    # Save to Airtable
    save_to_airtable("Social Media Strategy", {
        "User Email": user_email,
        "Business Name": business_name,
        "Industry": industry,
        "Plan": subscription,
        "PDF Filename": filename,
        "Date": datetime.now().isoformat()
    })
if __name__ == "__main__":
    run_social_calendar(
        business_name="CGL Coaching",
        industry="personal branding",
        subscription="Pro",
        user_email="demo@brandvision.com"
    )

   