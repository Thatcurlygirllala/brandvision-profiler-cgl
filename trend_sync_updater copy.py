# trend_sync_updater.py
# Pulls trending topics from Google Trends and pushes to Airtable

from pyairtable import Table
import requests
import datetime

# === CONFIGURATION ===
AIRTABLE_API_KEY = "your-airtable-api-key"
AIRTABLE_BASE_ID = "your-airtable-base-id"
TABLE_NAME = "Trends"

airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, TABLE_NAME)

# === FETCH TRENDS FROM GOOGLE TRENDING TOPICS ===
# Note: This version uses unofficial trend API (via rss feed workaround or manual injection)
# For real-time data, you can later use pytrends or scrape trends.google.com directly

def get_manual_google_trends():
    # Example trends - can be replaced with real data from Google or X scraping
    return [
        "Soft Launch Strategies",
        "TikTok Storytelling",
        "Emotional Branding",
        "Content Batching",
        "Quiet Luxury Marketing"
    ]

# === PUSH TO AIRTABLE ===

def update_airtable_trends():
    trends = get_manual_google_trends()
    today = datetime.date.today()

    for t in trends:
        airtable.create({
            "Trend": t,
            "DateAdded": str(today),
            "Source": "Manual Google Trends Sync"
        })

    print(f"{len(trends)} trends uploaded to Airtable.")

# === RUN ===
if __name__ == "__main__":
    update_airtable_trends()