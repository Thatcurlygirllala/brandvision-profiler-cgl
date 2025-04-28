import os
import requests
from dotenv import load_dotenv
import openai
import praw
from fpdf import FPDF
from mailjet_rest import Client
from datetime import datetime
import base64

# Load environment variables
load_dotenv()

# Airtable config
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("BASE_ID")
TABLE_NAME = os.getenv("AIRTABLE_TABLE_NAME")

# OpenAI config
openai.api_key = os.getenv("OPENAI_API_KEY")

# Mailjet config
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")

def fetch_reddit_posts(keyword):
    reddit = praw.Reddit(
        client_id="Df6fq7wtVBfL1qFgGJDg7A",
        client_secret="nKu6BLrK5EmNLtxqX07sM0Cc58pXbQ",
        user_agent="BrandVisionProfiler/1.0 by Illustrious-Fan4108"
    )
    posts = []
    try:
        for submission in reddit.subreddit("all").search(keyword, limit=10):
            posts.append(f"Title: {submission.title}\n{submission.selftext}\n")
    except Exception as e:
        print("Reddit fetch error:", e)
    return posts

def summarize_with_openai(posts, keyword):
    prompt = f"Summarize key emotional pain points and trends from these Reddit posts about '{keyword}':\n\n" + "\n".join(posts)
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI summary error:", e)
        return "Summary generation failed."

def generate_ai_hooks(summary, keyword):
    hook_prompt = f"Based on this Reddit summary about '{keyword}', generate 3 emotional, high-converting social media hooks and 1 CTA idea:\n\n{summary}"
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": hook_prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print("OpenAI hook generation error:", e)
        return "Hook generation failed."

def create_pdf_report(summary, keyword, hooks):
    def safe_text(text):
        return text.encode("latin-1", "replace").decode("latin-1")

    pdf = FPDF()

    # Cover Page
    pdf.add_page()
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 20, "Reddit Trend + Hook Report", ln=True, align="C")
    pdf.set_font("Arial", '', 14)
    pdf.cell(0, 10, f"Keyword: {keyword}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", 'I', 12)
    pdf.multi_cell(0, 10, "Real audience pain points + AI-powered marketing hooks")
    pdf.ln(20)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Powered by BrandVision Profiler by CGL", ln=True, align="C")
    pdf.cell(0, 10, "www.brandvisionprofiler.com", ln=True, align="C")

    # Reddit Summary Section
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "What Your Audience Is Feeling Right Now", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, safe_text(summary))

    # Hook Ideas Section
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Social Media Hook Ideas to Grab Attention", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, safe_text(hooks))

    # Save PDF
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"reddit_report_{keyword}_{timestamp}.pdf"
    pdf.output(filename)
    return filename

def send_report_via_mailjet(recipient_email, subject, body, filename):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY), version='v3.1')
    with open(filename, "rb") as f:
        encoded_file = base64.b64encode(f.read()).decode("utf-8")

    data = {
        'Messages': [
            {
                "From": {"Email": MAILJET_SENDER, "Name": "BrandVision"},
                "To": [{"Email": recipient_email}],
                "Subject": subject,
                "TextPart": body,
                "Attachments": [
                    {
                        "ContentType": "application/pdf",
                        "Filename": filename,
                        "Base64Content": encoded_file
                    }
                ]
            }
        ]
    }

    result = mailjet.send.create(data=data)
    return result.status_code, result.json()

def log_to_airtable(user_id, keyword):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}", "Content-Type": "application/json"}
    data = {
        "fields": {
            "User_ID": user_id,
            "Keyword": keyword,
            "Timestamp": datetime.utcnow().isoformat()
        }
    }
    requests.post(url, headers=headers, json=data)

def run_reddit_scanner(keyword, user_email="demo@brandvision.com"):
    posts = fetch_reddit_posts(keyword)
    if not posts:
        print("No Reddit posts found.")
        return
    summary = summarize_with_openai(posts, keyword)
    hooks = generate_ai_hooks(summary, keyword)
    filename = create_pdf_report(summary, keyword, hooks)
    subject = f"Reddit Trend Report: {keyword}"
    body = f"Hi! Here's your Reddit Trend + Hook Report on '{keyword}'."
    send_report_via_mailjet(user_email, subject, body, filename)
    log_to_airtable(user_email, keyword)
    print(f"Reddit + Hook report sent and logged for: {keyword}")

# Example run
if __name__ == "__main__":
    run_reddit_scanner("burnout recovery", user_email="demo@brandvision.com")
