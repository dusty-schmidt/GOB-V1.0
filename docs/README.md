# GOBV1 Documentation

Welcome to the GOBV1 (General Orchestrator Bot V1.0) documentation. This directory contains comprehensive guides for setup, configuration, and development.

## 🎯 Quick Start

**New to GOBV1?** Start with the [Setup Guide](SETUP.md) for modern native installation.

**Need legacy Docker setup?** See platform-specific guides below.

## 📚 Documentation Index

### 🚀 Setup & Installation
| Document | Description | Target Users |
|----------|-------------|--------------|
| **[SETUP.md](SETUP.md)** | **Modern setup** - Native conda environment | **Recommended for all users** |
| [DEBIAN_SETUP.md](DEBIAN_SETUP.md) | Docker setup for Debian/Ubuntu systems | Legacy Docker users |

### 🏗️ Architecture & Configuration
| Document | Description |
|----------|-------------|
| [DOCKER_ARCHITECTURE.md](DOCKER_ARCHITECTURE.md) | Docker build system and container architecture |
| [AGENT_NAMING_SYSTEM.md](AGENT_NAMING_SYSTEM.md) | Dynamic agent identity system |
| [STARTUP_ANALYSIS.md](STARTUP_ANALYSIS.md) | System startup process analysis |

### 📝 Reference
| Document | Description |
|----------|-------------|
| [README_SETUP.md](README_SETUP.md) | Legacy setup navigation (archived) |

## 🎯 Which Guide Should I Use?

### For New Installations (Recommended):
- **Start with [SETUP.md](SETUP.md)** - Modern native setup using conda
- Easier to manage, better performance, direct file access
- Works on Linux, macOS, and WSL2

### For Docker Deployments:
- **Linux**: [DEBIAN_SETUP.md](DEBIAN_SETUP.md)
- **Docker Architecture**: [DOCKER_ARCHITECTURE.md](DOCKER_ARCHITECTURE.md)

### For Advanced Configuration:
- **Agent Naming**: [AGENT_NAMING_SYSTEM.md](AGENT_NAMING_SYSTEM.md)
- **System Analysis**: [STARTUP_ANALYSIS.md](STARTUP_ANALYSIS.md)

## 🔧 System Requirements

### Minimum Requirements:
- **Memory**: 8GB RAM
- **Storage**: 2GB free space
- **OS**: Linux, macOS, or Windows 10/11
- **Python**: 3.11+ (for native setup)

### Recommended:
- **Memory**: 16GB RAM
- **CPU**: 4+ cores
- **Storage**: 10GB free space (for Docker setups)

## 🚀 Access Points

Once GOBV1 is running:

- **Web Interface**: http://localhost:50080 (native) or http://localhost:8080 (Docker)
- **CLI Management**: Use the `gob` command (native setup)
- **Direct Access**: SSH or container exec (Docker setups)

## 🆘 Getting Help

1. **Check the relevant setup guide** for your installation method
2. **Review system logs**: `gob logs` (native) or `docker logs` (Docker)
3. **Verify system status**: `gob status` or relevant status commands
4. **Check GitHub Issues**: [Repository Issues](https://github.com/dusty-schmidt/GOB-V1.0/issues)

## 🔄 Migration Guide

**Migrating from Docker to Native Setup?**
1. Export your configurations and data
2. Follow the [SETUP.md](SETUP.md) guide for fresh installation
3. Import your configurations
4. Archive old Docker containers

**Migrating from Legacy Agent Zero?**
1. Review the [AGENT_NAMING_SYSTEM.md](AGENT_NAMING_SYSTEM.md) for new features
2. Follow [SETUP.md](SETUP.md) for installation
3. Configure your existing agent definitions

---

**Repository**: [GOB-V1.0](https://github.com/dusty-schmidt/GOB-V1.0)  
**Last Updated**: 2025-09-06  
**Documentation Version**: 1.0
