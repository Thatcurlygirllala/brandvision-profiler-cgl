
import os
from mailjet_rest import Client
import base64

def send_email(to_email, keyword, pdf_file):
    mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_SECRET_KEY")))
    with open(pdf_file, "rb") as file:
        data = file.read()
    result = mailjet.send.create(data={
        'Messages': [{
            "From": {"Email": os.getenv("MAILJET_SENDER"), "Name": "BrandVision Profiler"},
            "To": [{"Email": to_email}],
            "Subject": f"Your Trend Domination Report: {keyword}",
            "TextPart": "Your trend report is ready.",
            "HTMLPart": f"<h3>{keyword}: Strategic trend report attached.</h3>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(data).decode()
            }]
        }]
    })
    print("Email status:", result.status_code)
