# 📊 AI-Powered Network & System Monitoring Reports  

This proof-of-concept application ingests one or more system log files and uses the [Gemini Developer API](https://ai.google.dev/) (`gemini-2.5-flash` model) to generate insights covering the most recent 7 days of activity.  

The **goal** is to demonstrate how generative AI can enhance the productivity of network and system administrators by assisting with log analysis, anomaly detection, and incident reporting.  

---

## ⚠ Important Notice  
This is **only a proof of concept**.  

- Do **not** use sensitive or production system logs unless you are certain your chosen AI provider guarantees that logs will not be retained or reused for training.  
- The sample logs in this repository (`/sample-logs`) are AI-generated. They were created by prompting a model to simulate web server access/error logs, Fail2Ban logs, syslogs, and other system logs relevant to the proposed setup.  

---

## Example Prompt for Generating Sample Logs
```
Imagine a server with hostname group-01-vm that is used to host a WordPress website for an organization called Group01. The VM runs Debian 12 with Apache, and Fail2Ban is enforced for various jails, including Apache jails.

Between August 1–19, 2025, the website was inaccessible for 1 hour 32 minutes on August 19 starting at 21:04.

Generate various types of logs (as found under /var/log) covering this period, with entries that could indicate downtime and possible causes.
```

---

## Concept Overview
### 1. Centralized Monitoring
Servers on the same network can be configured to periodically transfer their logs (e.g., via cron jobs) to a central "head node" running this application. Reports are then generated across all nodes.

### 2. Manual Log Upload

For systems outside the managed network, logs can be manually uploaded into the application for analysis.

### 3. Unified Reporting

Logs from multiple endpoints are summarized into a single AI-generated report, highlighting incidents, anomalies, and security alerts.

---

# Using the Reporter
## Prerequisites
### 1. `.env` file
Create a `.env` file containing the following details:
```
GOOGLE_API_KEY=<YOUR API KEY>
```

Where `<YOUR API KEY>` is a Google AI Studio API key generated from https://aistudio.google.com/. 


### 2. vars.cfg
In `vars.cfg` file, specify the location of the logs and the Gemini model you will be using. Note that the logs should be in this format:

`<hostname>.<logfile>`

The assumption is that when using cron to transfer logs to the head node, a command that would prepend the hostname to the log files is also used.

### 3. Python 3.11 environment
Install the required packages from `requirements.txt` by executing:

```
pip install -r requirements.txt
```

## Deployment
Run the following command:

```
streamlit run 📊 Network and System Monitoring Reporter.py
```

