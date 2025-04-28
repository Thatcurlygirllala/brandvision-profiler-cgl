
from flask import Flask, request, jsonify
from deep_dive_engine import fetch_reddit_posts, fetch_quora_questions, analyze_emotions, generate_deep_dive_summary
from generate_deep_dive_pdf import generate_deep_dive_pdf
from send_deep_dive_email import send_deep_dive_email

app = Flask(__name__)

@app.route('/generate-deep-dive', methods=['POST'])
def generate_deep_dive():
    try:
        data = request.get_json()
        keyword = data.get("keyword")
        user_email = data.get("email")

        reddit_posts = fetch_reddit_posts(keyword)
        quora_questions = fetch_quora_questions(keyword)
        reddit_emotions = analyze_emotions(" ".join(reddit_posts[:3]))
        summary = generate_deep_dive_summary(keyword, reddit_posts, quora_questions)
        pdf_file = generate_deep_dive_pdf(keyword, reddit_emotions, summary)
        send_deep_dive_email(pdf_file, user_email, keyword)

        return jsonify({"success": True, "pdf_file": pdf_file})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
