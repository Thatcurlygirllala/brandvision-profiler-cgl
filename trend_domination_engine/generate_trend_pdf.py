
from fpdf import FPDF
from datetime import datetime

def create_trend_pdf(keyword, summary, emotion_tags):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Trend Domination Report", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Trend: {keyword} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Detected Emotional Tones:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, emotion_tags)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "AI-Powered Trend Insights:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, summary)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "- Use emotion to guide content tone.\n"
        "- Lean into urgency, motivation, disruption.\n"
        "- Match audience’s current emotional state.\n"
        "- Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Unlock Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149"
    )

    filename = f"trend_domination_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
