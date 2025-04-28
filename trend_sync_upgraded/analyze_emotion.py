
from transformers import pipeline

emotion_clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)

def analyze_emotional_tone(text):
    results = emotion_clf(text)
    return ", ".join([f"{res['label']} ({round(res['score'], 2)})" for res in results[0]])
