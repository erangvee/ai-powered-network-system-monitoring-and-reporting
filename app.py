import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from glob import glob
from reporter import generate

load_dotenv()

# configure API key from https://aistudio.google.com/
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# choose a Gemini model (text-only for summaries)
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(
    page_title="AI-Powered Network Monitoring Reporting",
    layout="wide"
)

st.title("📊 AI-Powered Network & System Monitoring Reporting")
st.markdown("""
Generate AI-powered weekly reports for multiple servers.
Select a server and click "Generate Report" to process its logs.
""")

# directory containing logs
LOG_DIR = "./sample-logs"

# Detect servers automatically
log_files = glob(os.path.join(LOG_DIR, "*.*.log"))
servers = sorted(set(os.path.basename(f).split(".")[0] for f in log_files))

# Initialize session state
if "reports" not in st.session_state:
    st.session_state["reports"] = {}


# server selection
with st.container():
    selected_server = st.selectbox("Select server:", servers)
    generate_button = st.button("Generate Report")


reporter = st.empty()

# generate report button
if generate_button:
    generate.generate_report(selected_server, model)  # Your function to generate report
    report_text = st.session_state["reports"][selected_server]

    # Display the report in the placeholder (overwrites previous)
    with reporter.container():
        st.subheader(f"📑 Weekly Monitoring Report: {selected_server}")
        st.write(report_text)
        st.download_button(
            f"📥 Download Report: {selected_server}",
            report_text,
            file_name=f"weekly_report_{selected_server}.txt",
            mime="text/plain"
        )