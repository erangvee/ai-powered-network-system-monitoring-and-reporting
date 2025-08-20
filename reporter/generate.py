import streamlit as st
import os
from glob import glob


def load_server_logs(hostname, log_dir):
    """Load and concatenate all logs for a given server"""
    files = glob(os.path.join(log_dir, f"{hostname}.*log"))
    all_logs = ""
    for file_path in files:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        all_logs += f"\n\n--- FILE: {os.path.basename(file_path)} ---\n{content}"
    return all_logs

def generate_report(hostname, model, log_dir="./sample-logs"):
    """Generate a weekly report using Gemini API"""
    all_logs = load_server_logs(hostname, log_dir)
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

Logs:
{all_logs[-20000:]}  # Take the last 20k characters for safety

            """
    
    with st.spinner(f"Analyzing logs for {hostname}..."):
        response = model.generate_content(prompt)
        report = response.text
    st.session_state["reports"][hostname] = report
