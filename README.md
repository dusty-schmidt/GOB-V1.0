# GOBV1 - General Orchestrator Bot V1.0

An advanced AI agent orchestration system for autonomous task management.

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/dusty-schmidt/GOB-V1.0.git
cd GOB-V1.0
```

### 2. Run automatic setup
```bash
./setup.sh
```

### 3. Start GOBV1
```bash
scripts/gob start
```

### 4. Open in browser
http://localhost:50080

That's it! 🎉

## 🔧 Daily Usage

```bash
# Start GOBV1
scripts/gob start

# Check status  
scripts/gob status

# View logs
scripts/gob logs

# Stop GOBV1
scripts/gob stop

# Get help
scripts/gob help
```

## 📋 Requirements

- **Linux** or **macOS** (Windows with WSL2)
- **8GB+ RAM** recommended
- **2GB free disk space**
- **Internet connection** for setup

The setup script will automatically install:
- Miniconda (if needed)
- Python environment with all dependencies
- GOBV1 CLI tool

## 🆘 Troubleshooting

### Setup Issues
```bash
# Re-run setup if something failed
./setup.sh

# Check if conda is installed
conda --version

# Manual environment activation
conda activate gob
```

### Runtime Issues
```bash
# Check detailed status
scripts/gob status

# View recent logs
scripts/gob logs 50

# Restart if needed
scripts/gob restart
```

### Common Solutions
- **Port in use**: Another service using port 50080
- **Environment not found**: Run `./setup.sh` again
- **Permission denied**: Make sure `./gob` and `./setup.sh` are executable

## 📚 Documentation

- **[docs/](docs/)** - Complete documentation
- **[Setup Guide](docs/SETUP.md)** - Detailed manual setup
- **[Troubleshooting](docs/README.md)** - Common issues and solutions

## 🏗️ Development

```bash
# Activate environment
conda activate gob

# Make changes to code
# ...

# Restart to apply changes
scripts/gob restart

# Follow logs
scripts/gob follow
```

## 📁 Project Structure

```
GOB-V1.0/
├── gob -> scriptscripts/gob       # CLI management tool (symlink)
├── setup.sh               # Automatic setup script
├── agent.py               # Core agent system
├── models.py              # LLM configuration
├── run_ui.py              # Main server entry point
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (create this)
├── agents/                # AI agent definitions
├── python/                # Framework core
├── webui/                 # Web interface
├── scripts/               # Utility scripts\n│   └── gob                # CLI management script
├── docs/                  # Documentation
└── README.md              # This file
```

## ✅ What Works Out of the Box

- ✅ **Automatic setup** - One command installation
- ✅ **CLI management** - Simple start/stop/status commands  
- ✅ **Web interface** - Modern browser-based UI
- ✅ **Agent orchestration** - Multiple AI agents working together
- ✅ **Task management** - Autonomous task execution
- ✅ **Logging** - Comprehensive activity logs
- ✅ **Cross-platform** - Linux, macOS, WSL2

## 🔗 Links

- **Repository**: https://github.com/dusty-schmidt/GOB-V1.0
- **Web Interface**: http://localhost:50080 (when running)
- **Issues**: https://github.com/dusty-schmidt/GOB-V1.0/issues

---

**Need help?** Check the [documentation](docs/) or open an [issue](https://github.com/dusty-schmidt/GOB-V1.0/issues).
