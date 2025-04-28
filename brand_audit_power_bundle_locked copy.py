
import os
import requests
from bs4 import BeautifulSoup
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
import openai
import base64
from mailjet_rest import Client
from pyairtable import Table

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("BASE_ID")
AIRTABLE_TABLE_NAME = "AI Reports Table"
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")
openai.api_key = OPENAI_API_KEY

def clean_text(text):
    replacements = {
        "’": "'", "‘": "'", "“": '"', "”": '"',
        "–": "-", "—": "-", "→": "->", "✓": "-",
        "•": "-", "…": "...", "©": "(c)", "🌟": "*",
        "✅": "-", "🔥": "*", "💡": "*", "👉": "->"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

def fetch_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print("Fetch error:", e)
        return None

def analyze_cta_offer_clarity(html, brand_url):
    soup = BeautifulSoup(html, 'html.parser')
    text_content = soup.get_text(separator=' ', strip=True)
    trimmed_text = text_content[:4000]

    prompt = f"""
You are a UX and marketing strategist evaluating a website.

Website URL: {brand_url}

Here's a sample of the homepage text:
\"\"\"
{trimmed_text}
\"\"\"

Give a short report on:
1. What is this brand offering?
2. Is the CTA (call-to-action) clear?
3. What would confuse a first-time visitor?
4. Score this brand's offer clarity from 1–100.
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def analyze_seo(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string.strip() if soup.title else "No title"
    desc = soup.find('meta', attrs={"name": "description"})
    description = desc["content"].strip() if desc and desc.get("content") else "No description"
    h1s = [tag.get_text(strip=True) for tag in soup.find_all('h1')]
    return {"Title": title, "Description": description, "H1s": h1s or ["None found"]}

def run_google_tag_check(html):
    tags = {}
    tags["GA Found"] = "G-" in html or "UA-" in html
    tags["GSC Verified"] = 'google-site-verification' in html
    return tags

def analyze_competitor(brand_html, comp_html):
    combined = brand_html[:2000] + "\n---\n" + comp_html[:2000]
    prompt = f"""
Compare these two websites. The first is the brand being audited. The second is the competitor.

Give a clear, strategic comparison of:
- CTA clarity and positioning
- Visual tone and brand strength
- Emotional triggers or tone
- One major weakness of the competitor
- One angle the brand can use to stand out

Respond in bullet point summary.

\"\"\"
{combined}
\"\"\"
"""
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_pdf(seo_data, cta_summary, brand_url, tags=None, comp_summary=None):
    filename = f"brand_audit_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, clean_text("BrandVision Profiler: Brand Audit Report"), ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, clean_text(f"Website: {brand_url}"), ln=True, align="C")
    pdf.cell(0, 10, clean_text(f"Date: {datetime.now().strftime('%Y-%m-%d')}"), ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "SEO Overview", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, clean_text(f"Title: {seo_data['Title']}"))
    pdf.multi_cell(0, 10, clean_text(f"Description: {seo_data['Description']}"))
    pdf.multi_cell(0, 10, clean_text(f"H1 Tags: {', '.join(seo_data['H1s'])}"))

    if tags:
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Google Tools Scan", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"Google Analytics Installed: {'✅' if tags['GA Found'] else '❌'}")
        pdf.multi_cell(0, 10, f"Search Console Verified: {'✅' if tags['GSC Verified'] else '❌'}")

    if cta_summary:
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, clean_text("Offer & CTA Clarity"), ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, clean_text(cta_summary))

    if comp_summary:
        pdf.ln(5)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Competitor Comparison", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, clean_text(comp_summary))

    pdf.set_font("Arial", "I", 10)
    pdf.set_y(-20)
    pdf.cell(0, 10, clean_text("Powered by BrandVision Profiler | www.brandvisionprofiler.com"), 0, 0, "C")

    pdf.output(filename)
    return filename

def send_email_with_pdf(pdf_file, recipient_email, brand_url):
    mailjet = Client(auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY))
    with open(pdf_file, "rb") as file:
        pdf_data = file.read()
    data = {
        'Messages': [{
            "From": {"Email": MAILJET_SENDER, "Name": "BrandVision Profiler"},
            "To": [{"Email": recipient_email}],
            "Subject": f"Your Brand Audit Report – {brand_url}",
            "TextPart": "Your personalized audit report is ready.",
            "HTMLPart": f"<h3>Brand Audit Complete</h3><p>Attached is your PDF report for {brand_url}.</p>",
            "Attachments": [{
                "ContentType": "application/pdf",
                "Filename": pdf_file,
                "Base64Content": base64.b64encode(pdf_data).decode()
            }]
        }]
    }
    result = mailjet.send.create(data=data)
    print("Email sent:", result.status_code)

def log_to_airtable(user_email, brand_url, seo_data, pdf_file, plan_tier):
    table = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
    fields = {
        "User Email": user_email,
        "Report Type": "Brand Audit",
        "Source": "Brand Audit Tool",
        "Plan Tier": plan_tier,
        "URL Scanned": brand_url,
        "Title": seo_data["Title"],
        "Meta Description": seo_data["Description"],
        "PDF Filename": pdf_file,
        "Date": datetime.now().isoformat()
    }
    table.create(fields)

def run_brand_audit(user_email, brand_url, plan_tier="Free", competitor_url=None):
    html = fetch_html(brand_url)
    if not html:
        print("❌ Brand site fetch failed.")
        return

    seo_data = analyze_seo(html)
    cta_summary = analyze_cta_offer_clarity(html, brand_url)

    tags = None
    comp_summary = None

    if plan_tier in ["Power", "Premium", "VIP"]:
        tags = run_google_tag_check(html)
        if competitor_url:
            comp_html = fetch_html(competitor_url)
            if comp_html:
                comp_summary = analyze_competitor(html, comp_html)

    pdf_file = generate_pdf(seo_data, cta_summary, brand_url, tags, comp_summary)
    send_email_with_pdf(pdf_file, user_email, brand_url)
    log_to_airtable(user_email, brand_url, seo_data, pdf_file, plan_tier)
    print(f"✅ Audit complete. PDF: {pdf_file}")

# Example Test Run
if __name__ == "__main__":
    run_brand_audit(
        user_email="demo@brandvision.com",
        brand_url="https://yourbrand.com",
        plan_tier="Power",
        competitor_url="https://competitor.com"
    )