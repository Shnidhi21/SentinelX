import json
from pathlib import Path
import pandas as pd


DATA_FILE = Path("data/raw/training_events.json")


def load_events():
    """Load security events from the training dataset."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Training dataset not found. "
            "Run dataset_generator.py first."
        )

    with open(DATA_FILE, "r") as file:
        return json.load(file)


def create_features():
    """Create behavioral features for SentinelX."""

    events = load_events()

    df = pd.DataFrame(events)

    # Convert timestamp into datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # ---------------------------------------------------------
    # 1. Severity score
    # ---------------------------------------------------------

    severity_mapping = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    df["severity_score"] = df["severity"].map(severity_mapping)

    # ---------------------------------------------------------
    # 2. Event indicators
    # ---------------------------------------------------------

    df["failed_login"] = (
        df["event_type"] == "FAILED_LOGIN"
    ).astype(int)

    df["privilege_escalation"] = (
        df["event_type"] == "PRIVILEGE_ESCALATION"
    ).astype(int)

    df["port_scan"] = (
        df["event_type"] == "PORT_SCAN"
    ).astype(int)

    df["sensitive_file_access"] = (
        df["event_type"] == "SENSITIVE_FILE_ACCESS"
    ).astype(int)

    df["unusual_network"] = (
        df["event_type"] == "UNUSUAL_NETWORK_CONNECTION"
    ).astype(int)

    # ---------------------------------------------------------
    # 3. Time-based behavior
    # ---------------------------------------------------------

    df["hour"] = df["timestamp"].dt.hour

    # Activity between midnight and 5 AM
    df["unusual_hour"] = (
        (df["hour"] >= 0) &
        (df["hour"] <= 5)
    ).astype(int)

    # ---------------------------------------------------------
    # 4. User behavior
    # ---------------------------------------------------------

    df["user_event_count"] = (
        df.groupby("username")["username"]
        .transform("count")
    )

    df["user_failed_login_count"] = (
        df.groupby("username")["failed_login"]
        .transform("sum")
    )

    df["user_failed_login_rate"] = (
        df["user_failed_login_count"] /
        df["user_event_count"]
    )

    # ---------------------------------------------------------
    # 5. IP behavior
    # ---------------------------------------------------------

    df["ip_event_count"] = (
        df.groupby("source_ip")["source_ip"]
        .transform("count")
    )

    df["ip_unique_users"] = (
        df.groupby("source_ip")["username"]
        .transform("nunique")
    )

    # ---------------------------------------------------------
    # 6. File access behavior
    # ---------------------------------------------------------

    file_access_events = (
        df["event_type"] == "FILE_ACCESS"
    ).astype(int)

    sensitive_file_events = (
        df["event_type"] == "SENSITIVE_FILE_ACCESS"
    ).astype(int)

    df["user_file_access_count"] = (
        df.assign(file_access=file_access_events)
        .groupby("username")["file_access"]
        .transform("sum")
    )

    df["user_sensitive_file_access_count"] = (
        df.assign(sensitive=sensitive_file_events)
        .groupby("username")["sensitive"]
        .transform("sum")
    )

    # ---------------------------------------------------------
    # 7. Network behavior
    # ---------------------------------------------------------

    network_events = (
        df["event_type"].isin(
            [
                "NETWORK_CONNECTION",
                "UNUSUAL_NETWORK_CONNECTION"
            ]
        )
    ).astype(int)

    df["user_network_activity"] = (
        df.assign(network=network_events)
        .groupby("username")["network"]
        .transform("sum")
    )

    # ---------------------------------------------------------
    # 8. Process behavior
    # ---------------------------------------------------------

    process_events = (
        df["event_type"] == "PROCESS_START"
    ).astype(int)

    df["user_process_activity"] = (
        df.assign(process=process_events)
        .groupby("username")["process"]
        .transform("sum")
    )

    return df


if __name__ == "__main__":

    features = create_features()

    print("\n=== SENTINELX BEHAVIORAL DATASET ===\n")

    print(f"Total events: {len(features)}")

    print("\nBehavioral features created:")

    feature_columns = [
        "severity_score",
        "failed_login",
        "privilege_escalation",
        "port_scan",
        "sensitive_file_access",
        "unusual_network",
        "hour",
        "unusual_hour",
        "user_event_count",
        "user_failed_login_rate",
        "ip_event_count",
        "ip_unique_users",
        "user_file_access_count",
        "user_sensitive_file_access_count",
        "user_network_activity",
        "user_process_activity"
    ]

    for feature in feature_columns:
        print(f"- {feature}")

    print("\n=== SAMPLE ===\n")

    print(
        features[
            ["username", "event_type", "hour",
             "user_failed_login_rate",
             "user_file_access_count",
             "user_network_activity"]
        ].head(10).to_string(index=False)
    )