#!/usr/bin/env python3
"""
GOB Core State Manager Startup Script
Starts the state manager as a standalone service with health endpoint
"""

import sys
import os
import time
import signal
import threading
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Add GOB directory to Python path
sys.path.insert(0, '/home/ds/GOB')

from core.state_manager import get_state_manager

# Global instances
state_manager = None
health_server = None


class HealthHandler(BaseHTTPRequestHandler):
    """HTTP handler for health checks and core state"""

    def do_GET(self):
        global state_manager

        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = b'{"status": "healthy", "service": "gob-core"}'
            self.wfile.write(response)

        elif self.path == '/state':
            # Return core state information
            try:
                if state_manager:
                    core_state = state_manager.get_core_state()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps(core_state, indent=2).encode('utf-8')
                    self.wfile.write(response)
                else:
                    self.send_response(503)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = b'{"error": "State manager not available"}'
                    self.wfile.write(response)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({"error": str(e)}).encode('utf-8')
                self.wfile.write(response)

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress HTTP access logs"""
        pass


def start_health_server():
    """Start the health check HTTP server"""
    global health_server
    try:
        health_server = HTTPServer(('localhost', 8051), HealthHandler)
        print("Health endpoint started on http://localhost:8051/health")
        print("Core state endpoint available at http://localhost:8051/state")
        health_server.serve_forever()
    except Exception as e:
        print(f"Failed to start health server: {e}")


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global state_manager, health_server
    
    print(f"Received signal {signum}, shutting down...")
    
    # Stop health server
    if health_server:
        print("Stopping health server...")
        health_server.shutdown()
    
    # Stop state manager
    if state_manager:
        print("Stopping state manager...")
        state_manager.stop_monitoring()
    
    print("GOB Core State Manager stopped")
    sys.exit(0)


def main():
    """Main entry point"""
    global state_manager
    
    print("Starting GOB Core State Manager...")
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Start health server in background thread
        health_thread = threading.Thread(target=start_health_server, daemon=True)
        health_thread.start()
        
        # Start state manager
        state_manager = get_state_manager()
        state_manager.start_monitoring()
        print("State manager started successfully")
        
        # Keep the service running
        print("GOB Core State Manager is running...")
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"Error in GOB Core State Manager: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
