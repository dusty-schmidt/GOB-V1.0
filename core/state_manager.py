"""
GOB System State Manager - Centralized monitoring and state management
"""

import asyncio
import json
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
import uuid
import weakref
import psutil
import numpy as np
import os
from pathlib import Path


class EventType(Enum):
    AGENT_CREATED = "agent_created"
    AGENT_DESTROYED = "agent_destroyed"
    CONVERSATION_START = "conversation_start"
    CONVERSATION_END = "conversation_end"
    MESSAGE_SENT = "message_sent"
    MESSAGE_RECEIVED = "message_received"
    TOOL_EXECUTED = "tool_executed"
    MODEL_CALLED = "model_called"
    MEMORY_OPERATION = "memory_operation"
    ERROR_OCCURRED = "error_occurred"
    PERFORMANCE_METRIC = "performance_metric"
    SYSTEM_STATUS = "system_status"
    EXTENSION_CALLED = "extension_called"


@dataclass
class MonitoringEvent:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: EventType = EventType.SYSTEM_STATUS
    source_id: str = ""
    source_type: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentState:
    id: str
    name: str
    number: int
    profile: str
    status: str = "idle"  # idle, active, thinking, error, destroyed
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message_count: int = 0
    tool_usage: Dict[str, int] = field(default_factory=dict)
    model_calls: int = 0
    errors: int = 0
    subordinates: List[str] = field(default_factory=list)
    superior: Optional[str] = None
    current_task: Optional[str] = None
    context_window_tokens: int = 0
    memory_operations: int = 0
    total_tokens_used: int = 0
    average_response_time: float = 0.0


@dataclass
class ConversationState:
    id: str
    agent_id: str
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_message_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    message_count: int = 0
    status: str = "active"  # active, paused, completed, error
    topic: Optional[str] = None
    participants: List[str] = field(default_factory=list)


@dataclass
class SystemMetrics:
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_used_mb: float = 0.0
    disk_percent: float = 0.0
    active_agents: int = 0
    active_conversations: int = 0
    total_messages: int = 0
    total_tool_calls: int = 0
    total_model_calls: int = 0
    total_errors: int = 0
    average_response_time: float = 0.0
    total_tokens_used: int = 0


