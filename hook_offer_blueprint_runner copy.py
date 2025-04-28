
from hook_offer_engine import hook_offer_engine
from generate_hook_offer_pdf import generate_hook_offer_pdf
from log_to_airtable import log_to_airtable
import os

# === USER INPUT SECTION ===
user_email = "user@example.com"
brand = "Confident Coach Club"
topic = "confidence coaching"
user_tier = "Premium"
pdf_file_name = "hook_offer_blueprint.pdf"
pdf_path = os.path.join(os.getcwd(), pdf_file_name)
pdf_url = "https://example.com/" + pdf_file_name  # Replace this with your actual hosted link if needed

# === STEP 1: GENERATE HOOKS + OFFER ===
output = hook_offer_engine(topic, brand)

# === STEP 2: GENERATE PDF ===
generate_hook_offer_pdf(output, pdf_path)

# === STEP 3: LOG TO AIRTABLE ===
log_to_airtable(user_email, brand, topic, output, pdf_url, user_tier)

print("Hook & Offer Blueprint complete!")
print("PDF saved at:", pdf_path)