import re
import time
import streamlit as st

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="centered")

st.title("SkillBridge AI")
st.caption("Personalized Career Roadmap Generator & AI-Driven Job Scam Detector")

tab1, tab2 = st.tabs(["🗺️ Career Roadmap Generator", "🛡️ Job Scam Detector"])


# -------------------- TAB 1: CAREER ROADMAP GENERATOR --------------------
ROLE_ROADMAPS = {
    "full stack": {
        "stack": "HTML5, CSS3, JavaScript (ES6+), React, Python (FastAPI) / Node.js (Express), PostgreSQL / MongoDB, Git, Docker",
        "w1": "Master HTML5, CSS3 (Flexbox/Grid), JavaScript (async/await, DOM, fetch), and Git/GitHub.",
        "w2": "Build React UIs (hooks, state, routing) and consume REST APIs cleanly.",
        "w3": "Build backend APIs (FastAPI or Node/Express), auth, and SQL/NoSQL databases.",
        "w4": "Build & deploy 2 end-to-end projects, write clear READMEs, and practice role interviews.",
    },
    "python": {
        "stack": "Python 3, OOP, FastAPI / Django, SQLAlchemy, PostgreSQL, Pytest, Git, Docker",
        "w1": "Master Python data structures, OOP, file/exception handling, and core problem-solving.",
        "w2": "Build REST APIs with FastAPI + Pydantic validation and database models.",
        "w3": "Add automated tests (pytest), logging, error handling, and external API integrations.",
        "w4": "Deploy 2 backend/automation projects with clean docs and interview prep.",
    },
    "embedded": {
        "stack": "Embedded C/C++, ESP32 / STM32 / ARM, UART/SPI/I2C, FreeRTOS, MQTT, Python",
        "w1": "Master Embedded C (pointers, bitwise ops, volatile, interrupts) and GPIO/ADC/PWM.",
        "w2": "Work with UART, I2C, and SPI sensors + serial/hardware debugging.",
        "w3": "Learn FreeRTOS tasks/queues/semaphores and connect devices to cloud/dashboards.",
        "w4": "Build & document a complete hardware + firmware project with circuit/block diagrams.",
    },
    "data": {
        "stack": "Python, Pandas, NumPy, SQL, Excel, Power BI / Tableau, Statistics, Scikit-learn",
        "w1": "Master SQL (JOINs, GROUP BY, CTEs, window functions), Excel, and statistics.",
        "w2": "Clean, explore, and visualize datasets using Python (Pandas, Matplotlib/Seaborn).",
        "w3": "Create interactive BI dashboards and basic ML models/evaluation.",
        "w4": "Publish 2 data case studies with clear business takeaways and interview practice.",
    },
}


def build_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full-Stack Developer"
    key_match = next((v for k, v in ROLE_ROADMAPS.items() if k in clean_role.lower()), None)

    if key_match:
        stack_line = f"**Recommended Stack:** `{key_match['stack']}`\n\n"
        p1, p2, p3, p4 = key_match["w1"], key_match["w2"], key_match["w3"], key_match["w4"]
    else:
        stack_line = ""
        p1 = f"Learn core fundamentals, terminology, and key tools required for **{clean_role}**."
        p2 = f"Practice hands-on exercises and build small modules using standard **{clean_role}** tools."
        p3 = f"Learn workflows, debugging, testing, and best practices used in real **{clean_role}** teams."
        p4 = f"Build & showcase 2 practical **{clean_role}** projects and prepare for role-specific interviews."

    return f"""
### 12-Week Roadmap: {clean_role} ({exp_level})
{stack_line}1. **Weeks 1–3 (Foundations):** {p1}
2. **Weeks 4–6 (Core Skills):** {p2}
3. **Weeks 7–9 (Applied & Testing):** {p3}
4. **Weeks 10–12 (Projects & Prep):** {p4}
"""


