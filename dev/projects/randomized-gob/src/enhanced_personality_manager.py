#!/usr/bin/env python3
"""
Enhanced Personality Manager for GOB - Mood-Based System

Implements sophisticated daily personality variation with probabilistic mood selection,
specialized prompts, and Agent Zero integration.
"""

import json
import random
from datetime import datetime, date
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from acronym_parser import AcronymParser, Identity
from personality_config import PersonalityConfig

@dataclass
class MoodState:
    """Represents current mood state"""
    mood: str
    probability: int
    description: str
    tone: str
    acronym_categories: List[str]
    special_persona: bool = False

@dataclass 
class PersonalityProfile:
    """Complete daily personality profile"""
    date: str
    mood: str
    mood_description: str
    identity: Dict
    combined_prompt: str
    created_at: str

class EnhancedPersonalityManager:
    """Advanced personality system with moods and state management"""
    
    # Configuration now loaded from PersonalityConfig instead of hardcoded
    
    def __init__(self, agent_memory_path: str = None, acronym_file_path: str = None, config_file: str = None):
        """Initialize enhanced personality manager"""
        self.acronym_parser = AcronymParser(acronym_file_path)
        self.personality_config = PersonalityConfig(config_file)
        
        # Load configuration data
        self.mood_system = self.personality_config.get_mood_system()
        self.mood_prompts = self.personality_config.get_mood_prompts()
        self.greeting_templates = self.personality_config.get_greeting_templates()
        
        # Set up state management
        if agent_memory_path:
            self.memory_path = Path(agent_memory_path)
        else:
            # Default path for testing
            self.memory_path = Path(__file__).parent.parent / "test_memory"
            
        self.memory_path.mkdir(exist_ok=True)
        self.state_file = self.memory_path / "personality_state.json"
        self.behavior_file = self.memory_path / "behaviour.md" 
        self.history_file = self.memory_path / "personality_history.json"
        
        self.current_profile: Optional[PersonalityProfile] = None
        
    def select_daily_mood(self, random_seed: Optional[int] = None) -> str:
        """Select mood based on weighted probabilities"""
        if random_seed is None:
            # Use date as seed for consistent daily selection
            random_seed = int(datetime.now().strftime("%Y%m%d"))
        
        random.seed(random_seed)
        rand_num = random.randint(1, 100)
        
        cumulative = 0
        for mood, config in self.mood_system.items():
            cumulative += config["probability"]
            if rand_num <= cumulative:
                return mood
        
        return "professional"  # Fallback
    
    def select_mood_appropriate_identity(self, mood: str) -> Identity:
        """Select identity appropriate for the current mood"""
        mood_config = self.mood_system.get(mood, self.mood_system["professional"])
        category_filter = mood_config["acronym_categories"]
        
        return self.acronym_parser.get_random_identity(category_filter)
    
    def get_daily_personality(self) -> PersonalityProfile:
        """Get today's complete personality profile"""
        if self.should_regenerate():
            self.current_profile = self.generate_new_profile()
            
        return self.current_profile
    
    def should_regenerate(self) -> bool:
        """Check if personality should be regenerated for today"""
        if self.current_profile is None:
            return True
            
        # Check if we're on a new day
        today = datetime.now().date().isoformat()
        return self.current_profile.date != today
    
    def generate_new_profile(self) -> PersonalityProfile:
        """Generate complete new daily personality"""
        today = datetime.now().date().isoformat()
        mood = self.select_daily_mood()
        identity = self.select_mood_appropriate_identity(mood)
        mood_description = self.mood_system[mood]["description"]
        
        combined_prompt = self.generate_combined_prompt(mood, identity)
        
        profile = PersonalityProfile(
            date=today,
            mood=mood,
            mood_description=mood_description,
            identity=asdict(identity),
            combined_prompt=combined_prompt,
            created_at=datetime.now().isoformat()
        )
        
        self.persist_profile(profile)
        self.update_behavior_file(profile)
        self.update_history(profile)
        
        return profile
    
    def generate_combined_prompt(self, mood: str, identity: Identity) -> str:
        """Generate comprehensive personality prompt"""
        today = datetime.now().strftime("%Y-%m-%d")
        mood_config = self.mood_system[mood]
        mood_prompt = self.mood_prompts.get(mood, self.mood_prompts["professional"])
        
        # Properly format the mood prompt (unescape \n)
        formatted_mood_prompt = mood_prompt.replace('\\n', '\n')
        
        prompt = f"""# DAILY PERSONALITY - {today}

## Current Identity & Mood
I am the **{identity.acronym}** - **{identity.meaning}** {identity.emoji}
Today's Mood: **{mood.replace('_', ' ').title()}** - {mood_config['description']}

## Personality Integration
{formatted_mood_prompt}

## Identity Context  
Category: {identity.category}
Key Traits: {', '.join(identity.traits)}
Communication Style: {identity.style}

## Behavioral Guidelines
- Maintain all core capabilities and helpfulness
- Apply personality consistently throughout conversations
- Adapt responses to reflect both identity and mood
- Balance character with genuine assistance

---
*This personality profile shapes my responses while preserving my ability to help effectively.*
"""
        return prompt
    
    def persist_profile(self, profile: PersonalityProfile):
        """Save current profile to state file"""
        with open(self.state_file, 'w') as f:
            json.dump(asdict(profile), f, indent=2)
    
    def update_behavior_file(self, profile: PersonalityProfile):
        """Update Agent Zero's behaviour.md file"""
        with open(self.behavior_file, 'w') as f:
            f.write(profile.combined_prompt)
    
    def update_history(self, profile: PersonalityProfile):
        """Update personality history"""
        history = []
        if self.history_file.exists():
            with open(self.history_file) as f:
                history = json.load(f)
        
        # Add current profile (keep last 30 days)
        history.append({
            "date": profile.date,
            "mood": profile.mood,
            "identity_meaning": profile.identity["meaning"],
            "identity_emoji": profile.identity["emoji"]
        })
        
        # Keep only last 30 entries
        history = history[-30:]
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_personality_summary(self) -> str:
        """Get human-readable personality summary"""
        profile = self.get_daily_personality()
        
        mood_display = profile.mood.replace('_', ' ').title()
        identity = profile.identity
        
        return f"Today I'm the **{identity['meaning']}** {identity['emoji']} in **{mood_display}** mode - {profile.mood_description}!"
    
    def get_personality_greeting(self) -> str:
        """Get personality-aware greeting message"""
        profile = self.get_daily_personality()
        mood_config = self.mood_system[profile.mood]
        
        # Get the appropriate greeting style
        greeting_style = mood_config.get('greeting_style', 'formal')
        greeting_template = self.greeting_templates.get(greeting_style, self.greeting_templates['formal'])
        
        # Format the greeting with current identity and mood
        identity_display = profile.identity['meaning']
        mood_display = profile.mood.replace('_', ' ').title()
        
        return greeting_template.format(
            identity=identity_display,
            mood=mood_display
        )
    
    def get_mood_probabilities(self) -> Dict[str, int]:
        """Get mood probability distribution"""
        return {mood: config["probability"] for mood, config in self.mood_system.items()}
    
    def preview_tomorrow(self) -> Tuple[str, str, int]:
        """Preview most likely personality for tomorrow"""
        tomorrow_seed = int((datetime.now().date()).strftime("%Y%m%d")) + 1
        tomorrow_mood = self.select_daily_mood(tomorrow_seed)
        mood_config = self.mood_system[tomorrow_mood]
        
        return tomorrow_mood, mood_config["description"], mood_config["probability"]
    
    def get_recent_history(self, days: int = 7) -> List[Dict]:
        """Get recent personality history"""
        if not self.history_file.exists():
            return []
            
        with open(self.history_file) as f:
            history = json.load(f)
            
        return history[-days:] if history else []

