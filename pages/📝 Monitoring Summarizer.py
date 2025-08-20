import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from glob import glob

st.set_page_config(page_title="Summarizer", layout="wide")


load_dotenv()

# configure API key from https://aistudio.google.com/
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# choose a Gemini model (text-only for summaries)
model = genai.GenerativeModel("gemini-2.5-flash")


st.title("📊 AI-Powered Network & System Monitoring Reporting - Executive Summary")
st.markdown("""
Generate AI-powered weekly reports for multiple servers.
Select a server and click "Generate Report" to process its logs.
""")

# directory containing logs
LOG_DIR = "./sample-logs"

all_logs = ""
source_logs = os.listdir(LOG_DIR)
for filename in source_logs:
    file_path = os.path.join(LOG_DIR, filename)
    if os.path.isfile(file_path):  # make sure it's a file
        with open(file_path, "rb") as f:  # open in binary mode
            string_data = f.read().decode("utf-8", errors="replace")
        all_logs += f"\n\n--- FILE: {filename} ---\n{string_data}"
        
if st.button("Generate Weekly Report"):
        with st.spinner("Analyzing logs and generating weekly summary..."):
            prompt = f"""
             You are an IT assistant for network/system monitoring.

            Analyze the following log data and generate a **weekly report** covering the last 7 days of the logs.
            This means, if the last day is the 14th, the first day will be the 6th.

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
