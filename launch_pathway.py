@app.route("/launch_pathway", methods=["POST"])
def launch_pathway():
    data = request.json
    prompt = f"""You are a brand launch strategist. Based on this product idea, generate a 4-week launch roadmap.
    Include weekly goals, content focus, and CTA.
    Product: {data['product']}
    Niche: {data['niche']}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    roadmap = response["choices"][0]["message"]["content"]
    airtable = Table(os.getenv("AIRTABLE_API_KEY"), os.getenv("AIRTABLE_BASE_ID"), "LaunchPathways")
    airtable.create({ "UserID": data["user_id"], "Roadmap": roadmap })
    return jsonify({ "roadmap": roadmap })