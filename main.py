import json
import os
import re
import time
import urllib.error
import urllib.request
import streamlit as st

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="centered")

st.title("SkillBridge AI")
st.caption("Personalized Career Roadmap Generator & AI-Driven Job Scam Detector")

tab1, tab2 = st.tabs(["🗺️ Career Roadmap Generator", "🛡️ Job Scam Detector"])


def get_openai_key() -> str | None:
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    try:
        secret_key = st.secrets.get("OPENAI_API_KEY", None)
        if secret_key and str(secret_key).strip():
            return str(secret_key).strip()
    except Exception:
        pass

    return None


def call_openai(prompt: str, api_key: str, retries: int = 2) -> str:
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are SkillBridge AI, a practical career mentor and job-safety analyst. "
                    "Give clear, structured, accurate, and actionable responses tailored to the user's exact topic or job post."
                ),
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

    last_error = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"].strip()
        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="ignore")
            except Exception:
                pass
            last_error = RuntimeError(f"OpenAI HTTP {e.code}: {err_body[:200] or e.reason}")
            if e.code in (429, 500, 502, 503, 504) and attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise last_error
        except Exception as e:
            last_error = e
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise last_error

    raise RuntimeError("OpenAI request failed")


# -------------------- TAB 1: CAREER ROADMAP GENERATOR --------------------
def fallback_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Full-Stack Developer"
    return f"""
### 12-Week Roadmap: {clean_role} ({exp_level})

1. **Weeks 1–3 (Foundations):** Learn core fundamentals, terminology, rules/concepts, and primary tools for **{clean_role}**.
2. **Weeks 4–6 (Core Practice):** Practice hands-on exercises and build small foundational tasks in **{clean_role}**.
3. **Weeks 7–9 (Applied & Edge Cases):** Handle real-world scenarios, mistakes/debugging, and quality/safety standards.
4. **Weeks 10–12 (Capstone & Readiness):** Complete 2 practical projects/assessments and prepare for interviews or real-world execution.
"""


def generate_roadmap_ai(target_role: str, exp_level: str) -> tuple[str, str | None]:
    clean_role = target_role.strip() or "Full-Stack Developer"
    api_key = get_openai_key()

    if not api_key:
        return (
            fallback_roadmap(clean_role, exp_level),
            "OPENAI_API_KEY not found in Secrets/Environment. Showing fallback roadmap.",
        )

    prompt = (
        f"Create a clear, detailed 12-week roadmap for '{clean_role}' at '{exp_level}' level. "
        f"Keep it strictly relevant to '{clean_role}' (do not force unrelated software jargon if it's a non-tech/practical course). "
        f"Include: Overview, Key Skills/Tools, Weeks 1-3, Weeks 4-6, Weeks 7-9, Weeks 10-12 milestones, "
        f"2 practical projects/exercises, and an interview/readiness checklist."
    )

    try:
        return call_openai(prompt, api_key), None
    except Exception as e:
        return fallback_roadmap(clean_role, exp_level), f"OpenAI error: {e}"


with tab1:
    st.subheader("Custom Career Roadmap Generator")
    st.write("Enter any target role or course to generate a detailed AI-powered roadmap.")

    role = st.text_input(
        "Target Role / Course (e.g., Full-Stack Developer, Python Developer, Embedded Systems, Driving):",
        value="Full-Stack Developer",
    )
    level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Generate Roadmap"):
        with st.spinner("Calling OpenAI to generate your roadmap..."):
            roadmap_text, notice = generate_roadmap_ai(role, level)

        if notice:
            st.warning(notice)

        st.markdown(roadmap_text)


# -------------------- TAB 2: JOB SCAM DETECTOR --------------------
def fallback_scam_check(job_text: str) -> tuple[str, int, list[str]]:
    text = job_text.lower()
    score = 0
    flags = []

    patterns = [
        (r"\b(registration fee|security deposit|pay to apply|training fee|processing fee|refundable deposit)\b",
         "Requests upfront payment, registration fee, or security deposit.", 35),
        (r"\b(whatsapp|telegram)\b.*\b(contact|message|dm|number)\b|\b(contact|message|dm)\b.*\b(whatsapp|telegram)\b",
         "Directs candidates to WhatsApp/Telegram instead of an official portal/email.", 20),
        (r"\b(earn ₹|earn rs|daily payout|weekly payout|guaranteed income|no experience needed.*high salary)\b",
         "Promises unrealistic pay or guaranteed income with little/no experience.", 25),
        (r"\b(aadhaar|pan card|bank details|otp|cvv|passbook)\b",
         "Asks for sensitive ID, banking, or OTP details early.", 30),
        (r"\b(urgent hiring|limited slots|apply within 1 hour|immediate joining without interview|direct offer letter)\b",
         "Uses urgency pressure or skips interviews.", 20),
        (r"@gmail\.com|@yahoo\.com|@outlook\.com",
         "Uses a free email domain instead of an official company domain.", 15),
    ]

    for pat, reason, pts in patterns:
        if re.search(pat, text):
            score += pts
            flags.append(reason)

    score = min(score, 100)
    if score >= 50:
        verdict = "High Risk — Likely a Job Scam"
    elif score >= 20:
        verdict = "Medium Risk — Verify Carefully"
    else:
        verdict = "Low Risk — Looks Safer (Still Verify Company)"

    return verdict, score, flags


def analyze_scam_ai(job_text: str) -> tuple[str, str | None]:
    api_key = get_openai_key()
    if not api_key:
        verdict, score, flags = fallback_scam_check(job_text)
        bullets = "\n".join(f"- {f}" for f in flags) if flags else "- No obvious scam keywords detected."
        return (
            f"**{verdict}** (Offline Risk Score: {score}/100)\n\n**Red Flags:**\n{bullets}",
            "OPENAI_API_KEY not found in Secrets/Environment. Showing offline scan.",
        )

    prompt = (
        "Analyze the following job posting, internship offer, or recruiter message for job scam signs. "
        "Provide:\n"
        "1. **Risk Level** (Low / Medium / High) and short summary\n"
        "2. **Red Flags & Signals** found in the text\n"
        "3. **Safe Next Steps** to verify legitimacy\n\n"
        f"Text to analyze:\n{job_text}"
    )

    try:
        return call_openai(prompt, api_key), None
    except Exception as e:
        verdict, score, flags = fallback_scam_check(job_text)
        bullets = "\n".join(f"- {f}" for f in flags) if flags else "- No obvious scam keywords detected."
        return (
            f"**{verdict}** (Offline Risk Score: {score}/100)\n\n**Red Flags:**\n{bullets}",
            f"OpenAI error: {e}",
        )


with tab2:
    st.subheader("Job Scam Detector")
    st.write("Paste a job post, offer letter text, or recruiter message for AI-powered scam analysis.")

    job_input = st.text_area(
        "Job Posting / Recruiter Message:",
        height=180,
        placeholder="Paste the job description, salary details, contact info, or recruiter message here...",
    )

    if st.button("Analyze Job Posting"):
        if not job_input.strip():
            st.warning("Please paste a job posting or message first.")
        else:
            with st.spinner("Calling OpenAI to analyze job posting..."):
                result_md, notice = analyze_scam_ai(job_input)

            if notice:
                st.warning(notice)

            st.markdown(result_md)
