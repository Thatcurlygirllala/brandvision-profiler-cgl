import requests

# WeWeb API Configuration
WEWEB_API_KEY = "YOUR_WEWEB_API_KEY"

def update_client_dashboard(client_id, branding_report_url):
    """
    Updates the WeWeb Client Dashboard with the latest AI-generated branding report.
    """
    payload = {
        "client_id": client_id,
        "branding_report_url": branding_report_url
    }

    response = requests.post("https://api.weweb.io/update-dashboard", json=payload, headers={"Authorization": f"Bearer {WEWEB_API_KEY}"})
    
    return response.json()

def update_admin_dashboard(admin_id, total_reports, active_users):
    """
    Updates the Admin Dashboard with usage analytics and report status.
    """
    payload = {
        "admin_id": admin_id,
        "total_reports": total_reports,
        "active_users": active_users
    }

    response = requests.post("https://api.weweb.io/update-admin-dashboard", json=payload, headers={"Authorization": f"Bearer {WEWEB_API_KEY}"})
    
    return response.json()