

from pyairtable import Table

def log_to_airtable(user_email, brand, topic, output, pdf_url, user_tier):
    API_KEY = "patvoKnHc5LxxfSae.1e70f2c0bde687004f66e9ffc1a933180edc6bdf5fac8b6b5c7ef684d0208500"
    BASE_ID = "app4XhsFd5eKT76QK"
    TABLE_NAME = "Hook Offer Reports"

    table = Table(API_KEY, BASE_ID, TABLE_NAME)

    # Map long labels to Airtable-safe values
    score_map = {
        "Low – Disengaged or Doubtful": "Low",
        "Medium – Curious but hesitant": "Medium",
        "High – Emotionally Ready to Act": "High"
    }

    time_map = {
        "Quick – Can launch in 1–2 days": "Quick",
        "Mid – Takes 2–5 days to build": "Mid",
        "Deep – 1+ week, more structure": "Deep"
    }

    data = {
        "User_Email": user_email,
        "Brand_Name": brand,
        "Topic": topic,
        "Hooks": "\n".join(output["hooks"]),
        "CTAs": "\n".join(output["ctas"]),
        "Bio_Line": output["bio_line"],
        "Offer_Name": output["offer_name"],
        "Offer_Description": output["offer_description"],
        "Price": output["price"],
        "Delivery_Method": output["delivery_method"],
        "Confidence_Score": score_map.get(output["confidence_score"], "Medium"),
        "Time_to_Build": time_map.get(output["time_to_build"], "Quick"),
        "PDF_URL": pdf_url,
        "User_Tier": user_tier
    }

    table.create(data)