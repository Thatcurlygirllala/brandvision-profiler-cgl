import openai
import os

TONE_EXAMPLES = {
    "Empowering": "You’re one decision away from your next level.",
    "Uplifting": "Here’s your sign that things are turning around.",
    "Bold & Confident": "This offer isn’t for everyone — and that’s the point.",
    "Relatable & Real": "Let’s be honest… it’s hard AF running a biz and being a mom.",
    "Urgent & Action-Driven": "Waiting is costing you money — here’s proof.",
    "Playful & Fun": "POV: You turned your personality into profit.",
    "Calm & Reassuring": "Let’s take the pressure off your next launch.",
    "FOMO-Driven": "Everyone’s talking about this. You’ll wish you saw it sooner.",
    "Inspiring & Visionary": "You weren’t born to blend in — build the brand they’ll remember.",
    "Supportive & Nurturing": "You deserve strategy that supports your nervous system.",
    "Disruptive & Provocative": "If your content isn’t shaking the room, you’re missing sales.",
    "Luxury & Elevated": "This isn’t just strategy — it’s brand elegance.",
    "Grounded & Honest": "Not flashy. Just proven.",
    "Transformational": "Get ready to meet the version of you who leads and wins.",
    "Curious & Thought-Provoking": "What if your audience isn’t ghosting you — they’re just confused?"
}

def generate_swipe_copy(niche, audience, offer, emotion_tone, plan_tier):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    tone_sample = TONE_EXAMPLES.get(emotion_tone, "")

    prompt = f"""
You are a world-class copywriter trained in brand psychology and emotional marketing.

Create high-converting swipe copy for a brand in the "{niche}" niche targeting "{audience}".
The offer is: "{offer}"
The emotional tone is: "{emotion_tone}".

Use a voice and vibe that reflects this tone. Match the energy of this sample:
"{tone_sample}"

Return:
1. 5 Reels/TikTok Hooks
2. 5 CTA Phrases
3. 3 Instagram Bio Line Options
4. 5 Email Subject Lines

The style should match the selected tone and be tailored for a {plan_tier} tier user.
Make it scroll-stopping, emotionally intelligent, and ready to use.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85
    )

    return response["choices"][0]["message"]["content"]
