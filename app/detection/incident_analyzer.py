from pathlib import Path
import sys

# Allow Python to find the app package
sys.path.append(str(Path(__file__).resolve().parents[1]))

from detection.attack_chain import analyze_attack_chain
from detection.mitre_mapper import map_attack_chain
from detection.risk_engine import calculate_risk_score
from response.response_engine import determine_response

from intelligence.threat_intelligence import (
    load_deception_events,
    generate_threat_intelligence
)

from intelligence.pattern_matcher import (
    match_threat_pattern
)


def analyze_incident(events, ai_result, severity_score):

    # 1. Analyze attack chain
    attack_result = analyze_attack_chain(events)

    # 2. Extract observed attack stages
    attack_stages = attack_result["matched_steps"]

    # 3. Map attack stages to MITRE ATT&CK
    mitre_mappings = map_attack_chain(attack_stages)

    # 4. Calculate overall risk
    risk_result = calculate_risk_score(
        ai_result=ai_result,
        severity_score=severity_score,
        attack_stages=len(attack_stages),
        mitre_techniques=len(mitre_mappings)
    )

    # 5. Determine automated response
    response_result = determine_response(
        risk_result["risk_level"]
    )

    # 6. Generate threat intelligence
    deception_events = load_deception_events()

    threat_intelligence = generate_threat_intelligence(
        deception_events
    )

    # 7. Extract intelligence for pattern matching
    source_ip = "unknown"
    username = "unknown"

    if events:
        source_ip = events[0].get(
            "source_ip",
            "unknown"
        )

        username = events[0].get(
            "username",
            "unknown"
        )

    # 8. Extract deception behaviors
    behaviors = threat_intelligence.get(
        "behaviors",
        []
    )

    # 9. Match current threat against learned patterns
    pattern_result = match_threat_pattern(
        source_ip=source_ip,
        username=username,
        behaviors=behaviors
    )

    # 10. Return complete incident analysis
    return {
        "ai_result": ai_result,
        "attack_detected": attack_result["attack_detected"],
        "attack_stages": attack_stages,
        "mitre_mappings": mitre_mappings,
        "risk_score": risk_result["risk_score"],
        "risk_level": risk_result["risk_level"],
        "risk_reasons": risk_result["reasons"],
        "response_action": response_result["action"],
        "response_description": response_result["description"],
        "threat_intelligence": threat_intelligence,
        "pattern_analysis": pattern_result
    }


if __name__ == "__main__":

    test_events = [
        {
            "event_type": "FAILED_LOGIN",
            "source_ip": "185.73.44.21",
            "username": "admin"
        },
        {
            "event_type": "LOGIN",
            "source_ip": "185.73.44.21",
            "username": "admin"
        },
        {
            "event_type": "PROCESS_START",
            "source_ip": "185.73.44.21",
            "username": "admin"
        },
        {
            "event_type": "PRIVILEGE_ESCALATION",
            "source_ip": "185.73.44.21",
            "username": "admin"
        },
        {
            "event_type": "SENSITIVE_FILE_ACCESS",
            "source_ip": "185.73.44.21",
            "username": "admin"
        },
        {
            "event_type": "UNUSUAL_NETWORK_CONNECTION",
            "source_ip": "185.73.44.21",
            "username": "admin"
        }
    ]

    result = analyze_incident(
        events=test_events,
        ai_result="ANOMALY",
        severity_score=3
    )

    print(
        "\n=== SENTINELX INCIDENT ANALYZER ===\n"
    )

    print(
        f"AI Result: "
        f"{result['ai_result']}"
    )

    print(
        f"Attack Detected: "
        f"{result['attack_detected']}"
    )

    print(
        f"Risk Score: "
        f"{result['risk_score']}/100"
    )

    print(
        f"Risk Level: "
        f"{result['risk_level']}"
    )

    print("\nWhy was this risk score assigned?")

    for reason in result["risk_reasons"]:
        print(f"  → {reason}")

    print("\nAttack Stages:")

    for stage in result["attack_stages"]:
        print(f"  → {stage}")

    print("\nMITRE ATT&CK:")

    for mapping in result["mitre_mappings"]:

        print(
            f"  → {mapping['technique_id']} | "
            f"{mapping['technique']} | "
            f"{mapping['tactic']}"
        )

    print("\nAutomated Response:")

    print(
        f"  → {result['response_action']}"
    )

    print(
        f"  → {result['response_description']}"
    )

    print("\nThreat Intelligence:")

    intelligence = result[
        "threat_intelligence"
    ]

    print(
        f"  → Threat Level: "
        f"{intelligence['threat_level']}"
    )

    print(
        f"  → Activity Count: "
        f"{intelligence['activity_count']}"
    )

    print("\nSource IPs:")

    for ip in intelligence["source_ips"]:
        print(f"  → {ip}")

    print("\nTargeted Users:")

    for user in intelligence["targeted_users"]:
        print(f"  → {user}")

    print("\nObserved Behaviors:")

    for behavior, count in intelligence[
        "behavior_counts"
    ].items():

        print(
            f"  → {behavior}: {count}"
        )

    print("\nIntelligence Summary:")

    print(
        f"  → {intelligence['summary']}"
    )

    print("\nThreat Pattern Analysis:")

    pattern = result[
        "pattern_analysis"
    ]

    print(
        f"  → Classification: "
        f"{pattern['threat_classification']}"
    )

    print(
        f"  → Confidence: "
        f"{pattern['confidence']}"
    )

    print(
        f"  → Threat Matches: "
        f"{pattern['threat_matches']}"
    )

    print("\nPattern Analysis Reasons:")

    for reason in pattern["reasons"]:
        print(f"  → {reason}")