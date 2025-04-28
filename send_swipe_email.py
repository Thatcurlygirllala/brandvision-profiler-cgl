
import os
import base64
from mailjet_rest import Client

def send_email_with_pdf(pdf_file, recipient_email, emotion_tone, niche):
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
            "Subject": f"Swipe Copy Generator Results – {niche.title()} | {emotion_tone}",
            "TextPart": "Your personalized swipe copy report is ready.",
            "HTMLPart": f"""
                <h3>Your swipe copy report is attached</h3>
                <p>You've selected the <strong>{emotion_tone}</strong> tone for your <strong>{niche}</strong> niche.</p>
                <p>Use this copy to boost your social media, emails, and brand messaging immediately.</p>
                <p><a href='https://brandvisionprofiler.com/checkout?bundle=power149'>Unlock More with the AI Power Bundle</a></p>
            """,
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }

    result = mailjet.send.create(data=data)
    print("Email sent:", result.status_code)
