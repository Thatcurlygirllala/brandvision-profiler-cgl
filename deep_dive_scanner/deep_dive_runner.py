
from deep_dive_engine import fetch_reddit_posts, fetch_quora_questions, analyze_emotions, generate_deep_dive_summary
from generate_deep_dive_pdf import generate_deep_dive_pdf
from send_deep_dive_email import send_deep_dive_email

def run_deep_dive(keyword, user_email):
    reddit_posts = fetch_reddit_posts(keyword)
    quora_questions = fetch_quora_questions(keyword)
    reddit_emotions = analyze_emotions(" ".join(reddit_posts[:3]))
    summary = generate_deep_dive_summary(keyword, reddit_posts, quora_questions)
    pdf_file = generate_deep_dive_pdf(keyword, reddit_emotions, summary)
    send_deep_dive_email(pdf_file, user_email, keyword)
    print("✅ Deep Dive Scanner Complete")

if __name__ == "__main__":
    run_deep_dive("burnout recovery", "demo@brandvision.com")
