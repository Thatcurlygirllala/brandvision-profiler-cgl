# onboarding_assistant.py
# A scripted GPT-powered onboarding flow that collects key user info and gives a tool suggestion.

import openai
from pyairtable import Table
import datetime

# === CONFIGURATION ===
OPENAI_API_KEY = "your-openai-api-key"
AIRTABLE_API_KEY = "your-airtable-api-key"
AIRTABLE_BASE_ID = "your-airtable-base-id"
TABLE_NAME = "UserOnboarding"

openai.api_key = OPENAI_API_KEY
airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, TABLE_NAME)

# === ONBOARDING QUESTIONS ===
def onboarding_flow():
    print("Welcome to BrandVision Profiler!\nLet's get to know your brand and guide your first step.\n")

    user_name = input("What’s your name or brand name? ")
    brand_type = input("Describe your brand in one sentence: ")
    audience_type = input("Who is your ideal audience? (e.g., new moms, creative entrepreneurs, coaches) ")
    tone = input("What tone best fits your brand? (e.g., bold, calm, hype, spiritual) ")
    biggest_goal = input("What’s your biggest goal right now? (e.g., grow audience, launch offer, increase engagement) ")
    challenge = input("What’s the #1 thing holding you back right now? ")

    onboarding_summary = f"""
    User: {user_name}
    Brand Type: {brand_type}
    Audience: {audience_type}
    Tone: {tone}
    Goal: {biggest_goal}
    Challenge: {challenge}

    Based on this info, what is the BEST tool to start with inside the BrandVision Profiler app? Respond in a friendly and strategic tone.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a strategic brand coach AI."},
            {"role": "user", "content": onboarding_summary}
        ],
        temperature=0.7
    )

    recommendation = response['choices'][0]['message']['content']
    print("\n--- AI Tool Recommendation ---")
    print(recommendation)

    # Save to Airtable
    record = {
        "User": user_name,
        "BrandType": brand_type,
        "Audience": audience_type,
        "Tone": tone,
        "Goal": biggest_goal,
        "Challenge": challenge,
        "AIRecommendation": recommendation,
        "OnboardedAt": str(datetime.datetime.now())
    }
    airtable.create(record)

# === RUN SCRIPT ===
if __name__ == "__main__":
    onboarding_flow()