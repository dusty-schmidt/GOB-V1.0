#!/bin/bash

# GOB Core Service Management
# Simple management for ONLY the core service

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
GRAY='\033[0;37m'
NC='\033[0m'

show_help() {
    echo -e "${BLUE}GOB Core Service Management${NC}"
    echo
    echo -e "${YELLOW}Usage:${NC} $(basename "$0") [COMMAND]"
    echo
    echo -e "${YELLOW}Commands:${NC}"
    echo "  status      Show core service status"
    echo "  start       Start core service"
    echo "  stop        Stop core service"
    echo "  restart     Restart core service"
    echo "  logs        Show recent logs"
    echo "  follow      Follow live logs"
    echo "  health      Check health endpoint"
    echo "  uninstall   Remove core service"
    echo "  help        Show this help"
}

show_status() {
    echo -e "${BLUE}=== GOB Core Status ===${NC}"
    echo
    
    if systemctl is-active gob-core >/dev/null 2>&1; then
        echo -e "  ${GREEN}●${NC} gob-core: ${GREEN}running${NC}"
        
        # Show detailed status
        echo
        sudo systemctl status gob-core --no-pager -l | grep -E "(●|Active:|Main PID:|Memory:|CPU:)" || true
    elif systemctl is-enabled gob-core >/dev/null 2>&1; then
        echo -e "  ${GRAY}●${NC} gob-core: ${GRAY}stopped${NC}"
    else
        echo -e "  ${RED}●${NC} gob-core: ${RED}not installed${NC}"
    fi
    echo
}

check_health() {
    echo -e "${BLUE}=== Core Health Check ===${NC}"
    echo
    
    if curl -s http://localhost:8051/health >/dev/null 2>&1; then
        echo -e "  ${GREEN}✅${NC} Core service: healthy"
        echo
        echo -e "${BLUE}Health Response:${NC}"
        curl -s http://localhost:8051/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8051/health
    else
        echo -e "  ${RED}❌${NC} Core service: unhealthy or not responding"
        echo "     Health endpoint: http://localhost:8051/health"
    fi
    echo
}

start_service() {
    echo -e "${BLUE}=== Starting GOB Core ===${NC}"
    echo
    
    if systemctl is-active gob-core >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Core service is already running${NC}"
        return 0
    fi
    
    echo -e "🚀 Starting gob-core..."
    sudo systemctl start gob-core
    
    # Wait a moment
    sleep 2
    
    if systemctl is-active gob-core >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Core service started${NC}"
        
        # Quick health check
        sleep 1
        if curl -s http://localhost:8051/health >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Health check passed${NC}"
        else
            echo -e "${YELLOW}⚠️  Service started but health check pending...${NC}"
        fi
    else
        echo -e "${RED}❌ Failed to start core service${NC}"
        echo
        echo -e "${YELLOW}Recent logs:${NC}"
        sudo journalctl -u gob-core -n 5 --no-pager || true
    fi
}

stop_service() {
    echo -e "${BLUE}=== Stopping GOB Core ===${NC}"
    echo
    
    if ! systemctl is-active gob-core >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Core service is not running${NC}"
        return 0
    fi
    
    echo -e "⏹️  Stopping gob-core..."
    sudo systemctl stop gob-core
    
    echo -e "${GREEN}✅ Core service stopped${NC}"
}

restart_service() {
    echo -e "${BLUE}=== Restarting GOB Core ===${NC}"
    echo
    
    stop_service
    sleep 1
    start_service
}

show_logs() {
    echo -e "${BLUE}=== Recent Core Logs ===${NC}"
    echo
    
    sudo journalctl -u gob-core -n 20 --no-pager || true
}

follow_logs() {
    echo -e "${BLUE}=== Following Core Logs (Press Ctrl+C to exit) ===${NC}"
    echo
    
    sudo journalctl -u gob-core -f
}

uninstall_service() {
    echo -e "${YELLOW}⚠️  This will remove the GOB core service. Continue? (y/N)${NC}"
    read -r response
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo "Cancelled."
        exit 0
    fi
    
    echo -e "${BLUE}=== Uninstalling GOB Core ===${NC}"
    echo
    
    echo -e "🛑 Stopping and removing gob-core..."
    sudo systemctl stop gob-core 2>/dev/null || true
    sudo systemctl disable gob-core 2>/dev/null || true
    sudo rm -f "/etc/systemd/system/gob-core.service"
    
    sudo systemctl daemon-reload
    
    echo -e "${GREEN}✅ Core service uninstalled${NC}"
    echo -e "${BLUE}💡 The gob-core conda environment is still available${NC}"
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
    "health")
        check_health
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
