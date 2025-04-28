@app.route("/funnel_builder", methods=["POST"])
def funnel_builder():
    data = request.json
    prompt = f"""Create a simple 4-part funnel for this product:
    - Product: {data['product']}
    - Niche: {data['niche']}
    Include:
    - Webinar title
    - Sales page CTA
    - Squeeze page structure
    - Suggested offer stack
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    funnel = response["choices"][0]["message"]["content"]
    airtable = Table(os.getenv("AIRTABLE_API_KEY"), os.getenv("AIRTABLE_BASE_ID"), "Funnels")
    airtable.create({ "UserID": data["user_id"], "FunnelDetails": funnel })
    return jsonify({ "funnel": funnel })