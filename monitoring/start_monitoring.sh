#!/bin/bash

# GOB Monitoring System Launch Script
echo "🚀 Starting GOB Monitoring System..."

# Navigate to monitoring directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Start the monitoring server
python server.py "$@"
