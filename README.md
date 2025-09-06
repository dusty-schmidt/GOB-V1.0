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
./gob start
```

### 4. Open in browser
http://localhost:50080

That's it! 🎉

## 🔧 Daily Usage

```bash
# Start GOBV1
./gob start

# Check status  
./gob status

# View logs
./gob logs

# Stop GOBV1
./gob stop

# Get help
./gob help
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
conda activate gobv1
```

### Runtime Issues
```bash
# Check detailed status
./gob status

# View recent logs
./gob logs 50

# Restart if needed
./gob restart
```

### Common Solutions
- **Port in use**: Another service using port 50080
- **Environment not found**: Run `./setup.sh` again
- **Permission denied**: Make sure `./gob` and `./setup.sh` are executable

## 📚 Documentation

- **[docs/](docs/)** - Complete documentation
- **[Setup Guide](docs/SETUP.md)** - Detailed manual setup
- **[Architecture](docs/DOCKER_ARCHITECTURE.md)** - System architecture
- **[Troubleshooting](docs/README.md)** - Common issues and solutions

## 🏗️ Development

```bash
# Activate environment
conda activate gobv1

# Make changes to code
# ...

# Restart to apply changes
./gob restart

# Follow logs
./gob follow
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
