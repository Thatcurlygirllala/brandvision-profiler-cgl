import os
import openai
from dotenv import load_dotenv
<<<<<<< Updated upstream:trend_sync_insights_generator.py
from fpdf import FPDF
from transformers import pipeline
=======
>>>>>>> Stashed changes:BrandVisionProfiler/trendsync_engine.py

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

<<<<<<< Updated upstream:trend_sync_insights_generator.py
# Load emotion classifier model
emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)

def analyze_emotional_tone(text):
    results = emotion_clf(text)
    return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])
=======
# Check if emotion classifier is available
try:
    from transformers import pipeline
    emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)
    HAS_EMOTION_LIBS = True
except Exception:
    emotion_clf = None
    HAS_EMOTION_LIBS = False

# === Roberta-Based Emotion Analysis ===
def analyze_emotional_tone_roberta(text):
    try:
        results = emotion_clf(text)
        return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])
    except Exception as e:
        return f"Emotion classifier failed: {e}"
>>>>>>> Stashed changes:BrandVisionProfiler/trendsync_engine.py

# === GPT-4 Fallback for Emotion ===
def analyze_emotional_tone_gpt(text):
    prompt = f"""
You are an expert in branding psychology and emotional intelligence.

Analyze the emotional tone of this market insight:
"{text}"

List the top 3 emotional tones present and explain what each suggests about the audience's mindset or needs.
"""
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT-4 fallback failed: {e}"

# === Emotion Analyzer (Smart Wrapper) ===
def analyze_emotional_tone(text):
    if HAS_EMOTION_LIBS:
        return analyze_emotional_tone_roberta(text)
    else:
        return analyze_emotional_tone_gpt(text)

# === Trend Insight Generator ===
def generate_trend_insights(keyword, platform="multi"):
    prompt = f"""
You are a multi-platform trend analyst trained in branding psychology, cultural signals, and audience behavior.

Keyword: {keyword}
Platform: {platform}

Provide a TrendSync Market Report that includes:
1. Emotional tone trends (skepticism, motivation, urgency, burnout)
2. Cultural & psychological hooks driving this trend
3. Top emotional keywords from real conversations
4. Trend lifecycle (rising, peaking, fading)
5. Smart brand moves and content plays
6. CTA-ready hooks or campaign lines
7. Audience prediction: Who is leaning into this?

Make it strategic, emotionally intelligent, and brand-worthy.
"""

<<<<<<< Updated upstream:trend_sync_insights_generator.py
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
        "Next Moves:
"
        "- Use the trendâs emotion to sharpen your content tone.
"
        "- Align offers with urgency, disruption, or curiosity.
"
        "- Speak to current fears, desires, and unmet needs.

"
        "Need help applying this?
"
        "Book a Strategy Call â https://calendly.com/curlygirllala/30-minute-strategy-call"
    ))

    filename = f"trend_sync_insight_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def run_trend_insights(keyword, platform="multi"):
    ai_insights = generate_trend_insights(keyword, platform)
    emotion_result = analyze_emotional_tone(ai_insights)
    filename = create_trend_insight_pdf(keyword, ai_insights, emotion_result)
    print(f"â TrendSync Insight PDF saved: {filename}")
=======
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Trend insight generation failed: {e}"
>>>>>>> Stashed changes:BrandVisionProfiler/trendsync_engine.py
