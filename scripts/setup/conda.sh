#!/bin/bash
# File: scripts/setup/conda.sh
# Location: GOBV1 project setup conda management
# Role: Miniconda installation, channel configuration, and environment setup

# Source utilities and system detection
source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"
source "$(dirname "${BASH_SOURCE[0]}")/system.sh"
source "$(dirname "${BASH_SOURCE[0]}")/config.sh"

install_miniconda() {
    print_status "step" "Installing Miniconda..."
    
    # Check if conda is already installed
    if command_exists conda; then
        CONDA_PATH=$(which conda)
        print_status "success" "Conda already installed: $CONDA_PATH"
        return 0
    fi
    
    # Set installation directory
    MINICONDA_DIR="$HOME/miniconda3"
    
    if [ -d "$MINICONDA_DIR" ]; then
        print_status "warning" "Miniconda directory exists but conda not in PATH"
        print_status "info" "Attempting to source conda..."
        if [ -f "$MINICONDA_DIR/etc/profile.d/conda.sh" ]; then
            source "$MINICONDA_DIR/etc/profile.d/conda.sh"
            if command_exists conda; then
                print_status "success" "Conda sourced successfully"
                return 0
            fi
        fi
    fi
    
    print_status "info" "Downloading Miniconda installer..."
    INSTALLER_URL="https://repo.anaconda.com/miniconda/${MINICONDA_INSTALLER}"
    
    if command_exists wget; then
        wget -q "$INSTALLER_URL" -O "/tmp/$MINICONDA_INSTALLER"
    elif command_exists curl; then
        curl -s "$INSTALLER_URL" -o "/tmp/$MINICONDA_INSTALLER"
    else
        print_status "error" "Neither wget nor curl found. Please install one of them."
        exit 1
    fi
    
    if [ ! -f "/tmp/$MINICONDA_INSTALLER" ]; then
        print_status "error" "Failed to download Miniconda installer"
        exit 1
    fi
    
    print_status "info" "Installing Miniconda to $MINICONDA_DIR..."
    bash "/tmp/$MINICONDA_INSTALLER" -b -p "$MINICONDA_DIR" -f
    
    # Clean up installer
    rm -f "/tmp/$MINICONDA_INSTALLER"
    
    # Initialize conda
    print_status "info" "Initializing conda..."
    "$MINICONDA_DIR/bin/conda" init bash >/dev/null 2>&1
    
    # Source conda for current session
    source "$MINICONDA_DIR/etc/profile.d/conda.sh"
    
    if command_exists conda; then
        print_status "success" "Miniconda installed successfully: $(conda --version)"
    else
        print_status "error" "Miniconda installation failed"
        exit 1
    fi
}

configure_conda_channels() {
    print_status "step" "Configuring conda channels with forge priority..."
    
    # Check if channels are already configured properly
    local current_channels=$(conda config --show channels 2>/dev/null || echo "")
    
    # Set conda-forge as highest priority channel (skip if already first)
    if ! echo "$current_channels" | grep -A1 "channels:" | grep -q "conda-forge" || ! echo "$current_channels" | grep -A1 "channels:" | head -2 | tail -1 | grep -q "conda-forge"; then
        conda config --add channels conda-forge 2>/dev/null || true
    fi
    conda config --set channel_priority flexible 2>/dev/null || true
    
    # Add additional useful channels (skip if already present)
    if ! echo "$current_channels" | grep -q "bioconda"; then
        conda config --add channels bioconda 2>/dev/null || true  # For scientific packages
    fi
    if ! echo "$current_channels" | grep -q "pytorch"; then
        conda config --add channels pytorch 2>/dev/null || true   # For ML packages if needed
    fi
    
    # Show channel configuration
    print_status "info" "Channel configuration:"
    conda config --show channels
    
    print_status "success" "Conda channels configured with forge priority"
}

setup_mamba() {
    # Try to install mamba if not available (much faster than conda)
    if ! command_exists mamba; then
        print_status "info" "Installing mamba for faster package management..."
        conda install mamba -c conda-forge -y >/dev/null 2>&1 || true
    fi
    
    if command_exists mamba; then
        export CONDA_CMD="mamba"
        print_status "success" "Mamba available: $(mamba --version | head -1)"
        
        # Configure mamba to use same channels (skip if already configured)
        if ! mamba config --show channels 2>/dev/null | grep -q "conda-forge"; then
            mamba config --add channels conda-forge 2>/dev/null || true
        fi
        mamba config --set channel_priority flexible 2>/dev/null || true
        
        # Update config
        update_device_config "conda_command" "mamba"
    else
        export CONDA_CMD="conda"
        print_status "info" "Using conda (mamba not available)"
        update_device_config "conda_command" "conda"
    fi
}

setup_environment() {
    print_status "step" "Setting up conda environment..."
    
    # Initialize conda for current shell if needed
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    fi
    
    # Check if environment already exists
    if $CONDA_CMD env list | grep -q "^$CONDA_ENV "; then
        if [ "${VERBOSE:-0}" = "1" ] || [ -t 0 ]; then
            print_status "warning" "Environment '$CONDA_ENV' already exists"
            read -p "Do you want to recreate it? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                print_status "info" "Removing existing environment..."
                $CONDA_CMD env remove -n "$CONDA_ENV" -y
            else
                print_status "info" "Using existing environment"
                conda activate "$CONDA_ENV"
                return 0
            fi
        else
            # Non-interactive mode - use existing environment
            conda activate "$CONDA_ENV"
            return 0
        fi
    fi
    
    # Create environment with Python from conda-forge
    print_status "info" "Creating conda environment '$CONDA_ENV' with Python $PYTHON_VERSION from conda-forge..."
    $CONDA_CMD create -n "$CONDA_ENV" -c conda-forge python="$PYTHON_VERSION" -y
    print_status "success" "Environment created successfully"
    
    # Activate environment
    print_status "info" "Activating environment..."
    conda activate "$CONDA_ENV"
    print_status "success" "Environment activated: $(python --version)"
}

check_prerequisites() {
    print_status "step" "Checking and installing prerequisites..."
    
    # Load or create device configuration first
    if [ ! -f "$DEVICE_CONFIG_FILE" ]; then
        create_device_config
    else
        load_device_config
    fi
    
    # Detect system first
    detect_system
    
    # Install miniconda if needed
    install_miniconda
    
    # Configure channels
    configure_conda_channels
    
    # Setup mamba and update config
    setup_mamba
}

# Variant without prompting/creating config (used after prompts)
check_prerequisites_only() {
    print_status "step" "Checking and installing prerequisites..."
    detect_system
    install_miniconda
    configure_conda_channels
    setup_mamba
}

create_activation_script() {
    print_status "step" "Creating environment activation script..."
    
    cat > "$PROJECT_DIR/activate_gob.sh" << EOF
#!/bin/bash
# File: activate_gob.sh  
# Location: Project root directory
# Role: Convenience script to activate GOB conda environment

# Source conda
if [ -f "\$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "\$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "\$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "\$HOME/anaconda3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate $CONDA_ENV

echo "$PROJECT_NAME environment activated!"
echo "Project directory: $PROJECT_DIR"
echo "Python version: \$(python --version)"
echo ""
echo "Available commands:"
echo "  scripts/gob start   - Start $PROJECT_NAME"
echo "  scripts/gob status  - Check status" 
echo "  scripts/gob logs    - View logs"
EOF

    chmod +x "$PROJECT_DIR/activate_gob.sh"
    print_status "success" "Activation script created: ./activate_gob.sh"
}
