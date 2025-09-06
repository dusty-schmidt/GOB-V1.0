#!/bin/bash
# File: setup_new.sh
# Location: Project root directory
# Role: Simple setup runner that calls the modular setup system

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Source the modular setup system
source "$SCRIPT_DIR/scripts/setup/__init__.sh"

# Run the setup
run_setup "$@"
