
import os
from openai import OpenAI
from dotenv import load_dotenv
from generate_tracker_pdf import generate_tracker_pdf
from send_tracker_email import send_tracker_email
from log_tracker_to_airtable import log_tracker_to_airtable

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_monthly_tracker(brand_name, month):
    prompt = f"""
You are a 19-star brand strategist creating a VIP Monthly Tracker report.

Brand: {brand_name}
Month: {month}

Include:
1. Brand voice consistency insights
2. Emotional tone shifts in audience
3. Top performing content formats
4. Hooks/themes to amplify next month
5. Offer positioning or trend-based pivots

Keep it emotionally intelligent, strategic, and easy to act on.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_monthly_brand_tracker(brand_name, month, user_email="demo@brandvision.com"):
    print(f"Running Brand Tracker for: {brand_name} ({month})")
    content = generate_monthly_tracker(brand_name, month)
    pdf_file = generate_tracker_pdf(brand_name, month, content)
    send_tracker_email(user_email, brand_name, pdf_file)
    log_tracker_to_airtable(user_email, brand_name, month, pdf_file)
    print("✅ Tracker complete and sent.")
