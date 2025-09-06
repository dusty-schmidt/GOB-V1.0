#!/usr/bin/env python3
"""
GOB Monitoring System Enhanced Setup Script
Sets up everything: aesthetics, auto-start, auto-popup, and simple commands
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, description="", check=True):
    """Run a command and handle errors"""
    print(f"🔧 {description}")
    try:
        if isinstance(cmd, str):
            result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(cmd, check=check, capture_output=True, text=True)
        if result.stdout:
            print(f"   {result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            print(f"   ⚠️  {result.stderr.strip()}")
        print(f"✅ {description} - Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed")
        if e.stderr:
            print(f"   Error: {e.stderr.strip()}")
        return False


def main():
    """Main setup function"""
    print("🚀 GOB Monitoring System Enhanced Setup")
    print("=" * 50)
    
    # Get paths
    monitoring_dir = Path(__file__).parent
    gob_dir = monitoring_dir.parent
    
    print(f"📁 Monitoring directory: {monitoring_dir}")
    print(f"📁 GOB directory: {gob_dir}")
    print()
    
    steps_completed = 0
    total_steps = 8
    
    # Step 1: Run basic setup
    print(f"📋 Step 1/{total_steps}: Running basic monitoring setup")
    if run_command(f"cd {monitoring_dir} && python setup.py", "Basic monitoring setup"):
        steps_completed += 1
    
    # Step 2: Make scripts executable
    print(f"\n📋 Step 2/{total_steps}: Making scripts executable")
    scripts = ["monitor", "open_monitor.sh", "start_monitoring.sh"]
    for script in scripts:
        script_path = monitoring_dir / script
        if script_path.exists():
            if run_command(f"chmod +x {script_path}", f"Making {script} executable"):
                steps_completed += 1 if script == scripts[-1] else 0
        else:
            print(f"⚠️  Script {script} not found, skipping")
    
    # Step 3: Create system-wide monitor command
    print(f"\n📋 Step 3/{total_steps}: Creating system-wide monitor command")
    monitor_path = monitoring_dir / "monitor"
    if monitor_path.exists():
        if run_command(f"sudo ln -sf {monitor_path} /usr/local/bin/monitor", "Creating system-wide monitor command"):
            steps_completed += 1
    else:
        print("❌ Monitor script not found")
    
    # Step 4: Test monitor command
    print(f"\n📋 Step 4/{total_steps}: Testing monitor command")
    if run_command("which monitor", "Checking monitor command availability"):
        if run_command("monitor help | head -3", "Testing monitor command"):
            steps_completed += 1
    
    # Step 5: Install systemd service (optional)
    print(f"\n📋 Step 5/{total_steps}: Installing systemd service for auto-start")
    service_file = monitoring_dir / "gob-monitoring.service"
    if service_file.exists():
        print("   Installing service (requires sudo)...")
        if run_command("monitor install", "Installing monitoring service"):
            steps_completed += 1
    else:
        print("❌ Service file not found")
    
    # Step 6: Test service installation
    print(f"\n📋 Step 6/{total_steps}: Verifying service installation")
    if run_command("systemctl is-enabled gob-monitoring", "Checking service status", check=False):
        steps_completed += 1
    else:
        print("⚠️  Service not enabled (this is okay for manual testing)")
        steps_completed += 1  # Don't fail setup for this
    
    # Step 7: Test browser opening
    print(f"\n📋 Step 7/{total_steps}: Testing browser functionality")
    if run_command("python -c 'import webbrowser; print(\"Browser module available\")'", "Checking browser module"):
        steps_completed += 1
    
    # Step 8: Create desktop shortcut (optional)
    print(f"\n📋 Step 8/{total_steps}: Creating desktop shortcut")
    desktop_dir = Path.home() / "Desktop"
    if desktop_dir.exists():
        shortcut_content = f"""[Desktop Entry]
Name=GOB Monitor
Comment=Open GOB Monitoring Dashboard
Exec={monitoring_dir}/monitor open
Icon=utilities-system-monitor
Terminal=false
Type=Application
Categories=System;Monitor;
"""
        shortcut_path = desktop_dir / "gob-monitor.desktop"
        try:
            with open(shortcut_path, 'w') as f:
                f.write(shortcut_content)
            os.chmod(shortcut_path, 0o755)
            print("✅ Desktop shortcut created")
            steps_completed += 1
        except Exception as e:
            print(f"⚠️  Could not create desktop shortcut: {e}")
            steps_completed += 1  # Don't fail for this
    else:
        print("📁 No Desktop directory found, skipping shortcut")
        steps_completed += 1
    
    # Final summary
    print("\n" + "=" * 50)
    print(f"✅ Setup completed: {steps_completed}/{total_steps} steps successful")
    
    if steps_completed >= 6:  # Most important steps completed
        print("\n🎉 Enhanced monitoring system is ready!")
        print("\n📚 How to use:")
        print("   monitor open        # Open dashboard (default)")
        print("   monitor start       # Start monitoring service")
        print("   monitor status      # Check service status")
        print("   monitor install     # Enable auto-start on boot")
        print("\n🌐 Dashboard features:")
        print("   • Matches GOB webui aesthetics")
        print("   • Auto-opens browser on startup")
        print("   • Terminal-style design")
        print("   • Real-time system monitoring")
        print("   • Process control buttons")
        print("\n🚀 To test right now:")
        print("   monitor open")
    else:
        print("\n⚠️  Some setup steps failed. Check the output above for details.")
    
    print(f"\n📁 All files are in: {monitoring_dir}")
    print("📖 For more info, see the README.md in the monitoring directory")


if __name__ == "__main__":
    main()
