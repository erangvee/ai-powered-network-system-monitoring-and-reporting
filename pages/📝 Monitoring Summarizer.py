import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
from reporter import generate
from glob import glob

st.set_page_config(page_title="Summarizer", layout="wide")

load_dotenv()

# configure API key from https://aistudio.google.com/
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
            prompt = generate.load_prompt("prompt") + f"""
                    Logs:
                    {all_logs[-20000:]}  # Take the last 20k characters for safety
                    """

            response = model.generate_content(prompt)
            report = response.text

        st.subheader("📑 Weekly Monitoring Report")
        st.write(report)

        st.download_button(
            "📥 Download Report",
            report,
            file_name="weekly_network_report.txt",
            mime="text/plain"
        )
