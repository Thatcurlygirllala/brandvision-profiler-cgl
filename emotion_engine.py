
import os
from dotenv import load_dotenv
import openai

# Load keys
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Try importing Roberta model
try:
    from transformers import pipeline
    emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)
    HAS_ROBERTA = True
except:
    emotion_clf = None
    HAS_ROBERTA = False

# Roberta emotion classification
def analyze_emotional_tone_roberta(text):
    try:
        results = emotion_clf(text)
        return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])
    except Exception as e:
        return f"(Roberta failed: {str(e)})"

# GPT fallback if transformers not available
def analyze_emotional_tone_gpt(text):
    prompt = f"""
You are an expert in branding psychology and emotional intelligence.

Analyze the emotional tone of this content:
"{text}"

List the top 3 emotional tones present and describe what they reveal about the audience's mindset or desire.
"""
    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"(GPT-4 failed: {str(e)})"

# Unified wrapper
def analyze_emotional_tone(text):
    if HAS_ROBERTA:
        return analyze_emotional_tone_roberta(text)
    else:
        return analyze_emotional_tone_gpt(text)

# Entry point
def run_emotion_engine(data):
    insight = data.get("insight", "")
    if not insight:
        return {"error": "Missing insight"}
    
    result = analyze_emotional_tone(insight)
    return {
        "status": "success",
        "insight": insight,
        "emotion_analysis": result,
        "note": "Copy and paste the analysis for strategic use."
    }
