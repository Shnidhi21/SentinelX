import json
from pathlib import Path
from collections import Counter


DECEPTION_LOG = Path("data/raw/deception_events.json")


def load_deception_events():

    if not DECEPTION_LOG.exists():
        raise FileNotFoundError(
            "Deception events not found. "
            "Run deception_engine.py first."
        )

    with open(DECEPTION_LOG, "r") as file:
        return json.load(file)


def generate_threat_intelligence(events):

    if not events:
        return {
            "threat_level": "LOW",
            "source_ips": [],
            "targeted_users": [],
            "behaviors": [],
            "activity_count": 0,
            "summary": "No suspicious activity observed."
        }

    source_ips = list(
        set(event["source_ip"] for event in events)
    )

    targeted_users = list(
        set(event["username"] for event in events)
    )

    behavior_counts = Counter(
        event["behavior"] for event in events
    )

    behaviors = list(behavior_counts.keys())

    activity_count = len(events)

    if activity_count >= 6:
        threat_level = "CRITICAL"
    elif activity_count >= 4:
        threat_level = "HIGH"
    elif activity_count >= 2:
        threat_level = "MEDIUM"
    else:
        threat_level = "LOW"

    summary = (
        f"Observed {activity_count} suspicious activities "
        f"from {len(source_ips)} source IP(s), "
        f"targeting {len(targeted_users)} user(s)."
    )

    return {
        "threat_level": threat_level,
        "source_ips": source_ips,
        "targeted_users": targeted_users,
        "behaviors": behaviors,
        "behavior_counts": dict(behavior_counts),
        "activity_count": activity_count,
        "summary": summary
    }


if __name__ == "__main__":

    events = load_deception_events()

    intelligence = generate_threat_intelligence(events)

    print("\n=== SENTINELX THREAT INTELLIGENCE ===\n")

    print(f"Threat Level: {intelligence['threat_level']}")
    print(f"Activity Count: {intelligence['activity_count']}")

    print("\nSource IPs:")
    for ip in intelligence["source_ips"]:
        print(f"  → {ip}")

    print("\nTargeted Users:")
    for user in intelligence["targeted_users"]:
        print(f"  → {user}")

    print("\nObserved Behaviors:")
    for behavior, count in intelligence["behavior_counts"].items():
        print(f"  → {behavior}: {count}")

    print("\nIntelligence Summary:")
    print(f"  → {intelligence['summary']}")