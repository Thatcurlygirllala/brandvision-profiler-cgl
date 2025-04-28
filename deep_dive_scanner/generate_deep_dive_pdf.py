
from fpdf import FPDF
from datetime import datetime

def clean_text(text):
    return text.replace("â", "'").replace("â", '"').replace("â", '"').replace("â¢", "•").replace("â", "-")

def generate_deep_dive_pdf(keyword, reddit_emotions, summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Deep Dive Scanner", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Keyword: {keyword} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reddit Emotional Signal Map", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, reddit_emotions)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reddit + Quora Trend Strategy", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(summary))

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "✓ Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call
"
        "✓ Unlock the Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149

"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    filename = f"deep_dive_report_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
