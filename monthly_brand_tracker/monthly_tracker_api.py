
from flask import Flask, request, jsonify
from monthly_brand_tracker import run_monthly_brand_tracker

app = Flask(__name__)

@app.route("/generate-monthly-tracker", methods=["POST"])
def generate_tracker():
    data = request.get_json()
    try:
        brand = data.get("brand_name")
        month = data.get("month")
        email = data.get("email")
        run_monthly_brand_tracker(brand, month, email)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
