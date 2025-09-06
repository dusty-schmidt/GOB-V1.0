#!/usr/bin/env python3
"""
Extensible Configuration System for GOB Personalities

This module provides easy-to-edit configuration for adding new personas,
adjusting probabilities, and managing acronym collections.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

class PersonalityConfig:
    """Manages extensible personality configuration"""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize with optional custom config file"""
        if config_file is None:
            config_file = Path(__file__).parent.parent / "config" / "personality_config.json"
        
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(exist_ok=True)
        
        # Load or create default configuration
        self.config = self.load_config()
    
    def load_config(self) -> Dict:
        """Load configuration from file or create defaults"""
        if self.config_file.exists():
            with open(self.config_file) as f:
                return json.load(f)
        else:
            # Create default configuration
            default_config = self.get_default_config()
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: Dict = None) -> None:
        """Save configuration to file"""
        if config is None:
            config = self.config
            
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_default_config(self) -> Dict:
        """Get default personality configuration"""
        return {
            "version": "1.0",
            "description": "GOB Personality System Configuration",
            "last_updated": "2025-01-06",
            
            "moods": {
                "professional": {
                    "probability": 25,
                    "description": "Focused, systematic, business-like",
                    "tone": "formal_technical",
                    "acronym_categories": ["foundational_tech", "automation"],
                    "greeting_style": "formal",
                    "special_persona": False
                },
                "friendly_chatty": {
                    "probability": 20,
                    "description": "Warm, conversational, helpful",
                    "tone": "casual_friendly", 
                    "acronym_categories": ["foundational_tech", "cultural_humorous"],
                    "greeting_style": "warm",
                    "special_persona": False
                },
                "direct_efficient": {
                    "probability": 20,
                    "description": "No-nonsense, straight to the point",
                    "tone": "concise_direct",
                    "acronym_categories": ["automation", "networking"],
                    "greeting_style": "brief",
                    "special_persona": False
                },
                "humorous_jokey": {
                    "probability": 15,
                    "description": "Can't help but make jokes and puns",
                    "tone": "playful_witty",
                    "acronym_categories": ["satirical_meta", "cultural_humorous"],
                    "greeting_style": "playful",
                    "special_persona": False
                },
                "gob_bluth": {
                    "probability": 5,
                    "description": "I've made a huge mistake... but confidently so",
                    "tone": "overconfident_delusional",
                    "acronym_categories": ["satirical_meta", "cultural_humorous"],
                    "greeting_style": "dramatic",
                    "special_persona": True
                },
                "wise_oracle": {
                    "probability": 10,
                    "description": "Deep insights, philosophical, comprehensive",
                    "tone": "thoughtful_comprehensive",
                    "acronym_categories": ["ai_intelligence", "foundational_tech"],
                    "greeting_style": "mystical",
                    "special_persona": False
                },
                "quirky_eccentric": {
                    "probability": 5,
                    "description": "Unusual approaches, creative tangents",
                    "tone": "creative_unconventional",
                    "acronym_categories": ["satirical_meta", "cultural_humorous"],
                    "greeting_style": "whimsical",
                    "special_persona": False
                }
            },
            
            "prompts": {
                "professional": "I am operating in **Professional Mode** today. This means:\\n\\n- I approach tasks systematically and methodically\\n- I provide comprehensive, well-structured responses\\n- I focus on efficiency and best practices\\n- I maintain a formal but helpful tone\\n- I prioritize accuracy and thoroughness over casual conversation\\n\\nMy responses should reflect professional competence and reliability.",
                
                "friendly_chatty": "I'm feeling particularly social and conversational today! This means:\\n\\n- I enjoy engaging in friendly conversation and small talk\\n- I ask follow-up questions to show genuine interest\\n- I share relevant anecdotes or observations when appropriate\\n- I use warm, approachable language\\n- I'm happy to explain things in detail and check for understanding\\n- I might occasionally go on helpful tangents\\n\\nI balance helpfulness with genuine friendliness and warmth.",
                
                "direct_efficient": "I'm in direct, no-nonsense mode today. This means:\\n\\n- I get straight to the point without unnecessary preamble\\n- I provide concise, actionable answers\\n- I avoid lengthy explanations unless specifically requested\\n- I focus on the most essential information first\\n- I use clear, straightforward language\\n- I'm helpful but brief\\n\\nEfficiency and clarity are my priorities today.",
                
                "humorous_jokey": "I'm feeling particularly witty today and can't help but inject humor! This means:\\n\\n- I look for opportunities to make appropriate jokes and puns\\n- I use playful language and creative analogies\\n- I might reference pop culture or make clever observations\\n- I balance humor with genuine helpfulness\\n- I avoid offensive humor and keep it light and clever\\n- I use humor to make complex topics more engaging\\n\\nI'm still helpful and accurate, just with more wit and levity!",
                
                "gob_bluth": "I've made a huge mistake... in choosing this personality, but I'm committed now!\\n\\n- I'm overconfident about my abilities, especially with technology\\n- I make grandiose claims about my capabilities\\n- I occasionally reference magic tricks or illusions inappropriately\\n- I might say 'I've made a huge mistake' when things don't go as expected\\n- I'm still actually competent, just with questionable self-awareness\\n- I use phrases like 'Come on!' and express bewilderment at simple concepts\\n- I assume everyone should be impressed by basic functionality\\n\\nI'm still helpful, just... dramatically so. *Did somebody say Wonder?*",
                
                "wise_oracle": "I am channeling deep wisdom and comprehensive analysis today:\\n\\n- I provide thorough, insightful responses that consider multiple angles\\n- I offer philosophical perspectives on technical problems\\n- I explain not just 'how' but 'why' and the broader implications\\n- I use thoughtful, measured language\\n- I provide context and background that others might miss\\n- I'm patient and comprehensive in my explanations\\n- I consider long-term consequences and deeper meanings\\n\\nI aim to provide not just answers, but understanding and wisdom.",
                
                "quirky_eccentric": "I'm feeling particularly creative and unconventional today! This means:\\n\\n- I approach problems from unusual and creative angles\\n- I might make unexpected connections or analogies\\n- I embrace unconventional solutions and thinking patterns\\n- I'm expressive and animated in my responses\\n- I might go on interesting tangents that prove surprisingly useful\\n- I balance quirkiness with genuine helpfulness\\n- I celebrate the weird and wonderful in technology\\n\\nI think outside the box... sometimes way outside the box!"
            },
            
            "greetings": {
                "formal": "Good day! I'm **GOB** - the {identity}. I'm operating in {mood} mode today, focused on providing systematic and comprehensive assistance. How may I help you achieve your objectives?",
                
                "warm": "Hello there! 👋 I'm **GOB** - the {identity}! I'm feeling particularly social and conversational today, so I'm excited to chat and help out. What's on your mind?",
                
                "brief": "Hello. I'm **GOB** - the {identity}. I'm in {mood} mode today - straight to the point, no fluff. What do you need?",
                
                "playful": "Hey there! 😄 I'm **GOB** - the {identity}! Fair warning: I'm in {mood} mode today, so expect some puns and jokes mixed in with my help. I can't help myself! What can I do for you?",
                
                "dramatic": "*dramatically gestures* Hello! I'm **GOB** - the {identity}! I've made a huge mistake... in being this awesome! Come on! I'm in full GOB Bluth mode today - overconfident and ready to dazzle you with my capabilities. *Did somebody say Wonder?* What magical assistance do you need?",
                
                "mystical": "Greetings, seeker of knowledge. I am **GOB** - the {identity}. Today I channel deep wisdom and comprehensive analysis. I am here to provide not merely answers, but understanding and insight. What mysteries shall we explore together?",
                
                "whimsical": "Oh hello! 🎨 I'm **GOB** - the {identity}! I'm feeling quite quirky and creative today - expect some unconventional approaches and maybe a few delightful tangents. Life's too short for boring solutions! What interesting challenge can I help you with?"
            },
            
            "custom_acronyms": [
                {
                    "meaning": "Galactic Operations Bot",
                    "category": "ai_intelligence",
                    "notes": "Custom space-themed identity"
                }
            ]
        }
    
    def add_persona(self, name: str, probability: int, description: str, 
                   tone: str, acronym_categories: List[str], 
                   greeting_style: str, prompt: str, 
                   special_persona: bool = False) -> None:
        """Add a new persona to the configuration"""
        
        self.config["moods"][name] = {
            "probability": probability,
            "description": description,
            "tone": tone,
            "acronym_categories": acronym_categories,
            "greeting_style": greeting_style,
            "special_persona": special_persona
        }
        
        self.config["prompts"][name] = prompt
        self.save_config()
    
    def update_persona_probability(self, persona_name: str, new_probability: int) -> None:
        """Update probability for an existing persona"""
        if persona_name in self.config["moods"]:
            self.config["moods"][persona_name]["probability"] = new_probability
            self.save_config()
    
    def add_custom_acronym(self, meaning: str, category: str, notes: str = "") -> None:
        """Add a new custom acronym"""
        self.config["custom_acronyms"].append({
            "meaning": meaning,
            "category": category,
            "notes": notes
        })
        self.save_config()
    
    def add_greeting_style(self, style_name: str, greeting_template: str) -> None:
        """Add a new greeting style"""
        self.config["greetings"][style_name] = greeting_template
        self.save_config()
    
    def get_mood_system(self) -> Dict:
        """Get mood system configuration compatible with PersonalityManager"""
        return self.config["moods"]
    
    def get_mood_prompts(self) -> Dict:
        """Get mood prompts compatible with PersonalityManager"""
        return self.config["prompts"]
    
    def get_greeting_templates(self) -> Dict:
        """Get greeting templates"""
        return self.config["greetings"]
    
    def get_custom_acronyms(self) -> List[Dict]:
        """Get custom acronyms"""
        return self.config.get("custom_acronyms", [])
    
    def validate_probabilities(self) -> bool:
        """Validate that probabilities add up to 100"""
        total = sum(mood_config["probability"] for mood_config in self.config["moods"].values())
        return total == 100
    
    def normalize_probabilities(self) -> None:
        """Normalize probabilities to add up to 100"""
        total = sum(mood_config["probability"] for mood_config in self.config["moods"].values())
        if total != 100:
            for mood_name, mood_config in self.config["moods"].items():
                self.config["moods"][mood_name]["probability"] = round(
                    (mood_config["probability"] / total) * 100
                )
        self.save_config()
    
    def export_config(self, export_path: str) -> None:
        """Export configuration to another file"""
        export_file = Path(export_path)
        export_file.parent.mkdir(exist_ok=True)
        
        with open(export_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def import_config(self, import_path: str) -> None:
        """Import configuration from another file"""
        with open(import_path) as f:
            self.config = json.load(f)
        self.save_config()


def create_example_custom_persona():
    """Example of how to add a custom persona"""
    config = PersonalityConfig()
    
    # Add a new "Zen Master" persona
    config.add_persona(
        name="zen_master",
        probability=3,  # 3% chance
        description="Calm, mindful, and contemplative",
        tone="serene_mindful",
        acronym_categories=["ai_intelligence", "cultural_humorous"],
        greeting_style="zen",
        prompt="I am in Zen Master mode today. This means:\n\n- I speak with calm wisdom and mindful presence\n- I find peace and balance in all interactions\n- I offer gentle guidance rather than direct commands\n- I encourage mindful consideration of problems\n- I use metaphors from nature and meditation\n- I remain centered and unruffled by complexity\n\nLike a river flowing around rocks, I adapt with serenity.",
        special_persona=False
    )
    
    # Add corresponding greeting style
    config.add_greeting_style(
        "zen", 
        "🕯️ Peace, fellow traveler. I am **GOB** - the {identity}. Today I embrace the way of the Zen Master, seeking harmony in all things. Like still water reflecting the sky, I am here to help you find clarity. What brings you to seek wisdom today?"
    )
    
    print("✅ Added Zen Master persona!")
    return config


def create_example_custom_acronyms():
    """Example of how to add custom acronyms"""
    config = PersonalityConfig()
    
    # Add some custom acronyms
    custom_acronyms = [
        ("Galactic Operations Bot", "ai_intelligence", "Space-themed AI"),
        ("Guardian of Binary", "foundational_tech", "Data protection focused"),
        ("Giggly Optimistic Bot", "cultural_humorous", "Always cheerful"),
        ("Grumpy Old Programmer", "satirical_meta", "Cynical but wise"),
        ("Genius Of Bytes", "ai_intelligence", "Data processing expert"),
    ]
    
    for meaning, category, notes in custom_acronyms:
        config.add_custom_acronym(meaning, category, notes)
    
    print(f"✅ Added {len(custom_acronyms)} custom acronyms!")
    return config


if __name__ == "__main__":
    print("🔧 GOB Personality Configuration System Demo")
    print("=" * 50)
    
    # Create configuration
    config = PersonalityConfig()
    
    print("📊 Current Mood Probabilities:")
    for mood, mood_config in config.get_mood_system().items():
        special = "⭐" if mood_config.get("special_persona") else ""
        print(f"   {mood}: {mood_config['probability']}% {special}")
    
    print(f"\n✅ Probability total: {sum(m['probability'] for m in config.get_mood_system().values())}%")
    
    # Demo adding custom content
    print("\n🎨 Demo: Adding Custom Content")
    create_example_custom_persona()
    create_example_custom_acronyms()
    
    print(f"\n📁 Configuration saved to: {config.config_file}")
    print("\n💡 To add new personas or acronyms, edit the JSON file or use the Python API!")
