#!/usr/bin/env python3
"""
GOB Network Monitor - Terminal Hacker Style
Independent monitoring dashboard with htop/btop aesthetic
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import requests
import json
import time
from datetime import datetime, timedelta
import psutil
import socket
from pathlib import Path

# Terminal color scheme
COLORS = {
    'bg': '#0c0c0c',           # Deep black background
    'panel': '#1a1a1a',       # Dark panel background
    'border': '#333333',      # Border color
    'text': '#00ff00',        # Matrix green text
    'accent': '#00cc00',      # Bright green accent
    'warning': '#ffaa00',     # Orange warning
    'error': '#ff3333',       # Red error
    'info': '#00aaff',        # Blue info
    'muted': '#666666',       # Muted text
}

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "GOB Network Monitor"

# Core service endpoints
CORE_HEALTH_URL = "http://localhost:8051/health"
CORE_STATE_URL = "http://localhost:8051/state"
CORE_STATE_FILE = "/tmp/gob-core-state.json"

def get_core_status():
    """Get core service status with fallback to state file"""
    try:
        # Try HTTP endpoint first
        response = requests.get(CORE_STATE_URL, timeout=2)
        if response.status_code == 200:
            return response.json(), "online"
    except:
        pass
    
    try:
        # Fallback to state file
        if Path(CORE_STATE_FILE).exists():
            with open(CORE_STATE_FILE, 'r') as f:
                data = json.load(f)
                # Check if file is recent (within last 60 seconds)
                last_updated = datetime.fromisoformat(data.get('last_updated', ''))
                if (datetime.now().astimezone() - last_updated).total_seconds() < 60:
                    return data, "file"
    except:
        pass
    
    return None, "offline"

def get_system_info():
    """Get local system information"""
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        return {
            'hostname': socket.gethostname(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_used_gb': memory.used / (1024**3),
            'memory_total_gb': memory.total / (1024**3),
            'disk_percent': disk.percent,
            'disk_used_gb': disk.used / (1024**3),
            'disk_total_gb': disk.total / (1024**3),
            'uptime': datetime.now() - boot_time,
            'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else [0, 0, 0]
        }
    except:
        return None

def create_status_card(title, value, status="normal", unit=""):
    """Create a terminal-style status card"""
    color = COLORS['text']
    if status == "warning":
        color = COLORS['warning']
    elif status == "error":
        color = COLORS['error']
    elif status == "info":
        color = COLORS['info']
    
    return html.Div([
        html.Div(f"┌─ {title} ─┐", style={'color': COLORS['border'], 'font-family': 'monospace'}),
        html.Div(f"│ {value}{unit} │", style={
            'color': color, 
            'font-family': 'monospace', 
            'font-size': '18px',
            'font-weight': 'bold'
        }),
        html.Div("└─────────┘", style={'color': COLORS['border'], 'font-family': 'monospace'}),
    ], style={'margin': '10px', 'display': 'inline-block'})

def create_progress_bar(label, value, max_value, unit=""):
    """Create a terminal-style progress bar"""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    bar_length = 20
    filled = int((percentage / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    color = COLORS['text']
    if percentage > 80:
        color = COLORS['error']
    elif percentage > 60:
        color = COLORS['warning']
    
    return html.Div([
        html.Span(f"{label}: ", style={'color': COLORS['muted'], 'font-family': 'monospace'}),
        html.Span(f"[{bar}] ", style={'color': color, 'font-family': 'monospace'}),
        html.Span(f"{percentage:.1f}% ({value:.1f}{unit})", 
                 style={'color': COLORS['text'], 'font-family': 'monospace'})
    ], style={'margin': '5px 0'})

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("GOB NETWORK MONITOR", style={
            'color': COLORS['accent'],
            'font-family': 'monospace',
            'text-align': 'center',
            'margin': '20px 0',
            'font-size': '24px',
            'letter-spacing': '2px'
        }),
        html.Div(id='timestamp', style={
            'color': COLORS['muted'],
            'font-family': 'monospace',
            'text-align': 'center',
            'margin-bottom': '20px'
        })
    ]),
    
    # Main content
    html.Div(id='main-content'),
    
    # Auto-refresh
    dcc.Interval(
        id='interval-component',
        interval=30000,  # Update every 30 seconds
        n_intervals=0
    )
], style={
    'backgroundColor': COLORS['bg'],
    'color': COLORS['text'],
    'min-height': '100vh',
    'padding': '20px',
    'font-family': 'monospace'
})

@callback(
    [Output('main-content', 'children'),
     Output('timestamp', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    """Update the dashboard content"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = f"Last Update: {current_time}"
    
    # Get core status
    core_data, core_status = get_core_status()
    system_info = get_system_info()
    
    if core_status == "offline":
        # Core is down - show error message
        content = html.Div([
            html.Div([
                "╔══════════════════════════════════════╗",
                html.Br(),
                "║           CORE SERVICES DOWN         ║",
                html.Br(),
                "║                                      ║",
                html.Br(),
                "║  The GOB core service is not         ║",
                html.Br(),
                "║  responding. Check service status.   ║",
                html.Br(),
                "║                                      ║",
                html.Br(),
                "╚══════════════════════════════════════╝"
            ], style={
                'color': COLORS['error'],
                'font-family': 'monospace',
                'text-align': 'center',
                'font-size': '16px',
                'margin': '50px auto',
                'white-space': 'pre'
            }),
            
            # Show local system info even when core is down
            html.Div([
                html.H3("LOCAL SYSTEM STATUS", style={
                    'color': COLORS['info'],
                    'font-family': 'monospace',
                    'text-align': 'center',
                    'margin': '30px 0'
                }),
                html.Div(id='local-system-info')
            ]) if system_info else None
        ])
    else:
        # Core is up - show full dashboard
        status_indicator = "ONLINE" if core_status == "online" else "FILE"
        status_color = COLORS['accent'] if core_status == "online" else COLORS['warning']
        
        content = html.Div([
            # Core status header
            html.Div([
                html.Span("CORE STATUS: ", style={'color': COLORS['muted']}),
                html.Span(status_indicator, style={'color': status_color, 'font-weight': 'bold'})
            ], style={'text-align': 'center', 'margin': '20px 0', 'font-family': 'monospace'}),
            
            # Core service info
            html.Div([
                create_status_card("SERVICE", core_data.get('service_name', 'N/A')),
                create_status_card("VERSION", core_data.get('version', 'N/A')),
                create_status_card("UPTIME", f"{core_data.get('uptime_seconds', 0):.0f}", unit="s"),
                create_status_card("RESTARTS", str(core_data.get('restart_count', 0))),
            ], style={'text-align': 'center', 'margin': '20px 0'}),
            
            # System metrics
            html.Div([
                html.H3("SYSTEM METRICS", style={
                    'color': COLORS['info'],
                    'font-family': 'monospace',
                    'text-align': 'center',
                    'margin': '30px 0'
                }),
                create_progress_bar("CPU", core_data.get('current_cpu_percent', 0), 100, "%"),
                create_progress_bar("MEMORY", core_data.get('current_memory_percent', 0), 100, "%"),
                create_progress_bar("DISK", core_data.get('current_disk_percent', 0), 100, "%"),
            ], style={'max-width': '600px', 'margin': '0 auto'}),
            
            # Network info
            html.Div([
                html.H3("NETWORK INFO", style={
                    'color': COLORS['info'],
                    'font-family': 'monospace',
                    'text-align': 'center',
                    'margin': '30px 0'
                }),
                html.Div([
                    html.Span("HOSTNAME: ", style={'color': COLORS['muted']}),
                    html.Span(core_data.get('hostname', 'N/A'), style={'color': COLORS['text']})
                ], style={'text-align': 'center', 'margin': '10px 0'}),
                html.Div([
                    html.Span("LOCAL IP: ", style={'color': COLORS['muted']}),
                    html.Span(core_data.get('local_ip', 'N/A'), style={'color': COLORS['text']})
                ], style={'text-align': 'center', 'margin': '10px 0'}),
            ], style={'font-family': 'monospace'}),
        ])
    
    return content, timestamp

if __name__ == '__main__':
    print("Starting GOB Network Monitor...")
    print("Dashboard will be available at http://localhost:8050")
    app.run(host='0.0.0.0', port=8050, debug=False)
