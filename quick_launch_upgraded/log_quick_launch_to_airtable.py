
from pyairtable import Api
from datetime import datetime
import os

def log_quick_launch_to_airtable(email, industry, trend_score, ideas_text, pdf_filename=None):
    api_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("QUICK_LAUNCH_TABLE")

    api = Api(api_key)
    table = api.table(base_id, table_name)

    record = {
        "Email": email,
        "Generated At": datetime.utcnow().isoformat(),
        "Industry": industry,
        "Trend Score": str(trend_score),
        "AI Output": ideas_text
    }

    if pdf_filename:
        record["PDF Filename"] = pdf_filename

    table.create(record)
