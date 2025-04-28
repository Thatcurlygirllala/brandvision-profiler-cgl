
from swipe_engine import generate_swipe_copy
from generate_swipe_pdf import create_swipe_copy_pdf
from log_swipe_copy_to_airtable import log_swipe_copy_to_airtable
from send_swipe_email import send_email_with_pdf

if __name__ == "__main__":
    user_email = "demo@brandvision.com"
    user_name = "LaLa"
    niche = "wellness coaching"
    audience = "moms balancing business and burnout"
    offer = "90-day transformation program"
    emotion_tone = "Empowering"
    plan_tier = "Premium"

    print("Generating swipe copy...")
    result = generate_swipe_copy(niche, audience, offer, emotion_tone, plan_tier)

    print("Generating PDF...")
    pdf_file = create_swipe_copy_pdf(user_name, niche, emotion_tone, result)

    print("Logging to Airtable...")
    log_swipe_copy_to_airtable(user_email, niche, audience, offer, emotion_tone, plan_tier, result, pdf_file)

    print("Sending email with attachment...")
    send_email_with_pdf(pdf_file, user_email, emotion_tone, niche)

    print("✅ Swipe copy generated, saved, logged, and emailed successfully.")
