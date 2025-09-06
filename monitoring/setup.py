#!/usr/bin/env python3
"""
GOB Monitoring System Setup Script
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and handle errors"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True


def install_dependencies():
    """Install required Python packages"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        "Installing monitoring system dependencies"
    )


def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    base_dir = Path(__file__).parent
    
    directories = [
        base_dir / "logs",
        base_dir / "data",
        base_dir / "config"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"✅ Created/verified directory: {directory}")
    
    return True


def create_launch_script():
    """Create convenient launch script"""
    print("📜 Creating launch script...")
    
    launch_script = Path(__file__).parent / "start_monitoring.sh"
    launch_content = """#!/bin/bash

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
"""
    
    with open(launch_script, 'w') as f:
        f.write(launch_content)
    
    # Make script executable
    os.chmod(launch_script, 0o755)
    
    print(f"✅ Launch script created: {launch_script}")
    return True


def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    required_modules = [
        "psutil",
        "numpy", 
        "flask",
        "flask_cors"
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - Failed: {e}")
            return False
    
    return True


def main():
    """Main setup function"""
    print("🔧 GOB Monitoring System Setup")
    print("=" * 40)
    
    steps = [
        ("Check Python version", check_python_version),
        ("Install dependencies", install_dependencies),
        ("Create directories", create_directories),
        ("Create launch script", create_launch_script),
        ("Test imports", test_imports)
    ]
    
    for description, step_func in steps:
        print(f"\n📋 Step: {description}")
        if not step_func():
            print(f"\n❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n" + "=" * 40)
    print("✅ Setup completed successfully!")
    print("\n🚀 To start the monitoring system:")
    print("   ./start_monitoring.sh")
    print("   # or")
    print("   python server.py")
    print("\n🌐 Dashboard will be available at: http://localhost:8050")
    print("\n📚 For more options:")
    print("   python server.py --help")


if __name__ == "__main__":
    main()
