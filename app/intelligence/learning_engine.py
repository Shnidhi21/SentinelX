import json
from pathlib import Path
from collections import Counter


TRAINING_FILE = Path("data/raw/training_events.json")
DECEPTION_FILE = Path("data/raw/deception_events.json")
LEARNING_FILE = Path("data/processed/learned_threat_patterns.json")


def load_json_file(file_path):
    if not file_path.exists():
        return []

    with open(file_path, "r") as file:
        return json.load(file)


def analyze_threat_patterns(training_events, deception_events):

    learned_patterns = {
        "event_types": Counter(),
        "behaviors": Counter(),
        "source_ips": Counter(),
        "targeted_users": Counter()
    }

    # Learn from security telemetry
    for event in training_events:

        event_type = event.get("event_type")

        if event_type:
            learned_patterns["event_types"][event_type] += 1

    # Learn from deception activity
    for event in deception_events:

        behavior = event.get("behavior")
        source_ip = event.get("source_ip")
        username = event.get("username")

        if behavior:
            learned_patterns["behaviors"][behavior] += 1

        if source_ip:
            learned_patterns["source_ips"][source_ip] += 1

        if username:
            learned_patterns["targeted_users"][username] += 1

    return learned_patterns


def convert_counters_to_dict(learned_patterns):

    return {
        "event_types": dict(
            learned_patterns["event_types"]
        ),
        "behaviors": dict(
            learned_patterns["behaviors"]
        ),
        "source_ips": dict(
            learned_patterns["source_ips"]
        ),
        "targeted_users": dict(
            learned_patterns["targeted_users"]
        )
    }


def save_learned_patterns(patterns):

    LEARNING_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(LEARNING_FILE, "w") as file:
        json.dump(
            patterns,
            file,
            indent=4
        )

    print(
        f"\nLearned threat patterns saved to: "
        f"{LEARNING_FILE}"
    )


def run_learning():

    print("\n=== SENTINELX CONTINUOUS LEARNING ===\n")

    training_events = load_json_file(
        TRAINING_FILE
    )

    deception_events = load_json_file(
        DECEPTION_FILE
    )

    print(
        f"Security telemetry events: "
        f"{len(training_events)}"
    )

    print(
        f"Deception events: "
        f"{len(deception_events)}"
    )

    learned_patterns = analyze_threat_patterns(
        training_events,
        deception_events
    )

    patterns = convert_counters_to_dict(
        learned_patterns
    )

    save_learned_patterns(patterns)

    print("\n=== LEARNED THREAT PATTERNS ===")

    print("\nEvent Types:")
    for event_type, count in patterns["event_types"].items():
        print(
            f"  → {event_type}: {count}"
        )

    print("\nDeception Behaviors:")
    for behavior, count in patterns["behaviors"].items():
        print(
            f"  → {behavior}: {count}"
        )

    print("\nKnown Source IPs:")
    for ip, count in patterns["source_ips"].items():
        print(
            f"  → {ip}: {count}"
        )

    print("\nTargeted Users:")
    for user, count in patterns["targeted_users"].items():
        print(
            f"  → {user}: {count}"
        )

    print("\nLearning cycle complete.")


if __name__ == "__main__":
    run_learning()