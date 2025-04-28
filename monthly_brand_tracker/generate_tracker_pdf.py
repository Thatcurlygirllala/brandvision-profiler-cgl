
from fpdf import FPDF
from datetime import datetime

def generate_tracker_pdf(brand_name, month, content):
    filename = f"brand_tracker_{brand_name.replace(' ', '_')}_{month.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BrandVision Profiler: Monthly Brand Tracker", ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, f"Brand: {brand_name} | Month: {month}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Strategic Action Plan", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10,
        "✓ Align your next 30 days of content with suggested hooks.\n"
        "✓ Adjust your emotional messaging for audience tone shifts.\n"
        "✓ Apply offer pivots to match emerging trends.\n\n"
        "Need help applying this?\n"
        "- Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call\n"
        "- Unlock the Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149"
    )

    pdf.output(filename)
    return filename
