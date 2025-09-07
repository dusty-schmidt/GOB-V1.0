#!/bin/bash

# GOB Network Monitor Startup Wrapper
# Uses dedicated gob-monitor conda environment

set -e

# Source conda initialization
source ~/.bashrc

# Activate the dedicated gob-monitor conda environment
if command -v mamba >/dev/null 2>&1; then
    eval "$(mamba shell hook --shell bash)"
    mamba activate gob-monitor
else
    eval "$(conda shell hook --shell bash)"
    conda activate gob-monitor
fi

# Change to GOB directory
cd /home/ds/GOB

# Start the monitor service
exec python /home/ds/GOB/monitor/start_monitor.py
