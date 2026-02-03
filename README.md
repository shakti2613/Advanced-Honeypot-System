# 🔒 Advanced Honeypot System

A professional **network security honeypot** designed to monitor, detect, and analyze real-world cyber attacks in real time. This project simulates vulnerable network services on multiple commonly targeted ports and provides a modern web dashboard for live visualization and analysis.

---

## 🚀 Features

* 🕵️‍♂️ Monitors **12 commonly attacked ports** (SSH, HTTP, FTP, Telnet, MySQL, RDP, SMTP, etc.)
* ⚡ Real-time detection and logging of malicious connections
* 🧠 Automatic attack classification:

  * SQL Injection
  * Cross-Site Scripting (XSS)
  * Brute Force attacks
  * Port scanning & suspicious payloads
* 🌐 Filters localhost traffic (127.0.0.1) to avoid noise
* 📡 Logs **all external IP traffic** (LAN / WAN / Internet)
* 🧾 Detailed logs including:

  * Source IP address
  * Target port & protocol
  * Attack type & timestamp
  * Hexadecimal payload dumps
* 📊 **Beautiful web dashboard** with live attack visualization

---

## 🖥️ Web Dashboard

The Flask-based dashboard provides:

* Live connection statistics
* Protocol-wise attack distribution
* Top attacking IP addresses
* Recent attacks and payloads
* Easy-to-read logs for analysis

Accessible via browser:

```
http://localhost:8080
```

---

## 📁 Project Structure

```
honeypot_system/
│── dashboard.py          # Web dashboard server
│── honeypot_server.py    # Core honeypot logic
│── start.sh              # Start honeypot & dashboard
│── stop.sh               # Stop all services
│── templates/
│   └── dashboard.html    # Dashboard UI
│── logs/                 # All generated logs
│   ├── connections.txt
│   ├── attacks.txt
│   ├── payloads.txt
│   └── blocked_ips.txt
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/advanced-honeypot-system.git
cd advanced-honeypot-system
```

### 2️⃣ Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3️⃣ Start the System

```bash
chmod +x start.sh stop.sh
./start.sh
```

### 4️⃣ Stop the System

```bash
./stop.sh
```

> ⚠️ **Note:** Running on privileged ports (e.g., 22, 80) may require root privileges.

---

## 🎯 Use Cases

* Cybersecurity research & experimentation
* Learning attack patterns and attacker behavior
* Network defense and monitoring practice
* Academic projects and demonstrations

---

## 🛡️ Disclaimer

This project is intended **for educational and research purposes only**. Do not deploy on production systems or networks without proper authorization.

---

## 👩‍💻 Author

Developed as a cybersecurity and network defense project.

⭐ If you like this project, don’t forget to star the repository!
