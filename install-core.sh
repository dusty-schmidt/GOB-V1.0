#!/bin/bash

# GOB Core Service Installation
# Installs ONLY the core state manager - completely independent

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}    GOB Core Service Installation${NC}"
echo -e "${BLUE}========================================${NC}"
echo
echo -e "${BLUE}This installs ONLY the core state manager.${NC}"
echo -e "${BLUE}Monitoring and agent are separate setups.${NC}"
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo -e "${RED}❌ Please run this script as your normal user (not root)${NC}"
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

# Step 1: Create dedicated core environment
echo -e "${YELLOW}🔧 Step 1: Setting up dedicated core environment...${NC}"

if command -v conda &> /dev/null; then
    if conda env list | grep -q "gob-core"; then
        echo "   ✅ gob-core environment already exists"
    else
        echo "   📦 Creating gob-core conda environment..."
        conda create -n gob-core python=3.11 -y
        echo "   📦 Installing core dependencies..."
        /home/ds/miniconda3/envs/gob-core/bin/pip install psutil numpy
        echo "   ✅ Core environment created"
    fi
else
    echo -e "${RED}❌ Conda not found. Please install conda first.${NC}"
    exit 1
fi

# Step 2: Test core service
echo -e "${YELLOW}🔧 Step 2: Testing core service...${NC}"
echo "   🧪 Running core service test..."

# Test the core service manually
if /home/ds/miniconda3/envs/gob-core/bin/python "$GOB_DIR/core/start_core.py" &
then
    CORE_PID=$!
    sleep 3
    
    # Test health endpoint
    if curl -s http://localhost:8051/health | grep -q "healthy"; then
        echo "   ✅ Core service test passed"
        kill $CORE_PID 2>/dev/null || true
        wait $CORE_PID 2>/dev/null || true
    else
        echo -e "${RED}   ❌ Core service health check failed${NC}"
        kill $CORE_PID 2>/dev/null || true
        exit 1
    fi
else
    echo -e "${RED}   ❌ Core service failed to start${NC}"
    exit 1
fi

# Step 3: Install systemd service
echo -e "${YELLOW}🔧 Step 3: Installing systemd service...${NC}"

# Stop existing service
echo "   🛑 Stopping existing gob-core service..."
sudo systemctl stop gob-core 2>/dev/null || true

# Install service file
service_file="$GOB_DIR/services/gob-core.service"
if [ -f "$service_file" ]; then
    echo "   📋 Installing gob-core.service..."
    sudo cp "$service_file" /etc/systemd/system/
    sudo chmod 644 "/etc/systemd/system/gob-core.service"
else
    echo -e "${RED}   ❌ Service file not found: $service_file${NC}"
    exit 1
fi

# Reload systemd
echo "   🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable service for boot
echo "   ✅ Enabling gob-core for boot startup..."
sudo systemctl enable gob-core

# Step 4: Start and verify service
echo -e "${YELLOW}🔧 Step 4: Starting core service...${NC}"
echo "   🚀 Starting gob-core..."
sudo systemctl start gob-core

# Wait a moment for startup
sleep 3

# Check if service is running
if systemctl is-active gob-core >/dev/null 2>&1; then
    echo "   ✅ gob-core service is running"
    
    # Test health endpoint
    if curl -s http://localhost:8051/health | grep -q "healthy"; then
        echo "   ✅ Health check passed"
    else
        echo -e "${YELLOW}   ⚠️  Service running but health check failed${NC}"
    fi
else
    echo -e "${RED}   ❌ gob-core service failed to start${NC}"
    echo "   📋 Service status:"
    sudo systemctl status gob-core --no-pager -l || true
    exit 1
fi

echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}    Core Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
echo -e "${BLUE}🎯 Core Service Status:${NC}"
sudo systemctl status gob-core --no-pager -l | grep -E "(●|Active:|Main PID:)" || true
echo
echo -e "${BLUE}🌐 Core Health Check:${NC}"
curl -s http://localhost:8051/health | python3 -m json.tool 2>/dev/null || echo "Health endpoint not responding"
echo
echo -e "${BLUE}📋 Management Commands:${NC}"
echo "   • Check status: sudo systemctl status gob-core"
echo "   • View logs: sudo journalctl -u gob-core -f"
echo "   • Restart: sudo systemctl restart gob-core"
echo "   • Stop: sudo systemctl stop gob-core"
echo
echo -e "${GREEN}✅ GOB Core is now installed and will start automatically on boot!${NC}"
echo -e "${BLUE}💡 Next: Run './install-monitoring.sh' to set up the monitoring dashboard${NC}"
