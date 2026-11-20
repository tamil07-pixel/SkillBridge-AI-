import os
import re
import time
import streamlit as st

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="centered")

st.title("SkillBridge AI")
st.caption("Personalized Career Roadmap Generator & AI-Driven Job Scam Detector")

tab1, tab2 = st.tabs(["🗺️ Career Roadmap Generator", "🛡️ Job Scam Detector"])


# -------------------- TAB 1: CAREER ROADMAP GENERATOR --------------------
def fallback_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full Stack Developer"

    level_focus = {
        "Beginner": "Focus on strong fundamentals, guided mini-projects, and clean GitHub commits.",
        "Intermediate": "Focus on system design basics, API optimization, testing, and full-stack deployment.",
        "Advanced": "Focus on scalable architecture, performance tuning, security, and production workflows.",
    }.get(exp_level, "")

    return f"""
### Roadmap for {clean_role} ({exp_level})
> {level_focus}

1. **Core Foundations (Weeks 1–3)**
   - Master core programming concepts, data structures, and problem-solving tailored for **{clean_role}**.
   - Practice Git, GitHub branching, and writing clean technical documentation.

2. **Core Stack & Tools (Weeks 4–8)**
   - Build hands-on modules using the primary frameworks, REST APIs, and databases required for **{clean_role}**.
   - Learn authentication, error handling, and automated testing.

3. **Real-World Projects & Deployment (Weeks 9–12)**
   - Build and deploy 2 complete end-to-end projects with live links.
   - Document architecture decisions, challenges solved, and screenshots in your README.

4. **Interview & Portfolio Readiness**
   - Practice role-specific technical questions and tailor your resume around measurable project outcomes.
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
                return fallback_roadmap(target_role, exp_level), None
            # Add external LLM API call here if OPENAI_API_KEY is configured
            return fallback_roadmap(target_role, exp_level), None
        except Exception as e:
            if attempt < retries:
                time.sleep(1)
                continue
            return fallback_roadmap(target_role, exp_level), f"Switched to offline roadmap ({type(e).__name__})."

    return fallback_roadmap(target_role, exp_level), None


with tab1:
    st.subheader("Custom Career Roadmap Generator")
    st.write("Enter your target role to generate a step-by-step learning path and required skills.")

    role = st.text_input(
        "Target Role (e.g., Full Stack Developer, Python Developer, Embedded Systems Engineer):",
        value="Full Stack Developer",
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
