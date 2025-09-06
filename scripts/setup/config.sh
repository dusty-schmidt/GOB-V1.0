#!/bin/bash
# File: scripts/setup/config.sh
# Location: GOBV1 project setup configuration management
# Role: Device configuration creation, loading, and updating functions

# Source utilities and system detection
source "$(dirname "${BASH_SOURCE[0]}")/utils.sh"
source "$(dirname "${BASH_SOURCE[0]}")/system.sh"

# Config validation
is_valid_config() {
    local file="$1"
    [ -f "$file" ] || return 1
    grep -q '"gob_config"' "$file"
}

create_device_config() {
    print_status "step" "Creating device configuration..."
    
    # Check if config already exists
    if [ -f "$DEVICE_CONFIG_FILE" ]; then
        if [ "${VERBOSE:-0}" = "1" ] || [ -t 0 ]; then
            print_status "warning" "Device configuration already exists: $DEVICE_CONFIG_FILE"
            read -p "Do you want to recreate it? (y/N): " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                print_status "info" "Using existing device configuration"
                load_device_config
                return 0
            fi
        else
            # Non-interactive mode - use existing config
            print_status "info" "Using existing device configuration"
            load_device_config
            return 0
        fi
    fi
    
    # Collect system info first for smart defaults
    collect_device_info
    
    # Generate smart defaults
    DEFAULT_NICKNAME="${CURRENT_USER}-$(hostname | cut -d'.' -f1)"
    DEFAULT_FULL_NAME="$CURRENT_USER"
    
    if [ "${VERBOSE:-0}" = "1" ] || [ -t 0 ]; then
        echo -e "${CYAN}Device Configuration Setup${NC}"
        echo "Provide basic info (press Enter to use defaults):"
        echo
        
        # Device nickname with smart default
        read -p "Device Nickname [$DEFAULT_NICKNAME]: " DEVICE_NICKNAME
        export DEVICE_NICKNAME="${DEVICE_NICKNAME:-$DEFAULT_NICKNAME}"
        
        # Full name with default
        read -p "Your Full Name [$DEFAULT_FULL_NAME]: " USER_FULL_NAME
        export USER_FULL_NAME="${USER_FULL_NAME:-$DEFAULT_FULL_NAME}"
        
        # Date of birth with flexible format
        read -p "Date of Birth (MMDDYYYY or YYYY-MM-DD) [01011990]: " USER_DOB_INPUT
        USER_DOB_INPUT="${USER_DOB_INPUT:-01011990}"
    else
        # Non-interactive mode - use defaults
        export DEVICE_NICKNAME="$DEFAULT_NICKNAME"
        export USER_FULL_NAME="$DEFAULT_FULL_NAME"
        USER_DOB_INPUT="01011990"
    fi
    
    # Convert date format
    if [[ $USER_DOB_INPUT =~ ^[0-9]{8}$ ]]; then
        # MMDDYYYY format
        month="${USER_DOB_INPUT:0:2}"
        day="${USER_DOB_INPUT:2:2}"
        year="${USER_DOB_INPUT:4:4}"
        export USER_DOB="$year-$month-$day"
    elif [[ $USER_DOB_INPUT =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        # Already in YYYY-MM-DD format
        export USER_DOB="$USER_DOB_INPUT"
    else
        echo -e "${YELLOW}Invalid date format, using default: 1990-01-01${NC}"
        export USER_DOB="1990-01-01"
    fi
    
    # Use defaults for environment and Python version
    export CONDA_ENV="$DEFAULT_CONDA_ENV"
    export PYTHON_VERSION="$DEFAULT_PYTHON_VERSION"
    
    # Create device config JSON (home-level)
    cat > "$DEVICE_CONFIG_FILE" << EOF
{
  "device": {
    "nickname": "$DEVICE_NICKNAME",
    "hostname": "$HOSTNAME",
    "setup_timestamp": "$SETUP_TIMESTAMP",
    "config_version": "1.1"
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
  "gob_config": {
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

    # Also write a minimal project file to point to the home config (for visibility)
    cat > "$PROJECT_CONFIG_FILE" << EOF
{
  "$ref": "$DEVICE_CONFIG_FILE"
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
    
    if [ ! -f "$DEVICE_CONFIG_FILE" ] || ! is_valid_config "$DEVICE_CONFIG_FILE"; then
        print_status "warning" "No device configuration found, using defaults"
        export CONDA_ENV="$DEFAULT_CONDA_ENV"
        export PYTHON_VERSION="$DEFAULT_PYTHON_VERSION"
        return 0
    fi
    
    # Extract values from JSON (simple parsing for bash)
    export DEVICE_NICKNAME=$(grep '"nickname"' "$DEVICE_CONFIG_FILE" | sed 's/.*"nickname":[[:space:]]*"\([^"]*\)".*/\1/')
    export USER_FULL_NAME=$(grep '"full_name"' "$DEVICE_CONFIG_FILE" | sed 's/.*"full_name":[[:space:]]*"\([^"]*\)".*/\1/')
    # Extract gob_config values
    export CONDA_ENV=$(grep -E '"conda_environment"' "$DEVICE_CONFIG_FILE" | head -1 | sed 's/.*"conda_environment":[[:space:]]*"\([^"]*\)".*/\1/')
    export PYTHON_VERSION=$(grep -E '"python_version"' "$DEVICE_CONFIG_FILE" | head -1 | sed 's/.*"python_version":[[:space:]]*"\([^"]*\)".*/\1/')
    
    # Use defaults if extraction failed
    export CONDA_ENV="${CONDA_ENV:-$DEFAULT_CONDA_ENV}"
    export PYTHON_VERSION="${PYTHON_VERSION:-$DEFAULT_PYTHON_VERSION}"
    
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
                CURRENT_TIME=$(get_timestamp)
                sed -i.bak 's/"last_updated":[[:space:]]*"[^"]*"/"last_updated": "'"$CURRENT_TIME"'"/' "$DEVICE_CONFIG_FILE"
                ;;
        esac
        # Remove backup file
        rm -f "${DEVICE_CONFIG_FILE}.bak"
    fi
}

check_if_setup_complete() {
    if [ -f "$DEVICE_CONFIG_FILE" ] && is_valid_config "$DEVICE_CONFIG_FILE"; then
        local setup_complete=$(grep '"setup_completed"' "$DEVICE_CONFIG_FILE" | grep -q 'true' && echo "true" || echo "false")
        local env_exists=false
        local conda_available=false
        
        # Load existing config
        load_device_config
        
        # Check if conda is available
        if command_exists conda || command_exists mamba; then
            conda_available=true
            if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
                source "$HOME/miniconda3/etc/profile.d/conda.sh"
            fi
        fi
        
        # Check if environment exists
        if $conda_available && conda env list | grep -q "^$CONDA_ENV "; then
            env_exists=true
        fi
        
        if [ "$setup_complete" = "true" ] && [ "$conda_available" = "true" ] && [ "$env_exists" = "true" ]; then
            echo
            print_status "success" "Setup already completed for this device!"
            echo
            echo -e "${CYAN}Current Configuration:${NC}"
            echo -e "  Device: ${GREEN}$DEVICE_NICKNAME${NC}"
            echo -e "  User: ${GREEN}$USER_FULL_NAME${NC}"
            echo -e "  Environment: ${GREEN}$CONDA_ENV${NC}"
            echo -e "  Conda: ${GREEN}$(conda --version)${NC}"
            echo
            echo -e "${CYAN}To get started:${NC}"
            echo -e "  ${GREEN}source ./activate_gob.sh${NC}"
            echo -e "  ${GREEN}scripts/gob start${NC}"
            echo -e "\n${CYAN}Config:${NC} ${GREEN}$DEVICE_CONFIG_FILE${NC}"
            echo
            echo -e "${YELLOW}To force a fresh setup, delete: $DEVICE_CONFIG_FILE${NC}"
            echo
            return 0
        fi
    fi
    return 1
}
