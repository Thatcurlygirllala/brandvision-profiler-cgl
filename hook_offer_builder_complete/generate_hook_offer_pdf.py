
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch

def generate_hook_offer_pdf(output: dict, file_path: str):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, fontSize=12))
    styles.add(ParagraphStyle(name='SectionTitle', fontSize=13, spaceAfter=8, spaceBefore=12, leading=14, underlineWidth=1))
    styles.add(ParagraphStyle(name='CTA', fontSize=12, spaceAfter=10, textColor='blue', alignment=TA_CENTER))

    doc = SimpleDocTemplate(file_path, pagesize=letter,
                            rightMargin=40, leftMargin=40, topMargin=60, bottomMargin=40)
    content = []

    content.append(Paragraph("Hook & Offer Builder – Monetization Blueprint", styles['Title']))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Swipe Copy Hooks", styles['SectionTitle']))
    for hook in output["hooks"]:
        content.append(Paragraph(f"- {hook}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Call-to-Action Ideas", styles['SectionTitle']))
    for cta in output["ctas"]:
        content.append(Paragraph(f"- {cta}", styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Instagram Bio Line", styles['SectionTitle']))
    content.append(Paragraph(output["bio_line"], styles['Normal']))
    content.append(Spacer(1, 10))

    content.append(Paragraph("Monetizable Offer Blueprint", styles['SectionTitle']))
    content.append(Paragraph(f"<b>Offer Name:</b> {output['offer_name']}", styles['Normal']))
    content.append(Paragraph(f"<b>Description:</b> {output['offer_description']}", styles['Normal']))
    content.append(Paragraph(f"<b>Price:</b> {output['price']}", styles['Normal']))
    content.append(Paragraph(f"<b>Delivery Method:</b> {output['delivery_method']}", styles['Normal']))
    content.append(Paragraph(f"<b>Confidence Score:</b> {output['confidence_score']}", styles['Normal']))
    content.append(Paragraph(f"<b>Time to Build:</b> {output['time_to_build']}", styles['Normal']))
    content.append(Spacer(1, 14))

    content.append(Paragraph("Need Help Launching This?", styles['SectionTitle']))
    content.append(Paragraph("Your offer is ready – now let's make it convert.", styles['Normal']))
    content.append(Spacer(1, 6))
    content.append(Paragraph("• <b>Book a 1:1 Strategy Call</b> ($47)", styles['Normal']))
    content.append(Paragraph("• <b>Unlock the Swipe Vault</b> ($29)", styles['Normal']))
    content.append(Paragraph("• <b>Grab the Power Bundle</b> ($149)", styles['Normal']))
    content.append(Spacer(1, 10))
    content.append(Paragraph("→ Ready to go from insight to income? Upgrade now and launch like a pro.", styles['CTA']))

    doc.build(content)
