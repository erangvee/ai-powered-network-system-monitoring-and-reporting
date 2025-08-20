# streamlit_app.py
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

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
            prompt = f"""
             You are an IT assistant for network/system monitoring.

            Analyze the following log data and generate a **weekly report** covering the last 7 days.

            Requirements:

            1. Present **all sections in Markdown table format**.
            2. Include the following sections, each as its own table:

                - **Key Incidents Detected**
                    Columns: Date | Time | Server Name | Log Source | Description | Severity | Recommended Actions
                    
                - **Repeated Errors or Anomalies**
                    Columns: Date | Time | Server Name | Log Source | Description | Frequency | Notes
                    
                - **Security-Related Warnings**
                    Columns: Date | Time | Server Name | Log Source | Description | Severity | Recommended Actions
                    
                - **System Performance Trends**
                    Columns: Date | Time | Server Name | Metric | Observation | Recommendation
                    
                - **Summary of Suggested Actions for Administrators**
                    Columns: Section | Action | Priority | Notes

            3. Each table row should contain **one concise entry**.
            4. Keep descriptions informative but brief.
            5. Use proper capitalization and punctuation.

            In another section, give an executive summary that we can show to our top management.

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