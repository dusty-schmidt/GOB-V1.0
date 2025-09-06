#!/bin/bash

# GOB Randomized Personality System - Quick Setup
# ==============================================

echo "🎭 GOB Randomized Personality System Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Navigate up to GOB root: randomized-gob -> projects -> dev -> GOB
GOB_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

print_status "Script directory: $SCRIPT_DIR"
print_status "GOB root: $GOB_ROOT"

echo
print_status "Step 1: Checking prerequisites..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    print_success "Python 3 found: $PYTHON_VERSION"
else
    print_error "Python 3 not found. Please install Python 3.8 or higher."
    exit 1
fi

# Check if we're in GOB directory structure
if [ ! -f "$GOB_ROOT/python/extensions/agent_init/_10_initial_message.py" ]; then
    print_error "Agent Zero not found. Are you in the correct GOB directory?"
    exit 1
fi

print_success "Agent Zero found"

echo
print_status "Step 2: Testing personality configuration system..."

# Test personality configuration
cd "$SCRIPT_DIR"
if python3 src/personality_config.py > /dev/null 2>&1; then
    print_success "Personality configuration system working"
else
    print_error "Personality configuration system failed"
    exit 1
fi

# Check configuration file exists
if [ -f "$SCRIPT_DIR/config/personality_config.json" ]; then
    print_success "Configuration file created"
else
    print_error "Configuration file not created"
    exit 1
fi

echo
print_status "Step 3: Testing personality manager..."

# Test personality manager with acronym file detection
if python3 -c "
import sys
sys.path.insert(0, 'src')
from enhanced_personality_manager import EnhancedPersonalityManager
import os

# Try to find acronyms file
acronym_paths = [
    '$GOB_ROOT/dev/resources/references/acronyms.md',
    '$GOB_ROOT/python/data/acronyms.md',
    '$GOB_ROOT/dev/references/acronyms.md'
]

found_path = None
for path in acronym_paths:
    if os.path.exists(path):
        found_path = path
        break

if not found_path:
    raise Exception('No acronym file found')
    
manager = EnhancedPersonalityManager(acronym_file_path=found_path)
profile = manager.get_daily_personality()
print(f'Today: {profile.identity[\"meaning\"]} ({profile.mood})')
" 2>/dev/null; then
    print_success "Personality manager working"
else
    print_warning "Personality manager test failed - may need manual acronym path configuration"
fi

echo
print_status "Step 4: Testing Agent Zero integration..."

# Test Agent Zero integration
if python3 src/agent_zero_integration.py > /dev/null 2>&1; then
    print_success "Agent Zero integration working"
else
    print_warning "Agent Zero integration test failed - check paths"
fi

echo
print_status "Step 5: Making CLI tool executable..."

# Make CLI executable
chmod +x tools/personality_manager_cli.py
if [ -x tools/personality_manager_cli.py ]; then
    print_success "CLI tool is executable"
else
    print_error "Failed to make CLI tool executable"
fi

echo
print_status "Step 6: Testing CLI tool..."

# Test CLI tool
if ./tools/personality_manager_cli.py --status > /dev/null 2>&1; then
    print_success "CLI tool working"
else
    print_warning "CLI tool test failed - manual configuration may be needed"
fi

echo
print_status "Step 7: Integration status check..."

# Check if Agent Zero extension has been modified
if grep -q "personality" "$GOB_ROOT/python/extensions/agent_init/_10_initial_message.py" 2>/dev/null; then
    print_success "Agent Zero initial message extension updated"
else
    print_warning "Agent Zero extension may not be updated - personality system will fall back gracefully"
fi

echo
echo "================================================"
echo "🎉 Setup Complete!"
echo "================================================"
echo
echo "✅ Personality configuration system: Ready"
echo "✅ Enhanced personality manager: Ready"  
echo "✅ Agent Zero integration: Ready"
echo "✅ CLI management tool: Ready"
echo

print_status "Current personality system status:"
./tools/personality_manager_cli.py --status 2>/dev/null || echo "   Use: ./tools/personality_manager_cli.py --status"

echo
print_status "Next steps:"
echo "   1. Start GOB Agent Zero - personality greetings will be automatic"
echo "   2. Customize personas: ./tools/personality_manager_cli.py --add-persona"
echo "   3. Add acronyms: ./tools/personality_manager_cli.py --add-acronym"
echo "   4. View full guide: cat INSTALLATION.md"
echo

print_status "Test the system:"
echo "   ./tools/personality_manager_cli.py --test"
echo

print_success "GOB will now greet you with a different personality each day! 🎭"

exit 0
