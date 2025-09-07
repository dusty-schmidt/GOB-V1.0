"""
GOB Service Manager - Unified management of all GOB services
Coordinates the startup sequence and health monitoring of:
1. State Manager (core foundation)
2. Monitoring Dashboard 
3. Agent Framework
"""

import asyncio
import os
import subprocess
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import logging

from .state_manager import get_state_manager, EventType


class ServiceStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting" 
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass
class ServiceConfig:
    name: str
    systemd_name: str
    health_check_url: Optional[str] = None
    health_check_port: Optional[int] = None
    dependencies: List[str] = None
    startup_timeout: int = 60
    health_timeout: int = 30


class ServiceManager:
    """
    Manages the complete GOB service ecosystem with proper dependency ordering
    """
    
    def __init__(self, gob_directory: str = "/home/ds/GOB"):
        self.gob_directory = Path(gob_directory)
        self.state_manager = get_state_manager()
        
        # Service definitions with dependency order
        self.services = {
            "core": ServiceConfig(
                name="GOB Core State Manager",
                systemd_name="gob-core",
                health_check_port=8051,  # Internal health check port
                dependencies=[],
                startup_timeout=30
            ),
            "monitoring": ServiceConfig(
                name="GOB Monitoring Dashboard", 
                systemd_name="gob-monitoring",
                health_check_url="http://localhost:8050/api/status",
                health_check_port=8050,
                dependencies=["core"],
                startup_timeout=45
            ),
            "agent": ServiceConfig(
                name="GOB Agent Framework",
                systemd_name="gob-agent", 
                health_check_url="http://localhost:50080",
                health_check_port=50080,
                dependencies=["core", "monitoring"],
                startup_timeout=60
            )
        }
        
        # Setup logging
        self.logger = logging.getLogger("gob.service_manager")
        
    def get_service_status(self, service_name: str) -> ServiceStatus:
        """Get the current status of a systemd service"""
        try:
            result = subprocess.run(
                ["systemctl", "is-active", self.services[service_name].systemd_name],
                capture_output=True, text=True, timeout=10
            )
            
            status_map = {
                "active": ServiceStatus.RUNNING,
                "inactive": ServiceStatus.STOPPED,
                "failed": ServiceStatus.FAILED,
                "activating": ServiceStatus.STARTING,
                "deactivating": ServiceStatus.STOPPING
            }
            
            return status_map.get(result.stdout.strip(), ServiceStatus.UNKNOWN)
            
        except Exception as e:
            self.logger.error(f"Error checking status for {service_name}: {e}")
            return ServiceStatus.UNKNOWN
    
    def check_service_health(self, service_name: str) -> bool:
        """Check if a service is healthy via HTTP health check"""
        config = self.services[service_name]
        
        if not config.health_check_url:
            # For services without HTTP health checks, just check if systemd says it's active
            return self.get_service_status(service_name) == ServiceStatus.RUNNING
        
        try:
            response = requests.get(
                config.health_check_url, 
                timeout=5,
                headers={'User-Agent': 'GOB-ServiceManager/1.0'}
            )
            return response.status_code == 200
            
        except Exception as e:
            self.logger.debug(f"Health check failed for {service_name}: {e}")
            return False
    
    async def wait_for_service_health(self, service_name: str, timeout: int = 60) -> bool:
        """Wait for a service to become healthy"""
        config = self.services[service_name]
        start_time = time.time()
        
        self.logger.info(f"Waiting for {config.name} to become healthy...")
        
        while time.time() - start_time < timeout:
            if self.check_service_health(service_name):
                self.logger.info(f"{config.name} is healthy")
                return True
            
            await asyncio.sleep(2)
        
        self.logger.error(f"{config.name} failed to become healthy within {timeout}s")
        return False
    
    async def start_service(self, service_name: str) -> bool:
        """Start a single service"""
        config = self.services[service_name]
        
        # Check if already running
        if self.get_service_status(service_name) == ServiceStatus.RUNNING:
            if self.check_service_health(service_name):
                self.logger.info(f"{config.name} is already running and healthy")
                return True
        
        self.logger.info(f"Starting {config.name}...")
        
        try:
            # Start the systemd service
            result = subprocess.run(
                ["sudo", "systemctl", "start", config.systemd_name],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to start {config.name}: {result.stderr}")
                return False
            
            # Wait for service to become healthy
            return await self.wait_for_service_health(service_name, config.startup_timeout)
            
        except Exception as e:
            self.logger.error(f"Error starting {config.name}: {e}")
            return False
    
    async def stop_service(self, service_name: str) -> bool:
        """Stop a single service"""
        config = self.services[service_name]
        
        if self.get_service_status(service_name) == ServiceStatus.STOPPED:
            self.logger.info(f"{config.name} is already stopped")
            return True
        
        self.logger.info(f"Stopping {config.name}...")
        
        try:
            result = subprocess.run(
                ["sudo", "systemctl", "stop", config.systemd_name],
                capture_output=True, text=True, timeout=30
            )
            
            if result.returncode != 0:
                self.logger.error(f"Failed to stop {config.name}: {result.stderr}")
                return False
            
            # Wait for service to stop
            start_time = time.time()
            while time.time() - start_time < 30:
                if self.get_service_status(service_name) == ServiceStatus.STOPPED:
                    self.logger.info(f"{config.name} stopped successfully")
                    return True
                await asyncio.sleep(1)
            
            self.logger.warning(f"{config.name} did not stop within timeout")
            return False
            
        except Exception as e:
            self.logger.error(f"Error stopping {config.name}: {e}")
            return False
    
    def get_startup_order(self) -> List[str]:
        """Get the correct startup order based on dependencies"""
        ordered = []
        remaining = set(self.services.keys())
        
        while remaining:
            # Find services with no unmet dependencies
            ready = []
            for service in remaining:
                deps = self.services[service].dependencies or []
                if all(dep in ordered for dep in deps):
                    ready.append(service)
            
            if not ready:
                raise RuntimeError("Circular dependency detected in services")
            
            # Add ready services to order
            for service in sorted(ready):  # Sort for consistent ordering
                ordered.append(service)
                remaining.remove(service)
        
        return ordered
    
    async def start_all_services(self) -> bool:
        """Start all services in the correct dependency order"""
        self.logger.info("Starting all GOB services...")
        
        startup_order = self.get_startup_order()
        self.logger.info(f"Startup order: {' -> '.join(startup_order)}")
        
        for service_name in startup_order:
            success = await self.start_service(service_name)
            if not success:
                self.logger.error(f"Failed to start {service_name}, aborting startup sequence")
                return False
        
        self.logger.info("All GOB services started successfully!")
        return True
    
    async def stop_all_services(self) -> bool:
        """Stop all services in reverse dependency order"""
        self.logger.info("Stopping all GOB services...")
        
        startup_order = self.get_startup_order()
        shutdown_order = list(reversed(startup_order))
        self.logger.info(f"Shutdown order: {' -> '.join(shutdown_order)}")
        
        success = True
        for service_name in shutdown_order:
            if not await self.stop_service(service_name):
                success = False
        
        if success:
            self.logger.info("All GOB services stopped successfully!")
        else:
            self.logger.warning("Some services failed to stop cleanly")
        
        return success
    
    def get_system_status(self) -> Dict[str, Dict]:
        """Get comprehensive status of all services"""
        status = {}
        
        for service_name, config in self.services.items():
            service_status = self.get_service_status(service_name)
            is_healthy = self.check_service_health(service_name)
            
            status[service_name] = {
                "name": config.name,
                "systemd_name": config.systemd_name,
                "status": service_status.value,
                "healthy": is_healthy,
                "dependencies": config.dependencies or [],
                "health_check_url": config.health_check_url
            }
        
        return status


# Global service manager instance
_service_manager: Optional[ServiceManager] = None


def get_service_manager() -> ServiceManager:
    """Get the global service manager instance"""
    global _service_manager
    if _service_manager is None:
        _service_manager = ServiceManager()
    return _service_manager
