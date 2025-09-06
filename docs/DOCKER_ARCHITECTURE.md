# GOB Docker Architecture Documentation

## 🏗️ **Docker Build Architecture**

GOB uses a **two-layer Docker build system** for efficiency and maintainability:

```
┌─────────────────────────────────────────────┐
│                GOB Application Layer        │
│           (DockerfileLocal or docker/run/)  │
├─────────────────────────────────────────────┤
│              GOB Base Layer                 │
│               (docker/base/)                │
├─────────────────────────────────────────────┤
│          Kali Linux Rolling Base            │
│           (kalilinux/kali-rolling)          │
└─────────────────────────────────────────────┘
```

## 📁 **Docker Files Reference**

### **🟢 ACTIVE FILES (Currently Used)**

| File | Purpose | Usage |
|------|---------|-------|
| `DockerfileLocal` | **Main application image** for local development | Used by `run-gob-docker.ps1` |
| `docker/base/Dockerfile` | **Base system image** with all dependencies | Referenced by `DockerfileLocal` |
| `docker/base/build.txt` | Build commands and examples for base image | Manual reference |
| `run-gob-docker.ps1` | **Primary container runner** (Windows) | Daily use script |
| `gob-status.ps1` | Container status checker | Management tool |
| `docker-cleanup.ps1` | Docker cleanup utility | Maintenance tool |
| `.dockerignore` | Files to exclude from Docker context | Build optimization |

### **🟡 PARTIALLY USED FILES**

| File | Purpose | Status |
|------|---------|--------|
| `docker/run/Dockerfile` | Production Dockerfile for git-based builds | **IMPORTANT** - Used for production builds |
| `docker/run/fs/` | Runtime configuration files | **IMPORTANT** - Contains essential runtime scripts |

### **🗑️ CLEANED UP (Removed)**

| File | Purpose | Status |
|------|---------|--------|
| ~~`docker/run/docker-compose.yml`~~ | Docker Compose configuration | **REMOVED** - Used old ports |
| ~~`docker/run/build.txt`~~ | Build commands for run image | **REMOVED** - Redundant |
| ~~`run-gob-docker.sh`~~ | Linux version of runner script | **REMOVED** - Not needed on Windows |

### **🔧 SUPPORT FILES**

| File | Purpose | 
|------|---------|
| `python/helpers/docker.py` | Python Docker helper functions |

## 🚀 **Current Active Workflow**

### **Daily Usage:**
```powershell
# Start GOB
.\run-gob-docker.ps1

# Check status  
.\gob-status.ps1

# View logs
docker logs -f g-o-b
```

### **Build Process (when needed):**
```powershell
# 1. Build base image (rarely needed)
cd docker\base
docker build -t gob-base:local .
cd ..\..

# 2. Build application image
docker build -t g-o-b:latest -f DockerfileLocal .

# 3. Run container
.\run-gob-docker.ps1
```

## 🎯 **Image Configuration**

### **Current Setup:**
- **Image**: `g-o-b:latest` 
- **Base**: `gob-base:local`
- **Ports**: 8080 (web), 2222 (SSH)
- **Volume**: Current directory mounted as `/gob`
- **Restart**: `unless-stopped` (auto-starts on boot)

### **Access Points:**
- **Web UI**: http://localhost:8080
- **SSH**: `ssh root@localhost -p 2222`
- **Container**: `docker exec -it g-o-b bash`

## 🔄 **Container Lifecycle**

```
Windows Boot → Docker Desktop → GOB Container Auto-Start
     ↓
  GOB Available at localhost:8080
     ↓
Code Changes → docker restart g-o-b (picks up changes via volume mount)
     ↓
New Features → Rebuild image → .\run-gob-docker.ps1
```

## 📝 **Build Arguments**

### **DockerfileLocal:**
- `BRANCH=local` (default)
- `CACHE_DATE` (for cache invalidation)

### **docker/base/Dockerfile:**
- `CACHE_DATE` (for cache invalidation)

## 🗂️ **File Cleanup Recommendations**

### **Files to Remove (Unused):**
- `docker/run/Dockerfile` ← Redundant with DockerfileLocal
- `docker/run/docker-compose.yml` ← Uses old port config
- `docker/run/build.txt` ← Redundant build commands
- `run-gob-docker.sh` ← Linux version not needed on Windows

### **Files to Keep:**
- All files marked as **🟢 ACTIVE** above
- `python/helpers/docker.py` ← May be used by application code

## 🎛️ **Management Commands**

| Command | Purpose |
|---------|---------|
| `.\run-gob-docker.ps1` | Start/restart GOB container |
| `.\gob-status.ps1` | Check container status |
| `.\docker-cleanup.ps1` | Clean up Docker resources |
| `docker logs g-o-b` | View container logs |
| `docker restart g-o-b` | Restart after code changes |
| `docker stop g-o-b` | Stop container |

---

**Last Updated**: 2025-09-05  
**Active Configuration**: Local development with auto-start  
**Primary Script**: `run-gob-docker.ps1`
