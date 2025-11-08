import streamlit as st
import requests

st.title("AI Resume Analyzer & Question Generator (Phase 1)")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())

    st.write("✅ Resume uploaded successfully!")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume..."):
            files = {"file": open(uploaded_file.name, "rb")}
            response = requests.post("http://127.0.0.1:8000/analyze_resume/", files=files)

        if response.status_code == 200:
            st.subheader("AI Analysis Report:")
            st.write(response.json()["questions"])

        else:
            st.error("❌ Something went wrong. Please try again.")
