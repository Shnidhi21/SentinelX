import textwrap
import streamlit as st
import requests
import html


# ============================================================
# HTML RENDER HELPER
# ============================================================

def render_html(content, *args, **kwargs):
    return st.html(
        textwrap.dedent(content).strip()
    )


# ============================================================
# SENTINELX - SECURITY OPERATIONS DASHBOARD
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="SentinelX | Security Operations",
    page_icon="S",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

if "result" not in st.session_state:
    st.session_state.result = None


# ============================================================
# THEME
# ============================================================

if st.session_state.dark_mode:

    BG = "#050914"
    CARD = "#0b1220"
    CARD_2 = "#0f192b"
    TEXT = "#f4f7fb"
    MUTED = "#8b9bb5"
    BORDER = "#1c2b43"
    BLUE = "#27b7ff"
    GREEN = "#20e58a"
    RED = "#ff4d55"
    ORANGE = "#ffad1f"

else:

    BG = "#f4f7fb"
    CARD = "#ffffff"
    CARD_2 = "#eef4fa"
    TEXT = "#111827"
    MUTED = "#64748b"
    BORDER = "#d6e0ea"
    BLUE = "#078bd6"
    GREEN = "#079455"
    RED = "#dc2626"
    ORANGE = "#d97706"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>

.stApp {{
    background:
        radial-gradient(circle at 10% 10%, rgba(39,183,255,0.10), transparent 28%),
        radial-gradient(circle at 90% 20%, rgba(120,70,255,0.10), transparent 30%),
        {BG};
    color: {TEXT};
}}

.main .block-container {{
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}}

h1, h2, h3 {{
    color: {TEXT} !important;
}}

p {{
    color: {MUTED};
}}


/* ---------- FLOATING BACKGROUND ---------- */

.stApp::before {{
    content: "";
    position: fixed;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: rgba(39,183,255,0.08);
    filter: blur(70px);
    top: 15%;
    left: 3%;
    animation: floatOne 8s ease-in-out infinite;
    pointer-events: none;
}}

.stApp::after {{
    content: "";
    position: fixed;
    width: 240px;
    height: 240px;
    border-radius: 50%;
    background: rgba(130,80,255,0.08);
    filter: blur(70px);
    bottom: 10%;
    right: 3%;
    animation: floatTwo 10s ease-in-out infinite;
    pointer-events: none;
}}

@keyframes floatOne {{
    0%, 100% {{
        transform: translate(0, 0);
    }}

    50% {{
        transform: translate(35px, -30px);
    }}
}}

@keyframes floatTwo {{
    0%, 100% {{
        transform: translate(0, 0);
    }}

    50% {{
        transform: translate(-35px, 25px);
    }}
}}


/* ---------- BUTTON ---------- */

.stButton > button {{
    background: {CARD};
    color: {TEXT};
    border: 1px solid {BLUE};
    border-radius: 12px;
    padding: 0.65rem 1.2rem;
    font-weight: 700;
    transition: all 0.25s ease;
}}

.stButton > button:hover {{
    transform: translateY(-3px);
    border-color: {BLUE};
    box-shadow: 0 8px 30px rgba(39,183,255,0.25);
    color: {BLUE};
}}


/* ---------- HERO ---------- */

.hero {{
    position: relative;
    overflow: hidden;
    padding: 58px 48px;
    border-radius: 24px;
    background:
        linear-gradient(
            135deg,
            rgba(7, 16, 34, 0.98),
            rgba(8, 27, 52, 0.94),
            rgba(5, 14, 30, 0.98)
        );
    border: 1px solid rgba(0, 200, 255, 0.32);
    box-shadow:
        0 0 0 1px rgba(0, 200, 255, 0.04),
        0 0 35px rgba(0, 170, 255, 0.10),
        0 25px 70px rgba(0, 0, 0, 0.45),
        inset 0 0 45px rgba(0, 170, 255, 0.035);
}}

.hero::before {{
    content: "";
    position: absolute;
    top: -120px;
    right: -80px;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: rgba(0, 174, 255, 0.08);
    filter: blur(50px);
    pointer-events: none;
}}

.hero::after {{
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(0, 174, 255, 0.5),
        transparent
    );
}}

.hero::after {{
    content: "";
    position: absolute;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    right: -50px;
    top: -50px;
    background: rgba(39,183,255,0.08);
    filter: blur(10px);
}}

