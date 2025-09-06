"""
Monitoring Extension - Agent Initialization Hook
"""

from python.helpers.extension import Extension
import os
import sys

# Add monitoring path to Python path if running
monitoring_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../monitoring"))
if monitoring_path not in sys.path:
    sys.path.append(monitoring_path)

try:
    from core.state_manager import get_state_manager
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False


class MonitoringAgentInit(Extension):
    """Extension to monitor agent initialization events"""
    
    async def execute(self, **kwargs):
        if not MONITORING_AVAILABLE:
            return
        
        try:
            state_manager = get_state_manager()
            
            # Register the agent in monitoring
            agent_id = f"agent_{self.agent.number}_{self.agent.context.id}"
            
            state_manager.register_agent(
                agent_id=agent_id,
                agent_name=self.agent.agent_name,
                agent_number=self.agent.number,
                profile=self.agent.config.profile or "default",
                agent_ref=self.agent
            )
            
            # Update agent hierarchy if this is a subordinate
            if hasattr(self.agent, 'data') and self.agent.data.get("_superior"):
                superior = self.agent.data.get("_superior")
                superior_id = f"agent_{superior.number}_{superior.context.id}"
                
                if superior_id in state_manager.agents:
                    state_manager.agents[superior_id].subordinates.append(agent_id)
                    state_manager.agents[agent_id].superior = superior_id
            
        except Exception as e:
            # Fail silently to avoid breaking GOB functionality
            pass
