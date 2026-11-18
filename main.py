import os
import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🚀",
    layout="wide"
)

# Initialize Groq API
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("🔑 Groq API Key is missing! Please configure 'GROQ_API_KEY' in Streamlit Cloud Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# Groq generation function using fast & reliable llama model
def generate_ai_content(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

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