.brand {{
    position: relative;
    display: inline-block;
    margin-bottom: 14px;
    font-size: 52px;
    font-weight: 900;
    letter-spacing: 4px;
    text-transform: uppercase;

    background: linear-gradient(
        90deg,
        #ffffff 0%,
        #8eeaff 45%,
        #00c8ff 70%,
        #ffffff 100%
    );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;

    text-shadow:
        0 0 18px rgba(0, 200, 255, 0.35),
        0 0 40px rgba(0, 150, 255, 0.15);
}}
    
.tagline {{
    max-width: 850px;
    margin-bottom: 24px;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 2px;
    line-height: 1.7;
    text-transform: uppercase;
    color: rgba(190, 225, 240, 0.78);
    text-shadow: 0 0 14px rgba(0, 200, 255, 0.12);
}}



.status {{
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 9px 16px;
    border: 1px solid rgba(0, 255, 170, 0.28);
    border-radius: 999px;
    background: rgba(0, 255, 170, 0.055);
    color: #9fffe0;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    box-shadow:
        0 0 18px rgba(0, 255, 170, 0.08),
        inset 0 0 12px rgba(0, 255, 170, 0.025);
}}

.status-dot {{
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: {GREEN};
    box-shadow: 0 0 14px {GREEN};
    animation: pulse 1.8s infinite;
}}

@keyframes pulse {{
    0% {{
        box-shadow: 0 0 5px {GREEN};
    }}

    50% {{
        box-shadow: 0 0 22px {GREEN};
    }}

    100% {{
        box-shadow: 0 0 5px {GREEN};
    }}
}}


/* ---------- SECTION ---------- */

.section-title {{
    font-size: 25px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 8px;
}}

.section-subtitle {{
    color: {MUTED};
    margin-bottom: 20px;
}}


/* ---------- METRIC CARDS ---------- */

.metric {{
    background: linear-gradient(145deg, {CARD}, {CARD_2});
    border: 1px solid {BORDER};
    border-radius: 18px;
    padding: 24px;
    min-height: 135px;
    transition: all 0.25s ease;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}}

.metric:hover {{
    transform: translateY(-6px);
    border-color: {BLUE};
    box-shadow: 0 15px 40px rgba(39,183,255,0.15);
}}

.metric-label {{
    color: {MUTED};
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
}}

.metric-value {{
    margin-top: 15px;
    font-size: 29px;
    font-weight: 900;
    color: {TEXT};
}}

.danger {{
    color: {RED};
    text-shadow: 0 0 18px rgba(255,77,85,0.25);
}}

.warning {{
    color: {ORANGE};
}}

.safe {{
    color: {GREEN};
}}


/* ---------- PANELS ---------- */

.panel {{
    background: linear-gradient(145deg, {CARD}, {CARD_2});
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 26px;
    margin-top: 20px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.16);
}}

.panel-title {{
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 6px;
    color: {TEXT};
}}

.panel-description {{
    color: {MUTED};
    font-size: 13px;
    margin-bottom: 22px;
}}


/* ---------- RISK ---------- */

.risk-container {{
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 15px;
}}

.risk-circle {{
    width: 190px;
    height: 190px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        radial-gradient(circle, {CARD} 58%, transparent 59%),
        conic-gradient(
            {RED} 0deg,
            {RED} var(--risk-angle),
            {BORDER} var(--risk-angle),
            {BORDER} 360deg
        );
    box-shadow: 0 0 45px rgba(255,77,85,0.18);
}}

.risk-number {{
    font-size: 42px;
    font-weight: 900;
    color: {RED};
}}

.risk-small {{
    font-size: 12px;
    color: {MUTED};
    text-align: center;
}}


/* ---------- ATTACK CHAIN ---------- */

.attack-chain {{
    display: flex;
    align-items: center;
    gap: 10px;
    overflow-x: auto;
    padding: 10px 0 18px 0;
}}

.attack-step {{
    min-width: 145px;
    padding: 18px 12px;
    border-radius: 15px;
    text-align: center;
    background: rgba(255,77,85,0.06);
    border: 1px solid rgba(255,77,85,0.30);
    transition: all 0.25s ease;
}}

.attack-step:hover {{
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(255,77,85,0.15);
}}

.step-number {{
    width: 28px;
    height: 28px;
    margin: 0 auto 10px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    background: rgba(255,77,85,0.15);
    color: {RED};
    font-weight: 800;
}}

