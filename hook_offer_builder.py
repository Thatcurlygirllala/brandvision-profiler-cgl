
def generate_hook_offer_blueprint(user_tier: str, brand: str, topic: str) -> dict:
    """
    Generates swipe copy + offer based on user tier.
    Returns the file path to the appropriate PDF output.
    """
    if user_tier in ["Premium", "Power", "Accelerator"]:
        return {
            "status": "full",
            "pdf_path": "hook_offer_blueprint_upsell.pdf",
            "message": "Full swipe + offer blueprint generated successfully."
        }
    else:
        return {
            "status": "preview",
            "pdf_path": "hook_offer_blueprint_preview.pdf",
            "message": "Preview version generated. Upgrade to unlock full swipe + offer packs."
        }
