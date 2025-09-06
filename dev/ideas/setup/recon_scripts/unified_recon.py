#!/usr/bin/env python3
"""
Unified Reconnaissance Script for Agent Zero Setup

This script demonstrates how all the individual reconnaissance scripts
could be unified to produce structured JSON output for programmatic consumption.

Usage:
    python unified_recon.py [--json] [--verbose]
"""

import json
import sys
import os
import platform
import subprocess
import shutil
import random
from datetime import datetime

def run_cmd(cmd, silent=True):
    """Execute a command and return output, with better error handling."""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            if not silent:
                print(f"Command failed: {cmd}")
                print(f"Error: {result.stderr}")
            return None
    except subprocess.TimeoutExpired:
        if not silent:
            print(f"Command timed out: {cmd}")
        return None
    except Exception as e:
        if not silent:
            print(f"Command error: {cmd} - {e}")
        return None

def detect_os_info():
    """Enhanced OS detection with architecture and WSL detection."""
    system = platform.system()
    info = {
        "system": system,
        "release": platform.release(),
        "architecture": platform.machine(),
        "wsl": False
    }
    
    if system == "Windows":
        info["version"] = platform.version()
        # Check for WSL from Windows side
        wsl_check = run_cmd("wsl --status")
        info["wsl_available"] = wsl_check is not None
        
    elif system == "Darwin":
        info["version"] = platform.mac_ver()[0]
        # Check for Apple Silicon
        info["apple_silicon"] = platform.machine() == "arm64"
        
    elif system == "Linux":
        try:
            import distro
            info["distribution"] = distro.name(pretty=True)
            info["distribution_version"] = distro.version(pretty=True)
        except ImportError:
            info["distribution"] = "Unknown (no distro module)"
            info["distribution_version"] = platform.release()
        
        # Check if running in WSL
        wsl_check = os.path.exists("/proc/version") and "microsoft" in open("/proc/version").read().lower()
        info["wsl"] = wsl_check
        
        # Check for common package managers
        info["package_managers"] = []
        for pm in ["apt", "yum", "dnf", "pacman", "zypper"]:
            if shutil.which(pm):
                info["package_managers"].append(pm)
    
    return info

