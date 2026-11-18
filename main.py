import os
import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🚀",
    layout="wide"
)

# Initialize Gemini API using the new client
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("🔑 Gemini API Key is missing! Please configure 'GEMINI_API_KEY' in Streamlit Cloud Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# Safe generation function with new SDK and model fallbacks
def generate_ai_content(prompt):
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "429" in str(e) or "404" in str(e) or "quota" in str(e).lower() or "not found" in str(e).lower():
                continue
            else:
                raise e
    raise Exception("API quota exceeded for all models. Please try again later.")

# App Header
st.title("🚀 SkillBridge AI")
st.caption("AI-powered Career Roadmap Generator & Job Scam Detector")

# Navigation Tabs
tab1, tab2 = st.tabs(["🛣️ Career Roadmap Generator", "🔍 Job Scam Detector"])

# TAB 1: Career Roadmap Generator
with tab1:
    st.header("Custom Career Roadmap Generator")
    st.write("Enter your target role to generate a step-by-step learning path and required skills.")
    
    target_role = st.text_input("Target Role (e.g., Full Stack Developer, Embedded Systems Engineer):", key="roadmap_role")
    experience_level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"], key="roadmap_exp")
    
    if st.button("Generate Roadmap", type="primary", key="btn_roadmap"):
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
                try:
                    output_text = generate_ai_content(prompt)
                    st.markdown(output_text)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a target role!")

# TAB 2: Job Scam Detector
with tab2:
    st.header("Job Offer Scam Detector")
    st.write("Paste the job offer text or email message below to check its authenticity.")
    
    job_text = st.text_area("Enter Job Offer / Email Text:", height=200, key="scam_text")
    
    if st.button("Analyze Offer", type="primary", key="btn_scam"):
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
                try:
                    output_text = generate_ai_content(prompt)
                    st.markdown(output_text)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter text to analyze!")
