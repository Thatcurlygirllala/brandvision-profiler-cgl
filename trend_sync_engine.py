
import os
import openai
import requests
from pytrends.request import TrendReq
from airtable import Airtable
from datetime import datetime

# Load environment variables (you must set these in your .env or environment)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_TABLE_NAME = "TrendSyncLogs"

# Initialize Airtable and PyTrends
airtable = Airtable(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME, AIRTABLE_API_KEY)
pytrends = TrendReq(hl='en-US', tz=360)

# Set OpenAI key
openai.api_key = OPENAI_API_KEY

def fetch_google_trends(keyword):
    pytrends.build_payload([keyword], cat=0, timeframe='now 7-d', geo='', gprop='')
    related_queries = pytrends.related_queries()[keyword]['top']
    if related_queries is not None:
        return [item['query'] for item in related_queries.head(5).to_dict('records')]
    return []

def generate_emotional_analysis(trends_list):
    joined_trends = ", ".join(trends_list)
    prompt = f"""
    Given the following trending search keywords: {joined_trends}
    Identify the dominant emotional tones (e.g., urgency, burnout, curiosity, excitement), and suggest 3 powerful content hooks based on them.
    Return in this format:
    Emotion: <emotion>
    Hooks:
    1. <hook one>
    2. <hook two>
    3. <hook three>
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=300
    )
    return response['choices'][0]['message']['content']

def log_to_airtable(search_term, user_id, emotion, keywords, hooks):
    airtable.insert({
        'Search_Term': search_term,
        'User_ID': user_id,
        'Detected_Emotion': emotion,
        'Top_Trend_Keywords': ", ".join(keywords),
        'Generated_Hooks': hooks,
        'Timestamp': datetime.utcnow().isoformat()
    })

def run_trend_sync(search_term, user_id="guest"):
    print(f"Running TrendSync for: {search_term}")
    trend_keywords = fetch_google_trends(search_term)
    if not trend_keywords:
        print("No trend data found.")
        return "No trend data found for this keyword."

    analysis = generate_emotional_analysis(trend_keywords)
    # Extract the emotion line
    emotion_line = next((line for line in analysis.splitlines() if "Emotion:" in line), "Emotion: Unknown")
    detected_emotion = emotion_line.replace("Emotion:", "").strip()

    # Log to Airtable
    log_to_airtable(search_term, user_id, detected_emotion, trend_keywords, analysis)

    return analysis

# Example test run
if __name__ == "__main__":
    result = run_trend_sync("women in leadership", user_id="demo@brandvision.com")
    print(result)
