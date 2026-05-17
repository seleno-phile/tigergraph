#!/usr/bin/env python3
"""
Simple HTTP Server for Supply Chain Intelligence Dashboard
Serve the dashboard locally on port 8000
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class DashboardHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Add headers to prevent caching during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()
    
    def log_message(self, format, *args):
        # Custom logging format
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(port=PORT):
    """Start the development server"""
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", port), DashboardHTTPHandler) as httpd:
        print(f"=" * 60)
        print(f"Supply Chain Intelligence Dashboard")
        print(f"=" * 60)
        print(f"\n[OK] Server running at: http://localhost:{port}")
        print(f"[OK] Serving files from: {DIRECTORY}")
        print(f"\nPress Ctrl+C to stop the server\n")
        print(f"=" * 60)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(f"\n\n[OK] Server stopped gracefully")
            sys.exit(0)

if __name__ == "__main__":
    # Check if custom port provided
    if len(sys.argv) > 1:
        try:
            PORT = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(PORT)
