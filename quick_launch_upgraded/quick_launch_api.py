
from flask import Flask, request, jsonify
from quick_launch_engine import generate_quick_launch_ideas
from generate_quick_launch_pdf import export_to_pdf
from send_quick_launch_email import send_quick_launch_email
from log_quick_launch_to_airtable import log_quick_launch_to_airtable
from pytrends.request import TrendReq

app = Flask(__name__)

@app.route('/generate-quick-launch', methods=['POST'])
def generate_quick_launch():
    try:
        data = request.get_json()
        user_email = data.get('email')
        industry = data.get('industry', 'online business')
        budget = data.get('budget', 'any')
        skill_level = data.get('skill_level', 'beginner')
        time_commitment = data.get('time_commitment', 'part-time')

        try:
            pytrends = TrendReq()
            pytrends.build_payload([industry], timeframe='today 3-m')
            trend_data = pytrends.interest_over_time()
            trend_score = int(trend_data[industry].mean()) if not trend_data.empty else "No data"
        except Exception:
            trend_score = "Unavailable"

        prompt = (
            f"You are a premium AI business strategist and trend researcher.\n\n"
            f"Google Trends Insight: Interest in '{industry}' has an average score of {trend_score}/100 over the last 90 days.\n\n"
            f"Generate 3 low-competition business ideas someone can start this week based on:\n"
            f"- Budget: {budget}\n- Skill Level: {skill_level}\n- Industry: {industry}\n- Time Commitment: {time_commitment}\n\n"
            f"For each idea, include:\n"
            f"1. Business Name\n2. Emotional Trigger\n3. Audience Fit\n4. Offer or Service\n5. Pricing Strategy\n"
            f"6. Client Acquisition Tips\n7. Tools or Platforms Needed\n8. Startup Cost Estimate\n9. Next 3 Steps to Launch\n"
            f"10. Branding Hook or Slogan\n11. Launch Power Score (Rate 1–100)\n12. Score Breakdown\n13. Emotion Match Tag\n"
            f"14. Real Business Inspiration\n15. Suggested Instagram Caption"
        )

        result = generate_quick_launch_ideas(prompt)
        filename = export_to_pdf(result, industry)
        log_quick_launch_to_airtable(user_email, industry, trend_score, result, filename)
        send_quick_launch_email(user_email, "Quick Launch Vault Report", "Your custom business ideas are attached!", filename)

        return jsonify({
            "success": True,
            "email": user_email,
            "pdf_file": filename
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
