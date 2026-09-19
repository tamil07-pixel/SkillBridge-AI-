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
    
    target_role = st.text_input("Target Role (e.g., Full Stack Developer, Embedded Systems Engineer):")
    experience_level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Generate Roadmap", type="primary"):
        if target_role:
            with st.spinner("Generating roadmap..."):
                prompt = f"""
                Create a detailed, step-by-step career roadmap for a {experience_level} looking to become a {target_role}.
                Include:
                1. Key technical and soft skills to learn.
                2. Phase-by-phase learning timeline.
                3. Essential projects to build for Resume.
                4. Recommended certifications or resources.
                Keep the output clean, structured with markdown headings and bullet points.
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.warning("Please enter a target role!")

# TAB 2: Job Scam Detector
with tab2:
    st.header("Job Offer Scam Detector")
    st.write("Paste the job offer text or email message below to check its authenticity.")
    
    job_text = st.text_area("Enter Job Offer / Email Text:", height=200)
    
    if st.button("Analyze Offer", type="primary"):
        if job_text:
            with st.spinner("Analyzing text..."):
                prompt = f"""
                Analyze the following job description/offer message for potential scam indicators (e.g., asking for money, suspicious email domains, unrealistic salaries, lack of interview process).
                
                Text to analyze:
                {job_text}
                
                Provide:
                1. Risk Rating (Safe, Moderate Risk, High Risk / Scam)
                2. Key Red Flags detected (if any)
                3. Recommendation for the user
                """
                response = model.generate_content(prompt)
                st.markdown(response.text)
        else:
            st.warning("Please enter text to analyze!")
