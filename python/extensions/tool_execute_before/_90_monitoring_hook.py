"""
Monitoring Extension - Tool Execute Before Hook
"""

from python.helpers.extension import Extension
import os
import sys
import time

# Add monitoring path to Python path if running
monitoring_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../monitoring"))
if monitoring_path not in sys.path:
    sys.path.append(monitoring_path)

try:
    from core.state_manager import get_state_manager
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False


class MonitoringToolExecuteBefore(Extension):
    """Extension to monitor tool execution start events"""
    
    async def execute(self, tool_args=None, tool_name="", **kwargs):
        if not MONITORING_AVAILABLE:
            return
        
        try:
            state_manager = get_state_manager()
            agent_id = f"agent_{self.agent.number}_{self.agent.context.id}"
            
            # Update agent status to thinking
            state_manager.update_agent_status(
                agent_id=agent_id,
                status="thinking",
                current_task=f"executing_tool_{tool_name}"
            )
            
            # Store start time for execution tracking
            if hasattr(self.agent, 'loop_data'):
                self.agent.loop_data.params_temporary[f"tool_start_{tool_name}"] = time.time()
            
        except Exception as e:
            # Fail silently to avoid breaking GOB functionality
            pass
