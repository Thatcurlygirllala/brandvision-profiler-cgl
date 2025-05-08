import os
import openai
from dotenv import load_dotenv
from datetime import datetime
from fpdf import FPDF

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_bulk_report_for_client(client_name, industry, goals):
    prompt = f"""
You are a white-label branding strategist generating a bulk AI report for 
an agency client.

Client: {client_name}
Industry: {industry}
Goals: {goals}

Provide a white-labeled, professional branding strategy including:
1. Emotional pain points in this industry
2. Suggested brand positioning & voice
3. 3 high-converting content hooks
4. 2 monetization ideas
5. Branding tone & buyer motivation tips

Make this report strategic, emotionally intelligent, and agency-ready.
"""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def create_bulk_pdf(content, client_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: VIP Client Strategy Report", 
ln=True, align="C")

    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Client: {client_name} | Generated: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, content)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "For Internal Use Only", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, """This report is white-labeled for coaching,consulting, and agency use.
You may customize the offer, delivery, and format to fit your business model.
Need additional reports or automation? Contact 
support@brandvisionprofiler.com.""")

    filename = f"vip_bulk_strategy_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

def run_vip_bulk_launcher(client_name, industry, goals):
    content = generate_bulk_report_for_client(client_name, industry, 
goals)
    filename = create_bulk_pdf(content, client_name)
    print(f"VIP Strategy Report saved: {filename}")
