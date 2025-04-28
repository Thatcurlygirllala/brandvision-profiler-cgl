
from fpdf import FPDF
from datetime import datetime

def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "•": "*", "…": "...",
        "→": "->", "®": "", "©": "", "™": "", "\u200b": "", "\u2019": "'"
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text

def create_income_pdf(content, audience_description):
    cleaned_content = clean_text(content)
    cleaned_input = clean_text(audience_description)

    filename = f"income_blueprint_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Monetization Blueprint", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Input: {cleaned_input[:50]}... | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, cleaned_content)

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "- Turn this into a launch plan.\n"
        "- Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Unlock the Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    )

    pdf.output(filename)
    return filename
