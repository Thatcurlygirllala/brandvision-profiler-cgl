import os
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF
import openai
from airtable_connector import save_to_airtable
from transformers import pipeline

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load emotion classifier
emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)

# === MOCKED TWEETS FUNCTION (Replace with API when live) ===
def fetch_tweets(keyword, limit=100):
    return [
        f"{keyword} is amazing. I'm so ready to start!",
        f"Not sure if {keyword} is even legit anymore...",
        f"I'm overwhelmed with all these options!",
        f"{keyword} looks promising. Thinking about it.",
        f"Why does {keyword} sound like a scam?"
    ]

# === ADVANCED EMOTION CLASSIFIER ===
def classify_emotions_ai(tweets):
    combined_text = " ".join(tweets)
    result = emotion_clf(combined_text)
    return ", ".join([f"{r['label']} ({round(r['score'], 2)})" for r in result[0]])

# === AI INSIGHT GENERATOR ===
def generate_emotion_report(emotion_summary, keyword):
    prompt = f"""
You are an elite AI Branding Strategist.

Audience Sentiment about '{keyword}':
{emotion_summary}

Generate:
1. Emotional trends summary
2. Top 3 audience fears, frustrations, or hopes
3. Voice-of-customer quotes or phrases to reuse
4. 5 emotionally intelligent marketing hooks
5. One bold CTA or campaign move

Make this strategic and emotionally smart.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message["content"]

# === PDF REPORT GENERATOR ===
def generate_emotion_pdf(summary, keyword):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "BrandVision Profiler: Emotion Engine Report", ln=True, align="C")
    pdf.set_font("Arial", "I", 11)
    pdf.cell(0, 10, f"Keyword: {keyword} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, summary)

    filename = f"emotion_engine_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# === MAIN FUNCTION ===
def run_emotion_engine(keyword, user_email):
    tweets = fetch_tweets(keyword)
    emotion_summary = classify_emotions_ai(tweets)
    branding_summary = generate_emotion_report(emotion_summary, keyword)
    pdf_file = generate_emotion_pdf(branding_summary, keyword)

    save_to_airtable("Emotion Engine Logs", {
        "User Email": user_email,
        "Keyword/Handle": keyword,
        "Detected Emotions": emotion_summary,
        "AI Summary": branding_summary,
        "PDF Filename": pdf_file
    })

    print(f"✅ Emotion Engine completed for '{keyword}'. PDF saved as: {pdf_file}")