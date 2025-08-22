# 📊 AI-Powered Network & System Monitoring Reports  

[![Streamlit App](https://img.shields.io/badge/Live-Demo-FF4B4B?logo=streamlit&logoColor=white)](https://ai-powered-ns-reporting.streamlit.app/)  [![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)  [![Gemini API](https://img.shields.io/badge/Powered%20by-Gemini%202.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)  

---

This **proof-of-concept application** ingests one or more system log files and uses the [Gemini Developer API](https://ai.google.dev/) (`gemini-2.5-flash` model) to generate insights covering the most recent **7 days** of activity.  

The **goal** is to demonstrate how generative AI can enhance the productivity of network and system administrators by assisting with log analysis, anomaly detection, and incident reporting.  

---

## 🚀 [Live Demo](https://ai-powered-ns-reporting.streamlit.app/)  

---

## ⚠ Important Notice  
This is **only a proof of concept**.  

- Do **not** use sensitive or production system logs unless you are certain your chosen AI provider guarantees that logs will not be retained or reused for training.  
- The sample logs in this repository (`/sample-logs`) are AI-generated. They were created by prompting a model to simulate web server access/error logs, Fail2Ban logs, syslogs, and other system logs relevant to the proposed setup.  

---

## 📑 Example Prompt for Generating Sample Logs
```
Imagine a server with hostname group-01-vm that is used to host a WordPress website for an organization called Group01. 
The VM runs Debian 12 with Apache, and Fail2Ban is enforced for various jails, including Apache jails.

Between August 1–19, 2025, the website was inaccessible for 1 hour 32 minutes on August 19 starting at 21:04.

Generate various types of logs (as found under /var/log) covering this period, with entries that could indicate downtime and possible causes.
```

---

## 🔎 Concept Overview  

### 1. Centralized Monitoring  
Servers on the same network can periodically transfer their logs (e.g., via **cron jobs**) to a central **head node** running this application.  
The reporter then generates consolidated reports across all nodes.  

### 2. Manual Log Upload  
For systems outside the managed network, logs can be **manually uploaded** into the application for AI-based analysis.  

### 3. Unified Reporting  
Logs from multiple endpoints are aggregated into a **single AI-generated report**, highlighting:  
- Incidents  
- Anomalies  
- Security alerts  

---

# ⚙️ Using the Reporter  

## Prerequisites  

### 1. Secrets Configuration (`.streamlit/secrets.toml`)  
Create a `secrets.toml` file inside a `.streamlit/` folder containing your Google API key:  

```
GOOGLE_API_KEY = "<YOUR_API_KEY>"
```

👉 Replace `<YOUR_API_KEY>` with a Google AI Studio key from aistudio.google.com.


### 2. 2. Variables Configuration (`vars.cfg`)



Define your log directory and Gemini model in a `vars.cfg` file:

```
[DEFAULT]
LOG_DIR = ./sample-logs
GEMINI_MODEL = gemini-2.5-flash
```

#### 📌 Log format requirement:
Each log file must follow the naming convention:

`<hostname>.<logfile>`

When transferring logs via cron jobs, prepend the hostname to each file automatically.

### 3. Python environment
Ensure you are running minimum Python 3.11.

Install dependencies from `requirements.txt`:

```
pip install -r requirements.txt
```

### 4. `prompt`
Customize the prompt file as needed to adjust the style and scope of AI-generated reports.

## Deployment
Run the application with:

```
streamlit run 📊 Network and System Monitoring Reporter.py
```

