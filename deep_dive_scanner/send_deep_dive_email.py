
import os
import base64
from mailjet_rest import Client

def send_deep_dive_email(pdf_file, recipient_email, keyword):
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
            "Subject": f"Audience Intelligence Report – {keyword}",
            "TextPart": "Your Reddit + Quora insights are ready.",
            "HTMLPart": f"<h3>Your Deep Dive Scanner Report is ready for <b>{keyword}</b></h3><p>See attached PDF for trends, hooks, and monetization insights.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }

    result = mailjet.send.create(data=data)
    print("Email sent:", result.status_code)
