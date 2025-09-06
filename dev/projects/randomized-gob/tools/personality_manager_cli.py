#!/usr/bin/env python3
"""
GOB Personality Manager CLI Tool

Convenient command-line interface for managing GOB personalities and acronyms.
Makes it easy to add new personas, adjust probabilities, and customize the system.
"""

import argparse
import json
import sys
from pathlib import Path
import textwrap

# Add the src directory to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from personality_config import PersonalityConfig

def show_status(config: PersonalityConfig):
    """Display current configuration status"""
    print("🤖 GOB Personality System Status")
    print("=" * 50)
    
    moods = config.get_mood_system()
    total_prob = sum(m["probability"] for m in moods.values())
    
    print(f"📊 Personas ({len(moods)} total):")
    for mood, mood_config in sorted(moods.items(), key=lambda x: x[1]["probability"], reverse=True):
        special = "⭐ " if mood_config.get("special_persona") else ""
        print(f"   {special}{mood:<20} {mood_config['probability']:>3}%  {mood_config['description']}")
    
    print(f"\n✅ Total probability: {total_prob}% {'(Valid)' if total_prob == 100 else '(NEEDS FIXING)'}")
    
    custom_acronyms = config.get_custom_acronyms()
    print(f"\n🎯 Custom Acronyms: {len(custom_acronyms)}")
    for acronym in custom_acronyms:
        print(f"   • {acronym['meaning']} ({acronym['category']})")
    
    print(f"\n📁 Config file: {config.config_file}")

def add_persona_interactive(config: PersonalityConfig):
    """Interactive persona addition"""
    print("🎭 Add New Persona")
    print("-" * 20)
    
    name = input("Persona name (e.g., 'zen_master'): ").strip()
    if not name:
        print("❌ Name cannot be empty")
        return
    
    if name in config.get_mood_system():
        print(f"❌ Persona '{name}' already exists")
        return
    
    description = input("Description: ").strip()
    
    print(f"Probability (current total: {sum(m['probability'] for m in config.get_mood_system().values())}%): ", end="")
    try:
        probability = int(input())
    except ValueError:
        print("❌ Probability must be a number")
        return
    
    tone = input("Tone (e.g., 'calm_wise'): ").strip()
    
    print("\nAvailable categories: foundational_tech, automation, ai_intelligence, networking, cultural_humorous, satirical_meta")
    categories_input = input("Acronym categories (comma-separated): ").strip()
    acronym_categories = [cat.strip() for cat in categories_input.split(",") if cat.strip()]
    
    print("\nAvailable greeting styles: formal, warm, brief, playful, dramatic, mystical, whimsical")
    greeting_style = input("Greeting style: ").strip()
    
    special = input("Special persona? (y/N): ").lower().startswith('y')
    
    print("\n📝 Persona Prompt:")
    print("Enter the personality prompt (end with empty line):")
    prompt_lines = []
    while True:
        line = input()
        if not line:
            break
        prompt_lines.append(line)
    
    prompt = "\\n".join(prompt_lines)
    
    # Add the persona
    config.add_persona(
        name=name,
        probability=probability,
        description=description,
        tone=tone,
        acronym_categories=acronym_categories,
        greeting_style=greeting_style,
        prompt=prompt,
        special_persona=special
    )
    
    print(f"✅ Added persona '{name}'!")
    
    # Check if probabilities need normalization
    total = sum(m["probability"] for m in config.get_mood_system().values())
    if total != 100:
        print(f"⚠️  Total probability is now {total}%. Consider normalizing with --normalize")

def add_acronym_interactive(config: PersonalityConfig):
    """Interactive acronym addition"""
    print("🎯 Add New Acronym")
    print("-" * 18)
    
    meaning = input("Acronym meaning (e.g., 'Galactic Operations Bot'): ").strip()
    if not meaning:
        print("❌ Meaning cannot be empty")
        return
    
    print("\nAvailable categories:")
    print("  • foundational_tech - Core technology concepts")
    print("  • automation - Process automation and efficiency")
    print("  • ai_intelligence - AI and machine learning")
    print("  • networking - Network operations and connectivity")
    print("  • cultural_humorous - Pop culture and humor")
    print("  • satirical_meta - Self-referential and satirical")
    
    category = input("Category: ").strip()
    if not category:
        category = "foundational_tech"
    
    notes = input("Notes (optional): ").strip()
    
    config.add_custom_acronym(meaning, category, notes)
    print(f"✅ Added acronym '{meaning}'!")

