MITRE_MAPPING = {
    "FAILED_LOGIN": {
        "technique_id": "T1110",
        "technique": "Brute Force",
        "tactic": "Credential Access"
    },

    "PORT_SCAN": {
        "technique_id": "T1046",
        "technique": "Network Service Scanning",
        "tactic": "Discovery"
    },

    "PRIVILEGE_ESCALATION": {
        "technique_id": "T1068",
        "technique": "Exploitation for Privilege Escalation",
        "tactic": "Privilege Escalation"
    },

    "SENSITIVE_FILE_ACCESS": {
        "technique_id": "T1005",
        "technique": "Data from Local System",
        "tactic": "Collection"
    },

    "UNUSUAL_NETWORK_CONNECTION": {
        "technique_id": "T1071",
        "technique": "Application Layer Protocol",
        "tactic": "Command and Control"
    },

    
}


def map_event_to_mitre(event_type):

    return MITRE_MAPPING.get(
        event_type,
        {
            "technique_id": "UNKNOWN",
            "technique": "Unknown Technique",
            "tactic": "Unknown"
        }
    )


def map_attack_chain(event_types):

    mappings = []

    for event_type in event_types:

        mapping = map_event_to_mitre(event_type)

        if mapping["technique_id"] != "UNKNOWN":
            mappings.append({
                "event_type": event_type,
                **mapping
            })

    return mappings


if __name__ == "__main__":

    test_chain = [
        "FAILED_LOGIN",
        "LOGIN",
        "PROCESS_START",
        "PRIVILEGE_ESCALATION",
        "SENSITIVE_FILE_ACCESS",
        "UNUSUAL_NETWORK_CONNECTION"
    ]

    print("\n=== SENTINELX MITRE ATT&CK ANALYSIS ===\n")

    mappings = map_attack_chain(test_chain)

    for item in mappings:

        print(
            f"{item['event_type']}"
            f" → {item['technique_id']}"
            f" | {item['technique']}"
            f" | {item['tactic']}"
        )