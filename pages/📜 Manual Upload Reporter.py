# streamlit_app.py
import streamlit as st
import google.generativeai as genai
import os
import configparser

from reporter import generate
from dotenv import load_dotenv

load_dotenv()
config = configparser.ConfigParser()
config.read("vars.cfg")

# configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(config["DEFAULT"]["GEMINI_MODEL"])

st.set_page_config(page_title="AI-Powered Network Monitoring Reports", layout="wide")

st.title("📊 AI-Powered Network & System Monitoring Reports")
st.markdown("Upload your weekly network/system log files and generate AI-powered summary reports.")

uploaded_files = st.file_uploader(
    "Upload log files (text or .log files)", 
    type=["txt", "log"], 
    accept_multiple_files=True,
)

if uploaded_files:
    all_logs = ""
    for file in uploaded_files:
        string_data = file.read().decode("utf-8", errors="replace")
        all_logs += f"\n\n--- FILE: {file.name} ---\n{string_data}"

    st.success("✅ Logs successfully uploaded.")
    
    if st.button("Generate Weekly Report"):
        with st.spinner("Analyzing logs and generating weekly summary..."):
            prompt = generate.load_prompt("prompt") + f"""
                Logs:
                {all_logs[-20000:]}  # Take the last 20k characters for safety
            """

            response = model.generate_content(prompt)
            report = response.text

        st.subheader("📑 Weekly Monitoring Report")
        st.write(report)

        # Option to download
        st.download_button(
            "📥 Download Report",
            report,
            file_name="weekly_network_report.txt",
            mime="text/plain"
        )