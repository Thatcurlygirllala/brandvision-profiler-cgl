@app.route("/price_calculator", methods=["POST"])
def price_calculator():
    data = request.json
    prompt = f"""You are a pricing strategist. Recommend entry and premium pricing for:
    - Offer: {data['offer']}
    - Niche: {data['niche']}
    Include confidence score (Low/Med/High).
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    pricing = response["choices"][0]["message"]["content"]
    airtable = Table(os.getenv("AIRTABLE_API_KEY"), os.getenv("AIRTABLE_BASE_ID"), "PricingInsights")
    airtable.create({ "UserID": data["user_id"], "OfferType": data["offer"], "PricingResult": pricing })
    return jsonify({ "pricing": pricing })