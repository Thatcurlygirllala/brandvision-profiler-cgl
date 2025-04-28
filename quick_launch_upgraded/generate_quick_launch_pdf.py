
from fpdf import FPDF
from datetime import datetime

def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "•": "*", "…": "...",
        "→": "->", "®": "", "©": "", "™": "", "\u200b": "", "â": "✓", "â": "-", "â": "-"
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def export_to_pdf(ideas_text, keyword):
    cleaned_ideas = clean_text(ideas_text)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Quick Launch Vault", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Industry: {keyword} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cleaned_ideas)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "CTA + Bonus", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "Love one of these business ideas?\n"
        "✓ Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "✓ Get the AI Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    filename = f"vault_report_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
