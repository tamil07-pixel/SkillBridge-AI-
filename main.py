import os
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
        "title": "Full-Stack Developer",
        "stack": "HTML5, CSS3, JavaScript (ES6+), React, Python (FastAPI) / Node.js (Express), PostgreSQL / MongoDB, Git, Docker",
        "weeks_1_3": [
            "Master semantic HTML5, responsive CSS (Flexbox, Grid), and modern JavaScript (async/await, DOM, fetch API).",
            "Learn Git & GitHub workflows (branching, pull requests, clean commit messages).",
            "Build a responsive portfolio website and an interactive task/expense tracker."
        ],
        "weeks_4_6": [
            "Learn React: components, props, state, hooks (`useState`, `useEffect`), routing, and API integration.",
            "Build a frontend dashboard consuming a public REST API with search, filters, and error states."
        ],
        "weeks_7_9": [
            "Build REST APIs using FastAPI (Python) or Node.js + Express with JWT authentication and input validation.",
            "Design schemas and CRUD queries in PostgreSQL or MongoDB."
        ],
        "weeks_10_12": [
            "Build and deploy 2 full-stack projects (e.g., Job Tracker with Auth + AI Resume/Scam Analyzer).",
            "Add unit/API tests, environment variable security, and deploy on Render/Vercel/Streamlit."
        ],
        "interview": "Practice JavaScript closures/promises, REST API design, SQL joins/indexing, and explain your project architecture."
    },
    "python": {
        "title": "Python Developer",
        "stack": "Python 3, OOP, FastAPI / Django, SQLAlchemy, PostgreSQL, Pytest, Docker, Git",
        "weeks_1_3": [
            "Master Python data structures, list/dict comprehensions, file handling, decorators, and OOP principles.",
            "Solve 40+ array, string, hashing, and recursion problems to build strong logic."
        ],
        "weeks_4_6": [
            "Build production-grade REST APIs using FastAPI with Pydantic validation and async endpoints.",
            "Connect Python apps to PostgreSQL/SQLite using SQLAlchemy ORM."
        ],
        "weeks_7_9": [
            "Write automated tests using `pytest`, handle logging, rate limiting, and background tasks.",
            "Work with external APIs, JSON/CSV automation scripts, and environment configs."
        ],
        "weeks_10_12": [
            "Build 2 complete backend/automation projects, containerize with Docker, and deploy live.",
            "Write clear API documentation (Swagger/OpenAPI) and GitHub READMEs."
        ],
        "interview": "Revise Python memory management, GIL, decorators, generators, SQL optimization, and API security."
    },
    "embedded": {
        "title": "Embedded Systems & IoT Engineer",
        "stack": "Embedded C/C++, ARM Cortex / ESP32 / STM32, UART/SPI/I2C, RTOS, Python, MQTT, Linux Basics",
        "weeks_1_3": [
            "Master Embedded C (pointers, bitwise operations, memory layout, volatile keyword, interrupts).",
            "Work with GPIO, timers, ADC/PWM on ESP32 or STM32."
        ],
        "weeks_4_6": [
            "Implement communication protocols: UART, I2C, SPI, and CAN bus with real sensors.",
            "Debug hardware-software issues using serial monitors and logic analyzers."
        ],
        "weeks_7_9": [
            "Learn FreeRTOS basics (tasks, queues, semaphores, mutexes) for real-time scheduling.",
            "Connect devices to cloud dashboards via Wi-Fi/MQTT and Python FastAPI backends."
        ],
        "weeks_10_12": [
            "Build an end-to-end hardware + cloud project (e.g., Smart Telemetry / V2V / Sensor Alert System).",
            "Document circuit diagrams, firmware flowcharts, and demo videos on GitHub."
        ],
        "interview": "Prepare C pointers/memory questions, interrupt latency, I2C vs SPI, RTOS task synchronization, and register-level debugging."
    },
    "data": {
        "title": "Data Analyst / Data Science",
        "stack": "Python, Pandas, NumPy, SQL, Excel, Power BI / Tableau, Statistics, Scikit-learn",
        "weeks_1_3": [
            "Master SQL queries (JOINs, GROUP BY, CTEs, Window Functions) and advanced Excel (Pivot Tables, XLOOKUP).",
            "Learn descriptive statistics, probability, and hypothesis testing."
        ],
        "weeks_4_6": [
            "Use Python (Pandas, NumPy, Matplotlib/Seaborn) for data cleaning, EDA, and visualization.",
            "Analyze 3 real-world datasets and document business insights."
        ],
        "weeks_7_9": [
            "Build interactive KPI dashboards in Power BI or Tableau.",
            "Learn basic machine learning (Regression, Classification, Model Evaluation) with Scikit-learn."
        ],
        "weeks_10_12": [
            "Publish 2 end-to-end case studies combining SQL + Python + Dashboard storytelling.",
            "Quantify business impact in every project summary."
        ],
        "interview": "Practice SQL case studies, A/B testing scenarios, data cleaning edge cases, and dashboard metric definitions."
    }
}


