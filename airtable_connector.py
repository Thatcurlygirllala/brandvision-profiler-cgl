import os
from pyairtable import Api

# Load your environment variables (optional depending on app structure)
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
SWIPE_COPY_TABLE = os.getenv("SWIPE_COPY_TABLE")  # Or the name/id of your Swipe Copy Airtable Table

api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, SWIPE_COPY_TABLE)

def save_to_airtable(record_data):
    """
    Saves a record to Airtable Swipe Copy Table.
    Expects 'record_data' as a dictionary matching the table's fields.
    """
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID or not SWIPE_COPY_TABLE:
        raise ValueError("Missing Airtable configuration environment variables.")
    
    try:
        table.create(record_data)
    except Exception as e:
        print(f"Error saving to Airtable: {e}")