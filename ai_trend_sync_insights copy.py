
import os
import openai
import requests
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from pytrends.request import TrendReq

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def fetch_google_trends(keyword):
    try:
        pytrends = TrendReq()
        pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
        related = pytrends.related_queries()
        return related[keyword]['top'] if related[keyword] and related[keyword]['top'] is not None else []
    except Exception as e:
        print("Google Trends Error:", e)
        return []

def fetch_emotion_trend_insights(keyword):
    prompt = f"""
You are an AI trend analyst and brand strategist.

Keyword: {keyword}

1. Summarize emotional patterns you’d expect across Google, Reddit, TikTok, and X based on this topic.
2. Suggest emotional hooks or fears driving the trend (e.g., “AI is taking my job,” “burnout recovery,” “shiny object syndrome”).
3. Provide viral content angles, captions, or CTAs related to this trend.
4. Cross-reference with buyer intent: is this trend educational, curiosity-driven, or purchase-motivated?

Use brand psychology and emotional marketing in your analysis.
"""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_trend_pdf(insights, keyword):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: AI TrendSync Report", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Trend: {keyword} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, insights)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Step Suggestions", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "To turn this trend into strategy:

"
        "1. Use the hook in your next reel or carousel post.
"
        "2. Book a Strategy Call – https://calendly.com/curlygirllala/30-minute-strategy-call
"
        "3. Unlock the Power Bundle – https://brandvisionprofiler.com/checkout?bundle=power149

"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    filename = f"trend_sync_insights_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def run_trend_sync_insights(keyword):
    trends = fetch_google_trends(keyword)
    print("Related Google Trends:", trends)

    insights = fetch_emotion_trend_insights(keyword)
    filename = create_trend_pdf(insights, keyword)
    print(f"TrendSync PDF saved: {filename}")
