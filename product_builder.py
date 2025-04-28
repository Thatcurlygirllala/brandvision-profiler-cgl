from flask import Flask, request, jsonify
import openai, os
from pyairtable import Table

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")
airtable = Table(os.getenv("AIRTABLE_API_KEY"), os.getenv("AIRTABLE_BASE_ID"), "Products")

@app.route("/product_builder", methods=["POST"])
def product_builder():
    data = request.json
    prompt = f"""You are an AI product strategist. Based on this brand description, create:
    1. Product Title
    2. Offer Type (Course, Coaching, etc.)
    3. Format (Video, PDF, etc.)
    4. Delivery Method
    5. Bonus Idea
    6. Lead Magnet Suggestion
    Description: {data.get('description')}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_output = response["choices"][0]["message"]["content"]
    airtable.create({ "UserID": data["user_id"], "ProductSummary": ai_output })
    return jsonify({ "product": ai_output })