
import os
import OpenAI
from pyairtable import Api
from datetime import datetime

# ========== CONFIGURATION ==========
AIRTABLE_ACCESS_TOKEN = os.getenv("AIRTABLE_ACCESS_TOKEN")
AIRTABLE_BASE_ID = "your_base_id_here"  # Replace with your actual Base ID
AIRTABLE_TABLE_NAME = "Emotion Engine Logs"  # Replace with your table name
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY
api = Api(AIRTABLE_ACCESS_TOKEN)
airtable = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)

# ========== MOCKED TWEETS FUNCTION ==========
def fetch_tweets(keyword_or_handle, limit=100):
    return [
        f"{keyword_or_handle} is awesome, I’m so excited to get started!",
        f"Honestly, I’m not sure if {keyword_or_handle} is legit.",
        f"I need a better coach. Feeling totally overwhelmed lately.",
        f"Thinking of working with {keyword_or_handle} — looks good!",
        f"Why are all these 'experts' so vague?"
    ]

# ========== EMOTION CLASSIFIER ==========
def classify_emotions(tweets):
    emotion_map = {
        "overwhelmed": ["burned out", "too much", "tired", "stuck", "overwhelmed"],
        "motivated": ["excited", "pumped", "energized", "can't wait", "ready"],
        "skeptical": ["not sure", "seems fake", "don't trust", "is this worth it", "vague"],
        "curious": ["wondering", "thinking about", "might try"],
        "ready_to_buy": ["need this", "signing up", "take my money", "let's go"]
    }

    emotion_counts = {emotion: 0 for emotion in emotion_map}

    for tweet in tweets:
        for emotion, keywords in emotion_map.items():
            if any(keyword.lower() in tweet.lower() for keyword in keywords):
                emotion_counts[emotion] += 1

    return emotion_counts

# ========== AI INSIGHT GENERATOR ==========
def generate_branding_insight(emotion_data, keyword):
    prompt = f"""
You are a top-tier branding strategist. Based on this audience sentiment data from Twitter/X about '{keyword}':
{emotion_data}

Generate the following:
1. A short summary of what the audience is feeling
2. Three emotional branding strategies
3. Five content hooks that speak to these emotions
    """

client = openai.OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.8
)

return response.choices[0].message.content

# ========== EXTRACT HOOKS FROM AI RESPONSE ==========
def extract_hooks_from_ai(ai_text):
    lines = ai_text.split("\n")
    hooks = [line.strip("-• ") for line in lines if any(x in line.lower() for x in ["feeling", "how", "what", "thinking", "this is"])]
    return hooks[:5]

# ========== SAVE TO AIRTABLE ==========
def save_to_airtable(user_email, keyword, emotions, summary, hooks):
    airtable.create({
        "User Email": user_email,
        "Keyword/Handle": keyword,
        "Top Emotions": str(emotions),
        "AI Summary": summary,
        "Generated Hooks": "\n".join(hooks),
        "Timestamp": datetime.now().isoformat()
    })

# ========== MAIN PROCESS FUNCTION ==========
def process_emotion_engine(user_email, keyword):
    tweets = fetch_tweets(keyword)
    emotions = classify_emotions(tweets)
    summary = generate_branding_insight(emotions, keyword)
    hooks = extract_hooks_from_ai(summary)

    save_to_airtable(user_email, keyword, emotions, summary, hooks)

    return {
        "emotions": emotions,
        "summary": summary,
        "hooks": hooks
    }

# ========== TEST RUN ==========
if __name__ == "__main__":
    result = process_emotion_engine("test@email.com", "branding coach")
    print(result)
