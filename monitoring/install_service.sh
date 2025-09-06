#!/bin/bash

# GOB Monitoring System Service Installation Script
echo "🔧 Installing GOB Monitoring System as a service..."
echo "=========================================="

# Check if running as root for service installation
if [[ $EUID -eq 0 ]]; then
    echo "❌ Please run this script as your normal user (not root)"
    echo "   The script will use sudo when needed"
    exit 1
fi

# Check if sudo is available
if ! command -v sudo &> /dev/null; then
    echo "❌ sudo is required for service installation"
    exit 1
fi

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICE_FILE="$SCRIPT_DIR/gob-monitoring.service"

echo "📁 Script directory: $SCRIPT_DIR"
echo "📋 Service file: $SERVICE_FILE"

# Verify service file exists
if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ Service file not found: $SERVICE_FILE"
    exit 1
fi

# Stop existing service if running
echo ""
echo "🛑 Stopping existing service (if running)..."
sudo systemctl stop gob-monitoring 2>/dev/null || true
sudo systemctl disable gob-monitoring 2>/dev/null || true

# Copy service file to systemd
echo "📋 Installing systemd service..."
sudo cp "$SERVICE_FILE" /etc/systemd/system/

# Set proper permissions
sudo chmod 644 /etc/systemd/system/gob-monitoring.service

# Reload systemd to recognize the new service
echo "🔄 Reloading systemd..."
sudo systemctl daemon-reload

# Enable the service to start on boot
echo "✅ Enabling service for boot startup..."
sudo systemctl enable gob-monitoring

# Start the service
echo "🚀 Starting the service..."
sudo systemctl start gob-monitoring

# Wait a moment for service to start
sleep 3

# Check service status
echo ""
echo "📊 Service Status:"
sudo systemctl status gob-monitoring --no-pager -l

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo ""
echo "🎯 Service Commands:"
echo "   sudo systemctl start gob-monitoring    # Start the service"
echo "   sudo systemctl stop gob-monitoring     # Stop the service" 
echo "   sudo systemctl restart gob-monitoring  # Restart the service"
echo "   sudo systemctl status gob-monitoring   # Check status"
echo "   sudo systemctl disable gob-monitoring  # Disable auto-start"
echo ""
echo "📋 Logs:"
echo "   sudo journalctl -u gob-monitoring -f   # Follow live logs"
echo "   sudo journalctl -u gob-monitoring      # View all logs"
echo ""
echo "🌐 Dashboard: http://localhost:8050"
echo ""
echo "🔄 The service will:"
echo "   ✅ Start automatically on system boot"
echo "   ✅ Restart automatically if it crashes"  
echo "   ✅ Run in the background (no terminal needed)"
echo "   ✅ Survive user logout/login"
