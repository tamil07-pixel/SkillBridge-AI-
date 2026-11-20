import os
import time
import streamlit as st

st.set_page_config(page_title="Custom Career Roadmap Generator", layout="centered")

st.title("Custom Career Roadmap Generator")
st.write("Enter your target role to generate a step-by-step learning path and required skills.")

role = st.text_input(
    "Target Role (e.g., Full Stack Developer, Embedded Systems Engineer):",
    value="Full Stack Developer",
)
level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])


def fallback_roadmap(target_role: str, exp_level: str) -> str:
    clean_role = target_role.strip() or "Software Developer"
    return f"""
### Roadmap for {clean_role} ({exp_level})

1. **Core Foundations (Weeks 1–3)**
   - Master programming basics, data structures, and problem-solving relevant to **{clean_role}**.
   - Learn Git & GitHub for version control and clean project documentation.

2. **Core Stack & Tools (Weeks 4–8)**
   - Build hands-on modules using the primary frameworks, APIs, and databases needed for **{clean_role}**.
   - Practice debugging, testing, and reading official documentation.

3. **Projects & Deployment (Weeks 9–12)**
   - Build 2 real-world end-to-end projects and deploy them live.
   - Add clear READMEs, architecture notes, and live demos to your portfolio.

4. **Interview & Role Readiness**
   - Practice role-specific coding/system questions and refine your resume around measurable outcomes.
"""


def generate_with_retry(target_role: str, exp_level: str, retries: int = 2) -> tuple[str, str | None]:
    # Replace this block with your actual AI/API call if you use one
    api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

    for attempt in range(retries + 1):
        try:
            if not api_key:
                # No external key configured -> return structured local roadmap cleanly
                return fallback_roadmap(target_role, exp_level), "No API key found; showing structured offline roadmap."

            # Put your actual API client call here
            return fallback_roadmap(target_role, exp_level), None

        except Exception as e:
            if attempt < retries:
                time.sleep(1.5)
                continue
            return fallback_roadmap(target_role, exp_level), f"API call failed: {type(e).__name__}: {e}"

    return fallback_roadmap(target_role, exp_level), None


if st.button("Generate Roadmap"):
    with st.spinner("Generating your roadmap..."):
        roadmap_text, info_or_err = generate_with_retry(role, level)

    if info_or_err:
        st.warning(info_or_err)

    st.markdown(roadmap_text)
