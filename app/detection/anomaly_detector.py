import pandas as pd
from sklearn.ensemble import IsolationForest

from features import create_features


def train_detector():

    # Get our feature data
    df = create_features()

    # These are the features the AI will examine
    feature_columns = [
        "severity_score",
        "failed_login",
        "privilege_escalation",
        "port_scan",
        "sensitive_file_access",
        "unusual_network"
    ]

    X = df[feature_columns]

    # Create the AI anomaly detector
    model = IsolationForest(
        n_estimators=100,
        contamination=0.25,
        random_state=42
    )

    # Train the model
    model.fit(X)

    # Predict anomalies
    df["ai_prediction"] = model.predict(X)

    # Convert sklearn output into human-readable labels
    df["ai_result"] = df["ai_prediction"].map({
        1: "NORMAL",
        -1: "ANOMALY"
    })

    return df


if __name__ == "__main__":

    results = train_detector()

    print("\n=== SENTINELX AI DETECTION ===\n")

    print(
        results[
            [
                "event_type",
                "severity",
                "ai_result"
            ]
        ].to_string(index=False)
    )