
from fpdf import FPDF
from datetime import datetime

def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "→": "->", "✓": "-",
        "•": "-", "…": "...", "©": "(c)"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def create_swipe_copy_pdf(user_name, niche, emotion_tone, swipe_text):
    filename = f"swipe_copy_{user_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Swipe Copy Generator", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Niche: {niche} | Tone: {emotion_tone} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    for section in swipe_text.split("\n"):
        pdf.multi_cell(0, 10, clean_text(section))

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(
        "You're now equipped with high-converting swipe copy.\n\n"
        "✓ Book your Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "✓ Unlock advanced content tools in the Power Bundle:\n"
        "https://brandvisionprofiler.com/checkout?bundle=power149\n\n"
        "Powered by BrandVision Profiler | www.brandvisionprofiler.com"
    ))

    pdf.output(filename)
    return filename
