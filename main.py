import os
import re
import time
import urllib.request
import json
import streamlit as st

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="centered")

st.title("SkillBridge AI")
st.caption("Personalized Career Roadmap Generator & AI-Driven Job Scam Detector")

tab1, tab2 = st.tabs(["🗺️ Career Roadmap Generator", "🛡️ Job Scam Detector"])


def get_api_config() -> tuple[str | None, str]:
    """Returns (api_key, provider) checking env vars first, then st.secrets."""
    keys_to_check = [
        ("GROQ_API_KEY", "groq"),
        ("OPENAI_API_KEY", "openai"),
    ]
    for env_name, provider in keys_to_check:
        val = os.getenv(env_name)
        if val and val.strip():
            return val.strip(), provider

    try:
        for secret_name, provider in keys_to_check:
            val = st.secrets.get(secret_name, None)
            if val and str(val).strip():
                return str(val).strip(), provider
    except Exception:
        pass

    return None, "none"


def call_llm_api(prompt: str, api_key: str, provider: str, retries: int = 2) -> str:
    """Calls Groq or OpenAI Chat Completions API with basic retry on transient errors."""
    if provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        model = "llama-3.3-70b-versatile"
    else:
        url = "https://api.openai.com/v1/chat/completions"
        model = "gpt-4o-mini"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a clear, practical career mentor and job-safety analyst. Give structured, actionable, concise answers."
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.4,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "User-Agent": "SkillBridgeAI/1.0",
    }

    last_err = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=25) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body["choices"][0]["message"]["content"].strip()
        except Exception as e:
            last_err = e
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise last_err

    raise RuntimeError("Unexpected LLM failure")


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


def fallback_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full-Stack Developer"
    key_match = next((v for k, v in ROLE_ROADMAPS.items() if k in clean_role.lower()), None)

    if key_match:
        stack_line = f"**Core Tech Stack:** `{key_match['stack']}`\n\n"
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


def generate_roadmap(target_role: str, exp_level: str) -> tuple[str, str | None]:
    clean_role = target_role.strip() or "Full-Stack Developer"
    api_key, provider = get_api_config()

    if not api_key:
        return fallback_roadmap(clean_role, exp_level), "No API key found (`GROQ_API_KEY` or `OPENAI_API_KEY`); showing offline roadmap."

    prompt = (
        f"Create a clear, structured 12-week career roadmap for the role '{clean_role}' "
        f"at '{exp_level}' experience level. Include: recommended tech stack/tools, "
        f"Weeks 1-3, Weeks 4-6, Weeks 7-9, Weeks 10-12 milestones, 2 practical project ideas, "
        f"and key interview topics."
    )

    try:
        ai_text = call_llm_api(prompt, api_key, provider)
        return ai_text, None
    except Exception as e:
        return fallback_roadmap(clean_role, exp_level), f"AI request failed ({type(e).__name__}: {e}). Showing offline roadmap."


with tab1:
    st.subheader("Custom Career Roadmap Generator")
    st.write("Enter any target role or course to generate a clear step-by-step roadmap.")

    role = st.text_input(
        "Target Role (e.g., Full-Stack Developer, Python Developer, Embedded Systems Engineer):",
        value="Full-Stack Developer",
    )
    level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        with st.spinner("Generating your roadmap..."):
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


def analyze_job_with_ai(job_text: str) -> tuple[str, str | None]:
    api_key, provider = get_api_config()
    if not api_key:
        verdict, score, flags = analyze_job_offline(job_text)
        flag_bullets = "\n".join(f"- {f}" for f in flags) if flags else "- No strong scam keywords detected."
        out = f"**{verdict}** (Offline Risk Score: {score}/100)\n\n**Red Flags:**\n{flag_bullets}"
        return out, "No API key found; showing offline scam check."

    prompt = (
        "Analyze this job posting or recruiter message for potential job scam red flags. "
        "Provide: 1) Risk Level (Low / Medium / High), 2) Key Red Flags or Positive Signals, "
        "3) Practical Verification Steps before sharing details or applying.\n\n"
        f"Job Posting:\n{job_text}"
    )

    try:
        ai_analysis = call_llm_api(prompt, api_key, provider)
        return ai_analysis, None
    except Exception as e:
        verdict, score, flags = analyze_job_offline(job_text)
        flag_bullets = "\n".join(f"- {f}" for f in flags) if flags else "- No strong scam keywords detected."
        out = f"**{verdict}** (Offline Risk Score: {score}/100)\n\n**Red Flags:**\n{flag_bullets}"
        return out, f"AI check failed ({type(e).__name__}); showing offline scam check."


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
            with st.spinner("Analyzing job posting..."):
                result_md, notice = analyze_job_with_ai(job_input)

            if notice:
                st.warning(notice)

            st.markdown(result_md)
