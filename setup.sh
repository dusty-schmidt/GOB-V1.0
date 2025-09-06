#!/bin/bash
# File: setup.sh
# Location: Project root directory
# Role: Main setup script for GOBV1 project - handles Miniconda installation, 
#       environment creation, and dependency management with conda-forge priority

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default Configuration (can be overridden by device config)
PROJECT_NAME="GOBV1"
DEFAULT_CONDA_ENV="gobv1"
DEFAULT_PYTHON_VERSION="3.13"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MINICONDA_VERSION="latest"
DEVICE_CONFIG_FILE="$PROJECT_DIR/device_config.json"

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

collect_device_info() {
    print_status "step" "Collecting device information..."
    
    # Get system info
    HOSTNAME=$(hostname)
    OS_NAME=$(uname -s)
    OS_VERSION=$(uname -r)
    ARCHITECTURE=$(uname -m)
    
    # Get additional system details
    if command -v lscpu >/dev/null 2>&1; then
        CPU_INFO=$(lscpu | grep "Model name" | sed 's/Model name:[[:space:]]*//' || echo "Unknown")
    elif [[ "$OS_NAME" == "Darwin" ]]; then
        CPU_INFO=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Unknown")
    else
        CPU_INFO="Unknown"
    fi
    
    # Get memory info
    if command -v free >/dev/null 2>&1; then
        MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    elif [[ "$OS_NAME" == "Darwin" ]]; then
        MEMORY_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo "0")
        MEMORY_GB=$((MEMORY_BYTES / 1024 / 1024 / 1024))
    else
        MEMORY_GB="Unknown"
    fi
    
    # Get disk space
    DISK_SPACE=$(df -h "$PROJECT_DIR" | awk 'NR==2{print $4}' || echo "Unknown")
    
    # Get current user
    CURRENT_USER=$(whoami)
    
    # Get current date/time
    SETUP_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    echo "System Information Detected:"
    echo "  Hostname: $HOSTNAME"
    echo "  OS: $OS_NAME $OS_VERSION"
    echo "  Architecture: $ARCHITECTURE"
    echo "  CPU: $CPU_INFO"
    echo "  Memory: ${MEMORY_GB}GB"
    echo "  Available Disk: $DISK_SPACE"
    echo "  User: $CURRENT_USER"
    echo
}

