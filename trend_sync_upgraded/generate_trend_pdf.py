
from fpdf import FPDF
from datetime import datetime

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
        "- Use the trend’s emotion to sharpen your content tone.
"
        "- Align offers with urgency, disruption, or curiosity.
"
        "- Speak to current fears, desires, and unmet needs.

"
        "Need help applying this?
"
        "Book a Strategy Call → https://calendly.com/curlygirllala/30-minute-strategy-call"
    ))

    filename = f"trend_sync_insight_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
