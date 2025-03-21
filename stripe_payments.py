import stripe

stripe.api_key = "YOUR_STRIPE_SECRET_KEY"

def create_checkout_session(customer_email, plan_type):
    """
    Creates a Stripe Checkout session for new subscriptions and one-time payments.
    """
    prices = {
        "Pro": "price_123456789", 
        "Premium": "price_987654321",
        "AI_Business_Accelerator": "price_543219876"
    }

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer_email=customer_email,
        line_items=[{"price": prices[plan_type], "quantity": 1}],
        mode="subscription",
        success_url="https://yourwebsite.com/success",
        cancel_url="https://yourwebsite.com/cancel"
    )

    return session.url