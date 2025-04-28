
from quick_launch_engine import generate_quick_launch_ideas
from generate_quick_launch_pdf import export_to_pdf
from send_quick_launch_email import send_quick_launch_email
from log_quick_launch_to_airtable import log_quick_launch_to_airtable

def run_quick_launch():
    user_email = "test@brandvision.com"
    industry = "wellness"
    trend_score = 77
    budget = "low"
    skill_level = "beginner"
    time_commitment = "part-time"

    prompt = (
        f"You are a premium AI business strategist and trend researcher.\n\n"
        f"Google Trends Insight: Interest in '{industry}' has an average score of {trend_score}/100 over the last 90 days.\n\n"
        f"Generate 3 low-competition business ideas someone can start this week based on:\n"
        f"- Budget: {budget}\n- Skill Level: {skill_level}\n- Industry: {industry}\n- Time Commitment: {time_commitment}\n\n"
        f"For each idea, include:\n"
        f"1. Business Name\n2. Emotional Trigger\n3. Audience Fit\n4. Offer or Service\n5. Pricing Strategy\n"
        f"6. Client Acquisition Tips\n7. Tools or Platforms Needed\n8. Startup Cost Estimate\n9. Next 3 Steps to Launch\n"
        f"10. Branding Hook or Slogan\n11. Launch Power Score (Rate 1–100)\n12. Score Breakdown\n13. Emotion Match Tag\n"
        f"14. Real Business Inspiration\n15. Suggested Instagram Caption\n\n"
        f"Format everything in clean markdown."
    )

    result = generate_quick_launch_ideas(prompt)
    filename = export_to_pdf(result, industry)
    log_quick_launch_to_airtable(user_email, industry, trend_score, result, filename)
    send_quick_launch_email(user_email, "Quick Launch Vault Report", "Here's your personalized business idea vault!", filename)

if __name__ == "__main__":
    run_quick_launch()
