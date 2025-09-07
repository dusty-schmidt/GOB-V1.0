# GOB User Interface Directory

This directory contains all user interface components for the GOB (General Operations Bridge) system.

## Directory Structure

```
ui/
├── webui/                    # Main web user interfaces
│   └── agent-interface/      # Primary agent interaction interface
│       ├── index.html        # Main agent chat interface
│       ├── index.js          # Core JavaScript functionality
│       ├── css/              # Stylesheets
│       ├── js/               # JavaScript modules
│       └── components/       # Reusable UI components
│
└── admin-panel/              # Administrative interfaces
    ├── flask-backend-monitor/    # Flask-based backend monitoring (ACTIVE)
    │   ├── server.py             # Main Flask server with anti-twitching fixes
    │   ├── config/               # Configuration files
    │   ├── data/                 # Persistent data storage
    │   └── logs/                 # Monitor logs
    │
    └── dash-network-monitor/     # Dash-based network monitor (LEGACY)
        ├── app.py                # Dash application
        ├── start_monitor.py      # Startup script
        └── assets/               # Static assets
```

## Active Interfaces

### 1. Agent Interface (`webui/agent-interface/`)
- **Purpose**: Primary user interface for interacting with GOB agents
- **Technology**: HTML/JavaScript/CSS
- **Features**: Real-time chat, task management, file operations
- **Access**: Typically runs on port 8080

### 2. Flask Backend Monitor (`admin-panel/flask-backend-monitor/`)
- **Purpose**: Administrative monitoring and control of GOB backend systems
- **Technology**: Flask + JavaScript
- **Features**: 
  - Real-time system metrics (no visual twitching)
  - Process management and control
  - Event monitoring and logging
  - GOB interface with status light and real-time clock
- **Access**: http://localhost:8050
- **Status**: ✅ ACTIVE - Recently updated with anti-twitching fixes

## Starting the Interfaces

### Flask Backend Monitor
```bash
cd ui/admin-panel/flask-backend-monitor
python server.py
```

### Agent Interface
```bash
cd ui/webui/agent-interface
# Typically started via GOB's main run scripts
```

## Recent Updates

- **2025-09-06**: Reorganized UI structure into logical directories
- **2025-09-06**: Fixed twitching issues in Flask backend monitor
- **2025-09-06**: Implemented smooth, non-flickering updates for all dashboard components
- **2025-09-06**: Added real-time clock with seconds display
- **2025-09-06**: Optimized update intervals (time: 1s, data: 2s)

## Development Notes

- All monitoring interfaces follow GOB design preferences:
  - Status light in top-left corner
  - Centered title 'GENERAL OPERATIONS BRIDGE (GOB)'
  - Real-time clock with seconds in top-right
  - Structured sections for status and metrics
- Updates are designed to be imperceptible to users (no visual refreshing)
- Each interface should maintain its own conda environment for clean dependency separation
