#!/bin/bash
# File: activate_gob.sh  
# Location: Project root directory
# Role: Convenience script to activate GOB conda environment

# Source conda
if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
fi

# Activate environment
conda activate gob

echo "GOB environment activated!"
echo "Project directory: /home/ds/GOB"
echo "Python version: $(python --version)"
echo ""
echo "Available commands:"
echo "  scripts/gob start   - Start GOB"
echo "  scripts/gob status  - Check status" 
echo "  scripts/gob logs    - View logs"
