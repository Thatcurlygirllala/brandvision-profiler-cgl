
from datetime import datetime
from airtable_connector import save_to_airtable  # Make sure this exists or alias it to pyairtable if needed

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
