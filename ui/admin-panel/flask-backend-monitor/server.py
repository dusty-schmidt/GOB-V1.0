"""
GOB Monitoring Server - Independent monitoring and control system
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add GOB root directory to Python path for imports
gob_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(gob_root))

from core.state_manager import get_state_manager, shutdown_monitoring, EventType
from core.process_manager import ProcessManager, ProcessState

# Web server imports
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import threading
import time


class MonitoringServer:
    """
    Independent monitoring server that controls and observes the GOB system.
    Provides web API, process management, and real-time dashboard.
    """
    
    def __init__(self, port: int = 8053, gob_directory: str = "/home/ds/GOB", auto_open: bool = True):
        self.port = port
        self.gob_directory = Path(gob_directory)
        self.auto_open = auto_open

        # Core components - connect to existing state manager
        self.state_manager = get_state_manager()
        self.process_manager = ProcessManager(str(self.gob_directory))
        
        # Web application
        self.app = Flask(__name__)
        CORS(self.app)  # Enable CORS for dashboard
        
        # Runtime state
        self.running = False
        self.start_time = datetime.now()
        
        # Setup routes and callbacks
        self._setup_routes()
        self._setup_callbacks()
    
    def _setup_routes(self):
        """Setup Flask routes for the monitoring API"""
        
        @self.app.route('/')
        def dashboard():
            """Serve the main monitoring dashboard"""
            return render_template_string(DASHBOARD_HTML)
        
        @self.app.route('/api/status')
        def get_status():
            """Get comprehensive system status"""
            return jsonify({
                "monitoring": self.state_manager.get_system_status(),
                "process": self.process_manager.get_process_info(),
                "uptime": (datetime.now() - self.start_time).total_seconds()
            })
        
        @self.app.route('/api/agents')
        def get_agents():
            """Get agent summary and hierarchy"""
            return jsonify(self.state_manager.get_agent_summary())
        
        @self.app.route('/api/metrics')
        def get_metrics():
            """Get current system metrics"""
            import psutil
            import socket

            # Get system metrics
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                hostname = socket.gethostname()

                # Try to get local IP
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))
                    local_ip = s.getsockname()[0]
                    s.close()
                except:
                    local_ip = "127.0.0.1"

                # Combine with state manager metrics
                state_metrics = self.state_manager.current_metrics.__dict__

                return jsonify({
                    **state_metrics,
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'hostname': hostname,
                    'local_ip': local_ip
                })
            except Exception as e:
                # Fallback to just state manager metrics
                return jsonify(self.state_manager.current_metrics.__dict__)
        
        @self.app.route('/api/metrics/history')
        def get_metrics_history():
            """Get metrics history"""
            limit = request.args.get('limit', type=int)
            return jsonify(self.state_manager.get_metrics_history(limit))
        
        @self.app.route('/api/events')
        def get_events():
            """Get recent events"""
            limit = request.args.get('limit', 100, type=int)
            event_types = request.args.getlist('types')
            
            # Convert string event types to enum
            if event_types:
                try:
                    event_types = [EventType(t) for t in event_types]
                except ValueError:
                    event_types = None
            else:
                event_types = None
            
            return jsonify(self.state_manager.get_recent_events(limit, event_types))
        
        @self.app.route('/api/process/start', methods=['POST'])
        async def start_process():
            """Start the GOB process"""
            data = request.get_json() or {}
            python_file = data.get('python_file', 'run_ui.py')
            args = data.get('args', [])
            
            success = await self.process_manager.start_process(python_file, args)
            return jsonify({"success": success})
        
        @self.app.route('/api/process/stop', methods=['POST'])
        async def stop_process():
            """Stop the GOB process"""
            data = request.get_json() or {}
            force = data.get('force', False)
            
            success = await self.process_manager.stop_process(force)
            return jsonify({"success": success})
        
        @self.app.route('/api/process/restart', methods=['POST'])
        async def restart_process():
            """Restart the GOB process"""
            data = request.get_json() or {}
            python_file = data.get('python_file', 'run_ui.py')
            args = data.get('args', [])
            
            success = await self.process_manager.restart_process(python_file, args)
            return jsonify({"success": success})
        
        @self.app.route('/api/process/output')
        def get_process_output():
            """Get recent process output"""
            lines = request.args.get('lines', 50, type=int)
            source = request.args.get('source', 'both')
            
            return jsonify(self.process_manager.get_recent_output(lines, source))
        
        @self.app.route('/api/process/clear_output', methods=['POST'])
        def clear_output():
            """Clear process output buffers"""
            self.process_manager.clear_output_buffers()
            return jsonify({"success": True})
    
    def _setup_callbacks(self):
        """Setup callbacks for real-time monitoring"""
        
        def on_process_state_change(old_state: ProcessState, new_state: ProcessState):
            """Handle process state changes"""
            print(f"Process state changed: {old_state.value} -> {new_state.value}")
        
        def on_process_output(line: str, source: str):
            """Handle process output"""
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {source.upper()}: {line}")
        
        self.process_manager.add_state_change_callback(on_process_state_change)
        self.process_manager.add_output_callback(on_process_output)
    
    def _open_browser(self):
        """Open the dashboard in the default browser"""
        if not self.auto_open:
            return
            
        import subprocess
        import webbrowser
        import time
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        url = f"http://localhost:{self.port}"
        
        try:
            # Try to open browser
            webbrowser.open(url)
            print(f"🌐 Dashboard opened in browser: {url}")
        except Exception as e:
            print(f"⚠️  Could not auto-open browser: {e}")
            print(f"🌐 Please manually visit: {url}")
    
    def run(self):
        """Run the monitoring server"""
        print(f"🚀 Starting GOB Monitoring Server on port {self.port}")
        print(f"📁 GOB Directory: {self.gob_directory}")
        print(f"🌐 Dashboard: http://localhost:{self.port}")
        
        self.running = True
        
        # Open browser in background if requested
        if self.auto_open:
            threading.Thread(target=self._open_browser, daemon=True).start()
        
        try:
            # Run Flask app
            self.app.run(
                host='0.0.0.0',
                port=self.port,
                debug=False,
                threaded=True
            )
        except KeyboardInterrupt:
            print("\n🛑 Monitoring server stopped by user")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Shutdown the monitoring server"""
        print("🔄 Shutting down monitoring server...")
        
        self.running = False
        
        # Stop GOB process if running
        if self.process_manager.is_running():
            print("⏹️  Stopping GOB process...")
            asyncio.run(self.process_manager.stop_process())
        
        # Shutdown monitoring
        shutdown_monitoring()
        
        print("✅ Monitoring server shutdown complete")