create_device_config() {
    print_status "step" "Creating device configuration..."
    
    # Check if config already exists
    if [ -f "$DEVICE_CONFIG_FILE" ]; then
        print_status "warning" "Device configuration already exists: $DEVICE_CONFIG_FILE"
        read -p "Do you want to recreate it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "info" "Using existing device configuration"
            load_device_config
            return 0
        fi
    fi
    
    echo -e "${CYAN}Device Configuration Setup${NC}"
    echo "Please provide the following information:"
    echo
    
    # Collect user information
    read -p "Device Nickname (e.g., 'John-Laptop', 'DevServer01'): " DEVICE_NICKNAME
    while [ -z "$DEVICE_NICKNAME" ]; do
        echo -e "${RED}Device nickname is required${NC}"
        read -p "Device Nickname: " DEVICE_NICKNAME
    done
    
    read -p "Your Full Name: " USER_FULL_NAME
    while [ -z "$USER_FULL_NAME" ]; do
        echo -e "${RED}Full name is required${NC}"
        read -p "Your Full Name: " USER_FULL_NAME
    done
    
    read -p "Date of Birth (YYYY-MM-DD): " USER_DOB
    while [[ ! $USER_DOB =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; do
        echo -e "${RED}Please enter date in YYYY-MM-DD format${NC}"
        read -p "Date of Birth (YYYY-MM-DD): " USER_DOB
    done
    
    # Environment customization
    read -p "Conda Environment Name [$DEFAULT_CONDA_ENV]: " CUSTOM_CONDA_ENV
    CONDA_ENV="${CUSTOM_CONDA_ENV:-$DEFAULT_CONDA_ENV}"
    
    read -p "Python Version [$DEFAULT_PYTHON_VERSION]: " CUSTOM_PYTHON_VERSION
    PYTHON_VERSION="${CUSTOM_PYTHON_VERSION:-$DEFAULT_PYTHON_VERSION}"
    
    # Collect system info
    collect_device_info
    
    # Create device config JSON
    cat > "$DEVICE_CONFIG_FILE" << EOF
{
  "device": {
    "nickname": "$DEVICE_NICKNAME",
    "hostname": "$HOSTNAME",
    "setup_timestamp": "$SETUP_TIMESTAMP",
    "config_version": "1.0"
  },
  "user": {
    "full_name": "$USER_FULL_NAME",
    "date_of_birth": "$USER_DOB",
    "username": "$CURRENT_USER"
  },
  "system": {
    "os_name": "$OS_NAME",
    "os_version": "$OS_VERSION", 
    "architecture": "$ARCHITECTURE",
    "cpu_info": "$CPU_INFO",
    "memory_gb": "$MEMORY_GB",
    "disk_available": "$DISK_SPACE"
  },
  "gobv1_config": {
    "project_name": "$PROJECT_NAME",
    "conda_environment": "$CONDA_ENV",
    "python_version": "$PYTHON_VERSION",
    "project_directory": "$PROJECT_DIR"
  },
  "installation": {
    "conda_command": "",
    "miniconda_path": "",
    "setup_completed": false,
    "last_updated": "$SETUP_TIMESTAMP"
  }
}
EOF

    print_status "success" "Device configuration created: $DEVICE_CONFIG_FILE"
    
    # Display configuration summary
    echo
    echo -e "${CYAN}Configuration Summary:${NC}"
    echo -e "  Device: ${GREEN}$DEVICE_NICKNAME${NC} ($HOSTNAME)"
    echo -e "  User: ${GREEN}$USER_FULL_NAME${NC} (born $USER_DOB)"
    echo -e "  Environment: ${GREEN}$CONDA_ENV${NC} (Python $PYTHON_VERSION)"
    echo -e "  System: ${GREEN}$OS_NAME $ARCHITECTURE${NC}"
    echo
}

load_device_config() {
    print_status "info" "Loading device configuration..."
    
    if [ ! -f "$DEVICE_CONFIG_FILE" ]; then
        print_status "warning" "No device configuration found, using defaults"
        CONDA_ENV="$DEFAULT_CONDA_ENV"
        PYTHON_VERSION="$DEFAULT_PYTHON_VERSION"
        return 0
    fi
    
    # Extract values from JSON (simple parsing for bash)
    DEVICE_NICKNAME=$(grep '"nickname"' "$DEVICE_CONFIG_FILE" | sed 's/.*"nickname":[[:space:]]*"\([^"]*\)".*/\1/')
    USER_FULL_NAME=$(grep '"full_name"' "$DEVICE_CONFIG_FILE" | sed 's/.*"full_name":[[:space:]]*"\([^"]*\)".*/\1/')
    CONDA_ENV=$(grep '"conda_environment"' "$DEVICE_CONFIG_FILE" | sed 's/.*"conda_environment":[[:space:]]*"\([^"]*\)".*/\1/')
    PYTHON_VERSION=$(grep '"python_version"' "$DEVICE_CONFIG_FILE" | sed 's/.*"python_version":[[:space:]]*"\([^"]*\)".*/\1/')
    
    # Use defaults if extraction failed
    CONDA_ENV="${CONDA_ENV:-$DEFAULT_CONDA_ENV}"
    PYTHON_VERSION="${PYTHON_VERSION:-$DEFAULT_PYTHON_VERSION}"
    
    print_status "success" "Configuration loaded for device: $DEVICE_NICKNAME"
}

update_device_config() {
    local key="$1"
    local value="$2"
    
    if [ -f "$DEVICE_CONFIG_FILE" ]; then
        # Simple JSON update using sed (for more complex updates, would use jq)
        case "$key" in
            "conda_command")
                sed -i.bak 's/"conda_command":[[:space:]]*"[^"]*"/"conda_command": "'"$value"'"/' "$DEVICE_CONFIG_FILE"
                ;;
            "setup_completed")
                sed -i.bak 's/"setup_completed":[[:space:]]*[^,}]*/"setup_completed": '"$value"'/' "$DEVICE_CONFIG_FILE"
                ;;
            "last_updated")
                CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
                sed -i.bak 's/"last_updated":[[:space:]]*"[^"]*"/"last_updated": "'"$CURRENT_TIME"'"/' "$DEVICE_CONFIG_FILE"
                ;;
        esac
        # Remove backup file
        rm -f "${DEVICE_CONFIG_FILE}.bak"
    fi
}
    print_status "step" "Detecting system architecture..."
    
    case "$(uname -s)" in
        Linux*)  
            SYSTEM="Linux"
            case "$(uname -m)" in
                x86_64) ARCH="x86_64" ;;
                aarch64|arm64) ARCH="aarch64" ;;
                *) 
                    print_status "error" "Unsupported architecture: $(uname -m)"
                    exit 1
                    ;;
            esac
            ;;
        Darwin*)
            SYSTEM="MacOSX"
            case "$(uname -m)" in
                x86_64) ARCH="x86_64" ;;
                arm64) ARCH="arm64" ;;
                *) 
                    print_status "error" "Unsupported macOS architecture: $(uname -m)"
                    exit 1
                    ;;
            esac
            ;;
        *)
            print_status "error" "Unsupported operating system: $(uname -s)"
            exit 1
            ;;
    esac
    
    MINICONDA_INSTALLER="Miniconda3-${MINICONDA_VERSION}-${SYSTEM}-${ARCH}.sh"
    print_status "success" "Detected: ${SYSTEM} ${ARCH}"
}

