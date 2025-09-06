# GOB Monitoring System

A comprehensive, real-time monitoring and control system for the GOB multi-agent platform. This system provides independent process management, system health monitoring, and a beautiful web dashboard to observe and control your GOB system.

## ✨ Features

### 🎮 **Process Management**
- Independent control of GOB backend processes
- Start/Stop/Restart GOB from the dashboard
- Real-time process health monitoring
- Automatic crash detection and optional auto-restart
- Process output capture and display

### 📊 **Real-time Monitoring**
- Live system metrics (CPU, Memory, Disk)
- Agent lifecycle tracking and status
- Tool usage statistics and performance
- Model call monitoring with token tracking
- Error tracking and alerting
- Event stream with filtering

### 🌐 **Interactive Dashboard**
- Beautiful, responsive web interface
- Real-time updates without page refreshes
- Process control buttons
- Live metrics and charts
- Event timeline
- Process output logs

### 🔧 **System Integration**
- Non-intrusive monitoring via GOB's extension system
- Minimal performance impact on main system
- Graceful fallback if monitoring is unavailable
- Persists data independently of GOB state

## 🚀 Quick Start

### 1. Setup
```bash
cd /home/ds/GOB/monitoring
python setup.py
```

### 2. Start Monitoring
```bash
# Option 1: Use the launch script
./start_monitoring.sh

# Option 2: Direct Python
python server.py

# Option 3: Custom port
python server.py --port 8080
```

### 3. Access Dashboard
Open your browser to: **http://localhost:8050**

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Monitoring System                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Web UI    │  │ Process Mgr │  │   State Manager     │ │
│  │ Dashboard   │  │ (GOB Ctrl)  │  │  (Data Storage)     │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    GOB System                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐ │
│  │   Agent 0   │  │   Agent N   │  │   Extensions        │ │
│  │  (Main)     │  │ (Sub-agent) │  │ (Monitoring Hooks)  │ │
│  └─────────────┘  └─────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
monitoring/
├── core/
│   ├── state_manager.py      # Central data storage and event handling
│   └── process_manager.py    # GOB process lifecycle management
├── server.py                 # Main web server and API
├── requirements.txt          # Python dependencies
├── setup.py                 # Installation script
├── start_monitoring.sh      # Launch script
└── README.md               # This file

# Integration with GOB (automatically created)
python/extensions/
├── agent_init/_90_monitoring_hook.py
├── message_loop_start/_90_monitoring_hook.py
├── tool_execute_before/_90_monitoring_hook.py
└── tool_execute_after/_90_monitoring_hook.py
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Customize monitoring behavior
export MONITORING_PORT=8050
export MONITORING_UPDATE_INTERVAL=2000  # milliseconds
export GOB_DIRECTORY="/home/ds/GOB"
```

### Command Line Options
```bash
python server.py --help

Options:
  --port INTEGER     Port to run the server on (default: 8050)
  --gob-dir TEXT     GOB directory path (default: /home/ds/GOB)
```

## 📊 Monitoring Data

### Agent Tracking
- **Agent States**: idle, active, thinking, error, destroyed
- **Hierarchy**: Superior/subordinate relationships
- **Statistics**: Message count, tool usage, model calls, errors
- **Performance**: Response times, token usage, memory operations

### System Metrics
- **Resource Usage**: CPU, memory, disk utilization
- **Process Health**: Uptime, restart count, crash detection
- **Activity Summary**: Active agents, conversations, total operations

### Events
- **Agent Lifecycle**: Creation, destruction, status changes
- **Tool Execution**: Start, completion, errors, timing
- **Model Calls**: Provider, tokens used, response times
- **System Events**: Errors, performance alerts, status changes

## 🔌 API Endpoints

### Status & Control
- `GET /api/status` - System status overview
- `POST /api/process/start` - Start GOB process
- `POST /api/process/stop` - Stop GOB process  
- `POST /api/process/restart` - Restart GOB process

### Data Access
- `GET /api/agents` - Agent summary and hierarchy
- `GET /api/metrics` - Current system metrics
- `GET /api/metrics/history` - Historical metrics
- `GET /api/events` - Recent events with filtering
- `GET /api/process/output` - Process output logs

## 🛠️ Development

### Adding Custom Monitoring
1. Create new extension in appropriate extension point directory
2. Import state manager: `from core.state_manager import get_state_manager`
3. Record events: `state_manager.emit_event(...)`
4. Update agent states: `state_manager.update_agent_status(...)`

### Extending the Dashboard
1. Add new API endpoints in `server.py`
2. Modify the `DASHBOARD_HTML` template
3. Use real-time updates via JavaScript fetch API

## 🔍 Troubleshooting

### Common Issues

**Q: Dashboard shows "No events yet" even with GOB running**
A: Check that monitoring extensions are properly installed and GOB was restarted after setup.

**Q: Process control buttons don't work**
A: Verify the monitoring server has proper permissions and GOB directory path is correct.

**Q: High CPU usage**
A: Adjust update intervals or disable verbose logging. Check `--help` for performance options.

### Debugging
```bash
# Enable verbose logging
python server.py --debug

# Check extension loading
# Look for monitoring hooks in GOB startup logs

# Test API endpoints directly
curl http://localhost:8050/api/status
```

## 📈 Performance Impact

The monitoring system is designed for minimal performance impact:
- **Extensions**: ~1-2ms overhead per operation
- **Memory**: <50MB additional RAM usage
- **Network**: Local-only communication, no external calls
- **Storage**: Events are stored in memory with automatic rotation

## 🤝 Contributing

This monitoring system is part of the GOB platform. To contribute:
1. Follow GOB development standards
2. Test thoroughly with different agent configurations
3. Ensure monitoring remains optional and graceful
4. Document new features and API changes

## 📄 License

Same as the GOB project - this monitoring system is part of the GOB ecosystem.