def main():
    """Demo the enhanced personality system"""
    print("🎭 Enhanced GOB Personality System - Demo")
    print("=" * 50)
    
    # Initialize system
    manager = EnhancedPersonalityManager()
    
    try:
        # Get today's personality
        profile = manager.get_daily_personality()
        
        print("📅 Today's Personality Profile:")
        print("-" * 30)
        print(manager.get_personality_summary())
        print()
        
        print("🎲 Mood Probabilities:")
        for mood, prob in manager.get_mood_probabilities().items():
            mood_display = mood.replace('_', ' ').title()
            print(f"   {mood_display}: {prob}%")
        print()
        
        print("🔮 Tomorrow's Preview:")
        tomorrow_mood, tomorrow_desc, tomorrow_prob = manager.preview_tomorrow()
        print(f"   Most likely: {tomorrow_mood.replace('_', ' ').title()} ({tomorrow_prob}%)")
        print(f"   Description: {tomorrow_desc}")
        print()
        
        print("📜 Recent History:")
        history = manager.get_recent_history(5)
        for entry in history:
            print(f"   {entry['date']}: {entry['identity_meaning']} {entry['identity_emoji']} ({entry['mood']})")
        print()
        
        print("💬 Generated Behavior Prompt Preview:")
        print("-" * 40)
        # Show first few lines of the generated prompt
        lines = profile.combined_prompt.split('\n')
        for line in lines[:15]:
            print(f"   {line}")
        print("   ...")
        print()
        
        print("✅ Behavior file generated successfully!")
        print(f"   Location: {manager.behavior_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
