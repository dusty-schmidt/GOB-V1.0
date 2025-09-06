# GOB Auto-start Setup

## Overview
GOB has been configured to automatically start on boot and launch Firefox once it's ready. This setup includes health checking and robust error handling.

## Files Created

### Scripts
- `scripts/gob-autostart.sh` - Main auto-start script with health checking and Firefox launch
- `scripts/gob-autostart-manager.sh` - Management utility for controlling autostart behavior

### System Integration
- `/etc/systemd/system/gob-autostart.service` - Systemd service for boot startup
- `~/.config/autostart/gob-autostart.desktop` - Desktop session autostart entry

### Logs
- `autostart.log` - Auto-start script execution logs

## Current Configuration

### ✅ System Boot Startup: ENABLED
- GOB will start automatically when the system boots
- Runs as systemd service `gob-autostart.service`
- Starts after network is available

### ✅ Desktop Session Startup: ENABLED  
- GOB will start when you log into your desktop session
- Uses desktop autostart mechanism
- Provides redundancy for desktop/laptop usage

## Management Commands

### Check Status
```bash
./scripts/gob-autostart-manager.sh status
```

### Enable/Disable Boot Startup
```bash
./scripts/gob-autostart-manager.sh enable-boot
./scripts/gob-autostart-manager.sh disable-boot
```

### Enable/Disable Desktop Startup
```bash
./scripts/gob-autostart-manager.sh enable-desktop
./scripts/gob-autostart-manager.sh disable-desktop
```

### Test Startup Script
```bash
./scripts/gob-autostart-manager.sh test
```

## How It Works

1. **Auto-start Script** (`gob-autostart.sh`):
   - Starts GOB using the management CLI
   - Polls http://localhost:50080 every 5 seconds
   - Waits up to 120 seconds for HTTP 200 response
   - Launches Firefox once GOB is ready
   - Logs all activity to `autostart.log`

2. **Health Checking**:
   - Uses curl to check if GOB responds with HTTP 200
   - Handles startup delays gracefully
   - Provides detailed logging for troubleshooting

3. **Firefox Launch**:
   - Automatically detects Firefox installation
   - Tries multiple Firefox variants (firefox, firefox-esr)
   - Opens directly to http://localhost:50080

## Systemd Service Details

The systemd service:
- Runs as user 'ds' with proper permissions
- Sets correct conda environment variables
- Handles automatic restarts on failure
- Starts after network connectivity is established
- Includes display environment for Firefox GUI access

## Troubleshooting

### Check Service Status
```bash
sudo systemctl status gob-autostart.service
```

### View Service Logs
```bash
sudo journalctl -u gob-autostart.service -f
```

### View Auto-start Logs
```bash
tail -f autostart.log
```

### Manual Start Test
```bash
./scripts/gob-autostart.sh
```

## Customization

### Modify Startup Behavior
Edit `scripts/gob-autostart.sh` to:
- Change health check timeout (MAX_WAIT_TIME)
- Modify health check interval (HEALTH_CHECK_INTERVAL)
- Add additional startup actions
- Customize Firefox launch behavior

### Disable Auto-start
```bash
# Disable boot startup
./scripts/gob-autostart-manager.sh disable-boot

# Disable desktop startup  
./scripts/gob-autostart-manager.sh disable-desktop
```

## Recommendations

- **For Servers/Headless Systems**: Use boot startup only
- **For Desktop/Laptop Systems**: Desktop startup is usually preferred
- **For Development**: Both can be enabled for maximum reliability

The current configuration has both enabled for maximum coverage.