def list_personas(config: PersonalityConfig):
    """List all personas with details"""
    print("🎭 All Personas")
    print("=" * 50)
    
    moods = config.get_mood_system()
    prompts = config.get_mood_prompts()
    greetings = config.get_greeting_templates()
    
    for mood, mood_config in sorted(moods.items()):
        special = "⭐ SPECIAL " if mood_config.get("special_persona") else ""
        print(f"\n{special}{mood.upper()}")
        print("-" * (len(mood) + len(special)))
        print(f"Probability: {mood_config['probability']}%")
        print(f"Description: {mood_config['description']}")
        print(f"Tone: {mood_config['tone']}")
        print(f"Categories: {', '.join(mood_config['acronym_categories'])}")
        print(f"Greeting Style: {mood_config['greeting_style']}")
        
        if mood in prompts:
            print("\nPrompt Preview:")
            # Unescape and show first few lines
            prompt = prompts[mood].replace("\\n", "\n")
            lines = prompt.split("\n")[:3]
            for line in lines:
                print(f"  {line}")
            if len(prompt.split("\n")) > 3:
                print("  ...")
        
        if mood_config['greeting_style'] in greetings:
            print(f"\nGreeting: {greetings[mood_config['greeting_style']][:100]}...")

def update_probability(config: PersonalityConfig, persona: str, probability: int):
    """Update persona probability"""
    if persona not in config.get_mood_system():
        print(f"❌ Persona '{persona}' not found")
        return
    
    config.update_persona_probability(persona, probability)
    print(f"✅ Updated {persona} probability to {probability}%")
    
    total = sum(m["probability"] for m in config.get_mood_system().values())
    if total != 100:
        print(f"⚠️  Total probability is now {total}%. Consider normalizing with --normalize")

def normalize_probabilities(config: PersonalityConfig):
    """Normalize all probabilities to total 100%"""
    old_total = sum(m["probability"] for m in config.get_mood_system().values())
    print(f"📊 Normalizing probabilities (current total: {old_total}%)")
    
    config.normalize_probabilities()
    
    print("✅ Probabilities normalized to 100%!")
    show_status(config)

def test_personality(config: PersonalityConfig):
    """Test the personality system"""
    print("🧪 Testing Personality System")
    print("=" * 30)
    
    # Import the personality manager for testing
    try:
        from enhanced_personality_manager import EnhancedPersonalityManager
        import os
        acronym_path = os.path.join('/home/ds/GOB/dev/resources/references/acronyms.md')
        manager = EnhancedPersonalityManager(acronym_file_path=acronym_path)
        
        print("Testing 5 random personality selections:")
        for i in range(5):
            profile = manager.get_daily_personality()
            greeting = manager.get_personality_greeting()
            print(f"\n{i+1}. {profile.identity['meaning']} ({profile.mood})")
            print(f"   Greeting: {greeting[:80]}...")
            
    except ImportError:
        print("❌ Cannot import PersonalityManager - make sure it's available")
    except Exception as e:
        print(f"❌ Error testing: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="GOB Personality Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          %(prog)s --status                    # Show current configuration
          %(prog)s --add-persona               # Interactively add new persona
          %(prog)s --add-acronym               # Add new custom acronym
          %(prog)s --list                      # List all personas with details
          %(prog)s --update zen_master 8       # Set zen_master to 8% probability
          %(prog)s --normalize                 # Fix probabilities to total 100%
          %(prog)s --test                      # Test the personality system
        """)
    )
    
    parser.add_argument("--config", help="Custom config file path")
    parser.add_argument("--status", action="store_true", help="Show configuration status")
    parser.add_argument("--add-persona", action="store_true", help="Add new persona interactively")
    parser.add_argument("--add-acronym", action="store_true", help="Add new acronym interactively")
    parser.add_argument("--list", action="store_true", help="List all personas with details")
    parser.add_argument("--update", nargs=2, metavar=("PERSONA", "PROBABILITY"), 
                       help="Update persona probability")
    parser.add_argument("--normalize", action="store_true", help="Normalize probabilities to 100%")
    parser.add_argument("--test", action="store_true", help="Test the personality system")
    parser.add_argument("--export", help="Export configuration to file")
    parser.add_argument("--import", dest="import_file", help="Import configuration from file")
    
    args = parser.parse_args()
    
    # Initialize configuration
    config = PersonalityConfig(args.config)
    
    # Handle commands
    if args.status:
        show_status(config)
    elif args.add_persona:
        add_persona_interactive(config)
    elif args.add_acronym:
        add_acronym_interactive(config)
    elif args.list:
        list_personas(config)
    elif args.update:
        persona, probability = args.update
        try:
            probability = int(probability)
            update_probability(config, persona, probability)
        except ValueError:
            print("❌ Probability must be a number")
    elif args.normalize:
        normalize_probabilities(config)
    elif args.test:
        test_personality(config)
    elif args.export:
        config.export_config(args.export)
        print(f"✅ Configuration exported to {args.export}")
    elif args.import_file:
        config.import_config(args.import_file)
        print(f"✅ Configuration imported from {args.import_file}")
    else:
        # Default to showing status
        show_status(config)

if __name__ == "__main__":
    main()
