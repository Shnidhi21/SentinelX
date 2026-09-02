import json
from datetime import datetime
from pathlib import Path


DECEPTION_LOG = Path("data/raw/deception_events.json")


def classify_activity(activity):

    activity_lower = activity.lower()

    if "connected" in activity_lower:
        return "RECONNAISSANCE"

    elif "login" in activity_lower:
        return "CREDENTIAL_ACCESS"

    elif "enumerated" in activity_lower:
        return "DISCOVERY"

    elif "searched" in activity_lower:
        return "DISCOVERY"

    elif "sensitive file" in activity_lower:
        return "COLLECTION"

    elif "command" in activity_lower:
        return "EXECUTION"

    else:
        return "UNKNOWN"


def log_deception_activity(source_ip, username, activity):

    behavior = classify_activity(activity)

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "source_ip": source_ip,
        "username": username,
        "activity": activity,
        "behavior": behavior
    }

    print("\n=== DECEPTION ACTIVITY ===")
    print(f"Timestamp: {log_entry['timestamp']}")
    print(f"Source IP: {log_entry['source_ip']}")
    print(f"Username: {log_entry['username']}")
    print(f"Activity: {log_entry['activity']}")
    print(f"Behavior: {log_entry['behavior']}")

    return log_entry


def save_deception_events(events):

    DECEPTION_LOG.parent.mkdir(parents=True, exist_ok=True)

    with open(DECEPTION_LOG, "w") as file:
        json.dump(events, file, indent=4)

    print(f"\nDeception events saved to: {DECEPTION_LOG}")


def activate_deception(source_ip, username):

    deception_target = "DECOY_SERVER_01"

    return {
        "deception_activated": True,
        "source_ip": source_ip,
        "username": username,
        "deception_target": deception_target,
        "message": "Suspicious activity redirected to deception environment."
    }


def simulate_attacker_activity(source_ip, username):

    activities = [
        "Connected to decoy server",
        "Attempted login",
        "Enumerated directories",
        "Searched for configuration files",
        "Attempted access to sensitive file",
        "Attempted command execution"
    ]

    activity_log = []

    for activity in activities:

        event = log_deception_activity(
            source_ip=source_ip,
            username=username,
            activity=activity
        )

        activity_log.append(event)

    return activity_log


if __name__ == "__main__":

    result = activate_deception(
        source_ip="185.73.44.21",
        username="admin"
    )

    print("\n=== SENTINELX DECEPTION ENGINE ===\n")

    print(f"Deception Activated: {result['deception_activated']}")
    print(f"Source IP: {result['source_ip']}")
    print(f"Username: {result['username']}")
    print(f"Deception Target: {result['deception_target']}")
    print(f"Message: {result['message']}")

    activity_log = simulate_attacker_activity(
        source_ip=result["source_ip"],
        username=result["username"]
    )

    save_deception_events(activity_log)

    print("\n=== ATTACKER ACTIVITY SUMMARY ===")
    print(f"Activities captured: {len(activity_log)}")