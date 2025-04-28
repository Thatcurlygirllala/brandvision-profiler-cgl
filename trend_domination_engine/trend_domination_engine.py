
import os
from datetime import datetime
from openai import OpenAI
from analyze_emotion import analyze_emotion
from generate_trend_pdf import create_trend_pdf
from send_email_trend import send_email
from log_to_airtable_trend import log_to_airtable
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_trend_insights(keyword, platform="multi"):
    prompt = f"""
You are a multi-platform trend analyst trained in branding psychology, cultural signals, and audience behavior.

Keyword: {keyword}
Platform: {platform}

Provide a TrendSync Market Report that includes:
1. Emotional tone trends (skepticism, motivation, hype, urgency, burnout)
2. Cultural & psychological hooks driving this topic
3. Top emotional keywords from conversations
4. Where in the trend lifecycle this sits: rising, peaking, fading?
5. Strategic content moves brands can make
6. CTA-ready hooks or phrases
7. Prediction: What audiences are leaning into this?

Make it emotionally intelligent and brand-strategic.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message.content

def run_trend_domination(keyword, user_email="demo@brandvision.com"):
    print(f"Running Trend Domination Report for: {keyword}")
    ai_insights = generate_trend_insights(keyword)
    emotion_result = analyze_emotion(ai_insights)
    filename = create_trend_pdf(keyword, ai_insights, emotion_result)
    send_email(user_email, keyword, filename)
    log_to_airtable(user_email, keyword, emotion_result, filename)
    print(f"✅ Trend Domination report complete for '{keyword}'")
