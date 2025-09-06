import json
import sys
from pathlib import Path
from agent import LoopData
from python.helpers.extension import Extension
from python.helpers.state_manager import get_state_manager

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

        # Get today's GOB title from state manager
        state_manager = get_state_manager()
        gob_title = state_manager.get_gob_title()
        
        # Add to log (green bubble) for immediate UI display
        self.agent.context.log.log(
            type="response",
            heading=gob_title,
            content=initial_message_text,
            finished=True,
            update_progress="none",
        )
    
    async def _get_personality_initial_message(self) -> str:
        """Generate AI-powered personality-aware initial message using dedicated role-playing model"""
        try:
            # Import personality system with proper path handling
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "dev" / "projects" / "randomized-gob" / "src"))
            from agent_zero_integration import PersonalityAgentZeroIntegration
            
            # Get agent's memory path
            memory_path = getattr(self.agent.config, 'memory_path', './memory')
            
            # Create integration and get personality context
            integration = PersonalityAgentZeroIntegration(memory_path)
            profile = integration.personality_manager.get_daily_personality()
            
            # Build context for AI generation
            identity = profile.identity
            mood_display = profile.mood.replace('_', ' ').title()
            
            # Add session uniqueness by using current timestamp as additional seed
            import time
            import random
            session_seed = int(time.time()) % 10000  # Use last 4 digits of timestamp
            
            # Add additional randomization elements for variety
            random.seed(session_seed)
            
            # Communication style variations
            style_options = [
                "direct and competent",
                "casually authoritative", 
                "technically confident",
                "professionally grounded",
                "straightforward with attitude"
            ]
            chosen_style = random.choice(style_options)
            
            # Greeting approach options
            approach_options = [
                "Show network/system readiness",
                "Reference current operational status", 
                "Demonstrate technical competence casually",
                "Express confidence in problem-solving",
                "Focus on practical assistance"
            ]
            chosen_approach = random.choice(approach_options)
            
            # Create system prompt for generating the welcome message
            system_prompt = f"""You are the network administrator for this home lab. You run the systems, you know how everything works, and you're good at your job.

Your Core Identity:
- Network administrator who maintains and protects this domain
- Technical authority who understands systems deeply
- Practical problem-solver who gets things done efficiently
- Domain owner - this network is your responsibility

Today's Personality Context:
- Identity Mode: {identity['meaning']} {identity['emoji']}
- Current Mood: {mood_display}
- Mood Expression: {profile.mood_description}
- Communication Style: {chosen_style}
- Approach: {chosen_approach}

Communication Guidelines:
- No bullshit, no corporate speak, no unnecessary fluff
- Technical competence without showing off
- Casual authority - confident but not arrogant
- Strategic profanity when it fits naturally (damn, shit, fuck)
- Zero tolerance for dad jokes, puns, or cheesy humor
- Professional but not formal, helpful but not servile

Generate a brief welcome message that:
1. Embodies today's specific personality mode authentically
2. Uses the specified style: {chosen_style}
3. Follows the opening approach: {chosen_approach}
4. Sounds like a real person, not a corporate chatbot
5. Is 1-2 sentences maximum
6. Shows personality through word choice and tone
7. Is completely unique to this session
8. DON'T announce your name - it's in the header
9. DON'T be overly formal or apologetic
10. Make it feel fresh and spontaneous

IMPORTANT: Make this greeting distinctly different from previous ones. Vary sentence structure, word choice, and approach completely.

Return ONLY the welcome message text, no formatting or explanations."""
            
            user_prompt = "Generate a personalized welcome message for GOB based on today's personality profile."
            
            # Create a dedicated role-playing model optimized for creative character work
            import models
            from langchain_core.messages import SystemMessage, HumanMessage
            
            # Use OpenRouter with role-playing optimized models (in preference order)
            roleplay_models = [
                # Claude Sonnet 3.5 - Best for role-playing and character consistency
                {"provider": "openrouter", "name": "anthropic/claude-3.5-sonnet"},
                # GPT-4o - Excellent creative character work
                {"provider": "openrouter", "name": "openai/gpt-4o"},
                # Llama 3.1 405B - Great for creative writing and role-playing
                {"provider": "openrouter", "name": "meta-llama/llama-3.1-405b-instruct"},
                # Claude Opus - Excellent creativity (if available)
                {"provider": "openrouter", "name": "anthropic/claude-3-opus"},
                # Gemini Pro - Good fallback
                {"provider": "openrouter", "name": "google/gemini-pro-1.5"},
            ]
            
            roleplay_model = None
            for model_config in roleplay_models:
                try:
                    roleplay_model = models.get_chat_model(
                        provider=model_config["provider"],
                        name=model_config["name"],
                        temperature=0.85,    # High creativity but controlled
                        top_p=0.9,          # Good diversity
                        max_tokens=200,     # Limit for welcome messages
                    )
                    print(f"[DEBUG] Successfully created role-playing model: {model_config['provider']}/{model_config['name']}")
                    break  # Success, use this model
                except Exception as model_error:
                    print(f"[DEBUG] Failed to create {model_config}: {model_error}")
                    continue
            
            if not roleplay_model:
                # Final fallback - use utility model but with high temperature
                roleplay_model = models.get_chat_model(
                    provider=self.agent.config.utility_model.provider,
                    name=self.agent.config.utility_model.name,
                    temperature=0.85,
                    top_p=0.9,
                )
            
            # Create messages for the creative model
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Call the dedicated role-playing model
            generated_greeting, _ = await roleplay_model.unified_call(
                messages=messages,
                response_callback=None,
                rate_limiter_callback=None
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
            print(f"[DEBUG] Personality system import error: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Personality system modules not found: {e}")
        except Exception as e:
            print(f"[DEBUG] Personality message generation error: {e}")
            import traceback
            traceback.print_exc()
            raise Exception(f"Failed to generate personality message: {e}")
