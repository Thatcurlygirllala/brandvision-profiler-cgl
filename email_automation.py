import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.your-email-provider.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@example.com"
SMTP_PASSWORD = "your-email-password"

def send_ai_report_email(client_email, report_url):
    """
    Sends an AI-generated branding report via email.
    """
    msg = MIMEMultipart()
    msg["From"] = SMTP_USERNAME
    msg["To"] = client_email
    msg["Subject"] = "🚀 Your AI Branding Report is Ready!"

    body = f"""
    Hi there,

    Your AI-powered branding report is ready! 🎉 Click below to download:

    🔗 {report_url}

    If you have any questions, let us know.

    🚀 Upgrade to Premium for advanced AI branding insights!

    Best,
    The BrandVision AI Team
    """

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, client_email, msg.as_string())

    return "✅ Email Sent Successfully!"
