#!/bin/bash
# File: scripts/setup/cli.sh
# Location: GOBV1 project setup CLI and verification
# Role: CLI setup and installation verification functions

# Source utilities and config
source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"
source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

setup_cli() {
    print_status "step" "Setting up CLI tool..."
    
    # Make gob executable
    if [ -f "$PROJECT_DIR/scripts/gob" ]; then
        chmod +x "$PROJECT_DIR/scripts/gob"
        print_status "success" "GOB CLI made executable"
    else
        print_status "warning" "scripts/gob not found, skipping CLI setup"
        return 0
    fi
    
    # Offer to create system-wide symlink
    if [ -w "/usr/local/bin" ]; then
        ln -sf "$PROJECT_DIR/scripts/gob" /usr/local/bin/gob
        print_status "success" "CLI tool linked to /usr/local/bin/gob"
    else
        print_status "info" "Creating system-wide symlink (requires sudo)..."
        if sudo ln -sf "$PROJECT_DIR/scripts/gob" /usr/local/bin/gob 2>/dev/null; then
            print_status "success" "CLI tool linked to /usr/local/bin/gob"
        else
            print_status "warning" "Could not create system-wide link. Use scripts/gob instead"
        fi
    fi
}

run_verification() {
    print_status "step" "Verifying installation..."
    
    # Test Python environment
    print_status "info" "Testing Python environment..."
    python -c "
import sys
print(f'Python: {sys.version}')
print(f'Location: {sys.executable}')
" || print_status "error" "Python verification failed"
    
    # Test core imports
    print_status "info" "Testing core package imports..."
    python -c "
try:
    import flask, numpy, pandas, matplotlib
    print('✅ Core packages: OK')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
" || print_status "warning" "Some core packages failed to import"
    
    # Test CLI tool if it exists
    if [ -f "$PROJECT_DIR/scripts/gob" ]; then
        if "$PROJECT_DIR/scripts/gob" help >/dev/null 2>&1; then
            print_status "success" "CLI tool working correctly"
        else
            print_status "warning" "CLI tool verification failed"
        fi
    fi
    
    print_status "success" "Installation verification completed"
}

print_completion() {
    # Update device config to mark setup as complete
    update_device_config "setup_completed" "true"
    update_device_config "last_updated" ""
    
    echo
    print_status "success" "$PROJECT_NAME setup completed successfully!"
    echo
    echo -e "${CYAN}Device Configuration:${NC}"
    if [ -n "$DEVICE_NICKNAME" ]; then
        echo -e "  🏷️  Device: ${GREEN}$DEVICE_NICKNAME${NC}"
    fi
    if [ -n "$USER_FULL_NAME" ]; then
        echo -e "  👤 User: ${GREEN}$USER_FULL_NAME${NC}"
    fi
    echo -e "  📁 Config: ${GREEN}$DEVICE_CONFIG_FILE${NC}"
    echo
    echo -e "${CYAN}Installation Summary:${NC}"
    echo -e "  ✅ Miniconda: $(conda --version)"
    echo -e "  ✅ Environment: $CONDA_ENV (Python $PYTHON_VERSION)" 
    echo -e "  ✅ Package Manager: $CONDA_CMD"
    echo -e "  ✅ Channel Priority: conda-forge"
    echo -e "  ✅ Project Directory: $PROJECT_DIR"
    echo
    echo -e "${CYAN}Quick Start:${NC}"
    echo -e "${GREEN}1.${NC} Activate environment: ${YELLOW}source ./activate_gob.sh${NC}"
    echo -e "${GREEN}2.${NC} Start GOB: ${YELLOW}scripts/gob start${NC}"
    echo -e "${GREEN}3.${NC} Check status: ${YELLOW}scripts/gob status${NC}"  
    echo -e "${GREEN}4.${NC} Open in browser: ${YELLOW}http://localhost:50080${NC}"
    echo -e "${GREEN}5.${NC} View logs: ${YELLOW}scripts/gob logs${NC}"
    echo
    echo -e "${CYAN}Configuration Management:${NC}"
    echo -e "  View config: ${YELLOW}cat $DEVICE_CONFIG_FILE${NC}"
    echo -e "  Manual activation: ${YELLOW}conda activate ${CONDA_ENV}${NC}"
    echo -e "  Update packages: ${YELLOW}$CONDA_CMD update --all -c conda-forge${NC}"
    echo
}