def detect_hardware():
    """Enhanced hardware detection."""
    hardware = {
        "cpu": {
            "cores": os.cpu_count(),
            "architecture": platform.machine()
        },
        "memory": {},
        "gpu": [],
        "disk": {}
    }
    
    # Memory detection
    try:
        if platform.system() == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        memory_kb = int(line.split()[1])
                        hardware["memory"]["total_gb"] = round(memory_kb / 1024 / 1024, 1)
                        break
        elif platform.system() == "Darwin":
            mem_output = run_cmd("sysctl hw.memsize")
            if mem_output:
                memory_bytes = int(mem_output.split(": ")[1])
                hardware["memory"]["total_gb"] = round(memory_bytes / 1024**3, 1)
        elif platform.system() == "Windows":
            mem_output = run_cmd("wmic computersystem get TotalPhysicalMemory /format:value")
            if mem_output:
                for line in mem_output.split('\n'):
                    if line.startswith("TotalPhysicalMemory="):
                        memory_bytes = int(line.split("=")[1])
                        hardware["memory"]["total_gb"] = round(memory_bytes / 1024**3, 1)
                        break
    except Exception:
        hardware["memory"]["total_gb"] = None
    
    # GPU Detection (enhanced from original)
    system = platform.system()
    if system == "Windows":
        output = run_cmd("wmic path win32_VideoController get name")
        if output:
            lines = [line.strip() for line in output.splitlines() if line.strip() and "Name" not in line]
            for gpu_name in lines:
                hardware["gpu"].append({
                    "name": gpu_name,
                    "vendor": "unknown",
                    "driver_version": None
                })
    elif system == "Linux":
        output = run_cmd("lspci | grep -i 'vga\\|3d\\|2d\\|display'")
        if output:
            for line in output.splitlines():
                gpu_info = {"name": line.strip(), "vendor": "unknown", "driver_version": None}
                if "nvidia" in line.lower():
                    gpu_info["vendor"] = "NVIDIA"
                    # Try to get NVIDIA driver version
                    nvidia_version = run_cmd("nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits")
                    if nvidia_version:
                        gpu_info["driver_version"] = nvidia_version
                elif "amd" in line.lower() or "radeon" in line.lower():
                    gpu_info["vendor"] = "AMD"
                elif "intel" in line.lower():
                    gpu_info["vendor"] = "Intel"
                hardware["gpu"].append(gpu_info)
    elif system == "Darwin":
        output = run_cmd("system_profiler SPDisplaysDataType")
        if output:
            current_gpu = None
            for line in output.splitlines():
                if "Chipset Model" in line:
                    gpu_name = line.split(":")[1].strip()
                    current_gpu = {"name": gpu_name, "vendor": "unknown", "driver_version": None}
                    if "nvidia" in gpu_name.lower():
                        current_gpu["vendor"] = "NVIDIA"
                    elif "amd" in gpu_name.lower() or "radeon" in gpu_name.lower():
                        current_gpu["vendor"] = "AMD"
                    elif "intel" in gpu_name.lower():
                        current_gpu["vendor"] = "Intel"
                    hardware["gpu"].append(current_gpu)
    
    # Disk space detection (for current directory)
    try:
        if platform.system() != "Windows":
            df_output = run_cmd("df -h .")
            if df_output:
                lines = df_output.strip().split('\n')
                if len(lines) > 1:
                    fields = lines[1].split()
                    if len(fields) >= 4:
                        hardware["disk"]["available"] = fields[3]
        else:
            # Windows disk space check
            drive_output = run_cmd('wmic logicaldisk get size,freespace,caption /format:csv')
            if drive_output:
                hardware["disk"]["info"] = "Windows disk info available"
    except Exception:
        hardware["disk"]["available"] = "unknown"
    
    return hardware

def detect_python_env():
    """Enhanced Python environment detection."""
    python_info = {
        "current": {
            "executable": sys.executable,
            "version": platform.python_version()
        },
        "available": [],
        "virtual_env": None
    }
    
    # Check if in virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        python_info["virtual_env"] = sys.prefix
    
    # Find other Python installations
    candidates = ["python", "python3", "python2", "python3.11", "python3.12", "python3.13"]
    seen = set()
    
    for candidate in candidates:
        path = shutil.which(candidate)
        if path and path not in seen:
            seen.add(path)
            try:
                version_output = subprocess.check_output(
                    [path, "--version"], stderr=subprocess.STDOUT, text=True
                ).strip()
                
                # Check if pip is available
                pip_available = subprocess.run(
                    [path, "-m", "pip", "--version"], 
                    capture_output=True, text=True
                ).returncode == 0
                
                python_info["available"].append({
                    "name": candidate,
                    "executable": path,
                    "version": version_output,
                    "pip_available": pip_available
                })
            except Exception:
                python_info["available"].append({
                    "name": candidate,
                    "executable": path,
                    "version": "unknown",
                    "pip_available": False
                })
    
    return python_info

def detect_package_managers():
    """Enhanced package manager detection."""
    managers = {}
    
    # Conda ecosystem
    for tool in ["conda", "mamba", "micromamba"]:
        path = shutil.which(tool)
        if path:
            version_output = run_cmd(f"{tool} --version")
            manager_info = {
                "available": True,
                "executable": path,
                "version": version_output
            }
            
            if tool == "conda":
                # Try to get more conda info
                info_output = run_cmd("conda info --json")
                if info_output:
                    try:
                        conda_info = json.loads(info_output)
                        manager_info["base_env"] = conda_info.get("default_prefix")
                        manager_info["envs_dirs"] = conda_info.get("envs_dirs", [])
                    except json.JSONDecodeError:
                        pass
            
            managers[tool] = manager_info
        else:
            managers[tool] = {"available": False}
    
    return managers

