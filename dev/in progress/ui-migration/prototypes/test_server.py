#!/usr/bin/env python3
"""
Simple HTTP Server for Testing UI
Serves the minimal.html file locally for testing and evaluation.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

class UITestServer:
    def __init__(self, port=8080):
        self.port = port
        self.directory = Path(__file__).parent
        
    def start(self):
        """Start the test server."""
        # Change to the UI directory
        os.chdir(self.directory)
        
        # Create a simple handler that serves files
        handler = http.server.SimpleHTTPRequestHandler
        
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                print(f"🚀 UI Test Server Starting...")
                print(f"📂 Serving from: {self.directory}")
                print(f"🌐 Local URL: http://localhost:{self.port}/minimal.html")
                print(f"🔗 Network URL: http://{self.get_local_ip()}:{self.port}/minimal.html")
                print(f"⏹️  Press Ctrl+C to stop the server")
                print(f"────────────────────────────────────────")
                
                # Try to open browser automatically
                try:
                    webbrowser.open(f"http://localhost:{self.port}/minimal.html")
                    print("✅ Browser should open automatically")
                except:
                    print("⚠️  Could not open browser automatically")
                
                print(f"────────────────────────────────────────")
                
                # Start serving
                httpd.serve_forever()
                
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"❌ Port {self.port} is already in use")
                print(f"💡 Try a different port: python test_server.py --port 8081")
            else:
                print(f"❌ Server error: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            print(f"\n🛑 Server stopped by user")
            sys.exit(0)
    
    def get_local_ip(self):
        """Get local IP address for network access."""
        import socket
        try:
            # Connect to a remote address to determine local IP
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "localhost"

def main():
    """Main entry point."""
    port = 8080
    
    # Simple argument parsing
    if len(sys.argv) > 1:
        for i, arg in enumerate(sys.argv):
            if arg == "--port" and i + 1 < len(sys.argv):
                try:
                    port = int(sys.argv[i + 1])
                except ValueError:
                    print("❌ Invalid port number")
                    sys.exit(1)
            elif arg == "--help" or arg == "-h":
                print("UI Test Server")
                print("Usage: python test_server.py [--port PORT]")
                print("Default port: 8080")
                sys.exit(0)
    
    server = UITestServer(port)
    server.start()

if __name__ == "__main__":
    main()
