from mailjet_rest import Client

def send_blueprint_email(to_email, user_name, pdf_url):
    api_key = "ea441fc03cefe23b025427e0a0f7cd34"
    api_secret ="0e59a76e5d9f02d5358f9753d75a0d8b"
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')

    subject = "Your Hook & Offer Blueprint is Ready!"
    sender_email = "BrandVisionprofiler@gmail.com"
    sender_name = "BrandVision Profiler"
    reply_to = "BrandVisionprofiler@gmail.com"

    message = f"""
    <h2 style="font-family: sans-serif;">Hi {user_name},</h2>
    <p style="font-family: sans-serif;">
        Your personalized <strong>Hook & Offer Blueprint</strong> has been generated.
    </p>
    <p>
        <a href="{pdf_url}" style="background-color: #5C5C58; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
            Download Your Blueprint
        </a>
    </p>
    <br/>
    <p style="font-family: sans-serif;">
        Ready to launch with more firepower? 
        <a href="https://brandvisionprofiler.com/swipe-vault">Unlock the Swipe Vault</a> or 
        <a href="https://calendly.com/curlygirllala/30-minute-strategy-call">Book a Strategy Call</a>.
    </p>
    <p style="font-family: sans-serif; font-size: 12px; color: gray;">
        Sent by BrandVision Profiler | This email was generated automatically.
    </p>
    """

    data = {
      'Messages': [
        {
          "From": {
            "Email": sender_email,
            "Name": sender_name
          },
          "To": [
            {
              "Email": to_email,
              "Name": user_name
            }
          ],
          "Subject": subject,
          "TextPart": "Your Hook & Offer Blueprint is ready. Click to download.",
          "HTMLPart": message,
          "ReplyTo": {
            "Email": reply_to,
            "Name": sender_name
          }
        }
      ]
    }

    result = mailjet.send.create(data=data)
    return result.status_code, result.json()
