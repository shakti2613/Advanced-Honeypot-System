#!/usr/bin/env python3
"""
Test script to demonstrate honeypot functionality
This will now show attacks in the dashboard!
"""

import socket
import time

def send_attack(port, data, attack_name):
    """Send test attack to honeypot"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('localhost', port))
        sock.send(data)
        response = sock.recv(1024)
        print(f"✅ {attack_name} → Port {port} - SUCCESS!")
        sock.close()
        return True
    except Exception as e:
        print(f"❌ {attack_name} → Port {port} - FAILED: {e}")
        return False

def run_tests():
    """Run various attack simulations"""
    print("="*70)
    print("🧪 HONEYPOT TEST SUITE - Simulating Network Attacks")
    print("="*70)
    print("\n⚡ Testing honeypot with various attack types...")
    print("   These attacks WILL appear on the dashboard!")
    print("   Watch: http://localhost:5000\n")
    print("Make sure honeypot.py is running first!")
    print("Starting tests in 3 seconds...\n")
    time.sleep(3)
    
    tests = [
        # SQL Injection attacks
        (80, b"GET /?id=1' UNION SELECT * FROM users-- HTTP/1.1\r\nHost: test.com\r\n\r\n", "SQL Injection"),
        (3306, b"SELECT * FROM mysql.user WHERE user='root'", "MySQL Attack"),
        
        # XSS attacks
        (80, b"GET /?search=<script>alert('XSS')</script> HTTP/1.1\r\nHost: test.com\r\n\r\n", "XSS Attack"),
        
        # Directory Traversal
        (80, b"GET /../../../../etc/passwd HTTP/1.1\r\nHost: test.com\r\n\r\n", "Directory Traversal"),
        
        # SSH scanning
        (22, b"SSH-2.0-OpenSSH_8.0\r\n", "SSH Scan"),
        
        # Brute Force
        (22, b"admin:password123\r\n", "SSH Brute Force"),
        (23, b"root\r\npassword\r\n", "Telnet Login"),
        
        # RDP attack
        (3389, b"\x03\x00\x00\x13\x0e\xd0\x00\x00", "RDP Scan"),
        
        # HTTP reconnaissance
        (80, b"GET / HTTP/1.1\r\nHost: target.com\r\nUser-Agent: Nmap\r\n\r\n", "HTTP Recon"),
        (8080, b"GET /admin HTTP/1.1\r\nHost: admin.com\r\n\r\n", "Admin Panel Scan"),
        
        # FTP attack
        (21, b"USER anonymous\r\nPASS guest@\r\n", "FTP Brute Force"),
        
        # SMTP attack
        (25, b"HELO attacker.com\r\nMAIL FROM:<spam@evil.com>\r\n", "SMTP Abuse"),
        
        # MySQL exploit
        (3306, b"\x00\x00\x00\x0a5.7.31", "MySQL Exploit"),
        
        # PostgreSQL
        (5432, b"PGDATASTYLE=ISO", "PostgreSQL Scan"),
        
        # IMAP
        (143, b"A001 LOGIN admin password\r\n", "IMAP Brute Force"),
        
        # POP3
        (110, b"USER admin\r\nPASS 12345\r\n", "POP3 Brute Force"),
    ]
    
    print(f"🎯 Running {len(tests)} attack simulations...\n")
    
    success_count = 0
    for port, data, attack_name in tests:
        if send_attack(port, data, attack_name):
            success_count += 1
        time.sleep(0.3)  # Small delay between attacks
    
    print("\n" + "="*70)
    print(f"✅ Test Complete: {success_count}/{len(tests)} attacks sent successfully!")
    print("="*70)
    print("\n📊 NOW CHECK THE DASHBOARD:")
    print(f"   🌐 http://localhost:5000")
    print("\n📝 You should see:")
    print("   • Total attempts count increased")
    print("   • Port status cards showing which ports were hit")
    print("   • Detailed attack logs with your IP and data")
    print("   • Top targeted ports chart")
    print("\n💡 TIP: Try from another device on your network for more realistic test!")
    print("   Example: curl http://YOUR_PC_IP:80 from your phone\n")

if __name__ == '__main__':
    run_tests()