#!/bin/bash

# GOB Monitoring Service Control Script
SERVICE_NAME="gob-monitoring"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}🔍 Checking service status...${NC}"
    sudo systemctl status $SERVICE_NAME --no-pager -l
}

print_logs() {
    echo -e "${BLUE}📋 Recent logs:${NC}"
    sudo journalctl -u $SERVICE_NAME -n 20 --no-pager
}

case "$1" in
    start)
        echo -e "${GREEN}🚀 Starting GOB Monitoring Service...${NC}"
        sudo systemctl start $SERVICE_NAME
        sleep 2
        print_status
        ;;
    stop)
        echo -e "${RED}⏹️  Stopping GOB Monitoring Service...${NC}"
        sudo systemctl stop $SERVICE_NAME
        sleep 2
        print_status
        ;;
    restart)
        echo -e "${YELLOW}🔄 Restarting GOB Monitoring Service...${NC}"
        sudo systemctl restart $SERVICE_NAME
        sleep 3
        print_status
        ;;
    status)
        print_status
        ;;
    logs)
        print_logs
        ;;
    follow|tail)
        echo -e "${BLUE}📋 Following live logs (Press Ctrl+C to exit):${NC}"
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    enable)
        echo -e "${GREEN}✅ Enabling auto-start on boot...${NC}"
        sudo systemctl enable $SERVICE_NAME
        print_status
        ;;
    disable)
        echo -e "${YELLOW}❌ Disabling auto-start on boot...${NC}"
        sudo systemctl disable $SERVICE_NAME
        print_status
        ;;
    install)
        echo -e "${GREEN}🔧 Installing/Reinstalling service...${NC}"
        ./install_service.sh
        ;;
    uninstall)
        echo -e "${RED}🗑️  Uninstalling service...${NC}"
        sudo systemctl stop $SERVICE_NAME
        sudo systemctl disable $SERVICE_NAME
        sudo rm -f /etc/systemd/system/$SERVICE_NAME.service
        sudo systemctl daemon-reload
        echo -e "${GREEN}✅ Service uninstalled${NC}"
        ;;
    *)
        echo "GOB Monitoring Service Control"
        echo "Usage: $0 {command}"
        echo ""
        echo "Commands:"
        echo "  start      Start the monitoring service"
        echo "  stop       Stop the monitoring service"
        echo "  restart    Restart the monitoring service"
        echo "  status     Show service status"
        echo "  logs       Show recent logs"
        echo "  follow     Follow live logs"
        echo "  enable     Enable auto-start on boot"
        echo "  disable    Disable auto-start on boot"
        echo "  install    Install/reinstall the service"
        echo "  uninstall  Remove the service completely"
        echo ""
        echo "Examples:"
        echo "  $0 status     # Check if running"
        echo "  $0 restart    # Restart the service"
        echo "  $0 follow     # Watch live logs"
        echo ""
        echo "🌐 Dashboard: http://localhost:8050"
        exit 1
        ;;
esac
