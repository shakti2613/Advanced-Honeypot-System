#!/usr/bin/env python3
"""
Advanced Honeypot System with Real-time Network Scanning
Features: Multi-port monitoring, Real-time attack detection, Professional Web UI
"""

import socket
import threading
import datetime
import json
import os
from flask import Flask, render_template, jsonify
from collections import defaultdict
import time
import struct

app = Flask(__name__)

class HoneypotSystem:
    def __init__(self):
        self.attacks = []
        self.stats = {
            'total_attempts': 0,
            'unique_ips': set(),
            'ports_scanned': defaultdict(int),
            'protocols': defaultdict(int),
            'countries': defaultdict(int)
        }
        self.active_connections = []
        self.running = True
        self.log_file = f"honeypot_logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Common ports to monitor
        self.ports = [21, 22, 23, 25, 80, 110, 143, 443, 3306, 3389, 5432, 8080]
        
    def is_local_ip(self, ip):
        """Check if IP is localhost only (127.0.0.1)"""
        # Only filter out localhost - allow everything else including LAN IPs
        localhost_ips = ['127.0.0.1', 'localhost', '::1', '0.0.0.0']
        
        return ip in localhost_ips
    
    def log_attack(self, attack_data):
        """Log attack to file and memory (only external IPs)"""
        # Filter out local/test traffic
        if self.is_local_ip(attack_data['ip']):
            print(f"[IGNORED] Local traffic from {attack_data['ip']}:{attack_data['port']} - Not logging")
            return
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"""
{'='*80}
[{timestamp}] REAL ATTACK DETECTED
{'='*80}
Source IP: {attack_data['ip']}
Port: {attack_data['port']}
Protocol: {attack_data['protocol']}
Data Received: {attack_data['data'][:200]}
Attack Type: {attack_data['attack_type']}
Severity: {attack_data['severity']}
{'='*80}
"""
        
        # Write to log file
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
        
        # Store in memory for web UI
        attack_data['timestamp'] = timestamp
        self.attacks.insert(0, attack_data)
        if len(self.attacks) > 100:  # Keep last 100 attacks
            self.attacks.pop()
        
        # Update statistics
        self.stats['total_attempts'] += 1
        self.stats['unique_ips'].add(attack_data['ip'])
        self.stats['ports_scanned'][attack_data['port']] += 1
        self.stats['protocols'][attack_data['protocol']] += 1
        
        # Print alert for real attacks
        print(f"🚨 REAL ATTACK! {attack_data['attack_type']} from {attack_data['ip']}:{attack_data['port']}")
        
    def analyze_attack(self, data, port):
        """Analyze attack type based on payload"""
        data_lower = data.lower()
        
        if b'select' in data_lower or b'union' in data_lower or b'drop' in data_lower:
            return 'SQL Injection', 'HIGH'
        elif b'<script' in data_lower or b'javascript:' in data_lower:
            return 'XSS Attack', 'HIGH'
        elif b'../../../' in data_lower or b'..\\..\\' in data_lower:
            return 'Directory Traversal', 'MEDIUM'
        elif b'admin' in data_lower or b'root' in data_lower or b'password' in data_lower:
            return 'Brute Force / Credential Stuffing', 'MEDIUM'
        elif port == 22 and (b'ssh' in data_lower or len(data) > 0):
            return 'SSH Scanning/Attack', 'MEDIUM'
        elif port == 3306 and b'mysql' in data_lower:
            return 'MySQL Attack', 'HIGH'
        elif port == 3389:
            return 'RDP Attack', 'HIGH'
        elif b'get /' in data_lower or b'post /' in data_lower:
            return 'HTTP Reconnaissance', 'LOW'
        else:
            return 'Port Scanning', 'LOW'
    
    def create_response(self, port, protocol):
        """Create realistic responses to fool attackers"""
        responses = {
            21: b"220 ProFTPD 1.3.5 Server (Debian) [::ffff:192.168.1.1]\r\n",
            22: b"SSH-2.0-OpenSSH_7.4\r\n",
            23: b"Ubuntu 18.04.3 LTS\nlogin: ",
            25: b"220 smtp.example.com ESMTP Postfix\r\n",
            80: b"HTTP/1.1 200 OK\r\nServer: Apache/2.4.41 (Ubuntu)\r\n\r\n",
            110: b"+OK POP3 server ready\r\n",
            143: b"* OK [CAPABILITY IMAP4rev1] IMAP4 Server\r\n",
            443: b"HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n\r\n",
            3306: b"\x4a\x00\x00\x00\x0a5.7.31-0ubuntu0.18.04.1\x00",
            3389: b"\x03\x00\x00\x13\x0e\xd0\x00\x00\x124\x00",
            5432: b"PostgreSQL 12.4 on x86_64-pc-linux-gnu",
            8080: b"HTTP/1.1 200 OK\r\nServer: Tomcat/9.0.37\r\n\r\n"
        }
        return responses.get(port, b"")
    
    def handle_connection(self, conn, addr, port, protocol):
        """Handle incoming connection"""
        try:
            conn.settimeout(5)
            data = conn.recv(4096)
            
            if data:
                attack_type, severity = self.analyze_attack(data, port)
                
                attack_data = {
                    'ip': addr[0],
                    'port': port,
                    'protocol': protocol,
                    'data': data.hex(),
                    'attack_type': attack_type,
                    'severity': severity
                }
                
                self.log_attack(attack_data)
                
                # Send fake response
                response = self.create_response(port, protocol)
                if response:
                    conn.send(response)
                    time.sleep(0.5)
                    
                    # Try to receive more data
                    try:
                        more_data = conn.recv(4096)
                        if more_data:
                            attack_data['data'] += '\n' + more_data.hex()
                    except:
                        pass
        
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Error handling connection on port {port}: {e}")
        finally:
            conn.close()
    
    def start_listener(self, port, protocol='TCP'):
        """Start listener on specific port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('0.0.0.0', port))
            sock.listen(5)
            sock.settimeout(1)
            
            print(f"✓ Honeypot listening on port {port} ({protocol})")
            
            while self.running:
                try:
                    conn, addr = sock.accept()
                    thread = threading.Thread(
                        target=self.handle_connection,
                        args=(conn, addr, port, protocol)
                    )
                    thread.daemon = True
                    thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Error on port {port}: {e}")
                    break
        
        except Exception as e:
            print(f"✗ Could not start listener on port {port}: {e}")
        finally:
            sock.close()
    
    def start_all_listeners(self):
        """Start listeners on all ports"""
        print("\n" + "="*60)
        print("🔒 ADVANCED HONEYPOT SYSTEM - REAL-TIME NETWORK MONITORING")
        print("="*60)
        
        for port in self.ports:
            thread = threading.Thread(target=self.start_listener, args=(port,))
            thread.daemon = True
            thread.start()
            time.sleep(0.1)
        
        print(f"\n📝 Logging to: {self.log_file}")
        print(f"🌐 Web Dashboard: http://localhost:5000")
        print("\n⚠️  LOCALHOST FILTERING: Enabled")
        print("    Only 127.0.0.1 traffic will be filtered")
        print("    ALL other IPs (LAN, WAN, Internet) will be logged!")
        print("="*60 + "\n")
        print("🎯 Monitoring all network connections...")
        print("    Try connecting from another device on your network!\n")

# Global honeypot instance
honeypot = HoneypotSystem()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """Return current statistics"""
    return jsonify({
        'total_attempts': honeypot.stats['total_attempts'],
        'unique_ips': len(honeypot.stats['unique_ips']),
        'top_ports': dict(sorted(
            honeypot.stats['ports_scanned'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]),
        'protocols': dict(honeypot.stats['protocols']),
        'recent_attacks': honeypot.attacks[:20]
    })

@app.route('/api/attacks')
def get_attacks():
    """Return recent attacks"""
    return jsonify(honeypot.attacks[:50])

@app.route('/api/live')
def get_live():
    """Return live data for real-time updates"""
    return jsonify({
        'latest_attack': honeypot.attacks[0] if honeypot.attacks else None,
        'total_attempts': honeypot.stats['total_attempts'],
        'active_monitoring': len(honeypot.ports)
    })

def run_flask():
    """Run Flask web server"""
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Start honeypot listeners
    honeypot.start_all_listeners()
    
    # Start web server in separate thread
    web_thread = threading.Thread(target=run_flask)
    web_thread.daemon = True
    web_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down honeypot...")
        honeypot.running = False
        print(f"✓ Total attacks logged: {honeypot.stats['total_attempts']}")
        print(f"✓ Logs saved to: {honeypot.log_file}")