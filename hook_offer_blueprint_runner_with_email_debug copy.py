from hook_offer_engine import hook_offer_engine
from generate_hook_offer_pdf import generate_hook_offer_pdf
from log_to_airtable import log_to_airtable
from send_blueprint_email import send_blueprint_email
import os

# === USER INPUT SECTION ===
user_email = "BrandVisionprofiler@gmail.com"
user_name = "Confident Creator"
brand = "Confident Coach Club"
topic = "confidence coaching"
user_tier = "Premium"
pdf_file_name = "hook_offer_blueprint.pdf"
pdf_path = os.path.join(os.getcwd(), pdf_file_name)
pdf_url = "https://yourdomain.com/" + pdf_file_name  # Replace this with your actual public URL

# === STEP 1: GENERATE HOOKS + OFFER ===
output = hook_offer_engine(topic, brand)

# === STEP 2: GENERATE PDF ===
generate_hook_offer_pdf(output, pdf_path)

# === STEP 3: LOG TO AIRTABLE ===
log_to_airtable(user_email, brand, topic, output, pdf_url, user_tier)

# === STEP 4: SEND EMAIL WITH BLUEPRINT ===
status, response = send_blueprint_email(user_email, user_name, pdf_url)

print("========== MAILJET DEBUG ==========")
print("Mailjet Status Code:", status)
print("Mailjet Response:", response)
print("====================================")

print("Hook & Offer Blueprint complete!")
print("PDF saved at:", pdf_path)