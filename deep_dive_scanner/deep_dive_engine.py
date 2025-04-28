
import os
import openai
import praw
from transformers import pipeline
import requests
from bs4 import BeautifulSoup

# === Load API Keys ===
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Reddit Client ===
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

# === Emotion Classifier ===
emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)

def fetch_reddit_posts(keyword):
    posts = []
    try:
        for submission in reddit.subreddit("all").search(keyword, limit=10):
            posts.append(submission.title + " " + submission.selftext)
    except Exception as e:
        print("Reddit fetch error:", e)
    return posts

def fetch_quora_questions(keyword):
    url = f"https://www.quora.com/search?q={keyword.replace(' ', '%20')}"
    headers = {"User-Agent": "Mozilla/5.0"}
    questions = []
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for q in soup.find_all("a", href=True):
            text = q.get_text()
            if "?" in text and len(text) > 20:
                questions.append(text.strip())
            if len(questions) >= 10:
                break
    except Exception as e:
        print("Quora fetch error:", e)
    return list(set(questions))

def analyze_emotions(text):
    results = emotion_clf(text)
    return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])

def generate_deep_dive_summary(keyword, reddit_posts, quora_questions):
    reddit_input = "\n".join(reddit_posts[:5])
    quora_input = "\n".join(quora_questions[:5])
    
    prompt = f"""
You are a world-class branding strategist using Reddit + Quora to analyze market emotions and intent.

Keyword: {keyword}

Analyze Reddit posts for:
- Emotional signals
- Pain points
- Content hooks
- Offer gaps

Analyze Quora questions for:
- Purchase intent
- Content gaps
- CTA opportunities

Create a 3-part Brand Report:
1. Emotional Trends (Reddit)
2. Intent & Curiosity (Quora)
3. Offer Strategy + Suggested Hooks

Reddit Posts:
{reddit_input}

Quora Questions:
{quora_input}
"""

    client = openai.OpenAI()
    chat_response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return chat_response.choices[0].message.content
