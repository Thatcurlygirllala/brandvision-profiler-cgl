import os
from mailjet_rest import Client

# Load credentials
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")  # e.g. brandvisionprofiler@gmail.com
EMAIL_TO = os.getenv("EMAIL_ADDRESS")         # or dynamic per user

# Attach the last generated file
PDF_FILE_PATH = "Visionary_Next_Steps.pdf"

# Set up Mailjet client
mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')

# Compose the message
data = {
    'Messages': [
        {
            "From": {
                "Email": MAILJET_SENDER,
                "Name": "BrandVision Profiler"
            },
            "To": [
                {
                    "Email": EMAIL_TO,
                    "Name": "Visionary"
                }
            ],
            "Subject": "Your AI Branding Strategy: Next Best Move",
            "TextPart": "Your personalized next-step branding strategy is attached as a PDF.",
            "Attachments": [
                {
                    "ContentType": "application/pdf",
                    "Filename": "Visionary_Next_Steps.pdf",
                    "Base64Content": open(PDF_FILE_PATH, "rb").read().encode("base64").decode("utf-8")
                }
            ]
        }
    ]
}

# Send the email
result = mailjet.send.create(data=data)
print(result.status_code)
print(result.json())