def build_detailed_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full Stack Developer"
    role_key = clean_role.lower()

    matched = None
    for key, data in ROLE_ROADMAPS.items():
        if key in role_key:
            matched = data
            break

    level_guidance = {
        "Beginner": "Start from scratch: spend 60% of your time coding hands-on and 40% learning concepts. Avoid tutorial hell by building small features every week.",
        "Intermediate": "Skip basic syntax: focus on clean architecture, error handling, testing, database optimization, and deploying real projects.",
        "Advanced": "Focus on system design, scalability, security hardening, CI/CD pipelines, performance profiling, and production observability.",
    }.get(exp_level, "")

    if matched:
        w1 = "\n   - ".join(matched["weeks_1_3"])
        w2 = "\n   - ".join(matched["weeks_4_6"])
        w3 = "\n   - ".join(matched["weeks_7_9"])
        w4 = "\n   - ".join(matched["weeks_10_12"])

        return f"""
### 12-Week Actionable Roadmap: {clean_role} ({exp_level})

**Recommended Tech Stack:** `{matched["stack"]}`

> **Strategy for {exp_level} Level:** {level_guidance}

---

#### Phase 1: Foundations & Core Logic (Weeks 1–3)
   - {w1}

#### Phase 2: Core Frameworks & Integrations (Weeks 4–6)
   - {w2}

#### Phase 3: Backend, Data & Advanced Workflows (Weeks 7–9)
   - {w3}

#### Phase 4: Capstone Projects & Deployment (Weeks 10–12)
   - {w4}

#### Interview & Job Readiness Checklist
   - {matched["interview"]}
   - Keep 2 deployed projects with live links, architecture diagrams, and clear READMEs on GitHub.
"""

    # Custom detailed roadmap for any other role typed by the user
    return f"""
### 12-Week Actionable Roadmap: {clean_role} ({exp_level})

> **Strategy for {exp_level} Level:** {level_guidance}

---

#### Phase 1: Core Fundamentals & Tooling (Weeks 1–3)
   - Identify the top 4 core tools/languages listed across 15+ job postings for **{clean_role}**.
   - Master core syntax, problem-solving fundamentals, and Git/GitHub version control.
   - Build 2 small proof-of-concept scripts/modules to validate basics.

#### Phase 2: Practical Implementation & Workflows (Weeks 4–6)
   - Learn the primary industry framework/platform used in **{clean_role}** roles.
   - Practice working with real data, APIs, debugging tools, and error handling.
   - Build a functional mid-sized project solving a realistic problem.

#### Phase 3: Testing, Optimization & Real-World Standards (Weeks 7–9)
   - Add automated testing, logging, security best practices, and performance improvements.
   - Study how production systems for **{clean_role}** are structured and scaled.

#### Phase 4: Portfolio Projects & Interview Prep (Weeks 10–12)
   - Build and deploy 2 end-to-end portfolio projects tailored to **{clean_role}**.
   - Document problem statement, architecture, and measurable results in each GitHub README.
   - Practice role-specific technical questions and mock interviews.
"""