# HTML Dashboard Template
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>GOB Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📊</text></svg>">
    <style>
        @import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&family=Rubik:ital,wght@0,300..900;1,300..900&display=swap");
        
        :root {
          /* Terminal Color Palette - matching GOB webui */
          --term-bg: #0a0a0a;
          --term-fg: #ffffff;
          --term-fg-secondary: #ddd;
          --term-fg-muted: #888;
          --term-fg-dim: #666;
          --term-fg-faint: #555;
          --term-fg-dimmer: #444;
          --term-border: #333;
          --term-border-subtle: #222;
          --term-accent-green: #00ff00;
          
          /* GOB Color Palette */
          --color-background-dark: #131313;
          --color-text-dark: #d4d4d4;
          --color-primary-dark: #737a81;
          --color-secondary-dark: #656565;
          --color-accent-dark: #cf6679;
          --color-message-bg-dark: #2d2d2d;
          --color-panel-dark: #1a1a1a;
          --color-border-dark: #444444a8;
          --color-input-dark: #131313;
          
          /* Typography */
          --term-font: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
          --term-font-size: 13px;
          --term-line-height: 1.4;
          --font-family-main: "Rubik", Arial, Helvetica, sans-serif;
          --font-family-code: "Roboto Mono", monospace;
        }
        
        *, *::before, *::after {
          box-sizing: border-box;
        }
        
        /* Global Resets matching GOB */
        body, html {
          font-family: var(--term-font);
          font-size: var(--term-font-size);
          line-height: var(--term-line-height);
          background: var(--term-bg);
          color: var(--term-fg);
          margin: 0;
          padding: 0;
          height: 100%;
          min-height: 100vh;
          overflow-x: hidden;
          -webkit-font-smoothing: none;
          -moz-osx-font-smoothing: auto;
        }
        
        /* Scrollbar matching GOB */
        ::-webkit-scrollbar {
          width: 4px;
        }
        ::-webkit-scrollbar-track {
          background: var(--term-bg);
        }
        ::-webkit-scrollbar-thumb {
          background: var(--term-border);
        }
        
        /* Title bar matching GOB exactly */
        .terminal-title-bar {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          height: 24px;
          background: transparent;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 4px 16px;
          z-index: 2000;
          font-family: var(--term-font);
          font-size: var(--term-font-size);
        }
        
        .title-bar-left {
          display: flex;
          align-items: center;
          flex: 0 0 auto;
        }
        
        .title-bar-right {
          display: flex;
          align-items: center;
          gap: 16px;
          flex: 0 0 auto;
          margin-left: auto;
          position: relative;
        }
        
        .title-main {
          color: var(--term-fg-dim);
          font-size: var(--term-font-size);
          transition: all 0.3s ease;
        }
        
        .title-datetime {
          color: var(--term-fg-dim);
          font-size: var(--term-font-size);
        }
        
        /* System tray matching GOB */
        .title-system-tray {
          position: relative;
          cursor: pointer;
          color: var(--term-fg-faint);
        }
        
        .system-tray-icon {
          font-size: 14px;
          color: var(--term-fg-dim);
          transition: color 0.2s;
        }
        
        .system-tray-icon:hover {
          color: var(--term-fg-secondary);
        }
        
        .system-tray-dropdown {
          position: absolute;
          top: 100%;
          right: 0;
          background: var(--color-panel-dark);
          border: 1px solid var(--term-border);
          min-width: 180px;
          margin-top: 4px;
          z-index: 3000;
        }
        
        .system-tray-item {
          display: block;
          width: 100%;
          padding: 8px 12px;
          background: none;
          border: none;
          color: var(--term-fg-secondary);
          font-family: var(--term-font);
          font-size: var(--term-font-size);
          text-align: left;
          cursor: pointer;
          transition: all 0.2s;
        }
        
        .system-tray-item:hover {
          background: var(--term-border);
          color: var(--term-fg);
        }
        
        /* Main container - ensure content never goes under header */
        .container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 100px 20px 20px;
          min-height: calc(100vh - 100px);
        }

        /* GOB Header with cyberpunk/retro terminal aesthetic */
        .gob-header {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          width: 100%;
          height: 80px;
          background: linear-gradient(180deg,
            rgba(0, 0, 0, 0.95) 0%,
            rgba(0, 0, 0, 0.9) 70%,
            rgba(0, 0, 0, 0.7) 85%,
            rgba(0, 0, 0, 0.4) 95%,
            rgba(0, 0, 0, 0.1) 100%);
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 40px;
          z-index: 1000;
          border-bottom: 1px solid rgba(0, 255, 0, 0.2);
          box-shadow: 0 2px 10px rgba(0, 255, 0, 0.1);
        }

        .gob-left-section {
          display: flex;
          align-items: center;
          flex: 0 0 auto;
        }

        .gob-right-section {
          display: flex;
          align-items: center;
          gap: 16px;
          flex: 0 0 auto;
        }

        .status-light-corner {
          display: flex;
          align-items: center;
        }

        .status-light {
          width: 14px;
          height: 14px;
          border-radius: 50%;
          animation: pulse 2s infinite;
          box-shadow: 0 0 8px currentColor;
        }

        .status-online {
          background: var(--term-accent-green);
          color: var(--term-accent-green);
        }
        .status-offline {
          background: var(--term-fg-dim);
          color: var(--term-fg-dim);
        }
        .status-error {
          background: #ff4444;
          color: #ff4444;
        }

        .gob-title-center {
          flex: 1;
          text-align: center;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }

        .gob-title-main {
          color: var(--term-accent-green);
          font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
          font-size: 18px;
          font-weight: 700;
          letter-spacing: 1px;
          margin-bottom: 2px;
          text-shadow: 0 0 8px rgba(0, 255, 0, 0.5);
          text-transform: uppercase;
        }

        .gob-title-sub {
          color: var(--term-fg-dimmer);
          font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
          font-size: 11px;
          letter-spacing: 1px;
          opacity: 0.7;
          font-weight: 400;
        }

        .gob-clock {
          text-align: right;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
        }

        .gob-time {
          color: var(--term-accent-green);
          font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
          font-size: 14px;
          font-weight: 700;
          margin-bottom: 1px;
          text-shadow: 0 0 4px rgba(0, 255, 0, 0.3);
        }

        .gob-date {
          color: var(--term-fg-dimmer);
          font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
          font-size: 10px;
          font-weight: 400;
          opacity: 0.6;
        }
        
        /* Terminal sections layout */
        .terminal-sections {
          display: flex;
          flex-direction: column;
          gap: 32px;
          margin-top: 32px;
        }

        .terminal-section {
          background: transparent;
          padding: 0;
        }

        .section-title {
          color: var(--term-fg-dimmer);
          font-family: var(--term-font);
          font-size: 10px;
          text-transform: uppercase;
          margin-bottom: 16px;
          letter-spacing: 1px;
        }

        /* Terminal-style status cards */
        .status-cards {
          display: flex;
          gap: 32px;
          margin-bottom: 16px;
          flex-wrap: wrap;
        }

        .status-card {
          margin: 16px;
          display: inline-block;
          text-align: left;
        }

        .status-card-title {
          color: var(--term-fg-dimmer);
          font-family: var(--term-font);
          font-size: 10px;
          margin-bottom: 3px;
          text-transform: uppercase;
        }

        .status-card-value {
          color: var(--term-fg-secondary);
          font-family: var(--term-font);
          font-size: 16px;
          line-height: 1.4;
        }

        /* Terminal progress bars */
        .progress-bar {
          margin-bottom: 16px;
        }

        .progress-label {
          color: var(--term-fg-muted);
          font-family: var(--term-font);
          font-size: 13px;
          margin-bottom: 4px;
        }

        .progress-visual {
          font-family: var(--term-font);
          font-size: 13px;
          color: var(--term-fg-secondary);
        }

        .progress-bar-fill {
          color: var(--term-fg-secondary);
        }

        .progress-bar-empty {
          color: var(--term-fg-dimmer);
        }

        .progress-percentage {
          color: var(--term-fg-secondary);
          margin-left: 8px;
        }
        
        /* Process controls */
        .process-controls {
          display: flex;
          gap: 8px;
          margin: 12px 0;
        }
        
        .btn {
          padding: 6px 12px;
          border: 1px solid var(--term-border);
          background: var(--color-panel-dark);
          color: var(--term-fg-secondary);
          cursor: pointer;
          font-family: var(--term-font);
          font-size: 11px;
          transition: all 0.2s;
        }
        
        .btn:hover {
          background: var(--term-border);
          color: var(--term-fg);
        }
        
        .btn:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        .btn-success {
          border-color: var(--term-accent-green);
          color: var(--term-accent-green);
        }
        
        .btn-success:hover {
          background: var(--term-accent-green);
          color: var(--term-bg);
        }
        
        .btn-danger {
          border-color: #ff4444;
          color: #ff4444;
        }
        
        .btn-danger:hover {
          background: #ff4444;
          color: var(--term-bg);
        }
        
        .btn-warning {
          border-color: #ffaa00;
          color: #ffaa00;
        }
        
        .btn-warning:hover {
          background: #ffaa00;
          color: var(--term-bg);
        }
        
        /* Status indicators */
        .status-indicator {
          display: inline-block;
          width: 8px;
          height: 8px;
          margin-right: 8px;
          position: relative;
        }
        
        .status-running { background: var(--term-accent-green); }
        .status-stopped { background: var(--term-fg-dim); }
        .status-error { background: #ff4444; }
        .status-starting { 
          background: #ffaa00;
          animation: pulse 2s infinite;
        }
        
        /* Metrics grid */
        .metrics {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
          gap: 8px;
        }
        
        .metric {
          text-align: center;
          padding: 8px;
          background: var(--term-bg);
          border: 1px solid var(--term-border-subtle);
        }
        
        .metric-value {
          font-size: 16px;
          font-weight: bold;
          color: var(--term-fg);
          font-family: var(--term-font);
        }
        
        .metric-label {
          font-size: 10px;
          color: var(--term-fg-muted);
          margin-top: 2px;
        }
        
        /* Log container */
        .log-container {
          background: var(--term-bg);
          border: 1px solid var(--term-border-subtle);
          padding: 12px;
          max-height: 300px;
          overflow-y: auto;
          font-family: var(--term-font);
          font-size: 11px;
          line-height: 1.3;
        }
        
        .log-line {
          margin-bottom: 2px;
          color: var(--term-fg-secondary);
        }
        
        /* Events list */
        .events-list {
          max-height: 300px;
          overflow-y: auto;
        }
        
        .event {
          background: var(--term-bg);
          border: 1px solid var(--term-border-subtle);
          padding: 8px;
          margin-bottom: 4px;
          font-size: 11px;
        }
        
        .event-type {
          font-weight: bold;
          color: var(--term-accent-green);
          font-family: var(--term-font);
        }
        
        .event-time {
          color: var(--term-fg-faint);
          font-size: 10px;
        }
        
        /* Animations */
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.5; }
        }
        
        .pulsing {
          animation: pulse 2s infinite;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
          .gob-header {
            height: 90px;
            padding: 0 20px;
          }

          .gob-title-main {
            font-size: 16px;
            letter-spacing: 2px;
          }

          .gob-title-sub {
            font-size: 11px;
          }

          .gob-time {
            font-size: 13px;
          }

          .container {
            padding: 110px 10px 10px;
            min-height: calc(100vh - 110px);
          }

          .cards {
            grid-template-columns: 1fr;
            gap: 12px;
          }

          .card {
            padding: 12px;
          }

          .metrics {
            grid-template-columns: repeat(2, 1fr);
          }
        }

        /* Extra small screens / portrait phones */
        @media (max-width: 480px) {
          .gob-header {
            height: 100px;
            padding: 0 15px;
          }

          .gob-right-section {
            gap: 12px;
          }

          .container {
            padding: 120px 10px 10px;
            min-height: calc(100vh - 120px);
          }
        }
    </style>
