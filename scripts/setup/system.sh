#!/bin/bash
# File: scripts/setup/system.sh
# Location: GOBV1 project setup system detection
# Role: System detection, architecture detection, and device information collection

# Source utilities
source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"

collect_device_info() {
    print_status "step" "Collecting device information..."
    
    # Get system info
    export HOSTNAME=$(hostname)
    export OS_NAME=$(uname -s)
    export OS_VERSION=$(uname -r)
    export ARCHITECTURE=$(uname -m)
    
    # Get additional system details
    if command_exists lscpu; then
        export CPU_INFO=$(lscpu | grep "Model name" | sed 's/Model name:[[:space:]]*//' || echo "Unknown")
    elif [[ "$OS_NAME" == "Darwin" ]]; then
        export CPU_INFO=$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "Unknown")
    else
        export CPU_INFO="Unknown"
    fi
    
    # Get memory info
    if command_exists free; then
        export MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
    elif [[ "$OS_NAME" == "Darwin" ]]; then
        MEMORY_BYTES=$(sysctl -n hw.memsize 2>/dev/null || echo "0")
        export MEMORY_GB=$((MEMORY_BYTES / 1024 / 1024 / 1024))
    else
        export MEMORY_GB="Unknown"
    fi
    
    # Get disk space
    export DISK_SPACE=$(df -h "$PROJECT_DIR" | awk 'NR==2{print $4}' || echo "Unknown")
    
    # Get current user
    export CURRENT_USER=$(whoami)
    
    # Get current date/time
    export SETUP_TIMESTAMP=$(get_timestamp)
    
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

detect_system() {
    print_status "step" "Detecting system architecture..."
    
    case "$(uname -s)" in
        Linux*)  
            export SYSTEM="Linux"
            case "$(uname -m)" in
                x86_64) export ARCH="x86_64" ;;
                aarch64|arm64) export ARCH="aarch64" ;;
                *) 
                    print_status "error" "Unsupported architecture: $(uname -m)"
                    exit 1
                    ;;
            esac
            ;;
        Darwin*)
            export SYSTEM="MacOSX"
            case "$(uname -m)" in
                x86_64) export ARCH="x86_64" ;;
                arm64) export ARCH="arm64" ;;
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
    
    export MINICONDA_INSTALLER="Miniconda3-${MINICONDA_VERSION}-${SYSTEM}-${ARCH}.sh"
    print_status "success" "Detected: ${SYSTEM} ${ARCH}"
}
