import json
from pathlib import Path


LEARNING_FILE = Path(
    "data/processed/learned_threat_patterns.json"
)


def load_learned_patterns():

    if not LEARNING_FILE.exists():
        raise FileNotFoundError(
            "Learned threat patterns not found. "
            "Run learning_engine.py first."
        )

    with open(LEARNING_FILE, "r") as file:
        return json.load(file)


def check_ip(source_ip, patterns):

    known_ips = patterns.get("source_ips", {})

    return {
        "known": source_ip in known_ips,
        "observations": known_ips.get(source_ip, 0)
    }


def check_user(username, patterns):

    targeted_users = patterns.get("targeted_users", {})

    return {
        "known": username in targeted_users,
        "observations": targeted_users.get(username, 0)
    }


def check_behavior(behavior, patterns):

    behaviors = patterns.get("behaviors", {})

    return {
        "known": behavior in behaviors,
        "observations": behaviors.get(behavior, 0)
    }


def match_threat_pattern(
    source_ip,
    username,
    behaviors
):

    patterns = load_learned_patterns()

    ip_result = check_ip(
        source_ip,
        patterns
    )

    user_result = check_user(
        username,
        patterns
    )

    behavior_results = {}

    for behavior in behaviors:

        behavior_results[behavior] = check_behavior(
            behavior,
            patterns
        )

    known_behavior_count = sum(
        1
        for result in behavior_results.values()
        if result["known"]
    )

    unknown_behavior_count = sum(
        1
        for result in behavior_results.values()
        if not result["known"]
    )

    reasons = []

    # Determine threat classification

    if (
        not ip_result["known"]
        and not user_result["known"]
        and unknown_behavior_count > 0
    ):

        threat_classification = "NOVEL_THREAT"

        reasons.append(
            "Previously unseen source IP"
        )

        reasons.append(
            "Previously unseen user"
        )

        reasons.append(
            f"{unknown_behavior_count} previously unseen "
            f"behavior(s)"
        )

    elif ip_result["known"]:

        threat_classification = "KNOWN_THREAT"

        reasons.append(
            f"Source IP previously observed "
            f"({ip_result['observations']} event(s))"
        )

        if user_result["known"]:
            reasons.append(
                f"User previously targeted "
                f"({user_result['observations']} event(s))"
            )

        if known_behavior_count > 0:
            reasons.append(
                f"{known_behavior_count} known threat "
                f"behavior(s) observed"
            )

    elif known_behavior_count > 0:

        threat_classification = "BEHAVIORAL_MATCH"

        reasons.append(
            f"{known_behavior_count} known threat "
            f"behavior(s) observed"
        )

    else:

        threat_classification = "NO_MATCH"

        reasons.append(
            "No previously learned threat patterns matched"
        )

    # Calculate confidence

    threat_matches = 0

    if ip_result["known"]:
        threat_matches += 1

    if user_result["known"]:
        threat_matches += 1

    threat_matches += known_behavior_count

    if threat_classification == "NOVEL_THREAT":
        confidence = "UNKNOWN"

    elif threat_matches >= 4:
        confidence = "HIGH"

    elif threat_matches >= 2:
        confidence = "MEDIUM"

    elif threat_matches >= 1:
        confidence = "LOW"

    else:
        confidence = "UNKNOWN"

    return {
        "source_ip": source_ip,
        "username": username,
        "ip_match": ip_result,
        "user_match": user_result,
        "behavior_matches": behavior_results,
        "threat_matches": threat_matches,
        "threat_classification": threat_classification,
        "confidence": confidence,
        "reasons": reasons
    }


if __name__ == "__main__":

    test_source_ip = "203.0.113.77"
    test_username = "new_user"

    test_behaviors = [
        "LATERAL_MOVEMENT",
        "PERSISTENCE",
        "DEFENSE_EVASION"
    ]

    result = match_threat_pattern(
        source_ip=test_source_ip,
        username=test_username,
        behaviors=test_behaviors
    )

    print(
        "\n=== SENTINELX THREAT PATTERN MATCHER ===\n"
    )

    print(
        f"Source IP: {result['source_ip']}"
    )

    print(
        f"Username: {result['username']}"
    )

    print("\nIP Match:")

    print(
        f"  → Known: "
        f"{result['ip_match']['known']}"
    )

    print(
        f"  → Previous observations: "
        f"{result['ip_match']['observations']}"
    )

    print("\nUser Match:")

    print(
        f"  → Known: "
        f"{result['user_match']['known']}"
    )

    print(
        f"  → Previous observations: "
        f"{result['user_match']['observations']}"
    )

    print("\nBehavior Matches:")

    for behavior, match in result[
        "behavior_matches"
    ].items():

        print(
            f"  → {behavior}: "
            f"{match['known']} "
            f"({match['observations']} observation(s))"
        )

    print(
        f"\nThreat Classification: "
        f"{result['threat_classification']}"
    )

    print(
        f"Threat Matches: "
        f"{result['threat_matches']}"
    )

    print(
        f"Confidence: "
        f"{result['confidence']}"
    )

    print("\nWhy?")

    for reason in result["reasons"]:
        print(f"  → {reason}")