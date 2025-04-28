
from trend_sync_engine import generate_trend_insights
from analyze_emotion import analyze_emotional_tone
from generate_trend_pdf import create_trend_insight_pdf

def run_trend_sync(keyword, platform="multi"):
    insights = generate_trend_insights(keyword, platform)
    emotions = analyze_emotional_tone(insights)
    filename = create_trend_insight_pdf(keyword, insights, emotions)
    print(f"✅ TrendSync Insight PDF saved: {filename}")

if __name__ == "__main__":
    run_trend_sync("AI side hustles")
