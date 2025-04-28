@app.route("/affiliate_matcher", methods=["POST"])
def affiliate_matcher():
    data = request.json
    prompt = f"""Suggest 2 affiliate tools for this brand focused on {data['niche']}:
    Include name, link, and use-case.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    suggestions = response["choices"][0]["message"]["content"]
    airtable = Table(os.getenv("AIRTABLE_API_KEY"), os.getenv("AIRTABLE_BASE_ID"), "AffiliateTools")
    airtable.create({ "UserID": data["user_id"], "Suggestions": suggestions })
    return jsonify({ "suggestions": suggestions })