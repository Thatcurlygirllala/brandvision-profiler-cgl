
from flask import Flask, request, jsonify
from trend_sync_engine import generate_trend_insights
from analyze_emotion import analyze_emotional_tone
from generate_trend_pdf import create_trend_insight_pdf

app = Flask(__name__)

@app.route('/generate-trend-sync', methods=['POST'])
def trend_sync_api():
    try:
        data = request.get_json()
        keyword = data.get("keyword")
        platform = data.get("platform", "multi")

        insights = generate_trend_insights(keyword, platform)
        emotions = analyze_emotional_tone(insights)
        filename = create_trend_insight_pdf(keyword, insights, emotions)

        return jsonify({
            "success": True,
            "pdf": filename,
            "keyword": keyword,
            "emotions": emotions
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
