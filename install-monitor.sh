#!/bin/bash

# GOB Network Monitor Installation Script
# Independent monitoring dashboard with terminal hacker aesthetic

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    GOB Network Monitor Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo
echo -e "${BLUE}Terminal hacker style monitoring dashboard${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo -e "${RED}❌ Please run this script as your normal user (not root)${NC}"
    echo "   The script will use sudo when needed"
    exit 1
fi

# Check sudo availability
if ! command -v sudo &> /dev/null; then
    echo -e "${RED}❌ sudo is required for service installation${NC}"
    exit 1
fi

GOB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}📁 GOB Directory: $GOB_DIR${NC}"
echo

# Step 1: Create dedicated monitor environment
echo -e "${YELLOW}🔧 Step 1: Setting up dedicated monitor environment...${NC}"
if conda env list | grep -q "gob-monitor"; then
    echo "   ✅ gob-monitor environment already exists"
else
    echo "   📦 Creating gob-monitor conda environment..."
    conda create -n gob-monitor python=3.11 -y
    echo "   📦 Installing monitor dependencies..."
    /home/ds/miniconda3/envs/gob-monitor/bin/pip install dash plotly psutil requests numpy
    echo "   ✅ Monitor environment ready"
fi
echo

# Step 2: Test monitor service
echo -e "${YELLOW}🔧 Step 2: Testing monitor service...${NC}"
echo "   🧪 Running monitor service test..."

# Test the monitor service manually for a few seconds
if /home/ds/miniconda3/envs/gob-monitor/bin/python "$GOB_DIR/monitor/start_monitor.py" &
then
    MONITOR_PID=$!
    sleep 5
    
    # Test if monitor is responding
    if curl -s http://localhost:8050 >/dev/null 2>&1; then
        echo "   ✅ Monitor service test passed"
        kill $MONITOR_PID 2>/dev/null || true
        wait $MONITOR_PID 2>/dev/null || true
        sleep 2  # Give it time to shut down
    else
        echo -e "${RED}   ❌ Monitor service test failed${NC}"
        kill $MONITOR_PID 2>/dev/null || true
        exit 1
    fi
else
    echo -e "${RED}   ❌ Monitor service failed to start${NC}"
    exit 1
fi

# Step 3: Install systemd service
echo -e "${YELLOW}🔧 Step 3: Installing systemd service...${NC}"

# Stop existing service
echo "   🛑 Stopping existing gob-monitor service..."
sudo systemctl stop gob-monitor 2>/dev/null || true

# Install service file
service_file="$GOB_DIR/services/gob-monitor.service"
if [ -f "$service_file" ]; then
    echo "   📋 Installing gob-monitor.service..."
    sudo cp "$service_file" /etc/systemd/system/
    sudo chmod 644 "/etc/systemd/system/gob-monitor.service"
else
    echo -e "${RED}   ❌ Service file not found: $service_file${NC}"
    exit 1
fi

# Reload systemd
echo "   🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable service for boot
echo "   ✅ Enabling gob-monitor for boot startup..."
sudo systemctl enable gob-monitor

# Step 4: Start and verify service
echo -e "${YELLOW}🔧 Step 4: Starting monitor service...${NC}"
echo "   🚀 Starting gob-monitor..."
sudo systemctl start gob-monitor

# Wait a moment for startup
sleep 5

# Check if service is running
if systemctl is-active gob-monitor >/dev/null 2>&1; then
    echo "   ✅ gob-monitor service is running"
    
    # Test dashboard endpoint
    if curl -s http://localhost:8050 >/dev/null 2>&1; then
        echo "   ✅ Dashboard is accessible"
    else
        echo -e "${YELLOW}   ⚠️  Service running but dashboard not yet accessible...${NC}"
    fi
else
    echo -e "${RED}   ❌ gob-monitor service failed to start${NC}"
    echo "   📋 Service status:"
    sudo systemctl status gob-monitor --no-pager -l || true
    exit 1
fi

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    Monitor Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${BLUE}🎯 Monitor Service Status:${NC}"
sudo systemctl status gob-monitor --no-pager -l | grep -E "(●|Active:|Main PID:)" || true
echo
echo -e "${BLUE}🌐 Dashboard Access:${NC}"
echo "   • Monitor Dashboard: http://localhost:8050"
echo "   • Terminal hacker aesthetic with real-time updates"
echo "   • Shows core service status and system metrics"
echo
echo -e "${BLUE}📋 Management Commands:${NC}"
echo "   • Check status: sudo systemctl status gob-monitor"
echo "   • View logs: sudo journalctl -u gob-monitor -f"
echo "   • Restart: sudo systemctl restart gob-monitor"
echo "   • Stop: sudo systemctl stop gob-monitor"
echo
echo -e "${GREEN}✅ GOB Network Monitor is now installed and will start automatically on boot!${NC}"
echo -e "${BLUE}💡 The monitor runs independently and will show 'CORE SERVICES DOWN' if core is offline${NC}"
