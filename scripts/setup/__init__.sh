#!/bin/bash
# File: scripts/setup/__init__.sh
# Location: GOBV1 project setup main orchestrator
# Role: Coordinate all modules and expose main setup function

set -e

# Source all modules
SETUP_DIR="$(dirname "${BASH_SOURCE[0]}")"
source "$SETUP_DIR/utils.sh"
source "$SETUP_DIR/system.sh"
source "$SETUP_DIR/config.sh"
source "$SETUP_DIR/conda.sh"
source "$SETUP_DIR/dependencies.sh"
source "$SETUP_DIR/cli.sh"

# Run phase with spinner feedback
run_phase() {
    local phase_name="$1"
    local command="$2"

    start_phase "$phase_name"

    if [ "${VERBOSE:-0}" = "1" ]; then
        if $command; then
            complete_phase "$phase_name"
        else
            echo
            print_status "error" "Phase failed: $phase_name"
            exit 1
        fi
    else
        show_working "$phase_name..." &
        local spinner_pid=$!
        if $command >/dev/null 2>&1; then
            kill $spinner_pid 2>/dev/null; wait $spinner_pid 2>/dev/null
            complete_phase "$phase_name"
        else
            kill $spinner_pid 2>/dev/null; wait $spinner_pid 2>/dev/null
            echo
            print_status "error" "Phase failed: $phase_name"
            echo -e "${YELLOW}Run with VERBOSE=1 ./setup_new.sh for detailed logs${NC}"
            exit 1
        fi
    fi
}

# Main setup function
run_setup() {
    print_header
    
    # Check if setup is already complete and exit early if so
    if check_if_setup_complete; then
        exit 0
    fi
    
    echo -e "${CYAN}Collecting device information and preparing setup...${NC}"
    echo
    
    # Handle device configuration first (with prompts)
    if [ ! -f "$DEVICE_CONFIG_FILE" ]; then
        create_device_config
    else
        load_device_config
    fi
    
    echo
    echo -e "${CYAN}Starting $PROJECT_NAME setup for device: ${GREEN}$DEVICE_NICKNAME${NC}"
    if [ "${VERBOSE:-0}" = "1" ]; then
        echo -e "${YELLOW}Verbose mode enabled - showing detailed output${NC}"
    fi
    echo
    
    # Execute all phases with simpler progress
    run_phase "System Detection & Prerequisites" "check_prerequisites_only"
    run_phase "Conda Environment Setup" "setup_environment"
    run_phase "Dependencies Installation" "install_dependencies"
    run_phase "CLI Tools Configuration" "setup_cli"
    run_phase "Activation Script Creation" "create_activation_script"
    run_phase "Installation Verification" "run_verification"
    
    echo
    echo -e "${GREEN}✨ $PROJECT_NAME setup completed successfully!${NC}"
    print_completion
}

# Export the main function so it can be called from outside
export -f run_setup
