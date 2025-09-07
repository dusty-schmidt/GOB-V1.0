#!/bin/bash

# GOB Core State Manager Startup Wrapper
# Uses dedicated gob-core conda environment for minimal dependencies

set -e

# Source conda initialization
source ~/.bashrc

# Activate the dedicated gob-core conda environment
if command -v mamba >/dev/null 2>&1; then
    eval "$(mamba shell hook --shell bash)"
    mamba activate gob-core
else
    eval "$(conda shell hook --shell bash)"
    conda activate gob-core
fi

# Change to GOB directory
cd /home/ds/GOB

# Start the core service
exec python /home/ds/GOB/core/start_core.py
