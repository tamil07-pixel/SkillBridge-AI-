import os
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🚀",
    layout="wide"
)

# Initialize Gemini API
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 Gemini API Key is missing! Please configure 'GEMINI_API_KEY' in Streamlit Cloud Secrets.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# App Header
st.title("🚀 SkillBridge AI")
st.caption("AI-powered Career Roadmap Generator & Job Scam Detector")

# Navigation Tabs
tab1, tab2 = st.tabs(["🛣️ Career Roadmap Generator", "🔍 Job Scam Detector"])

# TAB 1: Career Roadmap Generator
with tab1:
    st.header("Custom Career Roadmap Generator")
    st.write("Enter your target role to generate a step-by-step learning path and required skills.")

    role = st.text_input("Target Role (e.g., Full Stack Developer, Embedded Systems Engineer):", key="roadmap_role")
    experience = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"], key="roadmap_exp")

    if st.button("Generate Roadmap", key="btn_roadmap"):
        if role.strip():
            with st.spinner("Generating your roadmap..."):
                try:
                    prompt = f"Create a step-by-step career roadmap for a {experience} level {role}. Include key skills, tools to learn, and recommended projects."
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a target role.")

# TAB 2: Job Scam Detector
with tab2:
    st.header("Job Scam Detector")
    st.write("Paste the job offer text or email below to check if it's potentially a scam.")

    job_text = st.text_area("Job Offer / Email Content:", height=150, key="scam_text")

    if st.button("Analyze Job Offer", key="btn_scam"):
        if job_text.strip():
            with st.spinner("Analyzing job offer..."):
                try:
                    prompt = f"Analyze the following job offer for red flags or signs of a scam. Provide a risk assessment and explanation:\n\n{job_text}"
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please paste some job offer text to analyze.")
