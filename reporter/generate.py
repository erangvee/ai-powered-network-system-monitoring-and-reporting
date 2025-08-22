import streamlit as st
import os
from glob import glob


def load_prompt(file_path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
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
    prompt = load_prompt("prompt") + f"""
            Logs:
            {all_logs[-20000:]} 
            """
    
    with st.spinner(f"Analyzing logs for {hostname}..."):
        response = model.generate_content(prompt)
        report = response.text
    st.session_state["reports"][hostname] = report
