#!/bin/bash
# GOB Service Installation Script

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}GOB Service Installer${NC}"
echo "======================"

# Check if running as root or with sudo
if [[ $EUID -eq 0 ]]; then
   SUDO=""
else
   SUDO="sudo"
   echo -e "${YELLOW}This script requires sudo privileges${NC}"
fi

# Service file paths
SERVICE_FILE="/home/ds/GOB/gob.service"
SYSTEMD_PATH="/etc/systemd/system/gob.service"

case "$1" in
    install)
        echo "Installing GOB service..."
        
        # Copy service file
        $SUDO cp "$SERVICE_FILE" "$SYSTEMD_PATH"
        
        # Reload systemd
        $SUDO systemctl daemon-reload
        
        # Enable service
        $SUDO systemctl enable gob.service
        
        echo -e "${GREEN}Service installed and enabled!${NC}"
        echo "Use 'systemctl start gob' to start the service"
        ;;
        
    uninstall)
        echo "Uninstalling GOB service..."
        
        # Stop service if running
        $SUDO systemctl stop gob.service 2>/dev/null || true
        
        # Disable service
        $SUDO systemctl disable gob.service 2>/dev/null || true
        
        # Remove service file
        $SUDO rm -f "$SYSTEMD_PATH"
        
        # Reload systemd
        $SUDO systemctl daemon-reload
        
        echo -e "${GREEN}Service uninstalled!${NC}"
        ;;
        
    start)
        echo "Starting GOB service..."
        $SUDO systemctl start gob.service
        echo -e "${GREEN}Service started!${NC}"
        ;;
        
    stop)
        echo "Stopping GOB service..."
        $SUDO systemctl stop gob.service
        echo -e "${GREEN}Service stopped!${NC}"
        ;;
        
    restart)
        echo "Restarting GOB service..."
        $SUDO systemctl restart gob.service
        echo -e "${GREEN}Service restarted!${NC}"
        ;;
        
    status)
        $SUDO systemctl status gob.service
        ;;
        
    logs)
        echo "=== Recent logs ==="
        $SUDO journalctl -u gob.service -n 50 --no-pager
        ;;
        
    *)
        echo "Usage: $0 {install|uninstall|start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  install    - Install and enable the systemd service"
        echo "  uninstall  - Remove the systemd service"
        echo "  start      - Start the service"
        echo "  stop       - Stop the service"
        echo "  restart    - Restart the service"
        echo "  status     - Show service status"
        echo "  logs       - Show recent service logs"
        exit 1
        ;;
esac
