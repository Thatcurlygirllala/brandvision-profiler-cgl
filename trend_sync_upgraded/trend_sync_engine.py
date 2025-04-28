
import openai
import os

def generate_trend_insights(keyword, platform="multi"):
    prompt = f"""
You are a multi-platform trend analyst trained in branding psychology, cultural signals, and audience behavior.

Keyword: {keyword}
Platform: {platform}

Provide a TrendSync Market Report that includes:
1. Emotional tone trends (skepticism, motivation, hype, urgency, burnout)
2. Cultural & psychological hooks driving this topic
3. Top emotional keywords from conversations
4. Where in the trend lifecycle this sits: rising, peaking, fading?
5. Strategic content moves brands can make
6. CTA-ready hooks or phrases
7. Prediction: What audiences are leaning into this?

Make it emotionally intelligent and brand-strategic.
"""
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )
    return response.choices[0].message.content
