import smtplib
from email.message import EmailMessage
import os
from datetime import datetime
from fpdf import FPDF  # Ensure fpdf is installed: pip install fpdf

def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(filename)

def send_email_with_attachment(recipient_email, subject, body, attachment_path):
    sender_email = os.getenv("EMAIL_ADDRESS")
    app_password = os.getenv("EMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        raise ValueError("Email credentials are not set in environment variables.")

    # Create the email message
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = subject
    message.set_content(body)

    # Attach the PDF file
    with open(attachment_path, "rb") as file:
        file_data = file.read()
        file_name = os.path.basename(attachment_path)
        message.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Send the email via Gmail's SMTP server
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(message)

if __name__ == "__main__":
    # Generate PDF
    offer_title = "Emotional Marketing Mastery"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    pdf_filename = f"offer_summary_{timestamp}.pdf"
    pdf_content = f"Offer Title: {offer_title}\n\nThis is the AI-generated summary content."
    generate_pdf(pdf_content, pdf_filename)

    # Send email
    recipient = "recipient@example.com"  # Replace with the actual recipient's email
    email_subject = f"Your Offer Summary: {offer_title}"
    email_body = "Please find attached your offer summary PDF."
    send_email_with_attachment(recipient, email_subject, email_body, pdf_filename)

    print(f"Email sent to {recipient} with attachment {pdf_filename}")