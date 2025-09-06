#!/usr/bin/env python3
"""
Test AI-Generated Welcome Messages for GOB Personality System
"""

import sys
import os
from pathlib import Path

# Add the personality system to Python path
sys.path.insert(0, 'dev/projects/randomized-gob/src')

from enhanced_personality_manager import EnhancedPersonalityManager

def simulate_ai_welcome_generation():
    """Simulate what the Agent Zero extension will do"""
    
    # Initialize personality manager with correct paths
    acronym_path = '/home/ds/GOB/dev/resources/references/acronyms.md'
    memory_path = '/home/ds/GOB/memory'
    
    manager = EnhancedPersonalityManager(
        agent_memory_path=memory_path,
        acronym_file_path=acronym_path
    )
    
    # Get today's personality
    profile = manager.get_daily_personality()
    identity = profile.identity
    mood_display = profile.mood.replace('_', ' ').title()
    
    print("🎭 Today's Personality Profile:")
    print(f"   Identity: {identity['meaning']} {identity['emoji']}")
    print(f"   Mood: {mood_display}")
    print(f"   Description: {profile.mood_description}")
    print()
    
    # Build the system prompt that Agent Zero will use
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
    
    print("📝 System Prompt Preview:")
    print("-" * 50)
    print(system_prompt[:400] + "...")
    print()
    
    print("🎯 Expected Format:")
    print("   Heading: GOB: the Grandmaster Of Backups") 
    print("   Content: [AI-generated message in today's personality style]")
    print()
    
    print("✅ Setup Complete!")
    print("   The Agent Zero extension will now use the LLM to generate")
    print("   authentic welcome messages based on the daily personality.")
    print()
    
    # Show what the old template system would have produced for comparison
    old_template_style = manager.get_personality_greeting()
    print("🔄 Old Template vs New AI Generation:")
    print(f"   Old Template: {old_template_style}")
    print("   New AI: [Will be generated dynamically by LLM each time]")
    
if __name__ == "__main__":
    simulate_ai_welcome_generation()
