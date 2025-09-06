# GOB Setup Guide

**Updated**: 2025-09-06  
**Approach**: Native conda environment with CLI management

## 🎯 Overview

GOB (General Orchestrator Bot) is a customized fork of Agent Zero focused on orchestration and task management. This guide covers the modern native setup using conda environments and the `gob` CLI manager.

## 📋 Prerequisites

- **Operating System**: Linux (Debian/Ubuntu tested) or macOS
- **Python**: 3.11+ via Miniconda or Anaconda
- **Memory**: 8GB+ RAM recommended
- **Storage**: 2GB+ free space for dependencies

## 🚀 Quick Start

### 1. Install Miniconda (if not already installed)

```bash
# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# Reload your shell
source ~/.bashrc
```

### 2. Install Mamba (faster package manager)

```bash
conda install mamba -c conda-forge -y
```

### 3. Clone GOB Repository

```bash
# Clone the repository
git clone https://github.com/dusty-schmidt/g-o-b.git /home/ds/GOB/gob
cd /home/ds/GOB/gob
```

### 4. Create and Setup Environment

```bash
# Create conda environment with Python 3.11
mamba create -n gob python=3.11 -y

# Activate the environment
eval "$(mamba shell hook --shell bash)"
mamba activate gob

# Install core dependencies via mamba (faster)
mamba install -c conda-forge flask docker-py lxml markdown pytz psutil \
  tiktoken nltk beautifulsoup4 pillow faiss-cpu pandas numpy -y

# Install AI/ML packages
mamba install -c conda-forge matplotlib opencv-python scipy -y

# Install remaining packages via pip
pip install -r requirements.txt
```

### 5. Install GOB CLI Manager

The GOB CLI tool should already be in the repository. Make it available system-wide:

```bash
# Make the CLI executable
chmod +x gob

# Create system-wide symlink (requires sudo)
sudo ln -sf $(pwd)/gob /usr/local/bin/gob
```

### 6. Start GOB

```bash
# Start GOB server
gob start

# Check status
gob status

# View logs if needed
gob logs
```

### 7. Access GOB

Open your browser and navigate to: **http://localhost:50080**

## 🔧 CLI Commands

The `gob` command provides complete management of your GOB instance:

| Command | Description | Example |
|---------|-------------|---------|
| `gob start` | Start the GOB server | `gob start` |
| `gob stop` | Stop the GOB server | `gob stop` |
| `gob restart` | Restart the GOB server | `gob restart` |
| `gob status` | Show detailed server status | `gob status` |
| `gob logs [lines]` | Show recent log entries | `gob logs 100` |
| `gob follow` | Follow logs in real-time | `gob follow` |
| `gob url` | Open GOB in browser | `gob url` |
| `gob help` | Show help information | `gob help` |

## 📁 Directory Structure

```
/home/ds/GOB/gob/                    # Main GOB directory
├── docs/                            # Documentation
├── python/                          # Core Python application
├── webui/                           # Web interface files
├── agents/                          # AI agent definitions
├── scripts/                         # Utility scripts
├── docker/                          # Docker configs (for production)
├── gob                             # CLI management script
├── run_ui.py                       # Core Flask application
├── requirements.txt                # Python dependencies
└── README.md                       # Project overview
```

## 🔧 Configuration

### Environment Variables

Create or edit `.env` file in the GOB directory:

```bash
# Web UI Configuration
WEB_UI_HOST=0.0.0.0
WEB_UI_PORT=50080

# Authentication (optional)
AUTH_LOGIN=your_username
AUTH_PASSWORD=your_password

# API Keys (add your keys here)
OPENAI_API_KEY=your_openai_key
# ... other API keys
```

### Port Configuration

- **Default HTTP Port**: 50080
- **SSH Port** (if using Docker): 50022
- **Change ports**: Edit `WEB_UI_PORT` in `.env` or use `--port` argument

## 🚨 Troubleshooting

### GOB Won't Start

```bash
# Check conda environment
mamba env list | grep gob

# Check if port is in use
ss -tulpn | grep 50080

# Check detailed logs
gob logs 50

# Try restarting
gob restart
```

### Dependencies Issues

```bash
# Reinstall dependencies in conda environment
mamba activate gob
pip install -r requirements.txt --force-reinstall
```

### Permission Issues

```bash
# Make sure CLI script is executable
chmod +x gob

# Check symlink
ls -la /usr/local/bin/gob
```

### Process Management

```bash
# If GOB process becomes unresponsive
pkill -f "python run_ui.py"
gob start

# Check for zombie processes
ps aux | grep python | grep run_ui
```

## 🔄 Daily Usage

### Starting a Development Session

```bash
# Navigate to GOB directory
cd /home/ds/GOB/gob

# Start GOB
gob start

# Open in browser
gob url
# OR manually: http://localhost:50080
```

### Making Changes

1. Edit files in the GOB directory
2. Changes to Python files require a restart: `gob restart`
3. Web UI changes may not require restart
4. Monitor logs: `gob follow`

### Stopping Development

```bash
# Stop GOB server
gob stop
```

## 🌐 Production Deployment

For production deployments, you can still use Docker:

```bash
# Build Docker image
docker build -t gob-prod -f DockerfileLocal .

# Run production container
docker run -d --name gob-prod -p 80:80 gob-prod
```

See `docs/DOCKER_ARCHITECTURE.md` for detailed Docker deployment information.

## 📚 Additional Documentation

- **Project Architecture**: See individual files in `docs/`
- **API Documentation**: Available at http://localhost:50080/docs (when running)
- **Agent Development**: See `agents/` directory
- **Troubleshooting**: This document + `gob logs`

## 🔄 Migration from Docker Setup

If you're migrating from the old Docker-based setup:

1. **Stop old containers**: `docker stop g-o-b g-o-b-dev`
2. **Follow this setup guide** from step 1
3. **Your data is preserved** in the GOB directory
4. **Old scripts are archived** in `.vault/obsolete-scripts/`

## 🆘 Getting Help

1. **Check logs**: `gob logs` or `gob follow`
2. **Check status**: `gob status` 
3. **Restart if needed**: `gob restart`
4. **Review this documentation**
5. **Check the repository issues**: GitHub issues page

---

## ✅ Quick Verification

After setup, verify everything works:

```bash
# 1. Check GOB status
gob status

# 2. Verify HTTP response
curl -I http://localhost:50080

# 3. Check recent logs
gob logs 10

# 4. Open in browser
gob url
```

You should see:
- ✅ GOB status showing "running"
- ✅ HTTP 200 OK response
- ✅ Clean startup logs
- ✅ GOB web interface in browser

---

**Setup complete!** 🎉 Your GOB instance is ready for development and use.
