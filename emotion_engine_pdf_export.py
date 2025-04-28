
import os
import openai
from pyairtable import Table
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF

# ========== LOAD ENV ==========
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("BASE_ID")
AIRTABLE_TABLE_NAME = "Emotion Engine Logs"

openai.api_key = OPENAI_API_KEY
airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

# ========== MOCKED TWEETS FUNCTION ==========
def fetch_tweets(keyword_or_handle, limit=100):
    return [
        f"{keyword_or_handle} is awesome, I’m so excited to get started!",
        f"Honestly, I’m not sure if {keyword_or_handle} is legit.",
        f"I need a better coach. Feeling totally overwhelmed lately.",
        f"Thinking of working with {keyword_or_handle} — looks good!",
        f"Why are all these 'experts' so vague?"
    ]

# ========== EMOTION CLASSIFIER ==========
def classify_emotions(tweets):
    emotion_map = {
        "overwhelmed": ["burned out", "too much", "tired", "stuck", "overwhelmed"],
        "motivated": ["excited", "pumped", "energized", "can't wait", "ready"],
        "skeptical": ["not sure", "seems fake", "don't trust", "is this worth it", "vague"],
        "curious": ["wondering", "thinking about", "might try"],
        "ready_to_buy": ["need this", "signing up", "take my money", "let's go"]
    }

    emotion_counts = {emotion: 0 for emotion in emotion_map}
    for tweet in tweets:
        for emotion, keywords in emotion_map.items():
            if any(keyword.lower() in tweet.lower() for keyword in keywords):
                emotion_counts[emotion] += 1
    return emotion_counts

# ========== AI INSIGHT GENERATOR ==========
def generate_branding_insight(emotion_data, keyword):
    prompt = f"""
You are a top-tier branding strategist. Based on this audience sentiment data from Twitter/X about '{keyword}':
{emotion_data}

Generate the following:
1. A short summary of what the audience is feeling
2. Three emotional branding strategies
3. Five content hooks that speak to these emotions
"""
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

# ========== HOOK EXTRACTOR ==========
def extract_hooks_from_ai(ai_text):
    lines = ai_text.split("\n")
    hooks = [line.strip("-• ") for line in lines if any(kw in line.lower() for kw in ["feeling", "why", "you", "what", "how", "?"])]
    return hooks[:5]

# ========== PDF REPORT ==========
def create_emotion_engine_pdf(keyword, emotional_summary, hooks, emotions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "BrandVision Profiler: Emotion Engine Report", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(200, 10, f"Keyword: {keyword} | {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="C")

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Top Emotional Signals", ln=True)
    pdf.set_font("Arial", "", 12)
    for emotion, count in emotions.items():
        pdf.cell(0, 10, f"{emotion.capitalize()}: {count}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "AI Emotional Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, emotional_summary)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Suggested Emotional Hooks", ln=True)
    pdf.set_font("Arial", "", 12)
    for hook in hooks:
        pdf.cell(0, 10, f"- {hook}", ln=True)

    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Next Steps", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, (
        "To use these insights:
"
        "- Turn hooks into posts or Reels
"
        "- Use emotion words in your next launch

"
        "Need help?
"
        "Book a Strategy Call: https://calendly.com/curlygirllala/30-minute-strategy-call
"
        "Power Bundle: https://brandvisionprofiler.com/checkout?bundle=power149
"
        "www.brandvisionprofiler.com"
    ))

    filename = f"emotion_engine_report_{keyword.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# ========== AIRTABLE LOGGER ==========
def save_to_airtable(user_email, keyword, emotions, summary, hooks):
    airtable.create({
        "User Email": user_email,
        "Keyword/Handle": keyword,
        "Top Emotions": str(emotions),
        "AI Summary": summary,
        "Generated Hooks": "\n".join(hooks),
        "Timestamp": datetime.now().isoformat()
    })

# ========== RUN ==========
def run_emotion_engine(user_email, keyword):
    tweets = fetch_tweets(keyword)
    emotions = classify_emotions(tweets)
    summary = generate_branding_insight(emotions, keyword)
    hooks = extract_hooks_from_ai(summary)
    pdf_path = create_emotion_engine_pdf(keyword, summary, hooks, emotions)
    save_to_airtable(user_email, keyword, emotions, summary, hooks)
    print(f"Emotion Engine Report generated: {pdf_path}")