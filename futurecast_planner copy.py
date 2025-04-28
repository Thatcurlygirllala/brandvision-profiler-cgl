# futurecast_planner.py
# Generates a content calendar based on plan type, emotional tone, trend, and brand focus.

import openai
import datetime
from pyairtable import Table

# === CONFIGURATION ===
OPENAI_API_KEY = "your-openai-api-key"
AIRTABLE_BASE_ID = "your-airtable-base-id"
AIRTABLE_API_KEY = "your-airtable-api-key"
TABLE_NAME = "ContentCalendar"

# === SETUP ===
openai.api_key = OPENAI_API_KEY
airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, TABLE_NAME)

# === PLAN LOGIC ===
PLAN_DAY_MAPPING = {
    "Basic": 7,
    "Pro": 7,
    "Premium": 30
}

# === GENERATE CALENDAR ===
def generate_content_calendar(user_name, brand_focus, tone, trend, plan_type):
    days = PLAN_DAY_MAPPING.get(plan_type, 7)
    prompt = f"""
    You are a content strategist. Create a {days}-day content calendar for a brand called "{user_name}" that focuses on "{brand_focus}".
    Use a {tone} tone. Incorporate this trend if relevant: "{trend}".
    
    For each day, include:
    - Date
    - Content Idea
    - Suggested Hook or Caption
    - Emotional Tone
    {"- CTA" if plan_type in ['Pro', 'Premium'] else ""}
    {"- Funnel Stage (Awareness, Interest, Desire, Action)" if plan_type == 'Premium' else ""}
    Format the result in a way that's easy to read or log into a database.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert branding strategist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content']

# === SAVE TO AIRTABLE ===
def save_calendar_to_airtable(calendar_text, user_name, plan_type):
    calendar_blocks = calendar_text.strip().split("\n\n")
    today = datetime.date.today()

    for i, block in enumerate(calendar_blocks):
        fields = {
            "RawOutput": block,
            "User": user_name,
            "Plan": plan_type,
            "GeneratedAt": str(today + datetime.timedelta(days=i))
        }
        airtable.create(fields)

# === USAGE EXAMPLE ===
if __name__ == "__main__":
    user = "CurlyGirlLala"
    brand_focus = "Empowering women entrepreneurs through branding"
    tone = "bold, uplifting"
    trend = "Soft Launch Strategies"
    plan = "Premium"  # Options: Basic, Pro, Premium

    calendar_output = generate_content_calendar(user, brand_focus, tone, trend, plan)
    save_calendar_to_airtable(calendar_output, user, plan)

    print("Content calendar generated and saved to Airtable!")
