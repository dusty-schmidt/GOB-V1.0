import json
import sys
from pathlib import Path
from agent import LoopData
from python.helpers.extension import Extension

# Add the randomized GOB project to Python path
gob_personality_path = Path(__file__).parent.parent.parent.parent / "dev" / "projects" / "randomized-gob" / "src"
if gob_personality_path.exists():
    sys.path.insert(0, str(gob_personality_path))


class InitialMessage(Extension):

    async def execute(self, **kwargs):
        """
        Add an initial greeting message when first user message is processed.
        Called only once per session via _process_chain method.
        """

        # Only add initial message for main agent (A0), not subordinate agents
        if self.agent.number != 0:
            return

        # If the context already contains log messages, do not add another initial message
        if self.agent.context.log.logs:
            return

        # Try to use personality system, fall back to standard message
        try:
            initial_message = await self._get_personality_initial_message()
        except Exception as e:
            # Fallback to standard initial message on any error
            print(f"[DEBUG] Personality system not available, using standard greeting: {e}")
            initial_message = self.agent.read_prompt("fw.initial_message.md")

        # add initial loop data to agent (for hist_add_ai_response)
        self.agent.loop_data = LoopData(user_message=None)

        # Add the message to history as an AI response
        self.agent.hist_add_ai_response(initial_message)

        # json parse the message, get the tool_args text
        initial_message_json = json.loads(initial_message)
        initial_message_text = initial_message_json.get("tool_args", {}).get("text", "Hello! How can I help you?")

        # Add to log (green bubble) for immediate UI display
        self.agent.context.log.log(
            type="response",
            heading="GOB: the Grandmaster Of Backups",
            content=initial_message_text,
            finished=True,
            update_progress="none",
        )
    
    async def _get_personality_initial_message(self) -> str:
        """Generate AI-powered personality-aware initial message"""
        try:
            from agent_zero_integration import PersonalityAgentZeroIntegration
            
            # Get agent's memory path
            memory_path = getattr(self.agent.config, 'memory_path', './memory')
            
            # Create integration and get personality context
            integration = PersonalityAgentZeroIntegration(memory_path)
            profile = integration.personality_manager.get_daily_personality()
            
            # Build context for AI generation
            identity = profile.identity
            mood_display = profile.mood.replace('_', ' ').title()
            
            # Create system prompt for generating the welcome message
            system_prompt = f"""You are GOB (Grandmaster Of Backups), an AI assistant with a dynamic personality system.

Today's Personality Profile:
- Identity: {identity['meaning']} {identity['emoji']}
- Mood: {mood_display}
- Personality Description: {profile.mood_description}
- Behavioral Style: {profile.combined_prompt[:300]}...

Generate a short, authentic welcome message that embodies today's personality. The message should:
1. Be in character for the specified mood and identity
2. Sound natural and engaging
3. Be 1-3 sentences maximum
4. Show personality without being excessive
5. Be appropriate for starting a conversation

Return ONLY the welcome message text, no additional formatting or explanations."""
            
            user_prompt = "Generate a personalized welcome message for GOB based on today's personality profile."
            
            # Generate the welcome message using the utility LLM
            generated_greeting = await self.agent.call_utility_model(
                system=system_prompt,
                message=user_prompt,
                background=False
            )
            
            # Clean up the generated text
            greeting_text = generated_greeting.strip().strip('"').strip("'")
            
            # Build the Agent Zero response format
            enhanced_message = {
                "thoughts": [
                    f"Today I'm the {identity['meaning']} in {mood_display} mode.",
                    f"My personality: {profile.mood_description}",
                    "Generated a personalized welcome message using AI that embodies today's personality.",
                    "Ready to assist with today's unique character and style."
                ],
                "headline": f"AI-generated greeting as: {identity['meaning']}",
                "tool_name": "response",
                "tool_args": {
                    "text": greeting_text
                }
            }
            
            # Convert to JSON string format expected by Agent Zero
            return json.dumps(enhanced_message, indent=4)
            
        except ImportError as e:
            raise Exception(f"Personality system modules not found: {e}")
        except Exception as e:
            raise Exception(f"Failed to generate personality message: {e}")
