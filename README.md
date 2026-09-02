# SentinelX

### AI-Powered Cybersecurity Threat Detection & Response Platform

SentinelX is a cybersecurity platform designed to detect suspicious behavioral patterns, correlate multi-stage attack activity, map incidents to MITRE ATT&CK techniques, assess risk, and recommend automated defensive responses.

## Why SentinelX?

Traditional security systems often rely heavily on known signatures and predefined indicators.

SentinelX explores a behavioral approach by combining:

- AI-based anomaly detection
- Behavioral feature analysis
- Attack-chain correlation
- MITRE ATT&CK mapping
- Risk scoring
- Threat intelligence
- Threat-pattern matching
- Automated response recommendations
- Deception mechanisms
- Continuous threat-pattern learning

## Architecture

```text
Security Events
       ↓
Telemetry Collection
       ↓
Feature Engineering
       ↓
AI Anomaly Detection
       ↓
Attack-Chain Correlation
       ↓
MITRE ATT&CK Mapping
       ↓
Risk Assessment
       ↓
Threat Intelligence
       ↓
Pattern Analysis
       ↓
Key Features
AI Anomaly Detection

Uses an Isolation Forest model to identify behavioral anomalies in security telemetry.

Behavioral Analysis

Extracts behavioral features such as:

Failed-login rate
Privilege escalation activity
Port scanning
Sensitive-file access
Unusual network activity
Process activity
User activity patterns
IP activity patterns
Unusual activity hours
Attack-Chain Detection

Correlates multiple security events to identify potential multi-stage attack behavior.

MITRE ATT&CK Mapping

Maps detected behaviors to relevant MITRE ATT&CK techniques and tactics.

Current mappings include:

Technique	MITRE ID	Tactic
Brute Force	T1110	Credential Access
Network Service Scanning	T1046	Discovery
Exploitation for Privilege Escalation	T1068	Privilege Escalation
Data from Local System	T1005	Collection
Application Layer Protocol	T1071	Command and Control
Risk Engine

Combines multiple security signals into a unified risk score from 0–100.

Risk levels:

LOW
MEDIUM
HIGH
CRITICAL
Automated Response

Based on risk severity, SentinelX can recommend:

Risk Level	Response
LOW	Monitor
MEDIUM	Alert
HIGH	Isolate
CRITICAL	Block & Deceive
Threat Intelligence

Analyzes observed attacker behavior, source IPs, targeted users, and activity patterns.

Deception Engine

Simulates defensive deception by redirecting suspicious activity toward decoy environments and recording attacker behavior.

Threat Pattern Learning

Stores previously observed threat patterns and compares future incidents against learned behavior.

Technology Stack
Python
FastAPI
Streamlit
Pandas
NumPy
Scikit-learn
Pydantic
Joblib
REST API
MITRE ATT&CK
Git & GitHub
Project Structure
SentinelX/
│
├── app/
│   ├── detection/
│   │   ├── anomaly_detector.py
│   │   ├── features.py
│   │   ├── train_model.py
│   │   ├── test_model.py
│   │   ├── attack_chain.py
│   │   ├── mitre_mapper.py
│   │   ├── risk_engine.py
│   │   └── incident_analyzer.py
│   │
│   ├── telemetry/
│   │   ├── collector.py
│   │   └── dataset_generator.py
│   │
│   ├── response/
│   │   └── response_engine.py
│   │
│   ├── deception/
│   │   └── deception_engine.py
│   │
│   ├── intelligence/
│   │   ├── threat_intelligence.py
│   │   ├── learning_engine.py
│   │   └── pattern_matcher.py
│   │
│   ├── main.py
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
Running SentinelX
1. Clone the repository
git clone https://github.com/Shnidhi21/SentinelX.git
cd SentinelX
2. Create a virtual environment
python -m venv venv
3. Activate the environment

Windows:

venv\Scripts\activate
4. Install dependencies
pip install -r requirements.txt
5. Generate the training dataset
python app/telemetry/dataset_generator.py
6. Train the anomaly detection model
python app/detection/train_model.py
7. Start the FastAPI backend
uvicorn app.main:app --reload

API documentation:

http://127.0.0.1:8000/docs
8. Start the dashboard

Open another terminal:

streamlit run app/dashboard.py
Example Detection Pipeline

A simulated incident can contain activity such as:

FAILED_LOGIN
      ↓
LOGIN
      ↓
PROCESS_START
      ↓
PRIVILEGE_ESCALATION
      ↓
SENSITIVE_FILE_ACCESS
      ↓
UNUSUAL_NETWORK_CONNECTION

SentinelX correlates these events and produces:

AI Detection       → ANOMALY
Attack Chain       → DETECTED
MITRE Techniques   → IDENTIFIED
Risk Score         → 97/100
Risk Level         → CRITICAL
Response           → BLOCK_AND_DECEIVE
Important Note

SentinelX is a research and learning project exploring behavioral anomaly detection and automated security response.

The current implementation uses synthetic security telemetry and simulated attack scenarios. It should not be interpreted as a production-grade intrusion detection system or as proof of true zero-day detection.

Future evaluation will focus on testing the system against genuinely held-out attack behaviors that were not represented during model development.

Future Improvements
Real-time system telemetry collection
Network traffic analysis
Cloud security monitoring
PostgreSQL/OpenSearch integration
Real-time alerting
Docker deployment
AWS integration
More robust attack-chain correlation
Adversarial testing
Evaluation using unseen attack datasets
Improved automated containment
LLM-assisted incident explanation
Project Goal

The long-term goal of SentinelX is to explore how AI, behavioral analytics, threat intelligence, deception, and automated response can work together to create a more adaptive cybersecurity defense system.
Automated Response
       ↓
Deception & Learning
