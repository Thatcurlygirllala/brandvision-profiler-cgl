import os
import openai
import praw
import requests
import base64
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
from mailjet_rest import Client
from transformers import pipeline

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Reddit API config
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# Emotion classifier
emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)

def fetch_reddit_posts(keyword):
    posts = []
    try:
        for submission in reddit.subreddit("all").search(keyword, limit=10):
            posts.append(submission.title + " " + submission.selftext)
    except Exception as e:
        print("Reddit fetch error:", e)
    return posts

def analyze_emotions(text):
    results = emotion_clf(text)
    return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])

def summarize_for_marketing(posts, keyword):
    condensed_insights = "\n".join(posts[:5])
    prompt = f"""
You are a Brand Marketing AI Assistant.

Summarize and feed the Reddit insights below into a marketing strategy brief. Include:

1. Emotional trends (frustration, excitement, skepticism, motivation, etc.)
2. Voice of customer â direct quotes or patterns that marketers can respond to
3. Purchase intent signals (hesitation, curiosity, urgency)
4. Offer ideas and high-converting content hooks
5. Validation across platforms (Google Trends, TikTok, Twitter) if mentioned

Keyword: {keyword}

Reddit Posts:
{condensed_insights}
"""
    client = openai.OpenAI()
    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_response.choices[0].message.content

def create_pdf_report(summary, keyword, hooks):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Emotion-Driven Reddit Report", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Keyword: {keyword} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, summary)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Voice of Customer & Suggested Hooks", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, hooks)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your Next Step", ln=True)
    pdf.set_font("Arial", "", 12)
    cta = (
        "Youâve just uncovered what your audience is really feeling. Now, act on it:\n\n"
        "1. Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "2. Get the Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    )
    pdf.multi_cell(0, 10, cta)

    filename = f"reddit_emotion_report_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def send_email_with_pdf(pdf_file, recipient_email, keyword):
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
            "Subject": f"Voice of Customer & Market Hook Report: {keyword}",
            "TextPart": "Your emotional marketing report is ready.",
            "HTMLPart": f"<h3>Your Reddit + Emotion Trend Report for <b>{keyword}</b> is ready!</h3><p>PDF attached for marketing strategy insights.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }
    result = mailjet.send.create(data=data)
    print("Email sent:", result.status_code)

def log_to_airtable(user_email, keyword, filename):
    airtable_url = f"https://api.airtable.com/v0/{os.getenv('BASE_ID')}/RedditScannerLogs"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIRTABLE_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "fields": {
            "User_ID": user_email,
            "Keyword": keyword,
            "Timestamp": datetime.now().isoformat(),
            "PDF_File_Name": filename
        }
    }
    response = requests.post(airtable_url, headers=headers, json=data)
    print("Airtable log status:", response.status_code)

def run_enhanced_reddit_scanner(keyword, user_email):
    print(f"Running Enhanced Reddit Scanner for: {keyword}")
    posts = fetch_reddit_posts(keyword)
    if not posts:
        print("No Reddit posts found.")
        return

    emotion_analysis = analyze_emotions(" ".join(posts[:3]))
    print("Detected Emotions:", emotion_analysis)

    ai_summary = summarize_for_marketing(posts, keyword)
    hooks = "\n\n[Marketing Suggestions & Hooks]\n" + "\n".join([line for line in ai_summary.split("\n") if "Hook" in line or "â¢" in line])

    pdf_filename = create_pdf_report(ai_summary, keyword, hooks)
    send_email_with_pdf(pdf_filename, user_email, keyword)
    log_to_airtable(user_email, keyword, pdf_filename)
    print(f"Enhanced Reddit + Emotion report sent and logged for: {keyword}")