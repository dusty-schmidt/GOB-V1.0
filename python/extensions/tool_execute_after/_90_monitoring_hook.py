"""
Monitoring Extension - Tool Execute After Hook
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


class MonitoringToolExecuteAfter(Extension):
    """Extension to monitor tool execution completion events"""
    
    async def execute(self, response=None, tool_name="", **kwargs):
        if not MONITORING_AVAILABLE:
            return
        
        try:
            state_manager = get_state_manager()
            agent_id = f"agent_{self.agent.number}_{self.agent.context.id}"
            
            # Calculate execution time
            execution_time = None
            if hasattr(self.agent, 'loop_data'):
                start_key = f"tool_start_{tool_name}"
                if start_key in self.agent.loop_data.params_temporary:
                    execution_time = time.time() - self.agent.loop_data.params_temporary[start_key]
                    del self.agent.loop_data.params_temporary[start_key]
            
            # Determine success from response
            success = True
            error_message = None
            if response and hasattr(response, 'success'):
                success = response.success
            elif response and hasattr(response, 'message') and "error" in str(response.message).lower():
                success = False
                error_message = str(response.message)
            
            # Record tool usage
            state_manager.record_tool_usage(
                agent_id=agent_id,
                tool_name=tool_name,
                execution_time=execution_time,
                success=success,
                error_message=error_message
            )
            
            # Update agent status back to active
            state_manager.update_agent_status(
                agent_id=agent_id,
                status="active",
                current_task="processing_response"
            )
            
        except Exception as e:
            # Fail silently to avoid breaking GOB functionality
            pass