def detect_docker_info():
    """Enhanced Docker detection."""
    docker_info = {"available": False}
    
    docker_path = shutil.which("docker")
    if not docker_path:
        return docker_info
    
    docker_info["available"] = True
    docker_info["executable"] = docker_path
    
    # Version check
    version_output = run_cmd("docker --version")
    if version_output:
        docker_info["version"] = version_output
    
    # Daemon check
    info_output = run_cmd("docker info")
    if info_output and "Server Version" in info_output:
        docker_info["daemon_running"] = True
        
        # Check for Docker Desktop indicators
        docker_info["desktop"] = "Docker Desktop" in info_output
        
        # Check user permissions (Linux)
        if platform.system() == "Linux":
            groups_output = run_cmd("groups")
            docker_info["user_in_docker_group"] = "docker" in (groups_output or "")
    else:
        docker_info["daemon_running"] = False
    
    return docker_info

def generate_device_name():
    """Generate a device name using the original algorithm."""
    adjectives = [
        "swift", "silent", "cosmic", "iron", "bright",
        "shadow", "lucky", "red", "quantum", "storm"
    ]
    nouns = [
        "falcon", "wolf", "tiger", "phoenix", "serpent",
        "dragon", "nebula", "raven", "hammer", "guardian"
    ]
    return f"{random.choice(adjectives)}-{random.choice(nouns)}-{random.randint(100,999)}"

def run_reconnaissance(json_output=False, verbose=False):
    """Run complete reconnaissance and return results."""
    if verbose and not json_output:
        print("🔍 Starting system reconnaissance...")
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "device": {
            "name": generate_device_name(),
            "generated": True
        },
        "os": detect_os_info(),
        "hardware": detect_hardware(),
        "python": detect_python_env(),
        "package_managers": detect_package_managers(),
        "docker": detect_docker_info()
    }
    
    if json_output:
        print(json.dumps(results, indent=2))
    else:
        # Human-readable output
        print(f"Device Name: {results['device']['name']}")
        print(f"OS: {results['os']['system']} ({results['os'].get('distribution', 'N/A')})")
        print(f"Architecture: {results['os']['architecture']}")
        
        if results['hardware']['memory'].get('total_gb'):
            print(f"Memory: {results['hardware']['memory']['total_gb']} GB")
        
        print(f"CPU Cores: {results['hardware']['cpu']['cores']}")
        
        if results['hardware']['gpu']:
            print("GPU(s):")
            for gpu in results['hardware']['gpu']:
                print(f"  - {gpu['name']} ({gpu['vendor']})")
        
        print(f"Python: {results['python']['current']['version']}")
        print(f"  Executable: {results['python']['current']['executable']}")
        
        conda_available = results['package_managers']['conda']['available']
        mamba_available = results['package_managers']['mamba']['available']
        print(f"Conda: {'✅' if conda_available else '❌'}")
        print(f"Mamba: {'✅' if mamba_available else '❌'}")
        
        docker_running = results['docker'].get('daemon_running', False)
        print(f"Docker: {'✅' if docker_running else '❌'}")
        
        if verbose:
            print(f"\n📊 Full reconnaissance completed at {results['timestamp']}")
    
    return results

def main():
    """Main entry point."""
    json_output = '--json' in sys.argv
    verbose = '--verbose' in sys.argv
    
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        return
    
    try:
        run_reconnaissance(json_output=json_output, verbose=verbose)
    except KeyboardInterrupt:
        print("\n❌ Reconnaissance interrupted by user")
        sys.exit(1)
    except Exception as e:
        if json_output:
            print(json.dumps({"error": str(e)}, indent=2))
        else:
            print(f"❌ Error during reconnaissance: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
