import os
from dotenv import load_dotenv
from mailjet_rest import Client

# Load environment variables
load_dotenv()
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")

# === SEND SUMMARY EMAIL WITH OPTIONAL PDF ATTACHMENT ===
def send_email_summary(recipient_email, subject, body_text, attachment_path=None):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

    message = {
        "From": {
            "Email": MAILJET_SENDER,
            "Name": "BrandVision Profiler"
        },
        "To": [{
            "Email": recipient_email,
            "Name": "Client"
        }],
        "Subject": subject,
        "TextPart": body_text,
        "HTMLPart": f"<h3>{subject}</h3><p>{body_text.replace(chr(10), '<br>')}</p>"
    }

    if attachment_path:
        with open(attachment_path, "rb") as f:
            content_bytes = f.read()
        import base64
        message["Attachments"] = [{
            "ContentType": "application/pdf",
            "Filename": os.path.basename(attachment_path),
            "Base64Content": base64.b64encode(content_bytes).decode('utf-8')
        }]

    data = {
        'Messages': [message]
    }

    result = mailjet.send.create(data=data)
    print("Email Status:", result.status_code)
    print("Email Response:", result.json())

# === EXAMPLE USAGE ===
# send_email_summary("client@email.com", "Your Branding Report is Ready", "Here's your insight summary...", "emotion_engine_report_test.pdf")
