# Obsolete Startup Scripts

**Moved on**: 2025-09-06  
**Reason**: Replaced by native `gob` CLI management tool

## What Was Moved

These scripts were designed for Docker-based deployments and have been superseded by the native conda environment approach with the `gob` CLI tool.

### Root Directory Scripts:
- `start-gob.ps1` - Universal PowerShell starter (Windows/Linux detection)
- `status.ps1` - Universal PowerShell status checker

### Linux Scripts:
- `run-gob-docker.sh` - Docker container runner for Linux
- `gob-status.sh` - Docker status checker for Linux

### Windows Scripts Directory:
- `windows/` - Entire directory with Windows-specific Docker scripts
  - `run-gob-docker.ps1`
  - `gob-status.ps1` 
  - `docker-cleanup.ps1`
  - `maintenance.ps1`

## Replacement

All functionality is now handled by the native `gob` CLI:

```bash
# Old way (Docker-focused)
./start-gob.ps1
./status.ps1
./scripts/linux/run-gob-docker.sh

# New way (native)
gob start
gob status
gob restart
gob logs
gob stop
```

## Why Obsolete

1. **Docker Dependency**: Required Docker containers and complex setup
2. **Platform Complexity**: Needed separate scripts for Windows/Linux
3. **Limited Features**: No process management, crash recovery, or environment handling
4. **Maintenance Overhead**: Multiple script files to maintain

## Benefits of New CLI

- ✅ Native conda environment (no Docker needed for development)
- ✅ Unified command interface across platforms
- ✅ Process management with PID tracking
- ✅ Environment auto-activation
- ✅ Health monitoring and crash recovery
- ✅ Log management and real-time following

## If You Need These Scripts

These scripts are preserved here for reference. If you need Docker-based deployment for production, you can:

1. Copy the relevant scripts back to the root directory
2. Use the `DockerfileLocal` and `docker/` directory (still maintained)
3. Adapt the scripts to work with current directory structure

## Core Application Unchanged

The core GOB application (`run_ui.py`, `initialize.py`, etc.) remains fully functional and unchanged. The CLI is a wrapper that enhances the existing startup process.
