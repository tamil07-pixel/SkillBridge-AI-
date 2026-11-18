import os
import streamlit as st
from google import genai

# Page configuration
st.set_page_config(
    page_title="Custom Career Roadmap Generator",
    page_icon="🚀",
    layout="centered"
)

# Initialize Session State for Usage Limit
if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

MAX_LIMIT = 20

# Fetching Gemini API Key from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API Key is missing! Please configure 'GEMINI_API_KEY' in Streamlit Cloud Secrets.")
    st.stop()

# Initialize Gemini client using the correct google-genai SDK
client = genai.Client(api_key=api_key)

st.title("Custom Career Roadmap Generator")
st.markdown("Enter your target role to generate a step-by-step learning path and required skills.")

# Show remaining limit
remaining = MAX_LIMIT - st.session_state.usage_count
st.sidebar.markdown(f"**Usage Limit:** {st.session_state.usage_count}/{MAX_LIMIT} used")

# User inputs
target_role = st.text_input("Target Role (e.g., Full Stack Developer, Embedded Systems Engineer):", "Software Developer")
experience_level = st.selectbox("Current Experience Level:", ["Beginner", "Intermediate", "Advanced"])

if st.button("Generate Roadmap"):
    if st.session_state.usage_count >= MAX_LIMIT:
        st.error("Daily limit reached! You have used all 20 free generations for now. Try again later.")
    elif not target_role.strip():
        st.warning("Please enter a target role.")
    else:
        with st.spinner("Generating your personalized career roadmap..."):
            try:
                prompt = f"""
                Create a detailed, step-by-step career roadmap and required technical skills for a {experience_level} aiming to become a {target_role}.
                Include key milestones, essential tools/technologies, and actionable advice. Format the output cleanly using Markdown.
                """
                
                # Correct API call structure for google-genai
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                
                # Increment usage count on success
                st.session_state.usage_count += 1
                
                st.success("Roadmap Generated Successfully!")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

