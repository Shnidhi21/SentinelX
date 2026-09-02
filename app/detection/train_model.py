from pathlib import Path
import joblib
from sklearn.ensemble import IsolationForest
from features import create_features


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


def train_model():

    print("\nLoading security dataset...")

    df = create_features()

    X = df[FEATURE_COLUMNS]

    print(f"Training samples: {len(X)}")
    print(f"Features used: {len(FEATURE_COLUMNS)}")

    print("\nTraining SentinelX behavioral AI detector...")

    model = IsolationForest(
        n_estimators=200,
        contamination=0.20,
        random_state=42
    )

    model.fit(X)

    predictions = model.predict(X)

    df["prediction"] = predictions

    df["result"] = df["prediction"].map({
        1: "NORMAL",
        -1: "ANOMALY"
    })

    MODEL_FILE.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(model, MODEL_FILE)

    print("\nTraining complete.")

    print(f"Model saved to: {MODEL_FILE}")

    print("\nDetection summary:")

    print(df["result"].value_counts())

    return model


if __name__ == "__main__":
    train_model()