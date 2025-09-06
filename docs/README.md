# GOBV1 Documentation

Welcome to GOBV1 (General Orchestrator Bot V1.0) documentation.

## 🚀 Getting Started

**New to GOBV1?** 
- **Quick Start**: Follow the main [README.md](../README.md)
- **Detailed Setup**: See [SETUP.md](SETUP.md) for complete instructions

**Already have GOBV1?**
- **Daily Usage**: `./gob help` for all commands
- **Web Interface**: http://localhost:50080

## 📚 Documentation

### Setup & Installation
| Document | Description | When to Use |
|----------|-------------|-------------|
| **[../README.md](../README.md)** | **Quick start guide** | **First time users** |
| **[SETUP.md](SETUP.md)** | **Complete setup guide** | **Detailed installation** |

### Architecture & System
| Document | Description |
|----------|-------------|
| [AGENT_NAMING_SYSTEM.md](AGENT_NAMING_SYSTEM.md) | Dynamic agent identity system |
| [STARTUP_ANALYSIS.md](STARTUP_ANALYSIS.md) | System startup process |

### Reference
| Document | Description |
|----------|-------------|
| [README_SETUP.md](README_SETUP.md) | Legacy setup guide (archived) |

## 🎯 Which Guide Do I Need?

### 🆕 **First Time Setup**
1. **Start**: [Main README](../README.md) ← **Start here**
2. **Run**: `./setup.sh` (automatic)
3. **Go**: `./gob start`

### 🔧 **Advanced Setup**  
1. **Read**: [SETUP.md](SETUP.md) ← Manual installation
2. **Configure**: Custom environment, ports, etc.
3. **Deploy**: Production configurations

## ⚡ Quick Commands

```bash
# Setup (one time)
./setup.sh

# Daily usage
./gob start      # Start GOBV1
./gob status     # Check status
./gob logs       # View logs
./gob stop       # Stop GOBV1
./gob help       # All commands

# Troubleshooting
./gob restart    # Restart if issues
./setup.sh       # Re-run setup
```

## 🔧 System Requirements

### Minimum
- **OS**: Linux or macOS (Windows with WSL2)  
- **RAM**: 8GB
- **Disk**: 2GB free space
- **Network**: Internet connection for setup

### Recommended  
- **RAM**: 16GB
- **CPU**: 4+ cores
- **Disk**: 5GB free space

## 📍 Access Points

Once running:
- **Web UI**: http://localhost:50080
- **CLI**: `./gob` commands
- **Logs**: `./gob logs` or `./gob follow`

## 🚨 Common Issues & Solutions

### Setup Problems
```bash
# Setup failed
./setup.sh                    # Try again

# Conda not found  
curl -O miniconda.sh          # Install Miniconda
bash miniconda.sh
source ~/.bashrc
```

### Runtime Problems
```bash
# Won't start
./gob status                  # Check what's wrong
./gob logs 50                 # Check error logs
./gob restart                 # Try restart

# Port busy
ss -tulpn | grep 50080        # Check what's using port
```

### Environment Problems
```bash
# Environment missing
conda env list                # List environments
./setup.sh                    # Recreate environment

# Dependencies broken
conda activate gobv1
pip install -r requirements.txt --force-reinstall
```

## 🆘 Getting Help

1. **Check status**: `./gob status`
2. **Check logs**: `./gob logs 50` 
3. **Restart**: `./gob restart`
4. **Re-setup**: `./setup.sh`
5. **Documentation**: Browse this `docs/` directory
6. **GitHub Issues**: [Report problems](https://github.com/dusty-schmidt/GOB-V1.0/issues)

## 🔗 External Links

- **Repository**: https://github.com/dusty-schmidt/GOB-V1.0
- **Issues**: https://github.com/dusty-schmidt/GOB-V1.0/issues
- **Web UI**: http://localhost:50080 (when running)

---

**Ready to start?** Go to [../README.md](../README.md) and follow the Quick Start! 🚀
