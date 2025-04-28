import os
from dotenv import load_dotenv
import requests
import base64

# Load environment variables
load_dotenv()

# Mailjet Config
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")  # Your Gmail: brandvisionprofiler@gmail.com

# === Email Settings ===
def send_pdf_email(to_email, to_name, pdf_path):
    subject = "Your Personalized Strategy Report – BrandVision Profiler"
    text_part = f"Hi {to_name},\n\nAttached is your Next Best Move strategy report from BrandVision Profiler.\nUse this to keep your momentum strong and aligned with your audience’s motivation."
    html_part = f"""
    <h3>Hi {to_name},</h3>
    <p>Your personalized strategy PDF is attached. It includes insights, tool recommendations, and a CTA to help you take your brand to the next level.</p>
    <p>Stay inspired and strategic!</p>
    <p>— The BrandVision Profiler Team</p>
    """

    # Read and encode PDF
    with open(pdf_path, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode()

    # Mailjet API endpoint
    url = "https://api.mailjet.com/v3.1/send"
    payload = {
        "Messages": [
            {
                "From": {
                    "Email": MAILJET_SENDER,
                    "Name": "BrandVision Profiler"
                },
                "To": [
                    {
                        "Email": to_email,
                        "Name": to_name
                    }
                ],
                "Subject": subject,
                "TextPart": text_part,
                "HTMLPart": html_part,
                "Attachments": [
                    {
                        "ContentType": "application/pdf",
                        "Filename": os.path.basename(pdf_path),
                        "Base64Content": encoded_file
                    }
                ]
            }
        ]
    }

    # Send request
    response = requests.post(
        url,
        auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
        json=payload
    )

    if response.status_code == 200:
        print(f"Email sent to {to_email} with PDF attached.")
    else:
        print(f"Failed to send email: {response.status_code}")
        print(response.text)