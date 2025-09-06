#!/bin/bash

source scripts/setup/progress.sh
source scripts/setup/utils.sh

echo -e "${CYAN}Testing Phase-Based Progress System${NC}"

# Test phases
phases=(
    "System Detection & Prerequisites"
    "Conda Environment Setup" 
    "Dependencies Installation"
    "CLI Tools Configuration"
    "Activation Script Creation"
    "Installation Verification"
)

for phase in "${phases[@]}"; do
    start_phase "$phase"
    
    # Simulate work with spinner
    show_working "$phase..." &
    spinner_pid=$!
    
    sleep 2  # Simulate work
    
    kill $spinner_pid 2>/dev/null
    wait $spinner_pid 2>/dev/null
    
    complete_phase "$phase"
done

echo
echo -e "${GREEN}✨ All phases completed!${NC}"
