from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/run-offer-summary", methods=["POST"])
def run_offer_summary():
    data = request.get_json()
    print("Received data:", data)
    return jsonify({"success": True, "message": "Offer Summary received."})
