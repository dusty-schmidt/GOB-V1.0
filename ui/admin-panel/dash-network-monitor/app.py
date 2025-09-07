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
import hashlib

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

# Initialize Dash app with assets folder
app = dash.Dash(__name__, assets_folder='assets')
app.title = "GOB Network Monitor"

# Suppress callback exceptions for dynamic content
app.config.suppress_callback_exceptions = True

# Global cache for component states to prevent unnecessary re-renders
_component_cache = {
    'status_light_hash': None,
    'core_status_hash': None,
    'system_metrics_hash': None,
    'last_status_light': None,
    'last_core_status': None,
    'last_system_metrics': None
}

# Add custom CSS for status light animations
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes pulse {
                0%, 100% {
                    opacity: 1;
                    text-shadow: 0 0 8px #00ff00;
                }
                50% {
                    opacity: 0.7;
                    text-shadow: 0 0 4px #00ff00;
                }
            }
            .status-light-online {
                animation: pulse 2s ease-in-out infinite !important;
                text-shadow: 0 0 8px #00ff00 !important;
                color: #00ff00 !important;
            }
            .status-light-warning {
                text-shadow: 0 0 6px #ffaa00 !important;
                color: #ffaa00 !important;
            }
            .status-light-offline {
                text-shadow: none !important;
                opacity: 0.3 !important;
                color: #444444 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

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

def create_content_hash(data):
    """Create a hash of data to detect changes"""
    if data is None:
        return None
    try:
        # Convert data to string and create hash
        content_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(content_str.encode()).hexdigest()
    except:
        return str(hash(str(data)))

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

def create_status_light(core_status):
    """Create standalone status light for corner"""
    # Determine status light color
    if core_status == "online":
        light_color = COLORS['accent_green']
    elif core_status == "file":
        light_color = COLORS['warning']
    else:
        light_color = COLORS['text_dimmer']

    return html.Div("●",
        className=f'status-light-{core_status}' if core_status in ['online', 'offline'] else 'status-light-warning',
        style={
            'color': light_color,
            'font-size': '24px',
            'line-height': '1',
            'text-shadow': f'0 0 8px {light_color}' if core_status != "offline" else 'none',
            'animation': 'pulse 2s ease-in-out infinite' if core_status == "online" else 'none'
        }
    )

def create_core_status_section(core_data, core_status):
    """Create detailed core status section"""
    font_family = "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace"

    # Determine status text and color
    if core_status == "online":
        status_text = "ONLINE"
        status_color = COLORS['accent_green']
        status_detail = "Core services operational"
    elif core_status == "file":
        status_text = "STANDBY"
        status_color = COLORS['warning']
        status_detail = "Reading from state file"
    else:
        status_text = "OFFLINE"
        status_color = COLORS['error']
        status_detail = "Core services unavailable"

    if core_status == "offline":
        return html.Div([
            html.Div("CORE STATUS", style={
                'color': COLORS['text_dimmer'],
                'font-family': font_family,
                'font-size': '10px',
                'text-transform': 'uppercase',
                'margin-bottom': '16px',
                'letter-spacing': '1px'
            }),
            html.Div([
                html.Div("CORE SERVICES OFFLINE", style={
                    'color': COLORS['error'],
                    'font-family': font_family,
                    'font-size': '16px',
                    'margin-bottom': '8px'
                }),
                html.Div("The GOB core service is not responding.", style={
                    'color': COLORS['text_muted'],
                    'font-family': font_family,
                    'font-size': '13px',
                    'margin-bottom': '8px'
                }),
                html.Div("Check service status: ./manage-core.sh status", style={
                    'color': COLORS['text_dim'],
                    'font-family': font_family,
                    'font-size': '11px'
                })
            ])
        ])

    return html.Div([
        html.Div("CORE STATUS", style={
            'color': COLORS['text_dimmer'],
            'font-family': font_family,
            'font-size': '10px',
            'text-transform': 'uppercase',
            'margin-bottom': '16px',
            'letter-spacing': '1px'
        }),

        # Status line
        html.Div([
            html.Span("STATUS: ", style={
                'color': COLORS['text_muted'],
                'font-family': font_family,
                'font-size': '13px'
            }),
            html.Span(status_text, style={
                'color': status_color,
                'font-family': font_family,
                'font-size': '13px',
                'font-weight': 'bold'
            }),
            html.Span(f" - {status_detail}", style={
                'color': COLORS['text_dim'],
                'font-family': font_family,
                'font-size': '13px',
                'margin-left': '8px'
            })
        ], style={'margin-bottom': '16px'}),

        # Core details grid
        html.Div([
            html.Div([
                create_status_card("service", core_data.get('service_name', 'N/A')),
                create_status_card("version", core_data.get('version', 'N/A')),
            ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-right': '32px'}),
            html.Div([
                create_status_card("uptime", f"{core_data.get('uptime_seconds', 0):.0f}s"),
                create_status_card("restarts", str(core_data.get('restart_count', 0))),
            ], style={'display': 'inline-block', 'vertical-align': 'top'}),
        ])
    ])

def create_system_metrics_section(core_data, system_info):
    """Create system metrics section"""
    font_family = "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace"

    return html.Div([
        html.Div("SYSTEM METRICS", style={
            'color': COLORS['text_dimmer'],
            'font-family': font_family,
            'font-size': '10px',
            'text-transform': 'uppercase',
            'margin-bottom': '16px',
            'letter-spacing': '1px'
        }),

        # Use core data if available, otherwise system info
        html.Div([
            create_progress_bar("cpu",
                core_data.get('current_cpu_percent', system_info.get('cpu_percent', 0)) if core_data else system_info.get('cpu_percent', 0),
                100, "%"),
            create_progress_bar("memory",
                core_data.get('current_memory_percent', system_info.get('memory_percent', 0)) if core_data else system_info.get('memory_percent', 0),
                100, "%"),
            create_progress_bar("disk",
                core_data.get('current_disk_percent', system_info.get('disk_percent', 0)) if core_data else system_info.get('disk_percent', 0),
                100, "%"),
        ], style={'max-width': '500px'}),

        # Network info
        html.Div([
            html.Div("NETWORK", style={
                'color': COLORS['text_dimmer'],
                'font-family': font_family,
                'font-size': '10px',
                'text-transform': 'uppercase',
                'margin': '24px 0 8px 0',
                'letter-spacing': '1px'
            }),
            html.Div([
                html.Span("hostname: ", style={
                    'color': COLORS['text_muted'],
                    'font-family': font_family,
                    'font-size': '13px'
                }),
                html.Span(core_data.get('hostname', system_info.get('hostname', 'N/A')) if core_data else system_info.get('hostname', 'N/A'), style={
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
                html.Span(core_data.get('local_ip', 'N/A') if core_data else 'N/A', style={
                    'color': COLORS['text_secondary'],
                    'font-family': font_family,
                    'font-size': '13px'
                })
            ], style={'margin': '4px 0'}),
        ])
    ])

# App layout - refined header with status light in corner
app.layout = html.Div([
    # Fixed header section
    html.Div([
        # Main header row
        html.Div([
            # Status light in top left corner
            html.Div(id='status-light-corner', style={
                'position': 'absolute',
                'top': '16px',
                'left': '16px'
            }),

            # Centered title
            html.Div([
                html.Div("GENERAL OPERATIONS BRIDGE", style={
                    'color': COLORS['text_secondary'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '18px',
                    'font-weight': 'bold',
                    'text-align': 'center',
                    'letter-spacing': '2px',
                    'margin-bottom': '4px'
                }),
                html.Div("(GOB)", style={
                    'color': COLORS['text_dim'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '13px',
                    'text-align': 'center',
                    'letter-spacing': '1px'
                })
            ], style={
                'flex': '1',
                'display': 'flex',
                'flex-direction': 'column',
                'justify-content': 'center',
                'align-items': 'center'
            }),

            # Time display in top right corner
            html.Div([
                html.Div(id='current-time', style={
                    'color': COLORS['text_secondary'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '14px',
                    'text-align': 'right',
                    'margin-bottom': '2px'
                }),
                html.Div(id='current-date', style={
                    'color': COLORS['text_dim'],
                    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
                    'font-size': '11px',
                    'text-align': 'right'
                })
            ], style={
                'position': 'absolute',
                'top': '16px',
                'right': '16px'
            })
        ], style={
            'position': 'relative',
            'padding': '24px 80px',
            'height': '80px',
            'display': 'flex',
            'align-items': 'center'
        })
    ], style={
        'position': 'fixed',
        'top': '0',
        'left': '0',
        'right': '0',
        'background': COLORS['bg'],
        'z-index': '2000',
        'border-bottom': f'1px solid {COLORS["border"]}'
    }),

    # Main content sections with proper spacing for fixed header
    html.Div([
        # Core status details section
        html.Div(id='core-status-section', style={
            'margin-bottom': '32px',
            'padding': '24px',
            'border': f'1px solid {COLORS["border_subtle"]}',
            'background': COLORS['bg']
        }),

        # System metrics section
        html.Div(id='system-metrics-section', style={
            'padding': '24px',
            'border': f'1px solid {COLORS["border_subtle"]}',
            'background': COLORS['bg']
        })
    ], style={'margin-top': '100px', 'padding': '16px'}),

    # Single interval for all updates with clientside optimization
    dcc.Interval(
        id='main-interval',
        interval=1000,  # Update every 1 second
        n_intervals=0
    ),

    # Hidden div to store data for clientside callbacks
    html.Div(id='data-store', style={'display': 'none'})
], style={
    'backgroundColor': COLORS['bg'],
    'color': COLORS['text'],
    'min-height': '100vh',
    'font-family': "'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace",
    'font-size': '13px',
    'line-height': '1.4'
})

# Single server-side callback to fetch all data
@callback(
    Output('data-store', 'children'),
    [Input('main-interval', 'n_intervals')],
    prevent_initial_call=False
)
def update_data_store(n):
    """Fetch all data and store in hidden div"""
    # Get current time
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    # Get core status
    core_data, core_status = get_core_status()
    system_info = get_system_info()

    # Package all data
    data = {
        'timestamp': now.isoformat(),
        'time': current_time,
        'date': current_date,
        'core_status': core_status,
        'core_data': core_data,
        'system_info': system_info
    }

    return json.dumps(data)

# Callback for dashboard data updates (every 5 seconds)
@callback(
    [Output('status-light-corner', 'children'),
     Output('core-status-section', 'children'),
     Output('system-metrics-section', 'children')],
    [Input('dashboard-interval', 'n_intervals')],
    prevent_initial_call=False
)
def update_dashboard_data(n):
    """Update the dashboard data (excluding time) with smart caching"""
    global _component_cache

    # Get core status
    core_data, core_status = get_core_status()
    system_info = get_system_info()

    # Create content hashes to detect changes
    status_light_hash = create_content_hash(core_status)
    core_status_hash = create_content_hash(core_data)
    system_metrics_hash = create_content_hash({
        'core': core_data,
        'system': system_info
    })

    # Only update components that have actually changed
    status_light = _component_cache['last_status_light']
    if status_light_hash != _component_cache['status_light_hash']:
        status_light = create_status_light(core_status)
        _component_cache['status_light_hash'] = status_light_hash
        _component_cache['last_status_light'] = status_light

    core_status_section = _component_cache['last_core_status']
    if core_status_hash != _component_cache['core_status_hash']:
        core_status_section = create_core_status_section(core_data, core_status)
        _component_cache['core_status_hash'] = core_status_hash
        _component_cache['last_core_status'] = core_status_section

    system_metrics_section = _component_cache['last_system_metrics']
    if system_metrics_hash != _component_cache['system_metrics_hash']:
        system_metrics_section = create_system_metrics_section(core_data, system_info)
        _component_cache['system_metrics_hash'] = system_metrics_hash
        _component_cache['last_system_metrics'] = system_metrics_section

    # Return cached components if no changes, or updated ones if changed
    return (
        status_light or create_status_light(core_status),
        core_status_section or create_core_status_section(core_data, core_status),
        system_metrics_section or create_system_metrics_section(core_data, system_info)
    )

if __name__ == '__main__':
    print("Starting GOB Network Monitor...")
    print("Dashboard will be available at http://localhost:8052")
    app.run(host='0.0.0.0', port=8052, debug=False)
