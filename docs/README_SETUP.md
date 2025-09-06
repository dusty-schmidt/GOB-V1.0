# GOB (General Orchestrator Bot) - Setup Documentation

## 🚀 **Quick Start**

### **On Windows:**
```powershell
# 1. Ensure Docker Desktop is running
# 2. Open PowerShell in project directory
cd C:\Users\JANET\dusty\g-o-b

# 3. Start GOB
.\run-gob-docker.ps1

# 4. Open browser to http://localhost:8080
```

### **Check Status:**
```powershell
.\gob-status.ps1
```

## 📚 **Documentation Index**

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** | 🖥️ Complete Windows setup guide | **Start here** for Windows users |
| **[DOCKER_ARCHITECTURE.md](DOCKER_ARCHITECTURE.md)** | 🏗️ Docker build system explanation | Understanding the build process |
| This README | 🎯 Quick reference and navigation | Finding the right documentation |

## 🎯 **Essential Information**

### **Access Points:**
- **Web UI**: http://localhost:8080
- **SSH**: `ssh root@localhost -p 2222`
- **Container Shell**: `docker exec -it g-o-b bash`

### **Key Scripts:**
- `.\run-gob-docker.ps1` - Start/restart GOB
- `.\gob-status.ps1` - Check container status  
- `.\docker-cleanup.ps1` - Clean up Docker resources

### **Auto-Start:**
✅ GOB automatically starts when Windows boots (via Docker Desktop)

## 🛠️ **Common Tasks**

### **Daily Development:**
```powershell
# Start working
.\gob-status.ps1          # Check if running
# If not running: .\run-gob-docker.ps1

# Make code changes in your editor
# Changes are live-mounted, restart to apply:
docker restart g-o-b

# View logs
docker logs -f g-o-b
```

### **Troubleshooting:**
```powershell
# Check Docker status
docker version

# Check container status
.\gob-status.ps1

# Clean up resources
.\docker-cleanup.ps1

# Full restart
docker stop g-o-b
.\run-gob-docker.ps1
```

## 🔧 **Configuration Files**

| File | Purpose |
|------|---------|
| `.env` | Environment variables and API keys |
| `DockerfileLocal` | Main Docker build configuration |
| `run-gob-docker.ps1` | Container startup script |

## 📂 **Project Structure**

```
g-o-b/
├── README_SETUP.md          # This file - setup navigation
├── WINDOWS_SETUP.md         # Complete Windows guide
├── DOCKER_ARCHITECTURE.md   # Docker build system docs
├── run-gob-docker.ps1       # Main startup script
├── gob-status.ps1           # Status checker
├── docker-cleanup.ps1       # Cleanup utility
├── DockerfileLocal          # Docker build file
├── .env                     # Configuration
└── docker/
    ├── base/                # Base image files
    └── run/                 # Runtime configuration
```

## 🆘 **Getting Help**

### **If Something's Not Working:**
1. 📖 **Read**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md) troubleshooting section
2. 🔍 **Check**: Run `.\gob-status.ps1` for current status
3. 📋 **Logs**: Run `docker logs g-o-b --tail 50` to see what happened
4. 🔄 **Restart**: Try `.\run-gob-docker.ps1` for a fresh start

### **Quick Diagnostics:**
```powershell
# Is Docker running?
docker version

# Is GOB container running?
docker ps

# Are the ports available?
netstat -ano | Select-String ":8080|:2222"

# What's in the logs?
docker logs g-o-b --tail 10
```

## 🎉 **You're All Set!**

If GOB is running and accessible at http://localhost:8080, you're ready to go!

For detailed setup, configuration, and troubleshooting, see **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)**.

---

**Version**: Custom GOB build  
**Platform**: Windows with Docker Desktop  
**Last Updated**: 2025-09-05
