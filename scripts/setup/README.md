# GOB Modular Setup System

This directory contains a modular setup system that replaces the monolithic `setup.sh` script with smaller, focused modules.

## Structure

```
scripts/setup/
├── __init__.sh           # Main orchestrator that coordinates all modules
├── utils.sh             # Shared utilities, colors, and helper functions
├── system.sh            # System detection and device information collection
├── config.sh            # Device configuration management
├── conda.sh             # Conda/environment management
├── dependencies.sh      # Smart dependency installation with fallbacks
├── cli.sh              # CLI setup and installation verification
└── README.md           # This documentation
```

## Key Features

### Smart Configuration Detection
- Automatically detects if setup has already been completed by checking `device_config.json`
- Uses sensible defaults: environment name "gob", Python 3.12
- Only prompts for essential information (device nickname, user name, date of birth)

### Intelligent Dependency Installation
- Multi-method approach: tries conda/mamba first, falls back to pip
- Batch installation for speed, individual fallback for reliability
- Special handling for problematic packages
- Comprehensive error reporting

### Modular Design Benefits
- **Maintainability**: Each module has a single responsibility
- **Testability**: Individual modules can be tested independently
- **Reusability**: Modules can be used by other scripts
- **Extensibility**: Easy to add new setup steps or modify existing ones

## Usage

### Primary Usage
```bash
# From project root
./setup_new.sh
```

### Direct Module Usage
```bash
# Source the init file to get access to all functions
source scripts/setup/__init__.sh

# Then call individual functions
check_prerequisites
setup_environment
install_dependencies
```

## Configuration

The system creates a `device_config.json` file in the project root with:
- Device information (hostname, nickname, system specs)
- User information (name, username, date of birth)
- Installation state (conda command, environment name, setup completion)

## Environment Details

- **Environment Name**: `gob` (fixed, not prompted)
- **Python Version**: `3.12` (fixed, not prompted)
- **Activation Script**: `activate_gob.sh` (created in project root)
- **Package Manager**: Prefers mamba over conda for speed

## Module Responsibilities

### `utils.sh`
- Color definitions and print functions
- Global variable initialization
- Helper functions (command_exists, get_timestamp)

### `system.sh`
- Operating system and architecture detection
- Hardware information collection (CPU, memory, disk)
- Miniconda installer URL generation

### `config.sh`
- Device configuration file creation and loading
- JSON parsing and updating
- Setup completion checking

### `conda.sh`
- Miniconda installation and initialization
- Conda channel configuration
- Environment creation and activation
- Mamba installation for faster package management

### `dependencies.sh`
- Requirements.txt parsing
- Multi-method package installation (conda → pip → individual)
- Package compatibility handling
- Installation result reporting

### `cli.sh`
- GOB CLI tool setup and linking
- Installation verification (Python environment, package imports, CLI)
- Final completion summary and instructions