.step-name {{
    color: {TEXT};
    font-size: 11px;
    font-weight: 800;
    word-break: break-word;
}}

.arrow {{
    color: {BLUE};
    font-size: 22px;
    font-weight: 900;
}}


/* ---------- MITRE ---------- */

.mitre-card {{
    background: rgba(39,183,255,0.05);
    border: 1px solid rgba(39,183,255,0.25);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 12px;
    transition: all 0.25s ease;
}}

.mitre-card:hover {{
    transform: translateX(5px);
    border-color: {BLUE};
    box-shadow: 0 10px 25px rgba(39,183,255,0.10);
}}

.technique-id {{
    color: {BLUE};
    font-weight: 900;
    font-size: 13px;
}}

.technique-name {{
    margin-top: 8px;
    color: {TEXT};
    font-size: 16px;
    font-weight: 800;
}}

.tactic {{
    margin-top: 8px;
    color: {MUTED};
    font-size: 12px;
}}


/* ---------- INTELLIGENCE ---------- */

.intel-row {{
    display: flex;
    justify-content: space-between;
    padding: 17px 0;
    border-bottom: 1px solid {BORDER};
}}

.intel-label {{
    color: {MUTED};
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}}

.intel-value {{
    color: {TEXT};
    font-weight: 800;
}}


/* ---------- RESPONSE ---------- */

.response {{
    margin-top: 25px;
    padding: 35px;
    border-radius: 22px;
    text-align: center;
    background:
        radial-gradient(
            circle at center,
            rgba(255,77,85,0.10),
            transparent 65%
        ),
        {CARD};
    border: 1px solid rgba(255,77,85,0.35);
    box-shadow: 0 0 40px rgba(255,77,85,0.08);
}}

.response-label {{
    color: {MUTED};
    font-size: 11px;
    font-weight: 900;
    letter-spacing: 2px;
}}

.response-action {{
    margin-top: 12px;
    color: {RED};
    font-size: 31px;
    font-weight: 900;
    animation: responsePulse 2s infinite;
}}

.response-description {{
    color: {MUTED};
    margin-top: 8px;
}}

@keyframes responsePulse {{
    0%, 100% {{
        text-shadow: 0 0 5px rgba(255,77,85,0.1);
    }}

    50% {{
        text-shadow: 0 0 25px rgba(255,77,85,0.45);
    }}
}}


/* ---------- REASONS ---------- */

.reason {{
    padding: 15px 18px;
    margin: 10px 0;
    border-radius: 12px;
    background: {CARD};
    border: 1px solid {BORDER};
    color: {TEXT};
    transition: all 0.2s ease;
}}

.reason:hover {{
    transform: translateX(5px);
    border-color: {RED};
}}

.reason-dot {{
    color: {RED};
    margin-right: 10px;
}}


/* ---------- FOOTER ---------- */

.footer {{
    margin-top: 55px;
    padding: 25px;
    text-align: center;
    border-top: 1px solid {BORDER};
    color: {MUTED};
    font-size: 12px;
    letter-spacing: 1px;
}}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

col1, col2 = st.columns([5, 1])

