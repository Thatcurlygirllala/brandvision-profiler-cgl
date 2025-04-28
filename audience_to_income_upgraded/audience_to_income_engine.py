
import openai
import os

def generate_income_blueprint(audience_description, user_strength="writing"):
    prompt = f"""
You are a 19-star AI monetization strategist helping brands turn their audience into income.

Audience: {audience_description}
User Strength: {user_strength}

Create an Audience-to-Income Blueprint:
1. Analyze emotional signals & engagement stage
2. Recommend 2 monetizable offers (aligned with emotions + strengths)
3. Suggest 3 soft-sell CTA post ideas
4. Funnel path (DM prompt → lead magnet → upsell)
5. Confidence-boosting language to reduce doubt
6. Quick win timeline (7-day warm-up)
7. Add a VIP upgrade suggestion with call-to-action
"""

    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