def run_simulated_roadmap(target_role: str, exp_level: str) -> str:
    status = st.empty()
    progress = st.progress(0)

    steps = [
        (25, "Initializing SkillBridge roadmap engine..."),
        (55, "Mapping skills and learning phases..."),
        (85, "Structuring projects and interview milestones..."),
        (100, "Roadmap ready!"),
    ]
    for pct, msg in steps:
        status.info(msg)
        progress.progress(pct)
        time.sleep(0.35)

    status.empty()
    progress.empty()
    return build_roadmap(target_role, exp_level)


with tab1:
    st.subheader("Custom Career Roadmap Generator")
    st.write("Enter your target role to generate a clear step-by-step roadmap.")

    role = st.text_input(
        "Target Role (e.g., Full-Stack Developer, Python Developer, Embedded Systems Engineer):",
        value="Full-Stack Developer",
    )
    level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        roadmap_text = run_simulated_roadmap(role, level)
        st.markdown(roadmap_text)


# -------------------- TAB 2: JOB SCAM DETECTOR --------------------
def analyze_job_simulated(job_text: str) -> tuple[str, int, list[str]]:
    status = st.empty()
    progress = st.progress(0)

    for pct, msg in [
        (30, "Scanning job posting text..."),
        (70, "Checking payment, contact, and urgency patterns..."),
        (100, "Analysis complete!"),
    ]:
        status.info(msg)
        progress.progress(pct)
        time.sleep(0.3)

    status.empty()
    progress.empty()

    text = job_text.lower()
    score = 0
    red_flags = []

    scam_patterns = [
        (r"\b(registration fee|security deposit|pay to apply|training fee|processing fee|refundable deposit)\b",
         "Asks for upfront payment, registration fee, or security deposit.", 35),
        (r"\b(whatsapp|telegram)\b.*\b(contact|message|dm|number)\b|\b(contact|message|dm)\b.*\b(whatsapp|telegram)\b",
         "Directs candidates to WhatsApp/Telegram instead of an official hiring portal/email.", 20),
        (r"\b(earn ₹|earn rs|daily payout|weekly payout|guaranteed income|no experience needed.*high salary|part[- ]time.*₹\s?\d{4,})\b",
         "Promises unrealistic pay or guaranteed income with little/no experience.", 25),
        (r"\b(aadhaar|pan card|bank details|otp|cvv|passbook)\b",
         "Asks for sensitive ID, banking, or OTP details early in hiring.", 30),
        (r"\b(urgent hiring|limited slots|apply within 1 hour|immediate joining without interview|direct offer letter)\b",
         "Uses urgency pressure or skips interviews/verification.", 20),
        (r"@gmail\.com|@yahoo\.com|@outlook\.com",
         "Uses a free email address instead of a company domain.", 15),
    ]

    for pattern, reason, weight in scam_patterns:
        if re.search(pattern, text):
            score += weight
            red_flags.append(reason)

    score = min(score, 100)
    if score >= 50:
        verdict = "High Risk — Likely a Job Scam"
    elif score >= 20:
        verdict = "Medium Risk — Verify Carefully"
    else:
        verdict = "Low Risk — Looks Safer (Still Verify Company)"

    return verdict, score, red_flags


with tab2:
    st.subheader("Job Scam Detector")
    st.write("Paste a job post, offer message, or recruiter email to check for scam signs.")

    job_input = st.text_area(
        "Job Posting / Recruiter Message:",
        height=180,
        placeholder="Paste the job description, salary promises, or recruiter message here...",
    )

    if st.button("Analyze Job Posting"):
        if not job_input.strip():
            st.warning("Please paste a job posting or message first.")
        else:
            verdict, risk_score, flags = analyze_job_simulated(job_input)

            if risk_score >= 50:
                st.error(f"**{verdict}** (Risk Score: {risk_score}/100)")
            elif risk_score >= 20:
                st.warning(f"**{verdict}** (Risk Score: {risk_score}/100)")
            else:
                st.success(f"**{verdict}** (Risk Score: {risk_score}/100)")

            if flags:
                st.markdown("**Detected Red Flags:**")
                for flag in flags:
                    st.markdown(f"- {flag}")
            else:
                st.markdown("- No obvious scam keywords or payment traps detected.")

            st.info("Tip: Never pay money for offer letters, laptops, or onboarding, and always verify the recruiter on the company's official career page.")
