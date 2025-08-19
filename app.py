# streamlit_app.py
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Choose a Gemini model (text-only for summaries)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="AI-Powered Network Monitoring Reports", layout="wide")

st.title("📊 AI-Powered Network & System Monitoring Reports")
st.markdown("Upload your weekly network/system log files and generate AI-powered summary reports.")

# Upload log files
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
            prompt = f"""
            You are an IT assistant for network/system monitoring.
            Analyze the following log data and generate a **weekly report** with:
            - Key incidents detected
            - Repeated errors or anomalies
            - Security-related warnings
            - System performance trends
            - Suggested actions for administrators

            Keep the report structured with bullet points and short paragraphs. Read only the logs from the latest 7 days.
            If you can format each section in table form, it will be better.
            
            Logs:
            {all_logs[:20000]}  # Truncate for safety if very large
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
