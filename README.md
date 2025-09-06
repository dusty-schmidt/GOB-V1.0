# GOB (General Orchestrator Bot)

A customized AI agent system built on Agent Zero, focused on orchestration and autonomous task management.

## 🚀 Quick Start

### Native Development (Recommended)

```bash
# Start GOB server
./gob start

# Check status and health
./gob status

# View recent logs
./gob logs

# Open in browser
./gob url

# Stop server
./gob stop
```

**Default Access**: http://localhost:50080

### Requirements
- **Python**: 3.11+ (via Miniconda/Anaconda)
- **Environment**: `gob` conda environment with all dependencies
- **System**: Linux/macOS/Windows with bash support

---

## 📋 Setup Process

### 1. Environment Setup
```bash
# Create and activate conda environment
conda create -n gob python=3.11
conda activate gob

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Run initial setup
python scripts/prepare.py

# Optional: Preload models
python scripts/preload.py
```

### 3. Launch GOB
```bash
# Using the CLI tool (auto-detects environment)
./gob start

# Or directly
python run_ui.py --host 0.0.0.0 --port 50080
```

---

## 📁 Project Structure

```
gob/
├── gob                 # CLI management tool
├── agent.py           # Core agent system
├── models.py          # LLM configuration
├── initialize.py      # System initialization
├── run_ui.py          # Main server entry point
├── run_tunnel.py      # Tunnel server
├── scripts/           # Utility scripts
│   ├── preload.py     # Model preloading
│   ├── prepare.py     # Environment setup
│   └── update_reqs.py # Requirements updater
├── python/            # Framework core
├── webui/             # Web interface
├── docs/              # Documentation
└── worklogs/          # Development history
```

---

## 🔧 CLI Management

The `./gob` script provides comprehensive server management:

| Command | Description |
|---------|-------------|
| `./gob start` | Start server with health checks |
| `./gob stop` | Graceful shutdown |
| `./gob restart` | Stop and start server |
| `./gob status` | Show server status and process info |
| `./gob logs [N]` | Show last N log lines (default: 50) |
| `./gob follow` | Follow logs in real-time |
| `./gob url` | Open GOB in browser |
| `./gob help` | Show all available commands |

---

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[Development Worklogs](worklogs/)** - Session notes and progress tracking
- **[TODO List](TODO.md)** - Planned improvements and features

---

## 🛠️ Development

### Making Changes
1. Edit code in your preferred IDE
2. Test changes: `./gob restart`
3. View logs: `./gob logs` or `./gob follow`
4. Commit significant changes and update worklogs

### Adding Dependencies
```bash
# Add to requirements.txt, then:
pip install -r requirements.txt
# Update lockfile:
python scripts/update_reqs.py
```

### Environment Management
- GOB automatically detects and activates the `gob` conda environment
- Supports both `mamba` and `conda` package managers
- Configuration stored in environment variables and settings files