install_miniconda() {
    print_status "step" "Installing Miniconda..."
    
    # Check if conda is already installed
    if command -v conda >/dev/null 2>&1; then
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
            if command -v conda >/dev/null 2>&1; then
                print_status "success" "Conda sourced successfully"
                return 0
            fi
        fi
    fi
    
    print_status "info" "Downloading Miniconda installer..."
    INSTALLER_URL="https://repo.anaconda.com/miniconda/${MINICONDA_INSTALLER}"
    
    if command -v wget >/dev/null 2>&1; then
        wget -q "$INSTALLER_URL" -O "/tmp/$MINICONDA_INSTALLER"
    elif command -v curl >/dev/null 2>&1; then
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
    
    if command -v conda >/dev/null 2>&1; then
        print_status "success" "Miniconda installed successfully: $(conda --version)"
    else
        print_status "error" "Miniconda installation failed"
        exit 1
    fi
}

configure_conda_channels() {
    print_status "step" "Configuring conda channels with forge priority..."
    
    # Set conda-forge as highest priority channel
    conda config --add channels conda-forge
    conda config --set channel_priority flexible
    
    # Add additional useful channels
    conda config --add channels bioconda  # For scientific packages
    conda config --add channels pytorch   # For ML packages if needed
    
    # Show channel configuration
    print_status "info" "Channel configuration:"
    conda config --show channels
    
    print_status "success" "Conda channels configured with forge priority"
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
    
    # Update config with conda command info
    update_device_config "conda_command" "$CONDA_CMD"
    
    # Configure channels
    configure_conda_channels
    
    # Try to install mamba if not available (much faster than conda)
    if ! command -v mamba >/dev/null 2>&1; then
        print_status "info" "Installing mamba for faster package management..."
        conda install mamba -c conda-forge -y >/dev/null 2>&1 || true
    fi
    
    if command -v mamba >/dev/null 2>&1; then
        CONDA_CMD="mamba"
        print_status "success" "Mamba available: $(mamba --version | head -1)"
        
        # Configure mamba to use same channels
        mamba config --add channels conda-forge
        mamba config --set channel_priority flexible
        
        # Update config
        update_device_config "conda_command" "mamba"
    else
        CONDA_CMD="conda"
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

install_dependencies() {
    print_status "step" "Installing dependencies from requirements.txt..."
    
    # Check if requirements.txt exists
    if [ ! -f "requirements.txt" ]; then
        print_status "error" "requirements.txt not found in project root"
        print_status "info" "Please ensure requirements.txt exists with version-pinned dependencies"
        exit 1
    fi
    
    print_status "info" "Found requirements.txt - using specified versions"
    
    # First install basic conda packages that are commonly available and stable
    print_status "info" "Installing base packages via $CONDA_CMD from conda-forge..."
    CONDA_BASE_PACKAGES=(
        "pip"
        "setuptools" 
        "wheel"
    )
    
    for package in "${CONDA_BASE_PACKAGES[@]}"; do
        $CONDA_CMD install -c conda-forge "$package" -y >/dev/null 2>&1 || true
    done
    
    # Upgrade pip to latest version
    print_status "info" "Upgrading pip..."
    python -m pip install --upgrade pip >/dev/null 2>&1
    
    # Install all dependencies from requirements.txt with exact versions
    print_status "info" "Installing dependencies from requirements.txt with specified versions..."
    
    # Use pip install with requirements.txt to respect version constraints
    if pip install -r requirements.txt --quiet; then
        print_status "success" "All dependencies installed from requirements.txt"
    else
        print_status "warning" "Some packages from requirements.txt may have failed"
        print_status "info" "Attempting to install packages individually for better error reporting..."
        
        # Try installing line by line for better error reporting
        while IFS= read -r line; do
            # Skip empty lines and comments
            if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
                package_name=$(echo "$line" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | cut -d'!' -f1)
                print_status "info" "Installing: $line"
                if pip install "$line" --quiet; then
                    print_status "success" "$package_name installed"
                else
                    print_status "error" "Failed to install: $line"
                fi
            fi
        done < requirements.txt
    fi
    
    print_status "success" "Dependencies installation completed"
}

setup_cli() {
    print_status "step" "Setting up CLI tool..."
    
    # Make gob executable
    if [ -f "scripts/gob" ]; then
        chmod +x scripts/gob
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

create_activation_script() {
    print_status "step" "Creating environment activation script..."
    
    cat > activate_gobv1.sh << EOF
#!/bin/bash
# File: activate_gobv1.sh  
# Location: Project root directory
# Role: Convenience script to activate GOBV1 conda environment

# Source conda
if [ -f "\$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "\$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "\$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "\$HOME/anaconda3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate $CONDA_ENV

echo "GOBV1 environment activated!"
echo "Project directory: $PROJECT_DIR"
echo "Python version: \$(python --version)"
echo ""
echo "Available commands:"
echo "  scripts/gob start   - Start GOBV1"
echo "  scripts/gob status  - Check status" 
echo "  scripts/gob logs    - View logs"
EOF

    chmod +x activate_gobv1.sh
    print_status "success" "Activation script created: ./activate_gobv1.sh"
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
    if [ -f "scripts/gob" ]; then
        if scripts/gob help >/dev/null 2>&1; then
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
    print_status "success" "$PROJECT_NAME enhanced setup completed successfully!"
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
    echo -e "${GREEN}1.${NC} Activate environment: ${YELLOW}source ./activate_gobv1.sh${NC}"
    echo -e "${GREEN}2.${NC} Start GOBV1: ${YELLOW}scripts/gob start${NC}"
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

# Main execution
main() {
    print_header
    check_prerequisites
    setup_environment  
    install_dependencies
    setup_cli
    create_activation_script
    run_verification
    print_completion
}

# Run main function with all arguments
main "$@"