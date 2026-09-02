import json
import random
from datetime import datetime, timedelta
from pathlib import Path


OUTPUT_FILE = Path("data/raw/training_events.json")


NORMAL_USERS = [
    "alice",
    "bob",
    "charlie",
    "david",
    "emma"
]

NORMAL_IPS = [
    "192.168.1.10",
    "192.168.1.15",
    "192.168.1.20",
    "192.168.1.25",
    "192.168.1.30"
]

ATTACKER_IPS = [
    "185.73.44.21",
    "91.204.17.63",
    "103.45.88.12",
    "172.67.19.44"
]


def generate_normal_event(timestamp):

    event_types = [
        "LOGIN",
        "FILE_ACCESS",
        "PROCESS_START",
        "NETWORK_CONNECTION",
        "LOGOUT"
    ]

    event_type = random.choice(event_types)

    return {
        "timestamp": timestamp.isoformat(),
        "event_type": event_type,
        "username": random.choice(NORMAL_USERS),
        "source_ip": random.choice(NORMAL_IPS),
        "details": "Normal user activity",
        "severity": "LOW"
    }


def generate_suspicious_event(timestamp):

    event_types = [
        "FAILED_LOGIN",
        "PORT_SCAN",
        "PRIVILEGE_ESCALATION",
        "SENSITIVE_FILE_ACCESS",
        "UNUSUAL_NETWORK_CONNECTION"
    ]

    event_type = random.choice(event_types)

    severity = random.choice([
        "MEDIUM",
        "HIGH"
    ])

    return {
        "timestamp": timestamp.isoformat(),
        "event_type": event_type,
        "username": random.choice(
            NORMAL_USERS + ["admin", "unknown"]
        ),
        "source_ip": random.choice(ATTACKER_IPS),
        "details": "Suspicious activity detected",
        "severity": severity
    }


def generate_dataset(
    normal_count=2000,
    suspicious_count=500
):

    events = []

    start_time = datetime.now() - timedelta(days=30)

    # Generate normal activity
    for i in range(normal_count):

        timestamp = start_time + timedelta(
            minutes=random.randint(0, 43200)
        )

        events.append(
            generate_normal_event(timestamp)
        )

    # Generate suspicious activity
    for i in range(suspicious_count):

        timestamp = start_time + timedelta(
            minutes=random.randint(0, 43200)
        )

        events.append(
            generate_suspicious_event(timestamp)
        )

    # Shuffle events so they aren't grouped by type
    random.shuffle(events)

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(OUTPUT_FILE, "w") as file:
        json.dump(
            events,
            file,
            indent=4
        )

    print(
        f"Dataset created successfully: "
        f"{len(events)} events"
    )

    print(
        f"Normal events: {normal_count}"
    )

    print(
        f"Suspicious events: {suspicious_count}"
    )

    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":

    generate_dataset()