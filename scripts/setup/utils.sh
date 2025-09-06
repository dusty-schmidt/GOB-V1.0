#!/bin/bash
# File: scripts/setup/utils.sh
# Location: GOBV1 project setup utilities
# Role: Shared utility functions for colors, printing, and common helpers

# Colors for output
export RED='\033[0;31m'
export GREEN='\033[0;32m'
export YELLOW='\033[1;33m'
export CYAN='\033[0;36m'
export BLUE='\033[0;34m'
export NC='\033[0m' # No Color

# Default Configuration
export PROJECT_NAME="GOB"
export DEFAULT_CONDA_ENV="gob"
export DEFAULT_PYTHON_VERSION="3.12"
export MINICONDA_VERSION="latest"

# Get project directory
get_project_dir() {
    echo "$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
}

# Initialize global variables
init_globals() {
    export PROJECT_DIR="$(get_project_dir)"
    # Primary device-level config in home directory
    export DEVICE_CONFIG_FILE="$HOME/.gobconfig.json"
    # Optional project-local reference for convenience
    export PROJECT_CONFIG_FILE="$PROJECT_DIR/.gobconfig.json"
}

print_header() {
    echo -e "${CYAN}=== $PROJECT_NAME Enhanced Setup ===${NC}"
    echo -e "${CYAN}Setting up $PROJECT_NAME in: $PROJECT_DIR${NC}"
    echo
}

print_status() {
    local status="$1"
    local message="$2"
    case $status in
        "success") echo -e "${GREEN}✅ ${message}${NC}" ;;
        "error") echo -e "${RED}❌ ${message}${NC}" ;;
        "warning") echo -e "${YELLOW}⚠️  ${message}${NC}" ;;
        "info") echo -e "${BLUE}ℹ️  ${message}${NC}" ;;
        "step") echo -e "${CYAN}🔧 ${message}${NC}" ;;
        *) echo -e "${message}" ;;
    esac
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Get current timestamp
get_timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

# Source clean progress implementation
source "$(dirname "${BASH_SOURCE[0]}")/progress.sh"

# Helper: ensure a directory exists
ensure_dir() {
    local d="$1"
    [ -d "$d" ] || mkdir -p "$d"
}

# Quiet execution function
run_quiet() {
    "$@" >/dev/null 2>&1
}

# Initialize globals when this script is sourced
init_globals
