def calculate_risk_score(
    ai_result,
    severity_score,
    attack_stages,
    mitre_techniques
):
    score = 0
    reasons = []

    # AI anomaly
    if ai_result == "ANOMALY":
        score += 30
        reasons.append("AI detected anomalous behavior")

    # Severity
    severity_points = min(severity_score * 10, 30)
    score += severity_points

    if severity_score >= 3:
        reasons.append("High event severity detected")

    # Attack chain
    attack_points = min(attack_stages * 5, 25)
    score += attack_points

    if attack_stages >= 3:
        reasons.append(
            f"Multi-stage attack behavior detected ({attack_stages} stages)"
        )

    # MITRE techniques
    mitre_points = min(mitre_techniques * 3, 15)
    score += mitre_points

    if mitre_techniques >= 2:
        reasons.append(
            f"Multiple MITRE ATT&CK techniques identified ({mitre_techniques})"
        )

    score = min(score, 100)

    if score >= 80:
        risk_level = "CRITICAL"
    elif score >= 60:
        risk_level = "HIGH"
    elif score >= 30:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons
    }


if __name__ == "__main__":

    result = calculate_risk_score(
        ai_result="ANOMALY",
        severity_score=3,
        attack_stages=5,
        mitre_techniques=4
    )

    print("\n=== SENTINELX RISK ENGINE ===\n")

    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_level']}")

    print("\nWhy was this risk score assigned?")
    for reason in result["reasons"]:
        print(f"  → {reason}")