#!/usr/bin/env python3
"""
Simple Frontend Server
Serves the frontend files for the integration checker
"""

import http.server
import socketserver
import os
from pathlib import Path

# Set the directory to serve
frontend_dir = Path(__file__).parent / "zero-cost-ai-marketplace" / "frontend"
os.chdir(frontend_dir)

PORT = 8080

# Check if port is already in use and use alternative
import socket
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if is_port_in_use(8080):
    PORT = 3000  # Use alternative port
    print(f"⚠️  Port 8080 is busy, using port {PORT} instead")

Handler = http.server.SimpleHTTPRequestHandler

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🌐 Frontend Server Starting...")
        print(f"📡 Serving at: http://localhost:{PORT}")
        print(f"📁 Directory: {frontend_dir}")
        print("=" * 50)
        httpd.serve_forever()
except Exception as e:
    print(f"❌ Error starting frontend server: {e}")
