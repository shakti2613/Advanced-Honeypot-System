# 🔒 Advanced Honeypot System (Real-Time)

A modern **Python-based network honeypot** designed to detect, classify, and log cyber attacks in real time. This updated version focuses on **HTTP-based attack detection**, clean architecture, and a lightweight web interface for monitoring suspicious activity.

---

## ✨ Key Highlights

* 🛡️ Real-time honeypot for monitoring malicious requests
* 🌐 Focused on **HTTP attack detection** (clean & modular design)
* 🧠 Automatic detection of common attacks:

  * SQL Injection
  * Cross-Site Scripting (XSS)
  * Brute-force & suspicious patterns
* 📊 Web dashboard for live visualization
* 🧾 Detailed logging with timestamps and payload data
* 🚫 Filters localhost traffic (127.0.0.1)
* 🌍 Logs all external IP traffic (LAN / WAN / Internet)

---

## 📁 Project Structure

```
honeypot/
│── honeypot.py                 # Core HTTP honeypot logic
│── test_honeypot.py            # Testing script
│── requirements.txt            # Python dependencies
│── templates/
│   └── index.html              # Web dashboard UI
│── honeypot_logs_*.txt         # Generated attack logs
│── README.md                   # Project documentation
│── QUICKSTART.md               # Quick usage guide
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/advanced-honeypot-system.git
cd advanced-honeypot-system/honeypot
```

### 2️⃣ Install Dependencies

```bash
pip3 install -r requirements.txt
```

---

## ▶️ Running the Honeypot

```bash
python3 honeypot.py
```

The honeypot will start listening for HTTP requests and automatically log any suspicious activity.

Open the dashboard in your browser:

```
http://localhost:5000
```

---

## 🧪 Testing

To simulate attacks or normal traffic:

```bash
python3 test_honeypot.py
```

---

## 📝 Logging Details

Each detected request is logged with:

* Source IP address
* Request method & path
* Detected attack type (if any)
* Timestamp
* Raw payload / request data

Log files are saved with timestamps:

```
honeypot_logs_YYYYMMDD_HHMMSS.txt
```

---

## 🎯 Use Cases

* Cybersecurity learning & labs
* Understanding web attack patterns
* Honeypot-based threat analysis
* Academic projects & demonstrations

---

## ⚠️ Disclaimer

This project is intended **strictly for educational and research purposes**. Do not deploy on production systems or public networks without permission.

---

## ⭐ Acknowledgement

If you find this project useful, consider starring the repository and sharing feedback.

