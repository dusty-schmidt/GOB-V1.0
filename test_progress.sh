#!/bin/bash
# Test the progress bar functionality

source scripts/setup/utils.sh

echo -e "${CYAN}Testing Progress Bar${NC}"
echo

for i in {1..7}; do
    case $i in
        1) desc="Checking prerequisites and system detection" ;;
        2) desc="Setting up conda environment" ;;
        3) desc="Installing dependencies (this may take a while)" ;;
        4) desc="Setting up CLI tools" ;;
        5) desc="Creating activation script" ;;
        6) desc="Verifying installation" ;;
        7) desc="Finalizing setup" ;;
    esac
    
    show_progress $i "$desc"
    sleep 2
    complete_step $i "✅ Step $i completed"
done

echo
echo -e "${GREEN}Progress bar test completed!${NC}"
