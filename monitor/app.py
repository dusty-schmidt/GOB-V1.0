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

# Terminal color scheme - matching webui terminal-theme-v2.css
COLORS = {
    'bg': '#0a0a0a',           # Deep black background (matches webui)
    'panel': '#0a0a0a',       # Same as background for seamless look
    'border': '#333333',      # Border color
    'border_subtle': '#222222', # Subtle borders
    'text': '#ffffff',        # Primary white text
    'text_secondary': '#dddddd', # Secondary text
    'text_muted': '#888888',  # Muted text
    'text_dim': '#666666',    # Dim text
    'text_faint': '#555555',  # Faint text
    'text_dimmer': '#444444', # Dimmer text
    'accent_green': '#00ff00', # Bright green accent
    'warning': '#ffaa00',     # Orange warning
    'error': '#ff0000',       # Red error
    'info': '#00aaff',        # Blue info
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
    """Create a terminal-style status card matching webui aesthetic"""
    color = COLORS['text_secondary']
    if status == "warning":
        color = COLORS['warning']
    elif status == "error":
        color = COLORS['error']
    elif status == "info":
        color = COLORS['info']
    elif status == "accent":
        color = COLORS['accent_green']

    # Clean, minimal terminal style without heavy borders
    return html.Div([
        html.Div(title.upper(), style={
            'color': COLORS['text_dimmer'],
            'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
            'font-size': '10px',
            'margin-bottom': '3px',
            'text-transform': 'uppercase'
        }),
        html.Div(f"{value}{unit}", style={
            'color': color,
            'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
            'font-size': '16px',
            'line-height': '1.4'
        }),
    ], style={'margin': '16px', 'display': 'inline-block', 'text-align': 'left'})

def create_progress_bar(label, value, max_value, unit=""):
    """Create a terminal-style progress bar matching webui aesthetic"""
    percentage = (value / max_value) * 100 if max_value > 0 else 0
    bar_length = 20
    filled = int((percentage / 100) * bar_length)
    bar = "█" * filled + "░" * (bar_length - filled)

    color = COLORS['text_secondary']
    if percentage > 80:
        color = COLORS['error']
    elif percentage > 60:
        color = COLORS['warning']

    font_family = "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace"

    return html.Div([
        html.Span(f"{label.upper()}: ", style={
            'color': COLORS['text_muted'],
            'font-family': font_family,
            'font-size': '13px'
        }),
        html.Span(f"[{bar}] ", style={
            'color': color,
            'font-family': font_family,
            'font-size': '13px'
        }),
        html.Span(f"{percentage:.1f}% ({value:.1f}{unit})", style={
            'color': COLORS['text_secondary'],
            'font-family': font_family,
            'font-size': '13px'
        })
    ], style={'margin': '8px 0', 'line-height': '1.4'})

# App layout - matching webui terminal aesthetic
app.layout = html.Div([
    # Header with webui-style title bar
    html.Div([
        html.Div("GOB NETWORK MONITOR", style={
            'color': COLORS['text_dim'],
            'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
            'font-size': '13px',
            'margin': '0',
            'padding': '4px 16px',
            'position': 'fixed',
            'top': '0',
            'left': '0',
            'right': '0',
            'height': '24px',
            'background': 'transparent',
            'display': 'flex',
            'align-items': 'center',
            'z-index': '2000'
        }),
        html.Div(id='timestamp', style={
            'color': COLORS['text_dim'],
            'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
            'font-size': '13px',
            'position': 'fixed',
            'top': '4px',
            'right': '16px',
            'z-index': '2000'
        })
    ]),

    # Main content with proper spacing for title bar
    html.Div(id='main-content', style={'margin-top': '32px'}),

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
    'padding': '16px',
    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
    'font-size': '13px',
    'line-height': '1.4'
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
        # Core is down - show error message in webui style
        content = html.Div([
            html.Div([
                html.Div("CORE SERVICES DOWN", style={
                    'color': COLORS['error'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '16px',
                    'margin-bottom': '8px',
                    'text-align': 'center'
                }),
                html.Div("The GOB core service is not responding.", style={
                    'color': COLORS['text_muted'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '13px',
                    'text-align': 'center',
                    'margin-bottom': '16px'
                }),
                html.Div("Check service status with: ./manage-core.sh status", style={
                    'color': COLORS['text_dim'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '13px',
                    'text-align': 'center'
                })
            ], style={
                'border': f'1px solid {COLORS["border"]}',
                'padding': '24px',
                'margin': '40px auto',
                'max-width': '400px',
                'background': COLORS['panel']
            }),
            
            # Show local system info even when core is down
            html.Div([
                html.Div("LOCAL SYSTEM STATUS", style={
                    'color': COLORS['text_dimmer'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '10px',
                    'text-transform': 'uppercase',
                    'text-align': 'center',
                    'margin': '32px 0 16px 0'
                }),
                html.Div([
                    create_progress_bar("CPU", system_info.get('cpu_percent', 0), 100, "%") if system_info else None,
                    create_progress_bar("MEMORY", system_info.get('memory_percent', 0), 100, "%") if system_info else None,
                    create_progress_bar("DISK", system_info.get('disk_percent', 0), 100, "%") if system_info else None,
                ], style={'max-width': '400px', 'margin': '0 auto'})
            ]) if system_info else None
        ])
    else:
        # Core is up - show full dashboard in webui style
        status_indicator = "ONLINE" if core_status == "online" else "FILE"
        status_color = COLORS['accent_green'] if core_status == "online" else COLORS['warning']

        font_family = "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace"

        content = html.Div([
            # Core status in floating style like webui
            html.Div([
                html.Span("gob> ", style={
                    'color': COLORS['text_dim'],
                    'font-family': font_family,
                    'font-size': '13px'
                }),
                html.Span(f"core status: {status_indicator.lower()}", style={
                    'color': status_color,
                    'font-family': font_family,
                    'font-size': '13px'
                })
            ], style={'margin': '16px 0'}),

            # Core service info in floating panels style
            html.Div([
                html.Div([
                    create_status_card("service", core_data.get('service_name', 'N/A')),
                    create_status_card("version", core_data.get('version', 'N/A')),
                ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '32px'}),
                html.Div([
                    create_status_card("uptime", f"{core_data.get('uptime_seconds', 0):.0f}s"),
                    create_status_card("restarts", str(core_data.get('restart_count', 0))),
                ], style={'display': 'inline-block', 'vertical-align': 'top'}),
            ], style={'margin': '24px 0'}),
            
            # System metrics in webui style
            html.Div([
                html.Div("SYSTEM METRICS", style={
                    'color': COLORS['text_dimmer'],
                    'font-family': font_family,
                    'font-size': '10px',
                    'text-transform': 'uppercase',
                    'margin': '32px 0 16px 0'
                }),
                create_progress_bar("cpu", core_data.get('current_cpu_percent', 0), 100, "%"),
                create_progress_bar("memory", core_data.get('current_memory_percent', 0), 100, "%"),
                create_progress_bar("disk", core_data.get('current_disk_percent', 0), 100, "%"),
            ], style={'max-width': '500px', 'margin': '0 0 32px 0'}),

            # Network info in webui floating style
            html.Div([
                html.Div("NETWORK", style={
                    'color': COLORS['text_dimmer'],
                    'font-family': font_family,
                    'font-size': '10px',
                    'text-transform': 'uppercase',
                    'margin-bottom': '8px'
                }),
                html.Div([
                    html.Span("hostname: ", style={
                        'color': COLORS['text_muted'],
                        'font-family': font_family,
                        'font-size': '13px'
                    }),
                    html.Span(core_data.get('hostname', 'N/A'), style={
                        'color': COLORS['text_secondary'],
                        'font-family': font_family,
                        'font-size': '13px'
                    })
                ], style={'margin': '4px 0'}),
                html.Div([
                    html.Span("local_ip: ", style={
                        'color': COLORS['text_muted'],
                        'font-family': font_family,
                        'font-size': '13px'
                    }),
                    html.Span(core_data.get('local_ip', 'N/A'), style={
                        'color': COLORS['text_secondary'],
                        'font-family': font_family,
                        'font-size': '13px'
                    })
                ], style={'margin': '4px 0'}),
            ], style={'margin': '0 0 32px 0'}),
        ])
    
    return content, timestamp

if __name__ == '__main__':
    print("Starting GOB Network Monitor...")
    print("Dashboard will be available at http://localhost:8050")
    app.run(host='0.0.0.0', port=8050, debug=False)
