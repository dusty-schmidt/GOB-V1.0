#!/usr/bin/env python3
"""
GOB Network Monitor Startup Script
Starts the monitoring dashboard as a standalone service
"""

import sys
import os
import time
import signal
import threading
from pathlib import Path

# Add GOB directory to Python path
sys.path.insert(0, '/home/ds/GOB')

# Global instances
monitor_app = None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"Received signal {signum}, shutting down...")
    print("GOB Network Monitor stopped")
    sys.exit(0)

def main():
    """Main entry point"""
    print("Starting GOB Network Monitor...")
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Change to monitor directory
        os.chdir('/home/ds/GOB/monitor')
        
        # Import and start the Dash app
        from app import app
        print("Network Monitor started successfully")
        print("Dashboard available at http://localhost:8050")
        
        # Start the app
        app.run(host='0.0.0.0', port=8050, debug=False)
        
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
    except Exception as e:
        print(f"Error in GOB Network Monitor: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
