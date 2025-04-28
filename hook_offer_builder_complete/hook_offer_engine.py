
import random

def hook_offer_engine(topic: str, brand: str = "") -> dict:
    sample_hooks = [
        f"You don’t need a massive audience to start as a {topic} expert.",
        f"Real growth starts when you stop overthinking and start sharing your value as a {topic}.",
        f"{brand} shows up with clarity, not perfection—and that’s why it converts."
    ]

    sample_ctas = [
        "DM me ‘LAUNCH’ if you're ready to make this real.",
        "Click the link in bio to get your custom strategy."
    ]

    bio_line = f"Helping {topic} experts turn clarity into cashflow."
    offer_name = f"{topic.title()} Monetization Blueprint"
    offer_description = (
        f"A simple but powerful system to help {topic} creators clarify their message, "
        f"structure their offer, and land their first paying clients—even with a small following."
    )
    price = random.choice(["$47", "$97"])
    delivery_method = "PDF Blueprint + 15-Minute Video Walkthrough"
    confidence_score = "Medium – Curious but hesitant"
    time_to_build = "Quick – Can launch in 1–2 days"

    return {
        "hooks": sample_hooks,
        "ctas": sample_ctas,
        "bio_line": bio_line,
        "offer_name": offer_name,
        "offer_description": offer_description,
        "price": price,
        "delivery_method": delivery_method,
        "confidence_score": confidence_score,
        "time_to_build": time_to_build
    }
