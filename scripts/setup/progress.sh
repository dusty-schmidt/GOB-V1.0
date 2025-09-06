#!/bin/bash
# File: scripts/setup/progress.sh
# Phase-based progress system

# Show phase progress
show_phase_progress() {
    local current=$1
    local total=$2
    local description="$3"
    local width=40
    
    local percentage=$((current * 100 / total))
    local filled=$((current * width / total))
    
    # Build progress bar
    local bar=""
    for ((i=0; i<filled; i++)); do bar+="█"; done
    for ((i=filled; i<width; i++)); do bar+="░"; done
    
    # Display progress
    printf "\r\033[36m[%s]\033[0m %3d%% %s" "$bar" "$percentage" "$description"
}

# Start new phase
start_phase() {
    local phase_name="$1"
    echo -e "\n\033[33m🔧 $phase_name\033[0m"
}

# Complete phase
complete_phase() {
    local phase_name="$1"
    printf "\r\033[K\033[32m✅ $phase_name\033[0m\n"
}

# Show working indicator (spinner)
show_working() {
    local message="$1"
    local chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    local i=0
    
    while true; do
        printf "\r\033[36m%s\033[0m %s" "${chars:$i:1}" "$message"
        i=$(((i+1) % ${#chars}))
        sleep 0.1
    done
}
