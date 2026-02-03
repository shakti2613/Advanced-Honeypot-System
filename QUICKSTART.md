# 🚀 QUICK START GUIDE

## Installation (1 minute)

```bash
# Install dependencies
pip install --break-system-packages Flask

# Run the honeypot (requires sudo for ports < 1024)
sudo python3 honeypot.py
```

## Access Dashboard
Open browser: **http://localhost:5000**

## ⚠️ IMPORTANT: About Real Attacks

**This honeypot NOW FILTERS local traffic!**
- ✅ Only logs EXTERNAL attacks from internet
- ❌ Ignores localhost (127.0.0.1) traffic
- ❌ Ignores local network (192.168.x.x, 10.x.x.x)
- ❌ Test scripts won't show attacks (filtered out!)

## To See REAL Attacks:

### Option 1: Cloud VPS (Fastest - attacks in 1-4 hours)
```bash
# Deploy on DigitalOcean, AWS, Linode, etc.
# Attacks start within hours!
```

### Option 2: Port Forwarding (Home Router)
```bash
# Forward ports to your honeypot machine
# Attacks start in 1-5 days
```

**Read: HOW_TO_GET_REAL_ATTACKS.md** for detailed guide!

## Test Local Filtering (Optional)
```bash
python3 test_honeypot.py
```
This will show connections but honeypot will IGNORE them (as designed).

## What You'll See

**Without Internet Exposure:**
- Dashboard shows: "Waiting for real external attacks..."
- No attacks logged (this is correct!)
- Terminal shows: "[IGNORED] Local traffic..."

**With Internet Exposure:**
- Real attacks appear on dashboard
- External IPs logged (185.x.x.x, 91.x.x.x, etc.)
- Terminal shows: "🚨 REAL ATTACK! from X.X.X.X"

## Features

The honeypot will:
- ✅ Monitor 12 common ports in real-time
- ✅ Detect and classify attacks automatically  
- ✅ Log everything to a timestamped .txt file
- ✅ Show live dashboard with beautiful UI
- ✅ Filter out local/test traffic automatically
- ✅ Only show REAL internet attacks!

## Stop Honeypot
Press `Ctrl+C` in the terminal running honeypot.py

---

**⚠️ LEGAL WARNING**: Only use on networks you own or have permission to monitor!

**💡 TIP**: For immediate real attacks, deploy on a cheap cloud VPS!