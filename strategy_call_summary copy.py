
import os
import base64
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv
from mailjet_rest import Client
from pyairtable import Table
import openai

# === Load Environment Variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("BASE_ID")
AIRTABLE_TABLE_NAME = "AI Reports Table"

# === Clean text for PDF ===
def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "→": "->", "✓": "-",
        "•": "-", "…": "...", "©": "(c)", "🌟": "*"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# === AI Summary Generator ===
def generate_call_summary(data):
    prompt = f"""
You are a premium brand strategy AI assistant helping a coach prepare for a 1-on-1 session.

Client Info:
Name: {data['user_name']}
Email: {data['user_email']}
Business: {data.get('business_name', 'N/A')}
Challenge: {data['challenge']}
Goal: {data['goal']}
Experience: {data['experience']}
Platforms: {data['platforms']}
Session: {data['session_type']}
Interested In: {data['interests']}

Instructions:
1. Summarize their core struggle.
2. Identify what they actually need.
3. Recommend a BrandVision Profiler path (tool, bundle, or coaching).
4. Score their brand confidence or clarity (1–100).
5. Suggest CTA language and emotional hooks.
6. Give the coach 3 smart talking points to use.

Make it sound like a real coach wrote it.
    """
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8
    )
    return response.choices[0].message.content

# === PDF Generator ===
def create_pdf(data, ai_summary):
    filename = f"strategy_summary_{data['user_name'].split()[0].lower()}_{data['user_email'].split('@')[0].lower()}_{data['session_type'].replace(' ', '').lower()}_{datetime.now().strftime('%Y%m%d')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    # Cover Page
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Strategy Call Summary", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, clean_text(f"{data['user_name']} | {data['session_type']} | {datetime.now().strftime('%Y-%m-%d')}"), ln=True, align="C")
    pdf.ln(10)

    # What the client shared
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "What the client shared:", ln=True)
    pdf.set_font("Arial", "", 12)
    for key in ['challenge', 'goal', 'experience', 'platforms', 'interests']:
        label = key.replace("_", " ").title()
        pdf.multi_cell(0, 10, clean_text(f"{label}: {data[key]}"))
        pdf.ln(2)

    # AI Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Coaching Summary:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(ai_summary))

    # Call Prep Box
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Call Prep Box", ln=True)
    pdf.set_font("Arial", "", 12)
    prep = (
        "• Ask: “What’s keeping you stuck right now?”\n"
        "• Reframe: “What I’m seeing is actually a clarity & consistency issue — not a content one.”\n"
        "• Show: “Let me screen share how the BrandVision Profiler pinpoints that in under 5 minutes.”\n"
        "• CTA: “I’ve got 2 solid paths for you depending on your pace and budget…”"
    )
    pdf.multi_cell(0, 10, clean_text(prep))

    pdf.output(filename)
    return filename

# === Email to Coach ===
def send_email_to_coach(pdf_file, coach_email, client_name):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY))
    with open(pdf_file, "rb") as file:
        pdf_data = file.read()
    data = {
        'Messages': [{
            "From": {
                "Email": MAILJET_SENDER,
                "Name": "BrandVision Profiler"
            },
            "To": [{"Email": coach_email}],
            "Subject": f"Strategy Call Summary: {client_name}",
            "TextPart": "New strategy call PDF attached.",
            "HTMLPart": f"<h3>Prep for your call with {client_name}</h3><p>PDF summary is attached below.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }
    result = mailjet.send.create(data=data)
    print("Email sent to coach:", result.status_code)

# === Airtable Logging ===
def log_to_airtable(data, pdf_file):
    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    fields = {
        "User Email": data['user_email'],
        "Client Name": data['user_name'],
        "Business Name": data.get('business_name', ''),
        "Challenge": data['challenge'],
        "Goal": data['goal'],
        "Session Type": data['session_type'],
        "Plan Interest": data['interests'],
        "PDF Filename": pdf_file,
        "Date": datetime.now().strftime('%Y-%m-%d')
    }
    table.create(fields)
    print("Logged to Airtable")

# === Main Runner ===
def run_strategy_call_summary(data):
    print(f"Generating strategy call summary for: {data['user_name']}")
    summary = generate_call_summary(data)
    pdf_file = create_pdf(data, summary)
    log_to_airtable(data, pdf_file)
    send_email_to_coach(pdf_file, "brandvisionprofiler@gmail.com", data['user_name'])
    print("✅ Strategy Call Summary complete.")

# === Sample Usage ===
if __name__ == "__main__":
    sample_data = {
        "user_name": "Jane Doe",
        "user_email": "jane@example.com",
        "business_name": "GlowUp Coaching",
        "challenge": "I post consistently but no one converts.",
        "goal": "Land 3 high-ticket clients in the next 60 days.",
        "experience": "Tried coaching but felt generic. Took courses that didn’t help much.",
        "platforms": "Instagram, Email",
        "interests": "Coaching, App, Possibly White Label",
        "session_type": "30-Min Strategy Call"
    }
    run_strategy_call_summary(sample_data)