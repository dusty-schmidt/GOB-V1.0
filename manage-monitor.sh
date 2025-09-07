#!/bin/bash

# GOB Network Monitor Management Script
# Simple management for the monitoring dashboard

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

show_help() {
    echo -e "${BLUE}GOB Network Monitor Management${NC}"
    echo
    echo -e "${YELLOW}Usage:${NC} $(basename "$0") [COMMAND]"
    echo
    echo -e "${YELLOW}Commands:${NC}"
    echo "  status      Show monitor service status"
    echo "  start       Start monitor service"
    echo "  stop        Stop monitor service"
    echo "  restart     Restart monitor service"
    echo "  logs        Show recent logs"
    echo "  follow      Follow live logs"
    echo "  dashboard   Show dashboard URL"
    echo "  uninstall   Remove monitor service"
    echo "  help        Show this help"
}

show_status() {
    echo -e "${BLUE}=== GOB Network Monitor Status ===${NC}"
    echo
    
    if systemctl is-active gob-monitor >/dev/null 2>&1; then
        echo -e "  ${GREEN}●${NC} gob-monitor: ${GREEN}running${NC}"
        
        # Show detailed status
        echo
        sudo systemctl status gob-monitor --no-pager -l | grep -E "(●|Active:|Main PID:|Memory:|CPU:)" || true
        
        # Check dashboard accessibility
        echo
        if curl -s http://localhost:8050 >/dev/null 2>&1; then
            echo -e "  ${GREEN}🌐${NC} Dashboard: ${GREEN}accessible at http://localhost:8050${NC}"
        else
            echo -e "  ${YELLOW}🌐${NC} Dashboard: ${YELLOW}starting up...${NC}"
        fi
    elif systemctl is-enabled gob-monitor >/dev/null 2>&1; then
        echo -e "  ${GRAY}●${NC} gob-monitor: ${GRAY}stopped${NC}"
    else
        echo -e "  ${RED}●${NC} gob-monitor: ${RED}not installed${NC}"
    fi
    echo
}

show_dashboard() {
    echo -e "${BLUE}=== Dashboard Information ===${NC}"
    echo
    
    if systemctl is-active gob-monitor >/dev/null 2>&1; then
        if curl -s http://localhost:8050 >/dev/null 2>&1; then
            echo -e "  ${GREEN}✅${NC} Dashboard URL: ${BLUE}http://localhost:8050${NC}"
            echo -e "  ${GREEN}✅${NC} Status: Online and accessible"
            echo -e "  ${GREEN}✅${NC} Style: Terminal hacker aesthetic"
            echo -e "  ${GREEN}✅${NC} Updates: Real-time (every 2 seconds)"
        else
            echo -e "  ${YELLOW}⚠️${NC} Dashboard: Starting up..."
            echo -e "  ${YELLOW}⚠️${NC} URL: http://localhost:8050 (may not be ready yet)"
        fi
    else
        echo -e "  ${RED}❌${NC} Monitor service is not running"
        echo -e "  ${RED}❌${NC} Start the service first: $(basename "$0") start"
    fi
    echo
}

start_service() {
    echo -e "${BLUE}=== Starting GOB Network Monitor ===${NC}"
    echo
    
    if systemctl is-active gob-monitor >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Monitor service is already running${NC}"
        return 0
    fi
    
    echo -e "🚀 Starting gob-monitor..."
    sudo systemctl start gob-monitor
    
    # Wait a moment
    sleep 3
    
    if systemctl is-active gob-monitor >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Monitor service started${NC}"
        
        # Wait for dashboard to be ready
        echo -e "⏳ Waiting for dashboard to be ready..."
        for i in {1..10}; do
            if curl -s http://localhost:8050 >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Dashboard is accessible at http://localhost:8050${NC}"
                break
            fi
            sleep 2
        done
        
        if ! curl -s http://localhost:8050 >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Service started but dashboard may still be starting up${NC}"
        fi
    else
        echo -e "${RED}❌ Failed to start monitor service${NC}"
        echo
        echo -e "${YELLOW}Recent logs:${NC}"
        sudo journalctl -u gob-monitor -n 5 --no-pager || true
    fi
}

stop_service() {
    echo -e "${BLUE}=== Stopping GOB Network Monitor ===${NC}"
    echo
    
    if ! systemctl is-active gob-monitor >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Monitor service is not running${NC}"
        return 0
    fi
    
    echo -e "⏹️  Stopping gob-monitor..."
    sudo systemctl stop gob-monitor
    
    echo -e "${GREEN}✅ Monitor service stopped${NC}"
}

restart_service() {
    echo -e "${BLUE}=== Restarting GOB Network Monitor ===${NC}"
    echo
    
    stop_service
    sleep 2
    start_service
}

show_logs() {
    echo -e "${BLUE}=== Recent Monitor Logs ===${NC}"
    echo
    
    sudo journalctl -u gob-monitor -n 20 --no-pager || true
}

follow_logs() {
    echo -e "${BLUE}=== Following Monitor Logs (Press Ctrl+C to exit) ===${NC}"
    echo
    
    sudo journalctl -u gob-monitor -f
}

uninstall_service() {
    echo -e "${YELLOW}⚠️  This will remove the GOB network monitor service. Continue? (y/N)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    
    echo -e "${BLUE}=== Uninstalling GOB Network Monitor ===${NC}"
    echo
    
    echo -e "🛑 Stopping and removing gob-monitor..."
    sudo systemctl stop gob-monitor 2>/dev/null || true
    sudo systemctl disable gob-monitor 2>/dev/null || true
    sudo rm -f "/etc/systemd/system/gob-monitor.service"
    
    sudo systemctl daemon-reload
    
    echo -e "${GREEN}✅ Monitor service uninstalled${NC}"
    echo -e "${BLUE}💡 The gob-monitor conda environment is still available${NC}"
}

# Main command dispatcher
case "${1:-help}" in
    "status")
        show_status
        ;;
    "start")
        start_service
        ;;
    "stop")
        stop_service
        ;;
    "restart")
        restart_service
        ;;
    "logs")
        show_logs
        ;;
    "follow")
        follow_logs
        ;;
    "dashboard")
        show_dashboard
        ;;
    "uninstall")
        uninstall_service
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        echo
        show_help
        exit 1
        ;;
esac
