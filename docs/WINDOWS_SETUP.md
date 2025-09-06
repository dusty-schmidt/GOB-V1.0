# GOB on Windows - Complete Setup Guide

## 🖥️ **Windows Prerequisites**

### **Required Software:**
- ✅ **Windows 10/11** (Home, Pro, or Enterprise)
- ✅ **Docker Desktop for Windows** (with WSL2 backend)
- ✅ **PowerShell 7.5+** (Core PowerShell, not Windows PowerShell 5.1)
- ✅ **Git for Windows** (for repository management)

### **Optional but Recommended:**
- 🔧 **Windows Terminal** (better PowerShell experience)
- 🌐 **Modern browser** (Chrome, Firefox, Edge)

## 🔧 **Initial Windows Setup**

### **1. Install Docker Desktop**
1. Download from [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install with **WSL2 backend** (default)
3. Ensure Docker Desktop starts on Windows boot
4. Verify: Open PowerShell and run `docker version`

### **2. Install PowerShell 7**
```powershell
# Option 1: Using winget (Windows 11)
winget install Microsoft.PowerShell

# Option 2: Download from GitHub releases
# https://github.com/PowerShell/PowerShell/releases
```

### **3. Clone GOB Repository**
```powershell
# Navigate to your development folder
cd C:\Users\$env:USERNAME\
mkdir dusty  # or your preferred dev folder
cd dusty

# Clone the repository
git clone https://github.com/dusty-schmidt/g-o-b.git
cd g-o-b
```

## 🚀 **Windows-Specific Launch Process**

### **First-Time Setup:**
1. **Ensure Docker Desktop is running** (check system tray)
2. **Open PowerShell 7** (not Windows PowerShell 5.1)
3. **Navigate to project directory:**
   ```powershell
   cd C:\Users\JANET\dusty\g-o-b
   ```
4. **Launch GOB:**
   ```powershell
   .\run-gob-docker.ps1
   ```

### **Daily Usage:**
```powershell
# Quick start (if already set up)
cd C:\Users\JANET\dusty\g-o-b
.\run-gob-docker.ps1

# Check status
.\gob-status.ps1

# View logs
docker logs -f g-o-b
```

## 🏃‍♂️ **Windows Boot Sequence**

### **What Happens When Windows Starts:**
1. **Windows boots** → **User logs in**
2. **Docker Desktop auto-starts** (if configured)
3. **GOB container auto-starts** (restart policy: `unless-stopped`)
4. **GOB is available** at http://localhost:8080

### **Configure Auto-Start:**
```powershell
# Docker Desktop should already be set to start on boot
# To verify/enable:
# 1. Right-click Docker Desktop icon in system tray
# 2. Settings → General → "Start Docker Desktop when you sign in to your computer"
```

## 🌐 **Windows Network & Firewall**

### **Port Configuration:**
- **Web UI**: `localhost:8080` (HTTP)
- **SSH Access**: `localhost:2222` (SSH)
- **Internal Services**: Handled automatically by Docker

### **Windows Firewall:**
Docker Desktop automatically handles firewall rules for `localhost` access. No manual configuration needed.

### **Network Troubleshooting:**
```powershell
# Check if ports are in use
netstat -ano | Select-String ":8080|:2222"

# Test web interface
curl -I http://localhost:8080

# Check Docker networking
docker network ls
```

## 📂 **Windows File System Integration**

### **Volume Mounting:**
- **Host Path**: `C:\Users\JANET\dusty\g-o-b`
- **Container Path**: `/gob`
- **Type**: Bind mount (live sync)

### **File Editing Workflow:**
1. **Edit files** on Windows using any editor (VS Code, Notepad++, etc.)
2. **Changes are immediately** reflected in the running container
3. **Restart container** to pick up changes: `docker restart g-o-b`

### **Windows Path Considerations:**
```powershell
# PowerShell automatically handles path conversion
# These are equivalent:
-v "$(Get-Location):/gob"           # PowerShell style
-v "${PWD}:/gob"                    # Alternative
-v "C:\Users\JANET\dusty\g-o-b:/gob" # Explicit path
```

## 🛠️ **Windows Management Scripts**

### **Primary Scripts:**
| Script | Purpose | When to Use |
|--------|---------|-------------|
| `.\run-gob-docker.ps1` | **Start/restart GOB** | Daily startup, after changes |
| `.\gob-status.ps1` | **Check status & get info** | Troubleshooting, quick check |
| `.\docker-cleanup.ps1` | **Clean up Docker resources** | Maintenance, disk space |

### **Usage Examples:**
```powershell
# Start GOB and open browser
.\run-gob-docker.ps1
# When prompted: y [to open browser]

# Quick status check
.\gob-status.ps1

# Cleanup old images/containers
.\docker-cleanup.ps1
# Choose option 1-5 based on what you want to clean
```

## 🔒 **Windows Security Considerations**

### **User Account Control (UAC):**
- Docker Desktop handles elevated permissions automatically
- PowerShell scripts run with normal user privileges
- No need to run as Administrator

### **Windows Defender:**
- Docker containers are isolated and safe
- Windows Defender may scan container files (normal)
- No special exclusions needed

### **SSH Access:**
```powershell
# SSH into GOB container from Windows
ssh root@localhost -p 2222

# Or use Docker exec (no SSH required)
docker exec -it g-o-b bash
```

## 📊 **Performance on Windows**

### **Resource Usage:**
- **RAM**: ~4-8GB (depends on Docker Desktop settings)
- **CPU**: 2-4 cores recommended
- **Disk**: ~10GB for images + container data
- **Network**: Localhost only (no external exposure)

### **Optimization Tips:**
```powershell
# Check Docker resource usage
docker system df

# Monitor container resources
docker stats g-o-b

# Adjust Docker Desktop settings:
# Settings → Resources → Advanced
# - Memory: 6GB (recommended)
# - CPUs: 4 (or half your cores)
```

## 🚨 **Windows Troubleshooting**

### **Common Issues:**

#### **Docker Desktop Not Starting:**
```powershell
# Check if Docker service is running
Get-Service -Name "*docker*"

# Restart Docker Desktop
# Right-click system tray icon → Restart Docker Desktop
```

#### **Port Conflicts:**
```powershell
# Find what's using port 8080
netstat -ano | Select-String ":8080"

# Alternative: use different ports
# Edit run-gob-docker.ps1 to change port mappings
```

#### **PowerShell Execution Policy:**
```powershell
# If scripts won't run, check execution policy
Get-ExecutionPolicy

# Set to allow local scripts (if needed)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

#### **Volume Mount Issues:**
```powershell
# Ensure Docker Desktop has access to C: drive
# Settings → Resources → File Sharing
# Add C:\ if not present
```

### **Log Analysis:**
```powershell
# Container logs
docker logs g-o-b --tail 50

# Docker Desktop logs
# Settings → Troubleshoot → Show logs
```

## 🔄 **Windows Update Process**

### **Code Changes:**
1. **Edit files** in your favorite Windows editor
2. **Restart container**: `docker restart g-o-b`
3. **Test changes** at http://localhost:8080

### **Image Rebuilds:**
```powershell
# When you need to rebuild the image
docker build -t g-o-b:latest -f DockerfileLocal .
.\run-gob-docker.ps1
```

### **System Updates:**
```powershell
# After Windows updates or Docker updates
.\gob-status.ps1  # Check if still running
# If not running:
.\run-gob-docker.ps1
```

## 📱 **Windows Integration Features**

### **Browser Integration:**
- GOB automatically opens in default browser when launched
- Bookmarkable: http://localhost:8080
- Works with any modern browser

### **File Explorer Integration:**
- Right-click in project folder → "Open in Terminal"
- Or use `cd` commands in PowerShell

### **Notifications:**
- Docker Desktop shows notifications in Action Center
- Container status visible in Docker Desktop Dashboard

## 🎯 **Quick Reference Card**

### **Essential Commands:**
```powershell
# Start GOB
.\run-gob-docker.ps1

# Status check  
.\gob-status.ps1

# View logs
docker logs g-o-b

# SSH into container
docker exec -it g-o-b bash

# Stop GOB
docker stop g-o-b

# Restart after changes
docker restart g-o-b

# Clean up resources
.\docker-cleanup.ps1
```

### **Key URLs:**
- **GOB Web UI**: http://localhost:8080
- **Docker Desktop**: http://localhost (when running)

### **Key Paths:**
- **Project**: `C:\Users\JANET\dusty\g-o-b\`
- **Scripts**: All `.ps1` files in project root
- **Config**: `.env` file in project root

---

**Last Updated**: 2025-09-05  
**Windows Version**: 10/11  
**PowerShell**: 7.5+  
**Docker Desktop**: Latest stable  
