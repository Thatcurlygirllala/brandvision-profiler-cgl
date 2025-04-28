
from log_to_airtable import log_to_airtable

output = {
    "hooks": ["You don’t need a big audience to sell.", "Start with clarity, not perfection."],
    "ctas": ["DM me ‘READY’", "Click link in bio to launch"],
    "bio_line": "Helping coaches convert clarity into clients.",
    "offer_name": "Confidence Coaching Starter Kit",
    "offer_description": "Your first offer, launched fast. Simple. Strategic. Stress-free.",
    "price": "$47",
    "delivery_method": "PDF + Video Call",
    "confidence_score": "Medium – Curious but hesitant",
    "time_to_build": "Quick – Can launch in 1–2 days"
}

user_email = "user@example.com"
brand = "Confident Coach Club"
topic = "confidence coaching"
pdf_url = "https://example.com/hook-offer.pdf"
user_tier = "Premium"

log_to_airtable(user_email, brand, topic, output, pdf_url, user_tier)
