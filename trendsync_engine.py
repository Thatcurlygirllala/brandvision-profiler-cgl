import os
import openai
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_emotional_tone(text):
    try:
        from transformers import pipeline
        emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)
        results = emotion_clf(text)
        return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])
    except Exception as e:
        print(f"Emotion analysis failed: {e}")
        return "Emotion classifier not available (transformers/torch not installed)."

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
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message.content

def create_trend_insight_pdf(keyword, insights, emotion_result):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: TrendSync Insights", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Trend: {keyword} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detected Emotional Tones:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, emotion_result)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "AI-Powered Insight Report:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, insights)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Your Brand Action Plan", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "Next Moves:\n"
        "- Use the trend’s emotion to sharpen your content tone.\n"
        "- Align offers with urgency, disruption, or curiosity.\n"
        "- Speak to current fears, desires, and unmet needs.\n\n"
        "Need help applying this?\n"
        "Book a Strategy Call – https://calendly.com/curlygirllala/30-minute-strategy-call"
    ))

    filename = f"trend_sync_insight_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def generate_trendsync_insights(keyword, platform="multi"):
    insights = generate_trend_insights(keyword, platform)
    emotion_result = analyze_emotional_tone(insights)
    filename = create_trend_insight_pdf(keyword, insights, emotion_result)
    print(f"✅ TrendSync Insight PDF saved: {filename}")
    return filename