def generate_roadmap(target_role: str, exp_level: str, retries: int = 1) -> tuple[str, str | None]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", None)
        except Exception:
            api_key = None

    for attempt in range(retries + 1):
        try:
            if not api_key:
                return build_detailed_roadmap(target_role, exp_level), None
            return build_detailed_roadmap(target_role, exp_level), None
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return build_detailed_roadmap(target_role, exp_level), f"Switched to offline roadmap ({type(e).__name__})."

    return build_detailed_roadmap(target_role, exp_level), None


with tab1:
    st.subheader("Custom Career Roadmap Generator")
    st.write("Enter your target role to generate a clear, week-by-week learning path, tech stack, and project plan.")

    role = st.text_input(
        "Target Role (e.g., Full Stack Developer, Python Developer, Embedded Systems Engineer, Data Analyst):",
        value="Full Stack Developer",
    )
    level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        with st.spinner("Building your step-by-step roadmap..."):
            roadmap_text, notice = generate_roadmap(role, level)

        if notice:
            st.warning(notice)

        st.markdown(roadmap_text)


# -------------------- TAB 2: JOB SCAM DETECTOR --------------------
def analyze_job_offline(job_text: str) -> tuple[str, int, list[str]]:
    text = job_text.lower()
    score = 0
    red_flags = []

    scam_patterns = [
        (r"\b(registration fee|security deposit|pay to apply|training fee|processing fee|refundable deposit)\b",
         "Asks for upfront payment, registration fee, or security deposit (major scam indicator).", 35),
        (r"\b(whatsapp|telegram)\b.*\b(contact|message|dm|number)\b|\b(contact|message|dm)\b.*\b(whatsapp|telegram)\b",
         "Pushes communication to WhatsApp/Telegram instead of an official company email/portal.", 20),
        (r"\b(earn ₹|earn rs|daily payout|weekly payout|guaranteed income|no experience needed.*high salary|part[- ]time.*₹\s?\d{4,})\b",
         "Promises unrealistic guaranteed income or high pay for zero experience.", 25),
        (r"\b(aadhaar|pan card|bank details|otp|cvv|passbook)\b",
         "Requests sensitive personal or banking documents before an official interview.", 30),
        (r"\b(urgent hiring|limited slots|apply within 1 hour|immediate joining without interview|direct offer letter)\b",
         "Uses high-pressure urgency or offers a job without any real interview process.", 20),
        (r"@gmail\.com|@yahoo\.com|@outlook\.com",
         "Uses a free personal email domain instead of an official company domain.", 15),
    ]

    for pattern, reason, weight in scam_patterns:
        if re.search(pattern, text):
            score += weight
            red_flags.append(reason)

    score = min(score, 100)

    if score >= 50:
        verdict = "High Risk — Likely a Job Scam"
    elif score >= 20:
        verdict = "Medium Risk — Verify Carefully Before Applying"
    else:
        verdict = "Low Risk — Looks Legitimate (Still Verify Company Details)"

    return verdict, score, red_flags


with tab2:
    st.subheader("Job Scam Detector")
    st.write("Paste a job description, recruiter message, or offer details to check for scam red flags.")

    job_input = st.text_area(
        "Job Posting / Message:",
        height=180,
        placeholder="Paste the job post, salary details, contact info, or recruiter message here...",
    )

    if st.button("Analyze Job Posting"):
        if not job_input.strip():
            st.warning("Please paste a job description or message first.")
        else:
            with st.spinner("Analyzing job details..."):
                verdict, risk_score, flags = analyze_job_offline(job_input)

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
