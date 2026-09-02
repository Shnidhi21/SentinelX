from datetime import datetime


# Order of behaviors that can form an attack chain
ATTACK_SEQUENCE = [
    "FAILED_LOGIN",
    "LOGIN",
    "PROCESS_START",
    "PRIVILEGE_ESCALATION",
    "SENSITIVE_FILE_ACCESS",
    "UNUSUAL_NETWORK_CONNECTION"
]


def analyze_attack_chain(events):
    """
    Analyze a sequence of security events and identify
    possible multi-stage attack behavior.
    """

    if not events:
        return {
            "attack_detected": False,
            "matched_steps": [],
            "risk_score": 0
        }

    matched_steps = []

    for event in events:
        event_type = event.get("event_type")

        if event_type in ATTACK_SEQUENCE:
            matched_steps.append(event_type)

    # Remove duplicates while preserving order
    matched_steps = list(dict.fromkeys(matched_steps))

    # Calculate risk based on how many attack stages appeared
    risk_score = min(len(matched_steps) * 20, 100)

    # Require at least 3 different stages
    attack_detected = len(matched_steps) >= 3

    return {
        "attack_detected": attack_detected,
        "matched_steps": matched_steps,
        "risk_score": risk_score
    }


def print_attack_analysis(result):

    print("\n=== SENTINELX ATTACK CHAIN ANALYSIS ===\n")

    if result["attack_detected"]:
        print("⚠ POSSIBLE MULTI-STAGE ATTACK DETECTED")

        print(f"\nRisk Score: {result['risk_score']}/100")

        print("\nAttack stages observed:")

        for step in result["matched_steps"]:
            print(f"  → {step}")

    else:
        print("No multi-stage attack detected.")

        print(f"\nRisk Score: {result['risk_score']}/100")


if __name__ == "__main__":

    # Test attack sequence
    test_events = [
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "FAILED_LOGIN"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "LOGIN"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "PROCESS_START"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "PRIVILEGE_ESCALATION"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "SENSITIVE_FILE_ACCESS"
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "UNUSUAL_NETWORK_CONNECTION"
        }
    ]

    result = analyze_attack_chain(test_events)

    print_attack_analysis(result)