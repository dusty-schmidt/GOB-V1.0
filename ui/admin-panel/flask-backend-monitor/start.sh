#!/bin/bash
# GOB Flask Backend Monitor Startup Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOB_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

echo "🚀 Starting GOB Flask Backend Monitor..."
echo "📁 GOB Root: $GOB_ROOT"
echo "📁 Monitor Dir: $SCRIPT_DIR"

# Change to the monitor directory
cd "$SCRIPT_DIR"

# Set Python path to include GOB root
export PYTHONPATH="$GOB_ROOT:$PYTHONPATH"

# Start the Flask server
echo "🌐 Starting Flask server on http://localhost:8050"
python server.py

echo "✅ Flask Backend Monitor stopped"
