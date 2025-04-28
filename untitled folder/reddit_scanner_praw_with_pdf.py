import os
import openai
import praw
from airtable import Airtable
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = os.getenv("REDDIT_SCANNER_TABLE", "RedditScannerLogs")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# Initialize Airtable, OpenAI, Reddit
airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
openai.api_key = OPENAI_API_KEY
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_CLIENT_SECRET, user_agent=REDDIT_USER_AGENT)

def fetch_reddit_threads(keyword, subreddit="all", limit=10):
    results = []
    for submission in reddit.subreddit(subreddit).search(keyword, limit=limit, sort="new"):
        if not submission.stickied:
            thread = f"Title: {submission.title}\nText: {submission.selftext}\n"
            results.append(thread)
    return results

def analyze_threads_with_ai(threads):
    combined = "\n\n".join(threads[:5])
    prompt = f"""
    Analyze the following Reddit threads and extract:
    - 3 audience pain points
    - 2 emotional trends
    - 2 viral content hook ideas
    - 1 monetizable offer idea

    Threads:
    {combined}

    Return in this format:
    Pain Points:
    1.
    2.
    3.

    Emotional Trends:
    - 
    - 

    Hook Ideas:
    1.
    2.

    Suggested Offer:
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response["choices"][0]["message"]["content"]

def log_to_airtable(search_term, user_id, summary):
    lines = summary.splitlines()
    pain_points = "\n".join([line for line in lines if line.startswith("1.") or line.startswith("2.") or line.startswith("3.")])
    emotional = "\n".join([line for line in lines if "Emotional Trends" in line or line.startswith("- ")])
    hooks = "\n".join([line for line in lines if "Hook Ideas" in line or line.startswith("1.") or line.startswith("2.")])
    offer_line = next((line for line in lines if "Suggested Offer:" in line or line.startswith("Suggested Offer")), "")

    airtable.insert({
        "Search_Term": search_term,
        "User_ID": user_id,
        "Pain_Points": pain_points,
        "Emotional_Trends": emotional,
        "Hook_Ideas": hooks,
        "Suggested_Offer": offer_line,
        "Timestamp": datetime.utcnow().isoformat()
    })

def create_pdf_report(summary, keyword):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Title Page
    pdf.cell(0, 10, "BrandVision Profiler", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Reddit Insights Report for: {keyword}", ln=True, align="C")
    pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")
    pdf.ln(20)

    # Add content
    pdf.set_font("Arial", "", 11)
    for line in summary.splitlines():
        if line.strip():
            pdf.multi_cell(0, 8, line)

    # Footer
    pdf.set_y(-20)
    pdf.set_font("Arial", "I", 8)
    pdf.cell(0, 10, "Powered by BrandVisionProfiler.com", 0, 0, "C")

    filename = f"reddit_insights_{keyword.replace(' ', '_')}.pdf"
    pdf.output(filename)
    return filename

def run_reddit_scanner(keyword, user_id="guest", subreddit="all"):
    print(f"Scanning Reddit for: {keyword} in r/{subreddit}")
    threads = fetch_reddit_threads(keyword, subreddit)
    if not threads:
        return "No threads found."

    summary = analyze_threads_with_ai(threads)
    log_to_airtable(keyword, user_id, summary)
    pdf_path = create_pdf_report(summary, keyword)
    print(f"PDF report created: {pdf_path}")
    return summary

# Run test
if __name__ == "__main__":
    result = run_reddit_scanner("burnout recovery", user_id="demo@brandvision.com")
    print(result)
