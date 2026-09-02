def determine_response(risk_level):

    if risk_level == "CRITICAL":
        action = "BLOCK_AND_DECEIVE"
        description = "Block the threat and activate deception."

    elif risk_level == "HIGH":
        action = "ISOLATE"
        description = "Isolate the affected system."

    elif risk_level == "MEDIUM":
        action = "ALERT"
        description = "Generate a security alert for investigation."

    else:
        action = "MONITOR"
        description = "Continue monitoring the activity."

    return {
        "risk_level": risk_level,
        "action": action,
        "description": description
    }


if __name__ == "__main__":

    result = determine_response("CRITICAL")

    print("\n=== SENTINELX RESPONSE ENGINE ===\n")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Response Action: {result['action']}")
    print(f"Description: {result['description']}")