</head>
<body class="dark-mode device-pointer">

    
    <div class="container">
        <!-- GOB Header with cyberpunk/retro terminal aesthetic -->
        <div class="gob-header">
            <!-- Status light in top left -->
            <div class="gob-left-section">
                <div class="status-light-corner" id="status-light-corner">
                    <div class="status-light status-offline"></div>
                </div>
            </div>

            <!-- Centered title with cyberpunk styling -->
            <div class="gob-title-center">
                <div class="gob-title-main">GENERAL_OPERATIONS_BRIDGE</div>
                <div class="gob-title-sub">[ GOB ] v1.0</div>
            </div>

            <!-- Terminal-style clock in top right -->
            <div class="gob-right-section">
                <div class="gob-clock">
                    <div class="gob-time" id="current-time">--:--:--</div>
                    <div class="gob-date" id="current-date">----/--/--</div>
                </div>
            </div>
        </div>
        
        <!-- Core Status Section -->
        <div class="terminal-section" id="core-status-section">
            <div class="section-title">CORE STATUS</div>
            <div class="status-cards">
                <div class="status-card">
                    <div class="status-card-title">SERVICE</div>
                    <div class="status-card-value" id="service-name">Loading...</div>
                </div>
                <div class="status-card">
                    <div class="status-card-title">VERSION</div>
                    <div class="status-card-value" id="service-version">--</div>
                </div>
                <div class="status-card">
                    <div class="status-card-title">UPTIME</div>
                    <div class="status-card-value" id="service-uptime">--</div>
                </div>
                <div class="status-card">
                    <div class="status-card-title">RESTARTS</div>
                    <div class="status-card-value" id="service-restarts">--</div>
                </div>
            </div>
            <div class="process-controls">
                <button class="btn btn-success" onclick="startProcess()">▶️ Start</button>
                <button class="btn btn-danger" onclick="stopProcess()">⏹️ Stop</button>
                <button class="btn btn-warning" onclick="restartProcess()">🔄 Restart</button>
            </div>
        </div>

        <!-- System Metrics Section -->
        <div class="terminal-section" id="system-metrics-section">
            <div class="section-title">SYSTEM METRICS</div>
            <div class="progress-bar">
                <div class="progress-label">CPU: <span class="progress-visual" id="cpu-bar">[░░░░░░░░░░░░░░░░░░░░] 0.0%</span></div>
            </div>
            <div class="progress-bar">
                <div class="progress-label">MEMORY: <span class="progress-visual" id="memory-bar">[░░░░░░░░░░░░░░░░░░░░] 0.0%</span></div>
            </div>
            <div class="progress-bar">
                <div class="progress-label">DISK: <span class="progress-visual" id="disk-bar">[░░░░░░░░░░░░░░░░░░░░] 0.0%</span></div>
            </div>

            <div class="section-title" style="margin-top: 24px;">NETWORK</div>
            <div style="margin: 4px 0;">
                <span style="color: var(--term-fg-muted); font-family: var(--term-font); font-size: 13px;">hostname: </span>
                <span style="color: var(--term-fg-secondary); font-family: var(--term-font); font-size: 13px;" id="hostname">--</span>
            </div>
            <div style="margin: 4px 0;">
                <span style="color: var(--term-fg-muted); font-family: var(--term-font); font-size: 13px;">local_ip: </span>
                <span style="color: var(--term-fg-secondary); font-family: var(--term-font); font-size: 13px;" id="local-ip">--</span>
            </div>
        </div>

        <!-- Events Section -->
        <div class="terminal-section">
            <div class="section-title">RECENT EVENTS</div>
            <div class="events-list" id="events-list">
                <div>Loading events...</div>
            </div>
        </div>
        
        <!-- Process Logs Section -->
        <div class="terminal-section">
            <div class="section-title">PROCESS OUTPUT</div>
            <div class="log-container" id="process-logs">
                <div>No output yet...</div>
            </div>
            <button class="btn btn-warning" onclick="clearLogs()" style="margin-top: 10px;">🗑️ Clear Logs</button>
        </div>
    </div>

    <script>
        // Global state
        let updateInterval;
        
        // Start auto-refresh and initialize
        window.onload = function() {
            updateDateTime();
            updateDashboard();
            updateInterval = setInterval(updateDashboard, 2000);
            setInterval(updateDateTime, 1000); // Update time every second
        };
        
        // Update datetime display for GOB header with retro terminal formatting
        function updateDateTime() {
            const now = new Date();

            // Terminal-style time format: HH:MM:SS
            const timeStr = String(now.getHours()).padStart(2, '0') + ':' +
                           String(now.getMinutes()).padStart(2, '0') + ':' +
                           String(now.getSeconds()).padStart(2, '0');

            // Retro date format: YYYY.MM.DD
            const dateStr = now.getFullYear() + '.' +
                           String(now.getMonth() + 1).padStart(2, '0') + '.' +
                           String(now.getDate()).padStart(2, '0');

            // Update GOB header time/date
            const timeElement = document.getElementById('current-time');
            const dateElement = document.getElementById('current-date');

            if (timeElement && timeElement.textContent !== timeStr) {
                timeElement.textContent = timeStr;
            }
            if (dateElement && dateElement.textContent !== dateStr) {
                dateElement.textContent = dateStr;
            }
        }

        // Create terminal-style progress bar
        function createProgressBar(label, value, maxValue, unit = '') {
            const percentage = maxValue > 0 ? (value / maxValue) * 100 : 0;
            const barLength = 20;
            const filled = Math.round((percentage / 100) * barLength);
            const bar = '█'.repeat(filled) + '░'.repeat(barLength - filled);

            let color = 'var(--term-fg-secondary)';
            if (percentage > 80) color = '#ff0000';
            else if (percentage > 60) color = '#ffaa00';

            return `<span style="color: ${color}">[${bar}]</span> ${percentage.toFixed(1)}% (${value.toFixed(1)}${unit})`;
        }
        
        // System tray functionality
        function toggleSystemTray() {
            const dropdown = document.getElementById('systemTrayDropdown');
            dropdown.style.display = dropdown.style.display === 'none' ? 'block' : 'none';
        }
        
        function openMainGOB() {
            window.open('http://localhost:50080', '_blank');
            document.getElementById('systemTrayDropdown').style.display = 'none';
        }
        
        // Click outside to close dropdown
        document.addEventListener('click', function(event) {
            const tray = document.querySelector('.title-system-tray');
            const dropdown = document.getElementById('systemTrayDropdown');
            if (!tray.contains(event.target)) {
                dropdown.style.display = 'none';
            }
        });
        
        // Update dashboard data
        async function updateDashboard() {
            try {
                await Promise.all([
                    updateStatus(),
                    updateMetrics(),
                    updateEvents(),
                    updateLogs()
                ]);
            } catch (error) {
                console.error('Dashboard update error:', error);
            }
        }
        
        // Update status light and core status
        async function updateStatus() {
            const response = await fetch('/api/status');
            const data = await response.json();

            const processInfo = data.process;
            const monitoring = data.monitoring;

            // Update status light - show online if monitoring system is running
            const statusLight = document.getElementById('status-light-corner').querySelector('.status-light');
            let statusClass = 'status-offline';

            // If monitoring system is running, show online even if no process is monitored
            if (data.monitoring && data.monitoring.monitoring_status === 'running') {
                statusClass = 'status-online';

                // Override with process status if there are issues
                if (processInfo.state === 'error' || processInfo.state === 'crashed') {
                    statusClass = 'status-error';
                }
            } else {
                statusClass = 'status-offline';
            }

            // Only update status light if changed
            if (!statusLight.classList.contains(statusClass)) {
                statusLight.className = `status-light ${statusClass}`;
            }

            // Update core status cards
            const serviceNameEl = document.getElementById('service-name');
            const serviceVersionEl = document.getElementById('service-version');
            const serviceUptimeEl = document.getElementById('service-uptime');
            const serviceRestartsEl = document.getElementById('service-restarts');

            // Show monitoring system status
            const serviceName = data.monitoring && data.monitoring.monitoring_status === 'running' ? 'GOB Monitor' : 'Offline';
            const serviceVersion = '1.0.0';
            const serviceUptime = data.monitoring && data.monitoring.uptime_seconds ? `${Math.round(data.monitoring.uptime_seconds)}s` : '0s';
            const serviceRestarts = '0';

            // Only update if content changed
            if (serviceNameEl.textContent !== serviceName) serviceNameEl.textContent = serviceName;
            if (serviceVersionEl.textContent !== serviceVersion) serviceVersionEl.textContent = serviceVersion;
            if (serviceUptimeEl.textContent !== serviceUptime) serviceUptimeEl.textContent = serviceUptime;
            if (serviceRestartsEl.textContent !== serviceRestarts) serviceRestartsEl.textContent = serviceRestarts;
        }
        
        // Update system metrics with terminal-style progress bars
        async function updateMetrics() {
            const response = await fetch('/api/metrics');
            const metrics = await response.json();

            // Update progress bars
            const cpuBar = document.getElementById('cpu-bar');
            const memoryBar = document.getElementById('memory-bar');
            const diskBar = document.getElementById('disk-bar');
            const hostnameEl = document.getElementById('hostname');
            const localIpEl = document.getElementById('local-ip');

            const cpuPercent = metrics.cpu_percent || 0;
            const memoryPercent = metrics.memory_percent || 0;
            const diskPercent = metrics.disk_percent || 0;

            // Create terminal progress bars
            const newCpuContent = createProgressBar('', cpuPercent, 100, '%');
            const newMemoryContent = createProgressBar('', memoryPercent, 100, '%');
            const newDiskContent = createProgressBar('', diskPercent, 100, '%');

            // Only update if content changed
            if (cpuBar && cpuBar.innerHTML !== newCpuContent) {
                cpuBar.innerHTML = newCpuContent;
            }
            if (memoryBar && memoryBar.innerHTML !== newMemoryContent) {
                memoryBar.innerHTML = newMemoryContent;
            }
            if (diskBar && diskBar.innerHTML !== newDiskContent) {
                diskBar.innerHTML = newDiskContent;
            }

            // Update network info
            const hostname = metrics.hostname || 'unknown';
            const localIp = metrics.local_ip || 'N/A';

            if (hostnameEl && hostnameEl.textContent !== hostname) {
                hostnameEl.textContent = hostname;
            }
            if (localIpEl && localIpEl.textContent !== localIp) {
                localIpEl.textContent = localIp;
            }
        }
        
        // Update recent events
        async function updateEvents() {
            const response = await fetch('/api/events?limit=10');
            const events = await response.json();

            const eventsEl = document.getElementById('events-list');

            let newEventsContent;
            if (events.length === 0) {
                newEventsContent = '<div>No events yet...</div>';
            } else {
                newEventsContent = events.map(event => `
                    <div class="event">
                        <div class="event-type">${event.event_type}</div>
                        <div>${event.source_type}: ${event.source_id}</div>
                        <div class="event-time">${new Date(event.timestamp).toLocaleTimeString()}</div>
                    </div>
                `).join('');
            }

            // Only update if content has changed to prevent flicker
            if (eventsEl.innerHTML !== newEventsContent) {
                eventsEl.innerHTML = newEventsContent;
            }
        }
        
        // Update process logs
        async function updateLogs() {
            const response = await fetch('/api/process/output?lines=20');
            const data = await response.json();

            const logsEl = document.getElementById('process-logs');
            const allLogs = [...(data.stdout || []), ...(data.stderr || [])];

            let newLogsContent;
            if (allLogs.length === 0) {
                newLogsContent = '<div>No output yet...</div>';
            } else {
                newLogsContent = allLogs.slice(-20).map(line =>
                    `<div class="log-line">${escapeHtml(line)}</div>`
                ).join('');
            }

            // Only update if content has changed to prevent flicker
            const currentScrollTop = logsEl.scrollTop;
            const currentScrollHeight = logsEl.scrollHeight;
            const wasAtBottom = currentScrollTop >= currentScrollHeight - logsEl.clientHeight - 5;

            if (logsEl.innerHTML !== newLogsContent) {
                logsEl.innerHTML = newLogsContent;

                // Auto-scroll to bottom only if user was already at bottom
                if (wasAtBottom) {
                    logsEl.scrollTop = logsEl.scrollHeight;
                }
            }
        }
        
        // Process control functions
        async function startProcess() {
            const btn = event.target;
            btn.disabled = true;
            btn.innerHTML = '⏳ Starting...';
            
            try {
                const response = await fetch('/api/process/start', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    showNotification('✅ Process started successfully', 'success');
                } else {
                    showNotification('❌ Failed to start process', 'error');
                }
            } catch (error) {
                showNotification('❌ Error starting process', 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '▶️ Start';
            }
        }
        
        async function stopProcess() {
            const btn = event.target;
            btn.disabled = true;
            btn.innerHTML = '⏳ Stopping...';
            
            try {
                const response = await fetch('/api/process/stop', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    showNotification('✅ Process stopped successfully', 'success');
                } else {
                    showNotification('❌ Failed to stop process', 'error');
                }
            } catch (error) {
                showNotification('❌ Error stopping process', 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '⏹️ Stop';
            }
        }
        
        async function restartProcess() {
            const btn = event.target;
            btn.disabled = true;
            btn.innerHTML = '⏳ Restarting...';
            
            try {
                const response = await fetch('/api/process/restart', { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    showNotification('✅ Process restarted successfully', 'success');
                } else {
                    showNotification('❌ Failed to restart process', 'error');
                }
            } catch (error) {
                showNotification('❌ Error restarting process', 'error');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '🔄 Restart';
            }
        }
        
        async function clearLogs() {
            try {
                await fetch('/api/process/clear_output', { method: 'POST' });
                document.getElementById('process-logs').innerHTML = '<div>Logs cleared</div>';
                showNotification('🗑️ Logs cleared', 'success');
            } catch (error) {
                showNotification('❌ Error clearing logs', 'error');
            }
        }
        
        // Utility functions
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        function showNotification(message, type = 'info') {
            // Simple notification - you could enhance this
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
        
        // Cleanup on page unload
        window.onbeforeunload = function() {
            if (updateInterval) {
                clearInterval(updateInterval);
            }
        };
    </script>
</body>
</html>
'''


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="GOB Monitoring Server")
    parser.add_argument("--port", type=int, default=8053, help="Port to run the server on")
    parser.add_argument("--gob-dir", default="/home/ds/GOB", help="GOB directory path")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open browser")
    
    args = parser.parse_args()
    
    server = MonitoringServer(
        port=args.port, 
        gob_directory=args.gob_dir,
        auto_open=not args.no_browser
    )
    server.run()
