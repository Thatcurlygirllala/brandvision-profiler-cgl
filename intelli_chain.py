# intelli_chain.py
# Multi-agent AI script: Emotion → Hook → Monetization

import openai
from pyairtable import Table
import datetime

# === CONFIGURATION ===
OPENAI_API_KEY = "your-openai-api-key"
AIRTABLE_API_KEY = "your-airtable-api-key"
AIRTABLE_BASE_ID = "your-airtable-base-id"
TABLE_NAME = "AI_StrategyVault"

openai.api_key = OPENAI_API_KEY
airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, TABLE_NAME)

# === AGENT FUNCTIONS ===

def emotion_agent(user_input, tone):
    prompt = f"Rewrite this content with a {tone} emotional tone: {user_input}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def hook_agent(emotional_content):
    prompt = f"Based on this message, write a scroll-stopping Instagram caption or hook: {emotional_content}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def monetization_agent(emotional_content):
    prompt = f"Suggest a monetizable CTA or offer idea based on this message: {emotional_content}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# === MAIN FUNCTION ===

def generate_intelli_chain(user_input, tone, username="TestUser"):
    # Run each agent step
    emotional = emotion_agent(user_input, tone)
    hook = hook_agent(emotional)
    monetization = monetization_agent(emotional)

    # Save to Airtable
    output = {
        "User": username,
        "InputPrompt": user_input,
        "Tone": tone,
        "EmotionAgentOutput": emotional,
        "HookAgentOutput": hook,
        "MonetizationOutput": monetization,
        "GeneratedAt": str(datetime.datetime.now())
    }
    airtable.create(output)

    return output

# === USAGE EXAMPLE ===
if __name__ == "__main__":
    input_text = "I want to share tips for women launching a personal brand after leaving corporate."
    tone = "bold and empowering"
    result = generate_intelli_chain(input_text, tone)
    print("AI Strategy Output:\n")
    for key, value in result.items():
        print(f"{key}: {value}\n")