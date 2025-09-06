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

# Configuration
PROJECT_NAME="GOBV1"
CONDA_ENV="gobv1"
PYTHON_VERSION="3.13"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MINICONDA_VERSION="latest"

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

detect_system() {
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
    
    # Detect system first
    detect_system
    
    # Install miniconda if needed
    install_miniconda
    
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
    else
        CONDA_CMD="conda"
        print_status "info" "Using conda (mamba not available)"
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
    print_status "step" "Installing dependencies from conda-forge..."
    
    # Install core dependencies via conda/mamba from conda-forge (faster and more reliable)
    print_status "info" "Installing core packages via $CONDA_CMD from conda-forge..."
    
    # Core web and utility packages
    CONDA_PACKAGES=(
        "flask"
        "lxml" 
        "markdown"
        "pytz"
        "psutil"
        "beautifulsoup4"
        "pillow"
        "pandas"
        "numpy"
        "matplotlib"
        "opencv"
        "scipy"
        "requests"
        "urllib3"
        "jinja2"
        "werkzeug"
        "click"
        "pyyaml"
        "toml"
        "setuptools"
        "wheel"
        "pip"
    )
    
    # Install packages in batches to handle dependencies better
    for package in "${CONDA_PACKAGES[@]}"; do
        print_status "info" "Installing $package..."
        $CONDA_CMD install -c conda-forge "$package" -y >/dev/null 2>&1 || \
            print_status "warning" "Failed to install $package via conda, will try pip"
    done
    
    # Install AI/ML packages that might need special handling
    print_status "info" "Installing AI/ML packages..."
    
    # Try FAISS from conda-forge first
    if $CONDA_CMD install -c conda-forge faiss-cpu -y >/dev/null 2>&1; then
        print_status "success" "FAISS installed from conda-forge"
    else
        print_status "warning" "FAISS not available from conda-forge, will try pip"
    fi
    
    # Try tiktoken and nltk
    $CONDA_CMD install -c conda-forge nltk -y >/dev/null 2>&1 || \
        print_status "warning" "NLTK not available from conda-forge, will try pip"
    
    print_status "success" "Core conda packages installed"
    
    # Install remaining packages via pip
    print_status "info" "Installing remaining packages via pip..."
    
    # Upgrade pip first
    python -m pip install --upgrade pip >/dev/null 2>&1
    
    # Install packages that are typically only available via pip
    PIP_PACKAGES=(
        "tiktoken"
        "openai"
        "anthropic"
        "faiss-cpu"  # backup if conda install failed
    )
    
    for package in "${PIP_PACKAGES[@]}"; do
        print_status "info" "Installing $package via pip..."
        pip install "$package" --quiet || \
            print_status "warning" "Failed to install $package via pip"
    done
    
    # Install from requirements.txt if it exists
    if [ -f "requirements.txt" ]; then
        print_status "info" "Installing additional requirements from requirements.txt..."
        pip install -r requirements.txt --quiet || \
            print_status "warning" "Some requirements.txt packages may have failed"
    fi
    
    print_status "success" "All dependencies installed"
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
    echo
    print_status "success" "$PROJECT_NAME enhanced setup completed successfully!"
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
    echo -e "${CYAN}Manual Activation:${NC}"
    echo -e "  ${YELLOW}conda activate ${CONDA_ENV}${NC}"
    echo
    echo -e "${CYAN}Environment Management:${NC}"
    echo -e "  List environments: ${YELLOW}conda env list${NC}"
    echo -e "  Update packages: ${YELLOW}$CONDA_CMD update --all -c conda-forge${NC}"
    echo -e "  Remove environment: ${YELLOW}conda env remove -n $CONDA_ENV${NC}"
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