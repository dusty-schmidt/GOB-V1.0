#!/bin/bash
# GOBV1 Automatic Setup Script

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

print_header() {
    echo -e "${CYAN}=== $PROJECT_NAME Setup ===${NC}"
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

check_prerequisites() {
    print_status "step" "Checking prerequisites..."
    
    # Check if conda or mamba is installed
    if ! command -v conda >/dev/null 2>&1; then
        print_status "error" "Conda not found. Please install Miniconda or Anaconda first."
        echo -e "\n${YELLOW}To install Miniconda:${NC}"
        echo "  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        echo "  bash Miniconda3-latest-Linux-x86_64.sh"
        echo "  source ~/.bashrc"
        exit 1
    fi
    
    print_status "success" "Conda found: $(conda --version)"
    
    # Try to install mamba if not available
    if ! command -v mamba >/dev/null 2>&1; then
        print_status "info" "Installing mamba for faster package management..."
        conda install mamba -c conda-forge -y >/dev/null 2>&1 || true
    fi
    
    if command -v mamba >/dev/null 2>&1; then
        CONDA_CMD="mamba"
        print_status "success" "Mamba available: $(mamba --version | head -1)"
    else
        CONDA_CMD="conda"
        print_status "info" "Using conda (mamba not available)"
    fi
}

setup_environment() {
    print_status "step" "Setting up conda environment..."
    
    # Source conda
    source ~/.bashrc >/dev/null 2>&1 || true
    if command -v mamba >/dev/null 2>&1; then
        eval "$(mamba shell hook --shell bash)" >/dev/null 2>&1 || true
    else
        eval "$(conda shell hook --shell bash)" >/dev/null 2>&1 || true
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
            return 0
        fi
    fi
    
    # Create environment
    print_status "info" "Creating conda environment '$CONDA_ENV' with Python $PYTHON_VERSION..."
    $CONDA_CMD create -n "$CONDA_ENV" python="$PYTHON_VERSION" -y
    print_status "success" "Environment created successfully"
    
    # Activate environment
    print_status "info" "Activating environment..."
    $CONDA_CMD activate "$CONDA_ENV"
    print_status "success" "Environment activated"
}

install_dependencies() {
    print_status "step" "Installing dependencies..."
    
    # Install core dependencies via conda/mamba (faster)
    print_status "info" "Installing core packages via $CONDA_CMD..."
    $CONDA_CMD install -c conda-forge \
        flask \
        lxml \
        markdown \
        pytz \
        psutil \
        tiktoken \
        nltk \
        beautifulsoup4 \
        pillow \
        faiss-cpu \
        pandas \
        numpy \
        matplotlib \
        opencv \
        scipy \
        -y >/dev/null 2>&1 || print_status "warning" "Some conda packages may have failed"
    
    # Install remaining packages via pip
    print_status "info" "Installing remaining packages via pip..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt --quiet || print_status "warning" "Some pip packages may have failed"
        print_status "success" "Python dependencies installed"
    else
        print_status "warning" "requirements.txt not found, skipping pip install"
    fi
}

setup_cli() {
    print_status "step" "Setting up CLI tool..."
    
    # Make gob executable
    chmod +x scripts/gob

    print_status "success" "GOB CLI made executable"
    
    # Offer to create system-wide symlink
    if [ -w "/usr/local/bin" ]; then
        ln -sf "$PROJECT_DIR/scripts/gob" /usr/local/bin/gob
        print_status "success" "CLI tool linked to /usr/local/bin/gob"
    else
        print_status "info" "Creating system-wide symlink (requires sudo)..."
        if sudo ln -sf "$PROJECT_DIR/scripts/gob" /usr/local/biscripts/gob 2>/dev/null; then
            print_status "success" "CLI tool linked to /usr/local/bin/gob"
        else
            print_status "warning" "Could not create system-wide link. Use scripts/gob instead"
        fi
    fi
}

run_verification() {
    print_status "step" "Verifying installation..."
    
    # Test CLI tool
    if scripts/gob help >/dev/null 2>&1; then
        print_status "success" "CLI tool working correctly"
    else
        print_status "error" "CLI tool verification failed"
        return 1
    fi
    
    # Test Python imports
    print_status "info" "Testing Python environment..."
    if $CONDA_CMD run -n "$CONDA_ENV" python -c "import flask, numpy, pandas" 2>/dev/null; then
        print_status "success" "Core Python packages working"
    else
        print_status "warning" "Some Python packages may have issues"
    fi
}

print_completion() {
    echo
    print_status "success" "$PROJECT_NAME setup completed successfully!"
    echo
    echo -e "${CYAN}Next steps:${NC}"
    echo -e "${GREEN}1.${NC} Start GOBV1: ${YELLOW}scripts/gob start${NC}"
    echo -e "${GREEN}2.${NC} Check status: ${YELLOW}scripts/gob status${NC}"  
    echo -e "${GREEN}3.${NC} Open in browser: ${YELLOW}http://localhost:50080${NC}"
    echo -e "${GREEN}4.${NC} View logs: ${YELLOW}scripts/gob logs${NC}"
    echo
    echo -e "${CYAN}Configuration:${NC}"
    echo -e "  Directory: ${PROJECT_DIR}"
    echo -e "  Environment: ${CONDA_ENV}"
    echo -e "  Python: $PYTHON_VERSION"
    echo -e "  URL: http://localhost:50080"
    echo
    echo -e "${YELLOW}To activate the environment manually:${NC}"
    echo -e "  ${CONDA_CMD} activate ${CONDA_ENV}"
    echo
}

# Main execution
main() {
    print_header
    check_prerequisites
    setup_environment
    install_dependencies
    setup_cli
    run_verification
    print_completion
}

# Run main function
main "$@"
