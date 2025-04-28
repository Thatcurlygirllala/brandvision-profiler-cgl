import os
import openai
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from airtable_connector import save_to_airtable
from mailjet_rest import Client
import base64

# === Load Environment Variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Tone Modeling Examples ===
TONE_EXAMPLES = {
    "Empowering": "You’re one decision away from your next level.",
    "Uplifting": "Here’s your sign that things are turning around.",
    "Bold & Confident": "This offer isn’t for everyone — and that’s the point.",
    "Relatable & Real": "Let’s be honest… it’s hard AF running a biz and being a mom.",
    "Urgent & Action-Driven": "Waiting is costing you money — here’s proof.",
    "Playful & Fun": "POV: You turned your personality into profit.",
    "Calm & Reassuring": "Let’s take the pressure off your next launch.",
    "FOMO-Driven": "Everyone’s talking about this. You’ll wish you saw it sooner.",
    "Inspiring & Visionary": "You weren’t born to blend in — build the brand they’ll remember.",
    "Supportive & Nurturing": "You deserve strategy that supports your nervous system.",
    "Disruptive & Provocative": "If your content isn’t shaking the room, you’re missing sales.",
    "Luxury & Elevated": "This isn’t just strategy — it’s brand elegance.",
    "Grounded & Honest": "Not flashy. Just proven.",
    "Transformational": "Get ready to meet the version of you who leads and wins.",
    "Curious & Thought-Provoking": "What if your audience isn’t ghosting you — they’re just confused?"
}

# === Clean text for PDF ===
def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "→": "->", "✓": "-",
        "•": "-", "…": "...", "©": "(c)"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

# === Generate Swipe Copy ===
def generate_swipe_copy(niche, audience, offer, emotion_tone, plan_tier):
    tone_sample = TONE_EXAMPLES.get(emotion_tone, "")

    prompt = f"""
You are a world-class copywriter trained in brand psychology and emotional marketing.

Create high-converting swipe copy for a brand in the "{niche}" niche targeting "{audience}".
The offer is: "{offer}"
The emotional tone is: "{emotion_tone}".

Use a voice and vibe that reflects this tone. Match the energy of this sample:
"{tone_sample}"

Return:
1. 5 Reels/TikTok Hooks
2. 5 CTA Phrases
3. 3 Instagram Bio Line Options
4. 5 Email Subject Lines

The style should match the selected tone and be tailored for a {plan_tier} tier user.
Make it scroll-stopping, emotionally intelligent, and ready to use.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )

    return response["choices"][0]["message"]["content"]

# === Create PDF ===
def create_swipe_copy_pdf(user_name, niche, emotion_tone, swipe_text):
    filename = f"swipe_copy_{user_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Swipe Copy Generator", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Niche: {niche} | Tone: {emotion_tone} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for section in swipe_text.split("\n"):
        pdf.multi_cell(0, 10, clean_text(section))

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(
        "You're now equipped with high-converting swipe copy.\n\n"
        "✓ Book your Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "✓ Unlock advanced content tools in the Power Bundle:\n"
        "https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    pdf.output(filename)
    return filename

# === Send Email with PDF ===
def send_email_with_pdf(pdf_file, recipient_email, emotion_tone, niche):
    mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_SECRET_KEY")))
    with open(pdf_file, "rb") as file:
        pdf_data = file.read()

    data = {
        'Messages': [{
            "From": {
                "Email": os.getenv("MAILJET_SENDER"),
                "Name": "BrandVision Profiler"
            },
            "To": [{"Email": recipient_email}],
            "Subject": f"Swipe Copy Generator Results – {niche.title()} | {emotion_tone}",
            "TextPart": "Your personalized swipe copy report is ready.",
            "HTMLPart": f"""
                <h3>Your swipe copy report is attached</h3>
                <p>You've selected the <strong>{emotion_tone}</strong> tone for your <strong>{niche}</strong> niche.</p>
                <p>Use this copy to boost your social media, emails, and brand messaging immediately.</p>
                <p><a href='https://brandvisionprofiler.com/checkout?bundle=power149'>Unlock More with the AI Power Bundle</a></p>
            """,
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }

    result = mailjet.send.create(data=data)
    print("Email sent:", result.status_code)

# === Airtable Logger ===
def log_swipe_copy_to_airtable(user_email, niche, audience, offer, emotion, plan, result, pdf_file):
    save_to_airtable("Swipe Copy Logs", {
        "User Email": user_email,
        "Niche": niche,
        "Audience": audience,
        "Offer": offer,
        "Emotion Tone": emotion,
        "Plan Tier": plan,
        "Generated Copy": result,
        "PDF Filename": pdf_file,
        "Timestamp": datetime.now().isoformat()
    })

# === Test Runner ===
if __name__ == "__main__":
    user_email = "demo@brandvision.com"
    niche = "wellness coaching"
    audience = "moms balancing business and burnout"
    offer = "90-day transformation program"
    emotion_tone = "Empowering"
    plan_tier = "Premium"

    print("Generating swipe copy...")
    result = generate_swipe_copy(niche, audience, offer, emotion_tone, plan_tier)

    print("Generating PDF...")
    pdf_file = create_swipe_copy_pdf("LaLa", niche, emotion_tone, result)

    print("Logging to Airtable...")
    log_swipe_copy_to_airtable(user_email, niche, audience, offer, emotion_tone, plan_tier, result, pdf_file)

    print("Sending email with attachment...")
    send_email_with_pdf(pdf_file, user_email, emotion_tone, niche)

    print("✅ Swipe copy generated, saved, logged, and emailed successfully.")