#!/usr/bin/env python3
"""
Agent Zero Integration for GOB Randomized Personality System

This module provides the bridge between the personality system and Agent Zero,
including the enhanced initial greeting message that announces today's personality.
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from enhanced_personality_manager import EnhancedPersonalityManager

class PersonalityAgentZeroIntegration:
    """Integrates personality system with Agent Zero framework"""
    
    def __init__(self, agent_memory_path: str):
        """Initialize with Agent Zero's memory path"""
        self.memory_path = Path(agent_memory_path)
        self.personality_manager = EnhancedPersonalityManager(
            agent_memory_path=agent_memory_path,
            acronym_file_path=self._get_acronym_path()
        )
        
    def _get_acronym_path(self) -> str:
        """Get path to acronym database"""
        # Look for acronyms in GOB structure
        possible_paths = [
            "/home/ds/GOB/dev/resources/references/acronyms.md",
            Path(__file__).parent.parent.parent.parent / "dev" / "resources" / "references" / "acronyms.md",
            Path(__file__).parent.parent / "resources" / "acronyms.md", 
            Path("dev") / "resources" / "references" / "acronyms.md"
        ]
        
        for path in possible_paths:
            path_obj = Path(path) if isinstance(path, str) else path
            if path_obj.exists():
                return str(path_obj)
                
        # Fallback - let the manager handle the default
        return None
    
    def get_enhanced_initial_message(self) -> Dict:
        """Generate enhanced initial message with personality announcement"""
        profile = self.personality_manager.get_daily_personality()
        
        # Create personality-aware greeting
        identity = profile.identity
        mood_display = profile.mood.replace('_', ' ').title()
        
        # Generate mood-specific greeting style
        greeting_text = self._generate_personality_greeting(profile, identity, mood_display)
        
        return {
            "thoughts": [
                f"Today I'm the {identity['meaning']} in {mood_display} mode.",
                f"My personality today is: {profile.mood_description}",
                "I should greet the user in a way that reflects today's personality.",
                "I'll announce my daily identity as part of my introduction."
            ],
            "headline": f"Greeting user as today's personality: {identity['meaning']}",
            "tool_name": "response",
            "tool_args": {
                "text": greeting_text
            }
        }
    
    def _generate_personality_greeting(self, profile, identity: Dict, mood_display: str) -> str:
        """Generate personality-appropriate greeting message using configuration system"""
        # Use the enhanced personality manager's greeting system
        return self.personality_manager.get_personality_greeting()
    
    def update_agent_zero_behavior(self) -> bool:
        """Update Agent Zero's behavior file with current personality"""
        try:
            profile = self.personality_manager.get_daily_personality()
            return True
        except Exception as e:
            print(f"Error updating Agent Zero behavior: {e}")
            return False
    
    def get_identity_command_response(self) -> str:
        """Generate response for :identity command"""
        try:
            return self.personality_manager.get_personality_summary()
        except Exception as e:
            return f"Error retrieving personality: {e}"
    
    def get_identity_preview_response(self) -> str:
        """Generate response for :identity preview command"""
        try:
            tomorrow_mood, tomorrow_desc, tomorrow_prob = self.personality_manager.preview_tomorrow()
            return f"Tomorrow I'll most likely be in **{tomorrow_mood.replace('_', ' ').title()}** mode ({tomorrow_prob}% chance) - {tomorrow_desc}"
        except Exception as e:
            return f"Error previewing tomorrow: {e}"
    
    def get_identity_history_response(self, days: int = 7) -> str:
        """Generate response for :identity history command"""
        try:
            history = self.personality_manager.get_recent_history(days)
            if not history:
                return "No personality history available yet."
                
            response = f"**Recent Personality History** (last {len(history)} days):\n"
            for entry in history:
                mood_display = entry['mood'].replace('_', ' ').title()
                response += f"• **{entry['date']}**: {entry['identity_meaning']} {entry['identity_emoji']} ({mood_display})\n"
                
            return response
        except Exception as e:
            return f"Error retrieving history: {e}"


def create_enhanced_initial_message_prompt(agent_memory_path: str) -> str:
    """Create enhanced fw.initial_message.md content with personality"""
    integration = PersonalityAgentZeroIntegration(agent_memory_path)
    enhanced_message = integration.get_enhanced_initial_message()
    
    return f"""```json
{json.dumps(enhanced_message, indent=4)}
```"""


def create_identity_tool_for_agent_zero():
    """Create Agent Zero tool for identity commands"""
    return """# Identity Tool for Agent Zero

This tool allows users to interact with GOB's personality system.

## Usage Examples:
- `:identity` - Show current personality
- `:identity preview` - Preview tomorrow's likely personality  
- `:identity history` - Show recent personality history

## Tool Implementation:

```python
from python.helpers.tool import Tool, Response
from src.agent_zero_integration import PersonalityAgentZeroIntegration

class IdentityTool(Tool):
    async def execute(self, **kwargs):
        command = kwargs.get('command', '').lower().strip()
        
        integration = PersonalityAgentZeroIntegration(self.agent.config.memory_path)
        
        if command == 'preview':
            response = integration.get_identity_preview_response()
        elif command == 'history':
            response = integration.get_identity_history_response()
        else:
            response = integration.get_identity_command_response()
            
        return Response(message=response, break_loop=False)
```
"""


if __name__ == "__main__":
    # Demo the Agent Zero integration
    print("🎭 GOB Agent Zero Integration Demo")
    print("=" * 50)
    
    # Use test memory path
    test_memory = Path(__file__).parent.parent / "test_memory"
    integration = PersonalityAgentZeroIntegration(str(test_memory))
    
    try:
        print("📝 Enhanced Initial Message:")
        print("-" * 30)
        message = integration.get_enhanced_initial_message()
        print(f"Thoughts: {message['thoughts'][0]}")
        print(f"Greeting: {message['tool_args']['text']}")
        print()
        
        print("🎭 Identity Command Responses:")
        print("-" * 30)
        print(f":identity → {integration.get_identity_command_response()}")
        print()
        print(f":identity preview → {integration.get_identity_preview_response()}")
        print()
        
        print("✅ Agent Zero integration ready!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
