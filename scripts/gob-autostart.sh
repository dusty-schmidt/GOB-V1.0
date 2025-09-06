#!/bin/bash

# GOB Auto-start Script with Health Check and Firefox Launch
# This script starts GOB, waits for it to be ready, then opens Firefox

set -e

# Configuration
GOB_DIR="/home/ds/GOB"
GOB_URL="http://localhost:50080"
MAX_WAIT_TIME=120  # Maximum wait time in seconds
HEALTH_CHECK_INTERVAL=5  # Check every 5 seconds

# Logging
LOG_FILE="$GOB_DIR/autostart.log"
exec 1> >(tee -a "$LOG_FILE")
exec 2>&1

echo "$(date): GOB Auto-start script initiated"

# Function to log messages
log() {
    echo "$(date): $1"
}

# Function to check if GOB is responding
check_gob_health() {
    curl -s -o /dev/null -w "%{http_code}" "$GOB_URL" 2>/dev/null
}

# Function to wait for GOB to be ready
wait_for_gob() {
    local elapsed=0
    log "Waiting for GOB to respond at $GOB_URL..."
    
    while [ $elapsed -lt $MAX_WAIT_TIME ]; do
        local response=$(check_gob_health)
        if [ "$response" = "200" ]; then
            log "GOB is ready! (HTTP 200 response received)"
            return 0
        fi
        
        log "GOB not ready yet (HTTP $response), waiting... (${elapsed}s elapsed)"
        sleep $HEALTH_CHECK_INTERVAL
        elapsed=$((elapsed + HEALTH_CHECK_INTERVAL))
    done
    
    log "ERROR: GOB failed to start within $MAX_WAIT_TIME seconds"
    return 1
}

# Function to launch Firefox
launch_firefox() {
    log "Launching Firefox to $GOB_URL..."
    
    # Try different Firefox commands in order of preference
    if command -v firefox >/dev/null 2>&1; then
        firefox "$GOB_URL" >/dev/null 2>&1 &
        log "Firefox launched successfully"
    elif command -v firefox-esr >/dev/null 2>&1; then
        firefox-esr "$GOB_URL" >/dev/null 2>&1 &
        log "Firefox ESR launched successfully"
    else
        log "WARNING: Firefox not found in PATH, trying to launch anyway..."
        # Try common Firefox paths
        for firefox_path in /usr/bin/firefox /usr/bin/firefox-esr /snap/bin/firefox; do
            if [ -x "$firefox_path" ]; then
                "$firefox_path" "$GOB_URL" >/dev/null 2>&1 &
                log "Firefox launched from $firefox_path"
                return 0
            fi
        done
        log "ERROR: Could not find Firefox executable"
        return 1
    fi
}

# Main execution
main() {
    cd "$GOB_DIR" || {
        log "ERROR: Could not change to GOB directory: $GOB_DIR"
        exit 1
    }
    
    log "Starting GOB server..."
    
    # Check if GOB is already running
    if [ "$(check_gob_health)" = "200" ]; then
        log "GOB is already running and responding"
    else
        # Start GOB using the management script
        if ! ./scripts/gob start; then
            log "ERROR: Failed to start GOB server"
            exit 1
        fi
        log "GOB start command completed"
    fi
    
    # Wait for GOB to be ready
    if wait_for_gob; then
        # Launch Firefox
        if launch_firefox; then
            log "GOB auto-start completed successfully"
        else
            log "GOB started but Firefox launch failed"
            exit 1
        fi
    else
        log "GOB auto-start failed - server not responding"
        exit 1
    fi
}

# Run main function
main "$@"
