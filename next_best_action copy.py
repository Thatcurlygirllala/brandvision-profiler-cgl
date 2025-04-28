import os
from dotenv import load_dotenv
from fpdf import FPDF
from datetime import datetime
from pyairtable import Api
from openai import OpenAI

# === Load .env variables ===
load_dotenv()

# === Airtable Config ===
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")  # or just use "AI Reports"

# === OpenAI Config ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# === Airtable Init ===
api = Api(AIRTABLE_API_KEY)
table = api.table(BASE_ID, TABLE_NAME)

# === Fetch latest record (no sort fallback) ===
records = table.all(max_records=1)
latest = records[0]['fields'] if records else {}

# === Extract fields ===
user_name = latest.get("Name", "Visionary")
last_tool_used = latest.get("Last Tool Used", "Swipe Copy Generator")
subscription_tier = latest.get("Subscription Plan", "Free")
emotion_tag = latest.get("Emotion Tag", "motivated")
pdf_needed = latest.get("Generate PDF?", True)

# === Prompt the AI Strategist ===
def generate_next_step(user_name, tool, tier, emotion):
    prompt = f"""
You are a branding strategist. The user is {user_name}, who just used the {tool}.
They are on the {tier} plan and their audience feels {emotion}.

Give 3 personalized, high-impact recommendations:
1. Their smartest next move inside the BrandVision Profiler
2. One bundle or tool that would accelerate progress (e.g., Power Bundle)
3. A confidence-building CTA
Keep the tone warm, strategic, and inspiring.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a master branding strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.75
    )
    return response.choices[0].message.content

# === PDF Generator ===
def create_pdf(content, username):
    import unicodedata

    def clean_text(text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Your Next Best Move", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"For: {username}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    for line in content.split("\n"):
        pdf.multi_cell(0, 10, txt=clean_text(line))

    file_path = f"{username}_Next_Steps.pdf"
    pdf.output(file_path)
    return file_path

# === Run It All ===
next_step_text = generate_next_step(user_name, last_tool_used, subscription_tier, emotion_tag)
print("\n--- YOUR NEXT BEST MOVE ---\n")
print(next_step_text)

pdf_path = None
if pdf_needed:
    pdf_path = create_pdf(next_step_text, user_name)
    print(f"\nPDF saved as: {pdf_path}")

# === Log it back to Airtable ===
log_data = {
    "Name": user_name,
    "Triggered From Tool": last_tool_used,
    "Subscription Plan": subscription_tier,
    "Emotion Tag": emotion_tag,
    "Suggested Next Step": next_step_text,
    "PDF Generated?": pdf_needed
}
table.create(log_data)
from send_email_mailjet import send_pdf_email

# Optional: replace with real email field from Airtable later
recipient_email = "brandvisionprofiler@gmail.com"

# Send email if PDF was created
if pdf_path:
    send_pdf_email(recipient_email, user_name, pdf_path)