@dataclass
class CoreState:
    """Persistent core system state information"""
    # Core service info
    service_name: str = "gob-core"
    version: str = "1.0.0"
    start_time: str = ""
    uptime_seconds: float = 0.0

    # System status
    status: str = "running"
    health: str = "healthy"
    last_updated: str = ""

    # Performance stats
    total_uptime_hours: float = 0.0
    restart_count: int = 0
    error_count: int = 0

    # Current metrics snapshot
    current_cpu_percent: float = 0.0
    current_memory_percent: float = 0.0
    current_disk_percent: float = 0.0

    # Agent system stats
    total_agents_created: int = 0
    total_conversations: int = 0
    total_messages_processed: int = 0

    # Network info
    hostname: str = ""
    local_ip: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class StateManager:
    """
    Centralized state manager for monitoring the entire GOB multi-agent system.
    Provides real-time tracking of agents, conversations, performance, and system health.
    """
    
    def __init__(self, max_events_history: int = 10000, max_metrics_history: int = 1000):
        self.max_events_history = max_events_history
        self.max_metrics_history = max_metrics_history
        
        # Core state storage
        self.agents: Dict[str, AgentState] = {}
        self.conversations: Dict[str, ConversationState] = {}
        self.events: deque = deque(maxlen=max_events_history)
        self.metrics_history: deque = deque(maxlen=max_metrics_history)
        
        # Real-time statistics
        self.current_metrics = SystemMetrics()
        self.event_counters = defaultdict(int)
        self.response_times = deque(maxlen=100)  # Last 100 response times
        
        # Event listeners and callbacks
        self.event_listeners: List[Callable[[MonitoringEvent], None]] = []
        self.metrics_listeners: List[Callable[[SystemMetrics], None]] = []
        
        # Threading and async support
        self._lock = threading.RLock()
        self._running = False
        self._monitor_thread = None
        
        # Performance tracking
        self.start_time = datetime.now(timezone.utc)
        self.last_cleanup = time.time()
        
        # Agent references for cleanup
        self._agent_refs: Dict[str, weakref.ref] = {}

        # Core state file management
        self.state_file_path = Path("/tmp/gob-core-state.json")
        self.core_state = CoreState()
        self._initialize_core_state()
        self._load_persistent_state()
        
    def start_monitoring(self):
        """Start the monitoring system with background metrics collection"""
        with self._lock:
            if self._running:
                return
                
            self._running = True
            self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self._monitor_thread.start()
            
            # Emit startup event
            self.emit_event(EventType.SYSTEM_STATUS, "state_manager", "system", {
                "status": "started",
                "max_events_history": self.max_events_history,
                "max_metrics_history": self.max_metrics_history
            })
    
    def stop_monitoring(self):
        """Stop the monitoring system"""
        with self._lock:
            self._running = False
            if self._monitor_thread:
                self._monitor_thread.join(timeout=5.0)

            # Save final state before stopping
            self.core_state.status = "stopped"
            self._save_core_state()

            self.emit_event(EventType.SYSTEM_STATUS, "state_manager", "system", {
                "status": "stopped"
            })
    
    def _monitor_loop(self):
        """Background monitoring loop for system metrics"""
        last_state_save = time.time()

        while self._running:
            try:
                self._collect_system_metrics()
                self._cleanup_stale_data()

                # Save core state every 30 seconds
                current_time = time.time()
                if current_time - last_state_save >= 30:
                    self._save_core_state()
                    last_state_save = current_time

                time.sleep(1.0)  # Collect metrics every second
            except Exception as e:
                self.emit_event(EventType.ERROR_OCCURRED, "state_manager", "system", {
                    "error": str(e),
                    "context": "metrics_collection"
                })
    
    def _collect_system_metrics(self):
        """Collect current system performance metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Calculate aggregated stats
            active_agents = len([a for a in self.agents.values() if a.status == "active"])
            active_conversations = len([c for c in self.conversations.values() if c.status == "active"])
            total_messages = sum(a.message_count for a in self.agents.values())
            total_tool_calls = sum(sum(a.tool_usage.values()) for a in self.agents.values())
            total_model_calls = sum(a.model_calls for a in self.agents.values())
            total_errors = sum(a.errors for a in self.agents.values())
            total_tokens = sum(a.total_tokens_used for a in self.agents.values())
            
            # Average response time
            avg_response_time = np.mean(list(self.response_times)) if self.response_times else 0.0
            
            # Update current metrics
            self.current_metrics = SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / 1024 / 1024,
                disk_percent=disk.percent,
                active_agents=active_agents,
                active_conversations=active_conversations,
                total_messages=total_messages,
                total_tool_calls=total_tool_calls,
                total_model_calls=total_model_calls,
                total_errors=total_errors,
                average_response_time=avg_response_time,
                total_tokens_used=total_tokens
            )
            
            # Store in history
            self.metrics_history.append(self.current_metrics)
            
            # Notify listeners
            for listener in self.metrics_listeners:
                try:
                    listener(self.current_metrics)
                except Exception as e:
                    pass  # Don't let listener errors break monitoring
                    
        except Exception as e:
            self.emit_event(EventType.ERROR_OCCURRED, "state_manager", "metrics", {
                "error": str(e)
            })
    
    def _cleanup_stale_data(self):
        """Clean up stale references and old data"""
        current_time = time.time()
        if current_time - self.last_cleanup < 60:  # Cleanup every minute
            return
            
        self.last_cleanup = current_time
        
        with self._lock:
            # Clean up destroyed agent references
            dead_refs = []
            for agent_id, weak_ref in self._agent_refs.items():
                if weak_ref() is None:
                    dead_refs.append(agent_id)
            
            for agent_id in dead_refs:
                del self._agent_refs[agent_id]
                if agent_id in self.agents:
                    self.agents[agent_id].status = "destroyed"
    
    def emit_event(self, event_type: EventType, source_id: str, source_type: str, 
                   data: Dict[str, Any], metadata: Dict[str, Any] = None):
        """Emit a monitoring event to all listeners"""
        event = MonitoringEvent(
            event_type=event_type,
            source_id=source_id,
            source_type=source_type,
            data=data,
            metadata=metadata or {}
        )
        
        with self._lock:
            self.events.append(event)
            self.event_counters[event_type] += 1
            
            # Notify event listeners
            for listener in self.event_listeners:
                try:
                    listener(event)
                except Exception as e:
                    pass  # Don't let listener errors break monitoring
    
    def register_agent(self, agent_id: str, agent_name: str, agent_number: int, 
                      profile: str, agent_ref: Any = None) -> AgentState:
        """Register a new agent for monitoring"""
        with self._lock:
            agent_state = AgentState(
                id=agent_id,
                name=agent_name,
                number=agent_number,
                profile=profile
            )
            
            self.agents[agent_id] = agent_state
            
            # Store weak reference for cleanup
            if agent_ref:
                self._agent_refs[agent_id] = weakref.ref(agent_ref)
            
            self.emit_event(EventType.AGENT_CREATED, agent_id, "agent", {
                "name": agent_name,
                "number": agent_number,
                "profile": profile
            })
            
            return agent_state
    
    def update_agent_status(self, agent_id: str, status: str, current_task: str = None):
        """Update agent status and current task"""
        with self._lock:
            if agent_id in self.agents:
                self.agents[agent_id].status = status
                self.agents[agent_id].last_activity = datetime.now(timezone.utc)
                if current_task:
                    self.agents[agent_id].current_task = current_task
                
                self.emit_event(EventType.SYSTEM_STATUS, agent_id, "agent", {
                    "status": status,
                    "task": current_task
                })
    
    def record_message(self, agent_id: str, conversation_id: str, message_type: str, 
                      content_length: int, response_time: float = None):
        """Record a message exchange"""
        with self._lock:
            # Update agent stats
            if agent_id in self.agents:
                self.agents[agent_id].message_count += 1
                self.agents[agent_id].last_activity = datetime.now(timezone.utc)
            
            # Update conversation stats
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = ConversationState(
                    id=conversation_id,
                    agent_id=agent_id,
                    participants=[agent_id]
                )
            
            conv = self.conversations[conversation_id]
            conv.message_count += 1
            conv.last_message_at = datetime.now(timezone.utc)
            
            # Track response time
            if response_time:
                self.response_times.append(response_time)
            
            self.emit_event(EventType.MESSAGE_SENT, agent_id, "message", {
                "conversation_id": conversation_id,
                "message_type": message_type,
                "content_length": content_length,
                "response_time": response_time
            })
    
    def record_tool_usage(self, agent_id: str, tool_name: str, execution_time: float = None,
                         success: bool = True, error_message: str = None):
        """Record tool usage by an agent"""
        with self._lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.tool_usage[tool_name] = agent.tool_usage.get(tool_name, 0) + 1
                agent.last_activity = datetime.now(timezone.utc)
                
                if not success:
                    agent.errors += 1
            
            self.emit_event(EventType.TOOL_EXECUTED, agent_id, "tool", {
                "tool_name": tool_name,
                "execution_time": execution_time,
                "success": success,
                "error_message": error_message
            })
    
    def record_model_call(self, agent_id: str, model_type: str, model_name: str, 
                         tokens_used: int, response_time: float):
        """Record LLM model call"""
        with self._lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.model_calls += 1
                agent.context_window_tokens = tokens_used
                agent.total_tokens_used += tokens_used
                agent.last_activity = datetime.now(timezone.utc)
                
            self.response_times.append(response_time)
            
            self.emit_event(EventType.MODEL_CALLED, agent_id, "model", {
                "model_type": model_type,
                "model_name": model_name,
                "tokens_used": tokens_used,
                "response_time": response_time
            })
    
    def record_memory_operation(self, agent_id: str, operation_type: str, 
                               data_size: int = None, success: bool = True):
        """Record memory operations (embeddings, storage, retrieval)"""
        with self._lock:
            if agent_id in self.agents:
                agent = self.agents[agent_id]
                agent.memory_operations += 1
                agent.last_activity = datetime.now(timezone.utc)
                
                if not success:
                    agent.errors += 1
            
            self.emit_event(EventType.MEMORY_OPERATION, agent_id, "memory", {
                "operation_type": operation_type,
                "data_size": data_size,
                "success": success
            })
    
    def record_extension_call(self, agent_id: str, extension_point: str, extension_name: str,
                             execution_time: float = None):
        """Record extension system calls"""
        self.emit_event(EventType.EXTENSION_CALLED, agent_id, "extension", {
            "extension_point": extension_point,
            "extension_name": extension_name,
            "execution_time": execution_time
        })
    
    def get_agent_hierarchy(self) -> Dict[str, List[str]]:
        """Get the hierarchical structure of agents"""
        hierarchy = {}
        with self._lock:
            for agent_id, agent in self.agents.items():
                if agent.superior:
                    if agent.superior not in hierarchy:
                        hierarchy[agent.superior] = []
                    hierarchy[agent.superior].append(agent_id)
        return hierarchy
    
    def get_recent_events(self, limit: int = 100, event_types: List[EventType] = None) -> List[Dict]:
        """Get recent events, optionally filtered by type"""
        with self._lock:
            events = list(self.events)
            
            if event_types:
                events = [e for e in events if e.event_type in event_types]
            
            # Sort by timestamp (most recent first) and limit
            events.sort(key=lambda x: x.timestamp, reverse=True)
            events = events[:limit]
            
            # Convert to dictionaries for JSON serialization
            return [self._event_to_dict(event) for event in events]
    
    def get_metrics_history(self, limit: int = None) -> List[Dict]:
        """Get system metrics history"""
        with self._lock:
            metrics = list(self.metrics_history)
            if limit:
                metrics = metrics[-limit:]
            
            # Convert metrics with proper datetime handling
            result = []
            for metric in metrics:
                metric_dict = asdict(metric)
                if 'timestamp' in metric_dict and metric_dict['timestamp']:
                    metric_dict['timestamp'] = metric_dict['timestamp'].isoformat()
                result.append(metric_dict)
            return result
    
    def get_agent_summary(self) -> Dict[str, Any]:
        """Get comprehensive agent summary"""
        with self._lock:
            agents_data = {}
            for agent_id, agent in self.agents.items():
                agent_dict = asdict(agent)
                # Convert datetime fields to ISO strings
                for field in ['created_at', 'last_activity']:
                    if field in agent_dict and agent_dict[field]:
                        agent_dict[field] = agent_dict[field].isoformat()
                agents_data[agent_id] = agent_dict
            
            conversations_data = {}
            for cid, conv in self.conversations.items():
                conv_dict = asdict(conv)
                # Convert datetime fields to ISO strings
                for field in ['started_at', 'last_message_at']:
                    if field in conv_dict and conv_dict[field]:
                        conv_dict[field] = conv_dict[field].isoformat()
                conversations_data[cid] = conv_dict
            
            return {
                "agents": agents_data,
                "total_agents": len(self.agents),
                "active_agents": len([a for a in self.agents.values() if a.status == "active"]),
                "agent_hierarchy": self.get_agent_hierarchy(),
                "total_conversations": len(self.conversations),
                "conversations": conversations_data
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        uptime = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        
        # Convert EventType keys to strings for JSON serialization
        event_counts = {}
        for event_type, count in self.event_counters.items():
            if isinstance(event_type, EventType):
                event_counts[event_type.value] = count
            else:
                event_counts[str(event_type)] = count
        
        # Convert current metrics with proper datetime handling
        current_metrics_dict = asdict(self.current_metrics)
        if 'timestamp' in current_metrics_dict:
            current_metrics_dict['timestamp'] = current_metrics_dict['timestamp'].isoformat()
        
        return {
            "uptime_seconds": uptime,
            "current_metrics": current_metrics_dict,
            "event_counts": event_counts,
            "total_events": len(self.events),
            "monitoring_status": "running" if self._running else "stopped"
        }
    
    def _event_to_dict(self, event: MonitoringEvent) -> Dict[str, Any]:
        """Convert MonitoringEvent to dictionary for serialization"""
        return {
            "id": event.id,
            "timestamp": event.timestamp.isoformat(),
            "event_type": event.event_type.value,
            "source_id": event.source_id,
            "source_type": event.source_type,
            "data": event.data,
            "metadata": event.metadata
        }
    
    def add_event_listener(self, listener: Callable[[MonitoringEvent], None]):
        """Add an event listener callback"""
        self.event_listeners.append(listener)
    
    def add_metrics_listener(self, listener: Callable[[SystemMetrics], None]):
        """Add a metrics listener callback"""
        self.metrics_listeners.append(listener)
    
    def remove_event_listener(self, listener: Callable[[MonitoringEvent], None]):
        """Remove an event listener callback"""
        if listener in self.event_listeners:
            self.event_listeners.remove(listener)
    
    def remove_metrics_listener(self, listener: Callable[[SystemMetrics], None]):
        """Remove a metrics listener callback"""
        if listener in self.metrics_listeners:
            self.metrics_listeners.remove(listener)

    def _initialize_core_state(self):
        """Initialize core state with system information"""
        import socket

        # Get hostname and IP
        try:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
        except:
            hostname = "unknown"
            local_ip = "unknown"

        # Initialize core state
        self.core_state.hostname = hostname
        self.core_state.local_ip = local_ip
        self.core_state.start_time = self.start_time.isoformat()
        self.core_state.last_updated = datetime.now(timezone.utc).isoformat()

    def _load_persistent_state(self):
        """Load persistent state from file if it exists"""
        try:
            if self.state_file_path.exists():
                with open(self.state_file_path, 'r') as f:
                    data = json.load(f)

                # Load restart count and total uptime
                if 'restart_count' in data:
                    self.core_state.restart_count = data['restart_count'] + 1
                else:
                    self.core_state.restart_count = 1

                if 'total_uptime_hours' in data:
                    self.core_state.total_uptime_hours = data['total_uptime_hours']

                if 'total_agents_created' in data:
                    self.core_state.total_agents_created = data['total_agents_created']

                if 'total_conversations' in data:
                    self.core_state.total_conversations = data['total_conversations']

                if 'total_messages_processed' in data:
                    self.core_state.total_messages_processed = data['total_messages_processed']

        except Exception as e:
            # If loading fails, start fresh
            self.core_state.restart_count = 1

    def _save_core_state(self):
        """Save current core state to file"""
        try:
            # Update current state
            now = datetime.now(timezone.utc)
            self.core_state.last_updated = now.isoformat()
            self.core_state.uptime_seconds = (now - self.start_time).total_seconds()

            # Update current metrics
            self.core_state.current_cpu_percent = self.current_metrics.cpu_percent
            self.core_state.current_memory_percent = self.current_metrics.memory_percent
            self.core_state.current_disk_percent = self.current_metrics.disk_percent

            # Update agent stats
            self.core_state.total_agents_created = len(self.agents)
            self.core_state.total_conversations = len(self.conversations)
            self.core_state.total_messages_processed = sum(a.message_count for a in self.agents.values())

            # Save to file
            with open(self.state_file_path, 'w') as f:
                json.dump(self.core_state.to_dict(), f, indent=2)

        except Exception as e:
            # Log error but don't crash the service
            self.emit_event(EventType.ERROR_OCCURRED, "state_manager", "system", {
                "error": f"Failed to save core state: {str(e)}",
                "context": "state_file_save"
            })

    def get_core_state(self) -> Dict[str, Any]:
        """Get current core state for monitoring dashboard"""
        self._save_core_state()  # Update state before returning
        return self.core_state.to_dict()


# Global state manager instance
_state_manager: Optional[StateManager] = None


def get_state_manager() -> StateManager:
    """Get the global state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
        _state_manager.start_monitoring()
    return _state_manager


def shutdown_monitoring():
    """Shutdown the global monitoring system"""
    global _state_manager
    if _state_manager:
        _state_manager.stop_monitoring()
        _state_manager = None
