#!/bin/bash

# Simple progress test
source scripts/setup/progress.sh

echo "Testing Simple Progress"
echo

for step in 1 2 3 4 5 6 7; do
    desc="Step $step: Processing..."
    
    show_progress $step "$desc"
    sleep 1
    
    complete_step $step "✅ Step $step completed"
done

echo
echo "Done!"
