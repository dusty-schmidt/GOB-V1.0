# GOB Core Services

This directory contains the foundational services for the GOB multi-agent system.

## Architecture Overview

The GOB system now uses a proper layered architecture with clear dependencies:

```
┌─────────────────────────────────────────┐
│           GOB Agent Framework           │  ← Main AI assistant
│         (gob-agent.service)             │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│        GOB Monitoring Dashboard         │  ← Web interface & control
│       (gob-monitoring.service)          │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│         GOB Core State Manager          │  ← Foundation layer
│         (gob-core.service)              │
└─────────────────────────────────────────┘
```

## Core Components

### 1. State Manager (`state_manager.py`)
- **Purpose**: Centralized monitoring and state management for the entire GOB system
- **Responsibilities**:
  - Track agent lifecycle and performance
  - Monitor system resources (CPU, memory, disk)
  - Collect and store events from all components
  - Provide real-time metrics and statistics
  - Manage agent hierarchy and relationships

### 2. Process Manager (`process_manager.py`)
- **Purpose**: Independent control of GOB backend processes
- **Responsibilities**:
  - Start/stop/restart GOB processes
  - Monitor process health and performance
  - Capture and buffer process output
  - Handle process crashes and auto-restart
  - Provide process status and metrics

### 3. Service Manager (`service_manager.py`)
- **Purpose**: Unified management of all GOB services
- **Responsibilities**:
  - Coordinate startup sequence with proper dependencies
  - Health monitoring of all services
  - Service discovery and status reporting
  - Graceful shutdown coordination

## Service Dependencies

### Boot Sequence
1. **gob-core.service** starts first (no dependencies)
   - Initializes state manager
   - Provides foundation for monitoring
   
2. **gob-monitoring.service** starts second
   - Depends on: `gob-core.service`
   - Waits for core service to be active
   - Provides web dashboard on port 8050
   
3. **gob-agent.service** starts last
   - Depends on: `gob-core.service`
   - Waits for monitoring dashboard to be healthy
   - Provides main AI interface on port 50080

### Health Checks
- **Core Service**: Systemd active status
- **Monitoring Service**: HTTP GET to `http://localhost:8050/api/status`
- **Agent Service**: HTTP GET to `http://localhost:50080`

## Management Commands

Use the unified service management script:

```bash
# Install all services for boot startup
./scripts/gob-services install

# Start all services in correct order
./scripts/gob-services start

# Check status of all services
./scripts/gob-services status

# Stop all services
./scripts/gob-services stop

# View logs
./scripts/gob-services logs
./scripts/gob-services logs gob-core 100
./scripts/gob-services follow gob-monitoring

# Uninstall services
./scripts/gob-services uninstall
```

## Service Files Location

All systemd service files are located in `/home/ds/GOB/services/`:
- `gob-core.service` - Core state manager
- `gob-monitoring.service` - Monitoring dashboard  
- `gob-agent.service` - Main agent framework

## Migration from Old Architecture

The core components were moved from `/home/ds/GOB/monitoring/core/` to `/home/ds/GOB/core/` to:

1. **Separate Concerns**: Core services are foundational, not just monitoring
2. **Clear Dependencies**: Other components can depend on core without circular references
3. **Better Organization**: Core services are now at the root level where they belong
4. **Easier Maintenance**: Core services can be managed independently

## Troubleshooting

### Check Service Status
```bash
sudo systemctl status gob-core
sudo systemctl status gob-monitoring  
sudo systemctl status gob-agent
```

### View Service Logs
```bash
sudo journalctl -u gob-core -f
sudo journalctl -u gob-monitoring -f
sudo journalctl -u gob-agent -f
```

### Manual Service Control
```bash
# Start services manually in order
sudo systemctl start gob-core
sudo systemctl start gob-monitoring
sudo systemctl start gob-agent

# Stop services in reverse order
sudo systemctl stop gob-agent
sudo systemctl stop gob-monitoring
sudo systemctl stop gob-core
```

### Health Check URLs
- Core Service: No HTTP endpoint (check systemd status)
- Monitoring: http://localhost:8050/api/status
- Agent: http://localhost:50080

## Configuration

### Environment Variables
- `GOB_DIRECTORY`: Path to GOB installation (default: `/home/ds/GOB`)
- `PYTHONPATH`: Set to GOB directory for imports
- `PATH`: Includes conda environment binaries

### Resource Limits
- **Core Service**: 256MB RAM, 25% CPU
- **Monitoring Service**: 512MB RAM, 50% CPU  
- **Agent Service**: 2GB RAM, 200% CPU

### Logging
- Core: systemd journal (`gob-core` identifier)
- Monitoring: systemd journal (`gob-monitoring` identifier)
- Agent: File logs in `/home/ds/GOB/logs/`
