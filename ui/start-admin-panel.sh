#!/bin/bash
# GOB UI Admin Panel Startup Script

echo "🎛️  GOB Admin Panel Startup"
echo "=========================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📁 UI Directory: $SCRIPT_DIR"
echo ""

# Check what's available
echo "Available Admin Interfaces:"
echo "1. Flask Backend Monitor (RECOMMENDED - Anti-twitching fixes applied)"
echo "2. Dash Network Monitor (LEGACY)"
echo ""

# Default to Flask Backend Monitor
read -p "Select interface (1-2) [1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo "🚀 Starting Flask Backend Monitor..."
        exec "$SCRIPT_DIR/admin-panel/flask-backend-monitor/start.sh"
        ;;
    2)
        echo "🚀 Starting Dash Network Monitor..."
        cd "$SCRIPT_DIR/admin-panel/dash-network-monitor"
        python start_monitor.py
        ;;
    *)
        echo "❌ Invalid choice. Starting Flask Backend Monitor (default)..."
        exec "$SCRIPT_DIR/admin-panel/flask-backend-monitor/start.sh"
        ;;
esac
