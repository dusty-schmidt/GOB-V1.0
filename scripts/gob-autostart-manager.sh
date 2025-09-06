#!/bin/bash

# GOB Autostart Management Script
# Helps manage boot startup and desktop autostart settings

set -e

SYSTEMD_SERVICE="gob-autostart.service"
DESKTOP_FILE="$HOME/.config/autostart/gob-autostart.desktop"

show_help() {
    cat << EOF
GOB Autostart Management Script

Usage: $(basename "$0") [COMMAND]

Commands:
    enable-boot     Enable GOB to start on system boot (systemd)
    disable-boot    Disable GOB system boot startup
    enable-desktop  Enable GOB to start when desktop session starts
    disable-desktop Disable GOB desktop session startup
    status          Show current autostart configuration
    test            Test the autostart script manually
    help            Show this help message

Examples:
    $(basename "$0") enable-boot     # Start GOB on system boot
    $(basename "$0") enable-desktop  # Start GOB when logging into desktop
    $(basename "$0") status          # Check current configuration
    $(basename "$0") test            # Test the startup script
EOF
}

check_systemd_status() {
    if systemctl is-enabled "$SYSTEMD_SERVICE" >/dev/null 2>&1; then
        echo "✅ System boot startup: ENABLED"
    else
        echo "❌ System boot startup: DISABLED"
    fi
}

check_desktop_status() {
    if [ -f "$DESKTOP_FILE" ] && [ -x "$DESKTOP_FILE" ]; then
        echo "✅ Desktop session startup: ENABLED"
    else
        echo "❌ Desktop session startup: DISABLED"
    fi
}

enable_boot() {
    echo "Enabling GOB system boot startup..."
    sudo systemctl enable "$SYSTEMD_SERVICE"
    echo "✅ GOB will now start automatically on system boot"
}

disable_boot() {
    echo "Disabling GOB system boot startup..."
    sudo systemctl disable "$SYSTEMD_SERVICE"
    echo "❌ GOB system boot startup disabled"
}

enable_desktop() {
    echo "Enabling GOB desktop session startup..."
    mkdir -p "$(dirname "$DESKTOP_FILE")"
    if [ ! -f "$DESKTOP_FILE" ]; then
        echo "❌ Desktop file not found. Please run the main setup first."
        exit 1
    fi
    chmod +x "$DESKTOP_FILE"
    echo "✅ GOB will now start automatically when you log into your desktop session"
}

disable_desktop() {
    echo "Disabling GOB desktop session startup..."
    if [ -f "$DESKTOP_FILE" ]; then
        chmod -x "$DESKTOP_FILE"
        echo "❌ GOB desktop session startup disabled"
    else
        echo "❌ Desktop autostart file not found (already disabled)"
    fi
}

show_status() {
    echo "GOB Autostart Configuration Status:"
    echo "=================================="
    check_systemd_status
    check_desktop_status
    echo
    echo "Recommendations:"
    echo "  - Use 'enable-boot' for server-like systems"
    echo "  - Use 'enable-desktop' for desktop/laptop systems"
    echo "  - You can enable both if desired"
}

test_startup() {
    echo "Testing GOB autostart script..."
    echo "==============================="
    cd "$(dirname "$0")/.."
    ./scripts/gob-autostart.sh
}

# Main execution
case "${1:-help}" in
    "enable-boot")
        enable_boot
        ;;
    "disable-boot")
        disable_boot
        ;;
    "enable-desktop")
        enable_desktop
        ;;
    "disable-desktop")
        disable_desktop
        ;;
    "status")
        show_status
        ;;
    "test")
        test_startup
        ;;
    "help"|*)
        show_help
        ;;
esac
