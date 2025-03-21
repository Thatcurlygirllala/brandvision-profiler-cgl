import os
from pyairtable import Api, Table

# ✅ Airtable Credentials (Stored in Environment Variables for Security)
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# ✅ Airtable Tables
CLIENTS_TABLE = "Clients"
REPORTS_TABLE = "Reports"
AFFILIATE_TABLE = "Affiliates"
EMAIL_REPORTS_TABLE = "Email Reports"
PAYMENTS_TABLE = "Payments"
TASK_TABLE = "Task Table"
AI_REPORTS_TABLE = "AI Reports"
SOCIAL_CALENDAR_TABLE = "Social Media Calendars"

# ✅ Initialize Airtable API
api = Api(AIRTABLE_API_KEY)


# ✅ Function to Store AI-Generated Social Media Calendar
def store_social_calendar(user_id, niche, plan_type, calendar_content, brand_audit_score):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, SOCIAL_CALENDAR_TABLE)
        record = {
            "User ID": user_id,
            "Niche": niche,
            "Plan Type": plan_type,
            "Calendar Content": calendar_content,
            "Brand Audit Score": brand_audit_score
        }
        table.create(record)
        print(f"✅ Social Media Calendar for {niche} stored successfully!")
    except Exception as e:
        print(f"❌ ERROR: Failed to store calendar in Airtable - {str(e)}")


# ✅ Function to Store AI-Generated Branding Reports
def store_branding_report(client_id, client_name, report_type, competitor_insights, brand_audit_score, download_link):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, REPORTS_TABLE)
        record = {
            "Client ID": client_id,
            "Client Name": client_name,
            "Report Type": report_type,
            "Competitor Analyzed": competitor_insights,
            "Brand Audit Score": brand_audit_score,
            "Download Link": download_link
        }
        table.create(record)
        print(f"✅ Branding Report stored successfully for {client_name}")
    except Exception as e:
        print(f"❌ ERROR: Failed to store branding report in Airtable - {str(e)}")


# ✅ Function to Store Affiliate & Commission Data
def store_affiliate_referral(client_id, affiliate_name, referral_code, commission_amount, total_sales):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, AFFILIATE_TABLE)
        record = {
            "Client ID": client_id,
            "Affiliate Name": affiliate_name,
            "Referral Code": referral_code,
            "Total Sales Generated": total_sales,
            "Commission Earned": commission_amount,
            "Affiliate Status": "Active"
        }
        table.create(record)
        print(f"✅ Affiliate referral for {affiliate_name} stored successfully!")
    except Exception as e:
        print(f"❌ ERROR: Failed to store affiliate referral - {str(e)}")


# ✅ Function to Log Email Reports
def log_email_report(email_id, client_id, email_type, subject, body, sent_date, delivery_status):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, EMAIL_REPORTS_TABLE)
        record = {
            "Email ID": email_id,
            "Client ID": client_id,
            "Email Type": email_type,
            "Subject": subject,
            "Body": body,
            "Sent Date": sent_date,
            "Delivery Status": delivery_status
        }
        table.create(record)
        print(f"✅ Email report logged successfully for Client ID {client_id}")
    except Exception as e:
        print(f"❌ ERROR: Failed to log email report - {str(e)}")


# ✅ Function to Store Payments & Transactions
def store_payment(client_id, client_name, amount_paid, payment_date, payment_method, payment_status):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, PAYMENTS_TABLE)
        record = {
            "Client ID": client_id,
            "Client Name": client_name,
            "Amount Paid": amount_paid,
            "Payment Date": payment_date,
            "Payment Method": payment_method,
            "Payment Status": payment_status
        }
        table.create(record)
        print(f"✅ Payment record stored successfully for {client_name}")
    except Exception as e:
        print(f"❌ ERROR: Failed to store payment record - {str(e)}")


# ✅ Function to Store Task Assignments
def store_task(task_id, client_id, task_name, assigned_to, due_date, status):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, TASK_TABLE)
        record = {
            "Task ID": task_id,
            "Client ID": client_id,
            "Task Name": task_name,
            "Assigned To": assigned_to,
            "Date Due": due_date,
            "Status": status
        }
        table.create(record)
        print(f"✅ Task record stored successfully for Client ID {client_id}")
    except Exception as e:
        print(f"❌ ERROR: Failed to store task record - {str(e)}")


# ✅ Function to Store AI Reports
def store_ai_report(report_id, client_name, report_type, ai_report_content, generated_date, brand_audit_score, report_status):
    try:
        table = Table(AIRTABLE_API_KEY, BASE_ID, AI_REPORTS_TABLE)
        record = {
            "Report ID": report_id,
            "Client Name": client_name,
            "Report Type": report_type,
            "AI Reports Table Content": ai_report_content,
            "Generated Date": generated_date,
            "Brand Audit Score": brand_audit_score,
            "Report Status": report_status
        }
        table.create(record)
        print(f"✅ AI Report stored successfully for {client_name}")
    except Exception as e:
        print(f"❌ ERROR: Failed to store AI Report - {str(e)}")
from pyairtable import Api

# Airtable API Configuration
AIRTABLE_API_KEY = "YOUR_AIRTABLE_API_KEY"
BASE_ID = "app4XhsFd5eKT76QK"

def store_ai_report(client_id, report_url):
    """
    Saves AI-generated branding reports in Airtable.
    """
    table = Api(AIRTABLE_API_KEY).table(BASE_ID, "AI Reports")
    
    record = {
        "Client ID": client_id,
        "Report URL": report_url,
        "Generated Date": str(datetime.date.today())
    }

    table.create(record)
