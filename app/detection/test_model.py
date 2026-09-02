import joblib
import pandas as pd
from pathlib import Path


MODEL_FILE = Path("app/detection/sentinelx_model.pkl")


FEATURE_COLUMNS = [
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


def create_new_event():
    """
    Create a security event that SentinelX has not seen directly.
    """

    event = {
    "severity_score": 1,
    "failed_login": 0,
    "privilege_escalation": 0,
    "port_scan": 0,
    "sensitive_file_access": 0,
    "unusual_network": 0,

    "hour": 3,
    "unusual_hour": 1,

    "user_event_count": 5,
    "user_failed_login_rate": 0.0,

    "ip_event_count": 5,
    "ip_unique_users": 4,

    "user_file_access_count": 2,
    "user_sensitive_file_access_count": 0,

    "user_network_activity": 150,
    "user_process_activity": 1
}

    return pd.DataFrame([event])[FEATURE_COLUMNS]


def test_model():

    print("\n=== SENTINELX BEHAVIORAL AI TEST ===\n")

    if not MODEL_FILE.exists():
        print("Model not found.")
        return

    model = joblib.load(MODEL_FILE)

    X = create_new_event()

    prediction = model.predict(X)[0]

    if prediction == -1:
        result = "ANOMALY"
    else:
        result = "NORMAL"

    print("New behavioral event tested.")
    print(f"AI Decision: {result}")


if __name__ == "__main__":
    test_model()