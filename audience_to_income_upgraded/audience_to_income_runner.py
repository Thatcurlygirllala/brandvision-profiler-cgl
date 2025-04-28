
from audience_to_income_engine import generate_income_blueprint
from generate_income_pdf import create_income_pdf
from send_income_email import send_email_with_attachment
from log_income_to_airtable import log_income_blueprint_to_airtable

def run_audience_to_income_blueprint(audience_description, user_strength="writing", user_email="demo@brandvision.com"):
    print(f"Generating 19-star Monetization Blueprint for: {audience_description}")
    summary = generate_income_blueprint(audience_description, user_strength)
    filename = create_income_pdf(summary, audience_description)
    log_income_blueprint_to_airtable(user_email, audience_description)

    email_subject = "Your Monetization Blueprint is Ready!"
    email_body = (
        f"Hi there,\n\nYour personalized Audience-to-Income Blueprint is ready.\n"
        f"Use it to launch confidently and convert your audience.\n\n"
        f"Book your strategy call here: https://calendly.com/curlygirllala/30-minute-strategy-call\n\n"
        f"– Team BrandVision Profiler"
    )
    send_email_with_attachment(user_email, email_subject, email_body, filename)
    print("✅ All steps completed successfully.")

if __name__ == "__main__":
    run_audience_to_income_blueprint(
        audience_description="People love my content but I don’t know what to sell",
        user_strength="speaking",
        user_email="demo@brandvision.com"
    )
