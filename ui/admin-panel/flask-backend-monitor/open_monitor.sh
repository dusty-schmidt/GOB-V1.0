#!/bin/bash
# GOB Monitoring Dashboard Browser Opener
# This script opens the monitoring dashboard in the default browser

# Configuration
MONITOR_URL="http://localhost:8050"
LOG_FILE="/home/ds/GOB/monitoring/logs/browser_opener.log"

# Ensure logs directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_message "Starting browser opener script"

# Wait for the monitoring service to be ready
attempt=0
max_attempts=30
while [ $attempt -lt $max_attempts ]; do
    if curl -s -f "$MONITOR_URL" > /dev/null 2>&1; then
        log_message "Monitoring service is ready"
        break
    fi
    log_message "Waiting for monitoring service... (attempt $((attempt + 1))/$max_attempts)"
    sleep 2
    attempt=$((attempt + 1))
done

if [ $attempt -eq $max_attempts ]; then
    log_message "ERROR: Monitoring service not ready after $max_attempts attempts"
    exit 1
fi

# Detect desktop environment and open browser accordingly
if [ -n "$DISPLAY" ]; then
    # We have a graphical display
    log_message "Display detected: $DISPLAY"
    
    # Try different methods to open browser
    if command -v xdg-open >/dev/null 2>&1; then
        log_message "Opening browser with xdg-open"
        DISPLAY=:0 xdg-open "$MONITOR_URL" 2>&1 | tee -a "$LOG_FILE"
    elif command -v firefox >/dev/null 2>&1; then
        log_message "Opening Firefox directly"
        DISPLAY=:0 firefox "$MONITOR_URL" >/dev/null 2>&1 &
    elif command -v google-chrome >/dev/null 2>&1; then
        log_message "Opening Chrome directly"
        DISPLAY=:0 google-chrome "$MONITOR_URL" >/dev/null 2>&1 &
    elif command -v chromium >/dev/null 2>&1; then
        log_message "Opening Chromium directly"
        DISPLAY=:0 chromium "$MONITOR_URL" >/dev/null 2>&1 &
    elif command -v chromium-browser >/dev/null 2>&1; then
        log_message "Opening Chromium browser directly"
        DISPLAY=:0 chromium-browser "$MONITOR_URL" >/dev/null 2>&1 &
    else
        log_message "No suitable browser found"
        exit 1
    fi
    
    log_message "Browser opening command completed"
else
    log_message "No display available - running in headless mode"
    # Could implement notification or alternative method here
fi

log_message "Browser opener script completed"
