"""
Monitoring Extension - Before Main LLM Call Hook
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


class MonitoringBeforeMainLLMCall(Extension):
    """Extension to monitor LLM call start events"""
    
    async def execute(self, loop_data=None, **kwargs):
        if not MONITORING_AVAILABLE:
            return
        
        try:
            state_manager = get_state_manager()
            agent_id = f"agent_{self.agent.number}_{self.agent.context.id}"
            
            # Update agent status to thinking
            state_manager.update_agent_status(
                agent_id=agent_id,
                status="thinking",
                current_task="calling_llm_model"
            )
            
            # Record start time for model call tracking
            if loop_data:
                loop_data.params_temporary["llm_call_start_time"] = time.time()
            
        except Exception as e:
            # Fail silently to avoid breaking GOB functionality
            pass
