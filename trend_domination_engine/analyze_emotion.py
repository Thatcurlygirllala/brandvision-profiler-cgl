
from transformers import pipeline

clf = pipeline("text-classification", model="SamLowe/roberta-base-go_emotions", top_k=5)

def analyze_emotion(text):
    result = clf(text)
    return ", ".join([f"{r['label']} ({round(r['score'], 2)})" for r in result[0]])
