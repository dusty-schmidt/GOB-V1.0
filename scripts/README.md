# GOB Scripts Directory

Cross-platform management scripts for GOB container operations.

## 🚀 Quick Start

From project root, use the universal scripts:

```powershell
# Start GOB (auto-detects platform)
.\start-gob.ps1

# Check status (auto-detects platform)  
.\status.ps1
```

## 📁 Directory Structure

```
scripts/
├── windows/                    # Windows PowerShell scripts
│   ├── run-gob-docker.ps1     # Start/restart GOB (Windows)
│   ├── gob-status.ps1         # Container status checker
│   ├── docker-cleanup.ps1     # Docker resource cleanup
│   └── maintenance.ps1        # General maintenance tasks
├── linux/                     # Linux/macOS bash scripts  
│   ├── run-gob-docker.sh      # Start/restart GOB (Linux)
│   └── gob-status.sh          # Container status checker
└── README.md                  # This file
```

## 🖥️ Platform-Specific Usage

### Windows:
```powershell
# Direct script usage
.\scripts\windows\run-gob-docker.ps1
.\scripts\windows\gob-status.ps1
.\scripts\windows\docker-cleanup.ps1
```

### Linux/macOS:
```bash
# Make executable first time
chmod +x scripts/linux/*.sh

# Direct script usage
./scripts/linux/run-gob-docker.sh
./scripts/linux/gob-status.sh
```

## 🎯 Configuration Differences

| Platform | Web Port | SSH Port | Container Name | Volume Mount |
|----------|----------|----------|----------------|--------------|
| **Windows** | 8080 | 2222 | `g-o-b` | `$(pwd):/gob` |
| **Linux** | 50080 | 50022 | `g-o-b` | `$(pwd):/gob` |

## 🔄 Cross-Platform Workflow

1. **Development**: Edit code on host OS
2. **Container restart**: `docker restart g-o-b`
3. **Test**: Access web UI at platform-specific port
4. **Status check**: Use universal `.\status.ps1`
5. **Commit**: Standard git workflow

---

**Note**: Universal scripts in project root auto-detect platform and call appropriate platform-specific scripts.