with col1:

    render_html(
        """
        <div class="hero">

            <div class="brand">
                SentinelX
            </div>

            <div class="tagline">
                AI-Powered Cybersecurity Threat Detection & Autonomous Response Platform
            </div>

            <div class="status">
                <span class="status-dot"></span>
                SENTINELX SYSTEM ONLINE
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.write("")
    st.write("")

    mode_text = (
        "Light Mode"
        if st.session_state.dark_mode
        else "Dark Mode"
    )

    if st.button(
        mode_text,
        use_container_width=True
    ):

        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()


# ============================================================
# API STATUS
# ============================================================

api_online = False

try:

    response = requests.get(
        f"{API_URL}/health",
        timeout=2
    )

    if response.status_code == 200:
        api_online = True

except requests.exceptions.RequestException:

    api_online = False


if api_online:

    st.success(
        "SentinelX backend connected successfully."
    )

else:

    st.error(
        "SentinelX backend is offline. Start FastAPI before running an analysis."
    )


# ============================================================
# THREAT SIMULATION
# ============================================================

render_html(
    """
    <div class="section-title">
        Threat Simulation
    </div>

    <div class="section-subtitle">
        Simulate a multi-stage attack and send the telemetry through
        the SentinelX detection pipeline.
    </div>
    """,
    unsafe_allow_html=True
)


if st.button(
    "ANALYZE SIMULATED ATTACK",
    use_container_width=False
):

    if not api_online:

        st.error(
            "FastAPI is not running. Start the backend first."
        )

    else:

        attack_events = [

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

        payload = {
            "events": attack_events,
            "ai_result": "ANOMALY",
            "severity_score": 3
        }

        try:

            with st.spinner(
                "Running SentinelX threat analysis..."
            ):

                api_response = requests.post(
                    f"{API_URL}/analyze",
                    json=payload,
                    timeout=10
                )

            if api_response.status_code == 200:

                st.session_state.result = api_response.json()

                st.success(
                    "Threat analysis completed successfully."
                )

            else:

                st.error(
                    f"Analysis failed. API returned status {api_response.status_code}."
                )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Could not connect to SentinelX API: {error}"
            )


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.result


if result is not None:

    # ========================================================
    # SECURITY OVERVIEW
    # ========================================================

    render_html(
        """
        <div class="section-title">
            Security Overview
        </div>
        """,
        unsafe_allow_html=True
    )

    risk_score = result.get(
        "risk_score",
        0
    )

    risk_level = result.get(
        "risk_level",
        "UNKNOWN"
    )

    ai_result = result.get(
        "ai_result",
        "UNKNOWN"
    )

    attack_detected = result.get(
        "attack_detected",
        False
    )

    risk_class = (
        "danger"
        if risk_score >= 60
        else (
            "warning"
            if risk_score >= 30
            else "safe"
        )
    )

    attack_text = (
        "DETECTED"
        if attack_detected
        else "CLEAR"
    )

    attack_class = (
        "danger"
        if attack_detected
        else "safe"
    )

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    RISK SCORE
                </div>

                <div class="metric-value {risk_class}">
                    {risk_score}/100
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c2:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    RISK LEVEL
                </div>

                <div class="metric-value {risk_class}">
                    {html.escape(str(risk_level))}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c3:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    AI DETECTION
                </div>

                <div class="metric-value danger">
                    {html.escape(str(ai_result))}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with c4:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    ATTACK STATUS
                </div>

                <div class="metric-value {attack_class}">
                    {attack_text}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # RISK VISUALIZATION
    # ========================================================

    render_html(
        """
        <div class="panel">

            <div class="panel-title">
                Risk Visualization
            </div>

            <div class="panel-description">
                SentinelX combines AI anomaly detection,
                attack-chain analysis, severity and
                MITRE ATT&CK mappings.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    risk_angle = max(
        0,
        min(
            360,
            risk_score * 3.6
        )
    )

    render_html(
        f"""
        <div class="risk-container">

            <div
                class="risk-circle"
                style="--risk-angle:{risk_angle}deg;"
            >

                <div>

                    <div class="risk-number">
                        {risk_score}
                    </div>

                    <div class="risk-small">
                        RISK / 100
                    </div>

                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # ATTACK CHAIN
    # ========================================================

    attack_stages = result.get(
        "attack_stages",
        []
    )

    render_html(
        """
        <div class="panel">

            <div class="panel-title">
                Attack Chain
            </div>

            <div class="panel-description">
                Observed sequence of suspicious activity
            </div>

            <div class="attack-chain">
        """,
        unsafe_allow_html=True
    )


    for index, stage in enumerate(attack_stages):

        render_html(
            f"""
            <div class="attack-step">

                <div class="step-number">
                    {index + 1}
                </div>

                <div class="step-name">
                    {html.escape(str(stage))}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        if index < len(attack_stages) - 1:

            render_html(
                """
                <div class="arrow">
                    →
                </div>
                """,
                unsafe_allow_html=True
            )


    render_html(
        """
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # MITRE + THREAT INTELLIGENCE
    # ========================================================

    left, right = st.columns(2)


    # ========================================================
    # MITRE ATT&CK
    # ========================================================

    with left:

        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    MITRE ATT&CK
                </div>

                <div class="panel-description">
                    Mapped adversary techniques
                </div>
            """,
            unsafe_allow_html=True
        )

        mappings = result.get(
            "mitre_mappings",
            []
        )


        for mapping in mappings:

            technique_id = mapping.get(
                "technique_id",
                "UNKNOWN"
            )

            technique = mapping.get(
                "technique",
                "Unknown Technique"
            )

            tactic = mapping.get(
                "tactic",
                "Unknown Tactic"
            )

            render_html(
                f"""
                <div class="mitre-card">

                    <div class="technique-id">
                        {html.escape(str(technique_id))}
                    </div>

                    <div class="technique-name">
                        {html.escape(str(technique))}
                    </div>

                    <div class="tactic">
                        {html.escape(str(tactic))}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        render_html(
            """
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # THREAT INTELLIGENCE
    # ========================================================

    with right:

        intelligence = result.get(
            "threat_intelligence",
            {}
        )

        threat_level = intelligence.get(
            "threat_level",
            "UNKNOWN"
        )

        source_ips = intelligence.get(
            "source_ips",
            []
        )

        targeted_users = intelligence.get(
            "targeted_users",
            []
        )

        activity_count = intelligence.get(
            "activity_count",
            0
        )


        render_html(
            """
            <div class="panel">

                <div class="panel-title">
                    Threat Intelligence
                </div>

                <div class="panel-description">
                    Intelligence gathered from observed activity
                </div>
            """,
            unsafe_allow_html=True
        )


        ip_text = (
            ", ".join(
                str(ip)
                for ip in source_ips
            )
            if source_ips
            else "None"
        )

        user_text = (
            ", ".join(
                str(user)
                for user in targeted_users
            )
            if targeted_users
            else "None"
        )


        render_html(
            f"""
            <div class="intel-row">

                <span class="intel-label">
                    THREAT LEVEL
                </span>

                <span class="intel-value danger">
                    {html.escape(str(threat_level))}
                </span>

            </div>


            <div class="intel-row">

                <span class="intel-label">
                    SOURCE IP
                </span>

                <span class="intel-value">
                    {html.escape(ip_text)}
                </span>

            </div>


            <div class="intel-row">

                <span class="intel-label">
                    TARGETED USER
                </span>

                <span class="intel-value">
                    {html.escape(user_text)}
                </span>

            </div>


            <div class="intel-row">

                <span class="intel-label">
                    ACTIVITIES CAPTURED
                </span>

                <span class="intel-value">
                    {activity_count}
                </span>

            </div>


            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # RESPONSE
    # ========================================================

    response_action = result.get(
        "response_action",
        "MONITOR"
    )

    response_description = result.get(
        "response_description",
        ""
    )


    render_html(
        f"""
        <div class="response">

            <div class="response-label">
                AUTOMATED RESPONSE ACTIVATED
            </div>

            <div class="response-action">
                {html.escape(str(response_action))}
            </div>

            <div class="response-description">
                {html.escape(str(response_description))}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # THREAT PATTERN ANALYSIS
    # ========================================================

    pattern = result.get(
        "pattern_analysis",
        {}
    )

    classification = pattern.get(
        "threat_classification",
        "UNKNOWN"
    )

    confidence = pattern.get(
        "confidence",
        "UNKNOWN"
    )

    matches = pattern.get(
        "threat_matches",
        0
    )


    render_html(
        """
        <div class="section-title">
            Threat Pattern Analysis
        </div>
        """,
        unsafe_allow_html=True
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    CLASSIFICATION
                </div>

                <div class="metric-value warning">
                    {html.escape(str(classification))}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p2:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    CONFIDENCE
                </div>

                <div class="metric-value warning">
                    {html.escape(str(confidence))}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with p3:

        render_html(
            f"""
            <div class="metric">

                <div class="metric-label">
                    THREAT MATCHES
                </div>

                <div class="metric-value warning">
                    {matches}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # WHY FLAGGED
    # ========================================================

    render_html(
        """
        <div class="section-title">
            Why SentinelX Flagged This Incident
        </div>
        """,
        unsafe_allow_html=True
    )


    reasons = result.get(
        "risk_reasons",
        []
    )


    for reason in reasons:

        render_html(
            f"""
            <div class="reason">

                <span class="reason-dot">
                    •
                </span>

                {html.escape(str(reason))}

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FOOTER
    # ========================================================

    render_html(
        """
        <div class="footer">

            SENTINELX &nbsp;•&nbsp;
            AI THREAT DETECTION &nbsp;•&nbsp;
            ATTACK CHAIN ANALYSIS &nbsp;•&nbsp;
            MITRE ATT&CK &nbsp;•&nbsp;
            AUTONOMOUS RESPONSE

        </div>
        """,
        unsafe_allow_html=True
    )