# offer_analyst.py
# Analyzes user's past content + preferences to recommend a monetizable offer path.

import openai
from pyairtable import Table
import datetime

# === CONFIGURATION ===
OPENAI_API_KEY = "your-openai-api-key"
AIRTABLE_API_KEY = "your-airtable-api-key"
AIRTABLE_BASE_ID = "your-airtable-base-id"
TABLE_NAME = "AI_StrategyVault"  # Table with past hooks/emotions/inputs

openai.api_key = OPENAI_API_KEY
airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, TABLE_NAME)

# === ANALYSIS + OFFER GENERATION ===

def get_recent_content(username, limit=5):
    all_records = airtable.all(formula=f"{{User}} = '{username}'")
    recent = sorted(all_records, key=lambda r: r['fields'].get('GeneratedAt', ''), reverse=True)[:limit]
    return [r['fields'].get('EmotionAgentOutput', '') for r in recent]

def suggest_offer(username):
    content_blocks = get_recent_content(username)
    combined_text = "\n\n".join(content_blocks)

    prompt = f"""
    The user has written the following emotionally charged content:

    {combined_text}

    Based on these patterns, suggest a monetizable offer that fits their brand tone and audience.
    Include:
    - Offer Name
    - Offer Type (Challenge, Masterclass, Digital Product, Coaching, etc.)
    - Ideal CTA
    - Emotional Hook
    - Funnel Starting Content Idea
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a top-tier branding + monetization strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.75
    )

    recommendation = response['choices'][0]['message']['content']

    # Save it to Airtable
    record = {
        "User": username,
        "GeneratedAt": str(datetime.datetime.now()),
        "AI_Offer_Recommendation": recommendation
    }
    airtable.create(record)

    return recommendation

# === USAGE EXAMPLE ===
if __name__ == "__main__":
    user = "CurlyGirlLala"
    result = suggest_offer(user)
    print("\n--- Monetizable Offer Recommendation ---\n")
    print(result)