# 🔐 SecureTheEye - A Secure IP Camera Protection System
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Maintained](https://img.shields.io/badge/Maintained-yes-brightgreen.svg)

**SecureTheEye** is a comprehensive Python-based desktop application designed to enhance the security of IP cameras in local area networks. It incorporates intelligent tools for automatic IP camera discovery, vulnerability assessment via the CVE database, AI-based remediation recommendations, and real-time intrusion detection using machine learning techniques.

---

## 🧠 Project Aim

To develop a comprehensive and user-friendly application that enhances the security of IP cameras with the help of automation and artificial intelligence in vulnerability scanning, abnormal behavior or network traffic detection, real-time alerting, and providing common remediation strategies. The goal is to mitigate the growing threats against IP cameras and improve user confidence in their deployment.

---

## ✅ Project Objectives

1. **IP Camera Discovery Tool**  
   Automatically identifies active IP cameras on the local network using Nmap scanning based on user-defined parameters such as IP address and port.

2. **Vulnerability Assessment Engine**  
   Integrates with the CVE (Common Vulnerabilities and Exposures) database to identify known vulnerabilities in discovered IP cameras.

3. **AI-Based Remediation and Reporting**  
   Provides basic, tailored remediation strategies for each vulnerability detected using an NLP-based ML model. Generates detailed, formatted reports summarizing findings and recommendations.

4. **Real-Time Intrusion Detection System (IDS)**  
   Incorporates a lightweight AI-based IDS to monitor IP camera traffic and alert users to abnormal behaviors or network attacks (e.g., SYN flooding), with automatic response features.

---

## 🖥️ Features Overview

- 🔍 **Auto Discovery** of IP cameras on LAN
- 📜 **Vulnerability Lookup** from the NVD CVE database
- 🤖 **AI Model** for remediation suggestions
- 📊 **Report Generation** in structured PDF format
- 🚨 **Real-Time IDS** with audio alerts
- 🎮 **User-Friendly Interface** built with PyQt5

---

## 🚀 Installation and Running Instructions

### Prerequisites

- Python 3.8 or newer : [Python](https://www.python.org/downloads/)

- [Nmap](https://nmap.org/download.html) must be installed and added to your system's environment variables.

### Step-by-Step Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/TingWai-85/SecureIPCamera.git
   cd SecureIPCamera
   ```

2. **Install Python Dependencies**
   Ensure you have ```pip``` installed. Then, run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Nmap**
   Download and install Nmap from the [official site](https://nmap.org/download.html), and ensure it's available in your system's PATH.

4. **Navigate to FrontEnd Directory**
   ```bash
   cd FrontEnd
   ```

5. **Run the Application**
   ```bash
   python Main_F.py
   ```

---

## 📦 Required Python Libraries

These are defined in requirements.txt:
  ```nginx
  PyQt5
  scapy
  joblib
  pandas
  pygame
  psutil
  python-nmap
  requests
  beautifulsoup4
  reportlab
  opencv-python
  ```
Install them via:
  ```bash
  pip install -r requirements.txt
  ```
---

## 📌 Technologies Used

- Python 3.8+
- PyQt5 – GUI development
- Scapy – Packet crafting and sniffing
- OpenCV – Video stream interaction
- Requests & BeautifulSoup4 – CVE scraping
- Joblib – Model persistence
- ReportLab – PDF report generation
- AI Models – Built using Scikit-learn for IDS and NLP-based remediation

---

## 📄 Sample Use-Cases

- Identify unsecured IP cameras on the network.
- Detect if an IP camera uses default credentials.
- Find known CVEs associated with a camera's firmware or open ports.
- Generate a mitigation report in PDF.
- Detect and alert on real-time SYN Flood or abnormal packet behavior.

---

## 🔒 Disclaimer

This project is built strictly for educational and research purposes. Do not use it to scan or interfere with devices or networks you do not own or have explicit permission to test. Unauthorized access or scanning may be considered illegal under cybersecurity laws.

---

## 🙌 Acknowledgements
