# GOBV1 Complete Setup Guide

This guide provides detailed setup instructions for GOBV1 (General Orchestrator Bot V1.0).

## 🎯 Overview

GOBV1 is an advanced AI agent orchestration system. This guide covers both **automatic setup** (recommended) and **manual setup** for advanced users.

## 🚀 Option 1: Automatic Setup (Recommended)

The easiest way to get started:

### 1. Clone and Setup
```bash
git clone https://github.com/dusty-schmidt/GOB-V1.0.git
cd GOB-V1.0
./setup.sh
```

### 2. Start GOBV1
```bash
scripts/gob start
```

### 3. Access GOBV1
Open http://localhost:50080 in your browser.

**That's it!** The setup script handles everything automatically.

---

## 🔧 Option 2: Manual Setup

For advanced users who want more control:

### Prerequisites
- **OS**: Linux, macOS, or Windows with WSL2
- **RAM**: 8GB+ recommended  
- **Disk**: 2GB+ free space
- **Python**: 3.11+ via Miniconda/Anaconda

### Step 1: Install Miniconda (if needed)
```bash
# Download Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install
bash Miniconda3-latest-Linux-x86_64.sh

# Reload shell
source ~/.bashrc

# Install mamba (optional but faster)
conda install mamba -c conda-forge -y
```

### Step 2: Clone Repository
```bash
git clone https://github.com/dusty-schmidt/GOB-V1.0.git
cd GOB-V1.0
```

### Step 3: Create Environment
```bash
# Create conda environment
mamba create -n gob python=3.13 -y

# Activate environment
mamba activate gob

# Install core packages (faster via conda)
mamba install -c conda-forge \
  flask lxml markdown pytz psutil tiktoken \
  nltk beautifulsoup4 pillow faiss-cpu \
  pandas numpy matplotlib opencv scipy -y

# Install remaining packages via pip
pip install -r requirements.txt
```

### Step 4: Setup CLI Tool
```bash
# Make CLI executable
chmod +x gob

# Optional: Create system-wide link
sudo ln -sf $(pwdscripts/gob /usr/local/bin/gob
```

### Step 5: Start GOBV1
```bash
scripts/gob start
```

---

## 🎛️ Configuration

### Environment Variables
Create/edit `.env` file in project directory:

```bash
# Web Interface
WEB_UI_HOST=0.0.0.0
WEB_UI_PORT=50080

# Authentication (optional)
AUTH_LOGIN=your_username
AUTH_PASSWORD=your_password

# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
# Add other API keys as needed
```

### Port Configuration
- **Default Port**: 50080
- **Change Port**: Edit `WEB_UI_PORT` in `.env`
- **Check Port Usage**: `ss -tulpn | grep 50080`

---

## 🔧 CLI Commands

The `gob` command provides complete management:

| Command | Description | Example |
|---------|-------------|---------|
| `scripts/gob start` | Start GOBV1 server | `scripts/gob start` |
| `scripts/gob stop` | Stop GOBV1 server | `scripts/gob stop` |
| `scripts/gob restart` | Restart GOBV1 server | `scripts/gob restart` |
| `scripts/gob status` | Show server status | `scripts/gob status` |
| `scripts/gob logs [N]` | Show last N log lines | `scripts/gob logs 100` |
| `scripts/gob follow` | Follow logs in real-time | `scripts/gob follow` |
| `scripts/gob url` | Open GOBV1 in browser | `scripts/gob url` |
| `scripts/gob help` | Show help | `scripts/gob help` |

---

## 📁 Directory Structure

```
GOB-V1.0/
├── gob                     # CLI management tool
├── setup.sh               # Automatic setup script
├── agent.py               # Core agent system
├── models.py              # LLM configuration
├── run_ui.py              # Main server entry point
├── requirements.txt       # Python dependencies
├── .env                   # Configuration (create this)
├── agents/                # AI agent definitions
├── python/                # Framework core
├── webui/                 # Web interface
├── scripts/               # Utility scripts
├── docs/                  # Documentation
└── README.md              # Quick start guide
```

---

## 🚨 Troubleshooting

### Setup Issues

**Setup script fails:**
```bash
# Check if conda is installed
conda --version

# Run setup again
./setup.sh

# Check setup log for errors
```

**Environment not found:**
```bash
# List environments
conda env list

# Recreate environment
conda env remove -n gob
./setup.sh
```

### Runtime Issues

**GOBV1 won't start:**
```bash
# Check if port is in use
ss -tulpn | grep 50080

# Check environment is activated
conda activate gob

# Check detailed logs
scripts/gob logs 50

# Try restart
scripts/gob restart
```

**Web interface not accessible:**
```bash
# Check if server is running
scripts/gob status

# Test local connection
curl -I http://localhost:50080

# Check firewall settings
```

**Dependencies issues:**
```bash
# Reinstall dependencies
conda activate gob
pip install -r requirements.txt --force-reinstall

# Or recreate environment
./setup.sh
```

### Performance Issues

**High memory usage:**
- Ensure you have 8GB+ RAM
- Close other applications
- Check `scripts/gob logs` for memory warnings

**Slow startup:**
- First startup downloads models (normal)
- Subsequent starts should be faster
- Check `scripts/gob follow` for progress

---

## 🔄 Daily Development Workflow

### Starting Development Session
```bash
cd GOB-V1.0
scripts/gob start
scripts/gob url  # Opens browser
```

### Making Changes
1. Edit code in your IDE
2. Save changes
3. Restart: `scripts/gob restart`
4. Test: `scripts/gob logs`

### Environment Management
```bash
# Manual activation (if needed)
conda activate gob

# Update dependencies
pip install -r requirements.txt

# Check Python version
python --version
```

---

## 🔧 Advanced Configuration

### Custom Environment Location
```bash
# If you want environment elsewhere
export CONDA_ENV_PATH=/path/to/your/envs
./setup.sh
```

### Development Mode
```bash
# Run directly with Python
conda activate gob
python run_ui.py --host 0.0.0.0 --port 50080 --debug

# Or use environment variables
export WEB_UI_HOST=127.0.0.1
export WEB_UI_PORT=8080
scripts/gob start
```

### Resource Limits
```bash
# Limit memory usage (Linux)
export GOBV1_MAX_MEMORY=4G

# Set CPU cores
export GOBV1_CPU_CORES=4
```

---

## ✅ Verification Checklist

After setup, verify everything works:

```bash
# 1. Check CLI tool
scripts/gob help

# 2. Check environment
conda activate gob
python -c "import flask, numpy, pandas"

# 3. Start GOBV1
scripts/gob start

# 4. Check web response
curl -I http://localhost:50080

# 5. Check logs
scripts/gob logs 10

# 6. Stop GOBV1
scripts/gob stop
```

If all steps pass, your installation is working correctly!

---

## 🆘 Getting Additional Help

1. **Check logs**: `scripts/gob logs` for recent activity
2. **Check status**: `scripts/gob status` for server state
3. **Restart**: `scripts/gob restart` often fixes issues
4. **Re-setup**: `./setup.sh` recreates environment
5. **Documentation**: Browse `docs/` directory
6. **GitHub Issues**: [Report bugs](https://github.com/dusty-schmidt/GOB-V1.0/issues)

---

**Setup Complete!** 🎉 

Your GOBV1 installation should now be ready for use. Access it at http://localhost:50080 and start orchestrating AI agents!
