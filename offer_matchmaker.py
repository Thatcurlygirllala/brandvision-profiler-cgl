
import openai
from datetime import datetime

def generate_offer_blueprint(
    user_path,
    client_type,
    audience_type,
    emotion_summary=None,
    content_topics=None,
    inquiry_summary=None,
    niche=None,
    trend_keywords=None
):
    base_prompt = f"You are a top-tier AI Monetization Strategist for BrandVision Profiler. Today’s date is {datetime.today().strftime('%B %d, %Y')}.\n"

    if user_path.lower() == "engagement":
        prompt = base_prompt + f"""
Client Type: {client_type}
Audience Type: {audience_type}

The user’s audience has been emotionally engaged, with this sentiment summary:
"{emotion_summary}"

They have posted about the following content topics:
{content_topics}

Generate a Monetization Blueprint that includes:
1. 3 Monetizable Offer Ideas based on emotional tone + content.
2. Pricing suggestions (starter, core, premium).
3. Real-time CTA hooks (reels, emails, lives) aligned to the audience.
4. A Micro-Funnel Plan (Free → Low-Ticket → Premium Offer).
5. Emotion-based Launch Language with matching tone for {audience_type}.
6. Trend-forward ideas using keywords: {trend_keywords}
7. One influencer/collaboration suggestion in their field: {niche}
"""

    elif user_path.lower() == "inquiry":
        prompt = base_prompt + f"""
Client Type: {client_type}
Audience Type: {audience_type}

The user is receiving service inquiries but has low public engagement.

Questions they’ve been asked:
"{inquiry_summary}"

Their content topics:
{content_topics}

Generate a Monetization Blueprint that includes:
1. 3 Offer Ideas based on common questions or service interest.
2. Time-to-build estimations (Quick, Mid, Long).
3. Offer Style Match based on {client_type}.
4. “What do you offer?” confidence script (1-2 sentence version).
5. Soft-sell CTAs and Pre-Sell Content Prompts for {audience_type}.
6. A 7-Day Launch Warm-Up Timeline (PDF-style content plan).
7. Optional influencer/collaboration match for niche: {niche}
"""

    else:
        prompt = base_prompt + "User path not recognized. Cannot generate blueprint."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=1600
    )

    return response.choices[0].message["content"]