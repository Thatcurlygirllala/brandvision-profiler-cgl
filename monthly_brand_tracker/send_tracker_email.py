
import os
from mailjet_rest import Client
import base64

def send_tracker_email(to_email, brand_name, pdf_file):
    mailjet = Client(auth=(os.getenv("MAILJET_API_KEY"), os.getenv("MAILJET_SECRET_KEY")))
    with open(pdf_file, "rb") as file:
        pdf_data = file.read()

    data = {
        'Messages': [{
            "From": {"Email": os.getenv("MAILJET_SENDER"), "Name": "BrandVision Profiler"},
            "To": [{"Email": to_email}],
            "Subject": f"Monthly Brand Tracker – {brand_name}",
            "TextPart": "Your VIP strategy report is here.",
            "HTMLPart": f"<h3>{brand_name}: Monthly Report</h3><p>See attached insights + CTA plan.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }
    result = mailjet.send.create(data=data)
    print("Email status:", result.status_code)
