"""
GOB Process Manager - Independent control of GOB backend processes
"""

import asyncio
import os
import signal
import subprocess
import threading
import time
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional, Dict, Any, List, Callable
import psutil

from .state_manager import get_state_manager, EventType


class ProcessState(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    CRASHED = "crashed"
    ERROR = "error"


class ProcessManager:
    """
    Manages the GOB backend process independently from monitoring.
    Provides start/stop/restart capabilities and health monitoring.
    """
    
    def __init__(self, gob_directory: str = "/home/ds/GOB"):
        self.gob_directory = Path(gob_directory)
        self.process: Optional[subprocess.Popen] = None
        self.state = ProcessState.STOPPED
        self.state_manager = get_state_manager()
        
        # Process monitoring
        self._monitor_thread: Optional[threading.Thread] = None
        self._monitoring = False
        self._last_heartbeat = time.time()
        
        # Startup/shutdown tracking
        self.start_time: Optional[datetime] = None
        self.stop_time: Optional[datetime] = None
        self.restart_count = 0
        self.crash_count = 0
        
        # Process output capture
        self.stdout_buffer: List[str] = []
        self.stderr_buffer: List[str] = []
        self.max_buffer_lines = 1000
        
        # Configuration
        self.startup_timeout = 30  # seconds
        self.shutdown_timeout = 10  # seconds
        self.health_check_interval = 5  # seconds
        self.auto_restart = False
        
        # Callbacks
        self.state_change_callbacks: List[Callable[[ProcessState, ProcessState], None]] = []
        self.output_callbacks: List[Callable[[str, str], None]] = []  # (line, source)
    
    def add_state_change_callback(self, callback: Callable[[ProcessState, ProcessState], None]):
        """Add callback for process state changes"""
        self.state_change_callbacks.append(callback)
    
    def add_output_callback(self, callback: Callable[[str, str], None]):
        """Add callback for process output (line, source)"""
        self.output_callbacks.append(callback)
    
    def _change_state(self, new_state: ProcessState):
        """Change process state and notify callbacks"""
        old_state = self.state
        self.state = new_state
        
        # Emit monitoring event
        self.state_manager.emit_event(
            EventType.SYSTEM_STATUS, 
            "process_manager", 
            "process", 
            {
                "old_state": old_state.value,
                "new_state": new_state.value,
                "pid": self.process.pid if self.process else None,
                "restart_count": self.restart_count,
                "crash_count": self.crash_count
            }
        )
        
        # Notify callbacks
        for callback in self.state_change_callbacks:
            try:
                callback(old_state, new_state)
            except Exception as e:
                pass  # Don't let callback errors break state management
    
    def _emit_output(self, line: str, source: str):
        """Emit process output to callbacks and buffers"""
        # Add to buffer
        if source == "stdout":
            self.stdout_buffer.append(line)
            if len(self.stdout_buffer) > self.max_buffer_lines:
                self.stdout_buffer.pop(0)
        else:
            self.stderr_buffer.append(line)
            if len(self.stderr_buffer) > self.max_buffer_lines:
                self.stderr_buffer.pop(0)
        
        # Notify callbacks
        for callback in self.output_callbacks:
            try:
                callback(line, source)
            except Exception as e:
                pass
    
    async def start_process(self, python_file: str = "run_ui.py", args: List[str] = None) -> bool:
        """Start the GOB process"""
        if self.state in [ProcessState.RUNNING, ProcessState.STARTING]:
            return False
        
        self._change_state(ProcessState.STARTING)
        
        try:
            # Prepare command
            cmd = ["python", python_file]
            if args:
                cmd.extend(args)
            
            # Start process
            self.process = subprocess.Popen(
                cmd,
                cwd=self.gob_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.start_time = datetime.now(timezone.utc)
            self._last_heartbeat = time.time()
            
            # Start monitoring thread
            self._start_monitoring()
            
            # Wait for process to stabilize
            await asyncio.sleep(2)
            
            if self.process.poll() is None:
                self._change_state(ProcessState.RUNNING)
                return True
            else:
                self._change_state(ProcessState.CRASHED)
                self.crash_count += 1
                return False
                
        except Exception as e:
            self._change_state(ProcessState.ERROR)
            self.state_manager.emit_event(
                EventType.ERROR_OCCURRED, 
                "process_manager", 
                "process", 
                {"error": str(e), "context": "start_process"}
            )
            return False
    
    async def stop_process(self, force: bool = False) -> bool:
        """Stop the GOB process"""
        if self.state == ProcessState.STOPPED:
            return True
        
        self._change_state(ProcessState.STOPPING)
        
        try:
            if self.process and self.process.poll() is None:
                if force:
                    # Force kill
                    self.process.kill()
                else:
                    # Graceful shutdown
                    self.process.terminate()
                
                # Wait for shutdown
                try:
                    self.process.wait(timeout=self.shutdown_timeout)
                except subprocess.TimeoutExpired:
                    # Force kill if graceful shutdown failed
                    self.process.kill()
                    self.process.wait(timeout=5)
            
            self._stop_monitoring()
            self.stop_time = datetime.now(timezone.utc)
            self._change_state(ProcessState.STOPPED)
            return True
            
        except Exception as e:
            self._change_state(ProcessState.ERROR)
            self.state_manager.emit_event(
                EventType.ERROR_OCCURRED, 
                "process_manager", 
                "process", 
                {"error": str(e), "context": "stop_process"}
            )
            return False
    
    async def restart_process(self, python_file: str = "run_ui.py", args: List[str] = None) -> bool:
        """Restart the GOB process"""
        self.restart_count += 1
        
        # Stop if running
        if self.state != ProcessState.STOPPED:
            await self.stop_process()
            await asyncio.sleep(1)
        
        # Start again
        return await self.start_process(python_file, args)
    
    def _start_monitoring(self):
        """Start background monitoring of the process"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
    
    def _stop_monitoring(self):
        """Stop background monitoring"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=2)
    
    def _monitor_loop(self):
        """Background monitoring loop for process health"""
        while self._monitoring and self.process:
            try:
                # Check if process is still alive
                if self.process.poll() is not None:
                    # Process has terminated
                    self._handle_process_death()
                    break
                
                # Read output
                self._read_process_output()
                
                # Health check
                self._perform_health_check()
                
                time.sleep(0.1)  # Fast polling for responsiveness
                
            except Exception as e:
                self.state_manager.emit_event(
                    EventType.ERROR_OCCURRED, 
                    "process_manager", 
                    "monitor", 
                    {"error": str(e)}
                )
    
    def _read_process_output(self):
        """Read and process output from the GOB process"""
        if not self.process:
            return
        
        try:
            # Read stdout
            if self.process.stdout:
                while True:
                    try:
                        line = self.process.stdout.readline()
                        if not line:
                            break
                        line = line.rstrip()
                        if line:
                            self._emit_output(line, "stdout")
                    except:
                        break
            
            # Read stderr
            if self.process.stderr:
                while True:
                    try:
                        line = self.process.stderr.readline()
                        if not line:
                            break
                        line = line.rstrip()
                        if line:
                            self._emit_output(line, "stderr")
                    except:
                        break
                        
        except Exception as e:
            pass  # Don't break monitoring for output reading errors
    
    def _perform_health_check(self):
        """Perform health checks on the running process"""
        if not self.process:
            return
        
        current_time = time.time()
        
        # Update heartbeat if process is responsive
        if self.process.poll() is None:
            self._last_heartbeat = current_time
        
        # Check for hanging process
        if current_time - self._last_heartbeat > 300:  # 5 minutes without heartbeat
            self.state_manager.emit_event(
                EventType.ERROR_OCCURRED, 
                "process_manager", 
                "health_check", 
                {"issue": "process_hanging", "last_heartbeat": self._last_heartbeat}
            )
    
    def _handle_process_death(self):
        """Handle unexpected process termination"""
        if not self.process:
            return
        
        exit_code = self.process.returncode
        
        if self.state == ProcessState.STOPPING:
            # Expected shutdown
            self._change_state(ProcessState.STOPPED)
        else:
            # Unexpected crash
            self.crash_count += 1
            self._change_state(ProcessState.CRASHED)
            
            self.state_manager.emit_event(
                EventType.ERROR_OCCURRED, 
                "process_manager", 
                "process", 
                {
                    "event": "process_crashed",
                    "exit_code": exit_code,
                    "crash_count": self.crash_count
                }
            )
            
            # Auto-restart if enabled
            if self.auto_restart:
                asyncio.create_task(self.restart_process())
        
        self._stop_monitoring()
    
    def get_process_info(self) -> Dict[str, Any]:
        """Get comprehensive process information"""
        info = {
            "state": self.state.value,
            "pid": self.process.pid if self.process else None,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "stop_time": self.stop_time.isoformat() if self.stop_time else None,
            "restart_count": self.restart_count,
            "crash_count": self.crash_count,
            "auto_restart": self.auto_restart,
        }
        
        # Add runtime info if process is running
        if self.process and self.process.poll() is None:
            try:
                psutil_process = psutil.Process(self.process.pid)
                info.update({
                    "cpu_percent": psutil_process.cpu_percent(),
                    "memory_mb": psutil_process.memory_info().rss / 1024 / 1024,
                    "uptime_seconds": (datetime.now(timezone.utc) - self.start_time).total_seconds() if self.start_time else 0,
                    "status": psutil_process.status(),
                    "num_threads": psutil_process.num_threads(),
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        return info
    
    def get_recent_output(self, lines: int = 50, source: str = "both") -> Dict[str, List[str]]:
        """Get recent process output"""
        result = {}
        
        if source in ["stdout", "both"]:
            result["stdout"] = self.stdout_buffer[-lines:] if lines > 0 else self.stdout_buffer.copy()
        
        if source in ["stderr", "both"]:
            result["stderr"] = self.stderr_buffer[-lines:] if lines > 0 else self.stderr_buffer.copy()
        
        return result
    
    def clear_output_buffers(self):
        """Clear the output buffers"""
        self.stdout_buffer.clear()
        self.stderr_buffer.clear()
    
    def is_running(self) -> bool:
        """Check if the process is currently running"""
        return self.state == ProcessState.RUNNING and self.process and self.process.poll() is None
    
    def get_uptime(self) -> Optional[float]:
        """Get process uptime in seconds"""
        if self.start_time and self.is_running():
            return (datetime.now(timezone.utc) - self.start_time).total_seconds()
        return None
    
    async def send_signal(self, sig: signal.Signals) -> bool:
        """Send a signal to the process"""
        if not self.process or self.process.poll() is not None:
            return False
        
        try:
            if hasattr(signal, sig.name):
                self.process.send_signal(sig)
                return True
        except Exception as e:
            self.state_manager.emit_event(
                EventType.ERROR_OCCURRED, 
                "process_manager", 
                "signal", 
                {"error": str(e), "signal": sig.name}
            )
        
        return False
