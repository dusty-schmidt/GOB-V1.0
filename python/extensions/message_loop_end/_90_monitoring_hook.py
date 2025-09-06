"""
Monitoring Extension - Message Loop End Hook
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


class MonitoringMessageLoopEnd(Extension):
    """Extension to monitor message loop end events"""
    
    async def execute(self, loop_data=None, **kwargs):
        if not MONITORING_AVAILABLE:
            return
        
        try:
            state_manager = get_state_manager()
            agent_id = f"agent_{self.agent.number}_{self.agent.context.id}"
            
            # Calculate total response time if we have start time
            response_time = None
            if loop_data and "monitoring_start_time" in loop_data.params_temporary:
                response_time = time.time() - loop_data.params_temporary["monitoring_start_time"]
                del loop_data.params_temporary["monitoring_start_time"]
            
            # Calculate LLM call time if we have it
            llm_call_time = None
            if loop_data and "llm_call_start_time" in loop_data.params_temporary:
                llm_call_time = time.time() - loop_data.params_temporary["llm_call_start_time"]
                del loop_data.params_temporary["llm_call_start_time"]
                
                # Record model call if we have the info
                if hasattr(self.agent, 'get_chat_model'):
                    try:
                        chat_model = self.agent.get_chat_model()
                        model_name = getattr(chat_model, 'model_name', 'unknown')
                        
                        # Estimate tokens used (rough approximation)
                        tokens_used = 0
                        if hasattr(self.agent, 'data') and hasattr(self.agent.data.get('ctx_window', {}), 'get'):
                            ctx_data = self.agent.data.get('ctx_window', {})
                            tokens_used = ctx_data.get('tokens', 0)
                        
                        state_manager.record_model_call(
                            agent_id=agent_id,
                            model_type="chat",
                            model_name=model_name,
                            tokens_used=tokens_used,
                            response_time=llm_call_time
                        )
                    except Exception:
                        pass  # Don't break if model info unavailable
            
            # Record message if we have user message info
            if loop_data and loop_data.user_message:
                conversation_id = self.agent.context.id
                content_length = len(str(loop_data.user_message.content)) if hasattr(loop_data.user_message, 'content') else 0
                
                state_manager.record_message(
                    agent_id=agent_id,
                    conversation_id=conversation_id,
                    message_type="user_message",
                    content_length=content_length,
                    response_time=response_time
                )
            
            # Update agent status back to idle
            state_manager.update_agent_status(
                agent_id=agent_id,
                status="idle",
                current_task=None
            )
            
        except Exception as e:
            # Fail silently to avoid breaking GOB functionality
            pass
