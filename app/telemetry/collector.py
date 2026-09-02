from datetime import datetime
import json
from pathlib import Path


DATA_FILE = Path("data/raw/security_events.json")


def record_event(
    event_type,
    username,
    source_ip,
    details,
    severity="LOW"
):
    """Create and save a security event."""

    event = {
        "timestamp": datetime.now().isoformat(),
        "event_type": event_type,
        "username": username,
        "source_ip": source_ip,
        "details": details,
        "severity": severity
    }

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as file:
            events = json.load(file)
    else:
        events = []

    events.append(event)

    with open(DATA_FILE, "w") as file:
        json.dump(events, file, indent=4)

    print(
        f"[{severity}] {event_type} | "
        f"User: {username} | "
        f"IP: {source_ip}"
    )


def generate_test_events():
    """Generate normal and suspicious security activity."""

    events = [

        # NORMAL ACTIVITY

        {
            "event_type": "LOGIN",
            "username": "alice",
            "source_ip": "192.168.1.20",
            "details": "Successful login",
            "severity": "LOW"
        },

        {
            "event_type": "FILE_ACCESS",
            "username": "alice",
            "source_ip": "192.168.1.20",
            "details": "Opened project documentation",
            "severity": "LOW"
        },

        {
            "event_type": "PROCESS_START",
            "username": "alice",
            "source_ip": "192.168.1.20",
            "details": "Started Microsoft Edge",
            "severity": "LOW"
        },

        # SUSPICIOUS ACTIVITY

        {
            "event_type": "FAILED_LOGIN",
            "username": "admin",
            "source_ip": "185.73.44.21",
            "details": "Multiple failed login attempts",
            "severity": "MEDIUM"
        },

        {
            "event_type": "PRIVILEGE_ESCALATION",
            "username": "admin",
            "source_ip": "185.73.44.21",
            "details": "Attempted privilege escalation",
            "severity": "HIGH"
        },

        {
            "event_type": "PORT_SCAN",
            "username": "unknown",
            "source_ip": "185.73.44.21",
            "details": "Multiple ports scanned",
            "severity": "HIGH"
        },

        {
            "event_type": "SENSITIVE_FILE_ACCESS",
            "username": "admin",
            "source_ip": "185.73.44.21",
            "details": "Attempted access to sensitive database",
            "severity": "HIGH"
        },

        {
            "event_type": "UNUSUAL_NETWORK_CONNECTION",
            "username": "admin",
            "source_ip": "185.73.44.21",
            "details": "Connection to previously unseen external host",
            "severity": "HIGH"
        }
    ]

    for event in events:
        record_event(**event)


if __name__ == "__main__":
    generate_test_events()