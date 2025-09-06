#!/usr/bin/env python3
"""
Acronym Parser for Randomized GOB Identity System

Parses the existing acronym database and categorizes identities
for use in daily rotation and personality variation.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from pathlib import Path
import random

@dataclass
class Identity:
    """Represents a single GOB identity"""
    acronym: str           # "GOB"
    meaning: str           # "General Operations Bot" 
    category: str          # "foundational_tech"
    traits: List[str]      # ["professional", "systematic"]
    style: str             # "formal_technical"
    description: str       # Generated personality description
    emoji: str             # Category emoji

class AcronymParser:
    """Parses and categorizes acronyms for identity generation"""
    
    # Category mappings based on existing structure
    CATEGORIES = {
        "foundational_tech": {
            "emoji": "🧠",
            "description": "Professional and systematic",
            "traits": ["professional", "systematic", "reliable", "thorough"],
            "style": "formal_technical"
        },
        "networking": {
            "emoji": "📡", 
            "description": "Infrastructure and connectivity focused",
            "traits": ["technical", "precise", "network-focused", "analytical"],
            "style": "technical_detailed"
        },
        "automation": {
            "emoji": "⚙️",
            "description": "Process and efficiency oriented", 
            "traits": ["efficient", "organized", "process-driven", "optimization-focused"],
            "style": "methodical_structured"
        },
        "ai_intelligence": {
            "emoji": "🛰️",
            "description": "Advanced reasoning and analytical",
            "traits": ["insightful", "analytical", "comprehensive", "strategic"],
            "style": "thoughtful_comprehensive"
        },
        "satirical_meta": {
            "emoji": "🧪",
            "description": "Humorous and self-aware",
            "traits": ["playful", "witty", "self-aware", "creative"],
            "style": "humorous_clever"
        },
        "cultural_humorous": {
            "emoji": "🎭",
            "description": "Creative and entertaining",
            "traits": ["creative", "entertaining", "expressive", "engaging"],
            "style": "friendly_creative"
        }
    }
    
    def __init__(self, acronym_file_path: str = None):
        """Initialize parser with acronym database"""
        if acronym_file_path is None:
            # Default path relative to project structure
            base_path = Path(__file__).parent.parent.parent
            acronym_file_path = base_path / "resources" / "references" / "acronyms.md"
        
        self.acronym_file = Path(acronym_file_path)
        self.identities: List[Identity] = []
        
    def parse_acronyms(self) -> List[Identity]:
        """Parse acronym file and return categorized identities"""
        if not self.acronym_file.exists():
            raise FileNotFoundError(f"Acronym file not found: {self.acronym_file}")
            
        with open(self.acronym_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        self.identities = self._parse_content(content)
        return self.identities
    
    def _parse_content(self, content: str) -> List[Identity]:
        """Parse the markdown content and extract identities"""
        identities = []
        current_category = None
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Detect category headers
            category = self._detect_category(line)
            if category:
                current_category = category
                continue
                
            # Parse acronym meanings
            if line and not line.startswith('#') and current_category:
                meaning = line.strip()
                if meaning:
                    identity = self._create_identity(meaning, current_category)
                    if identity:
                        identities.append(identity)
        
        return identities
    
    def _detect_category(self, line: str) -> Optional[str]:
        """Detect category from header line"""
        if "Foundational / Legitimate Tech" in line:
            return "foundational_tech"
        elif "Networking / Infrastructure" in line:
            return "networking"  
        elif "Automation / Runtime" in line:
            return "automation"
        elif "AI / Intelligence / Futuristic" in line:
            return "ai_intelligence"
        elif "Satirical / Meta / Absurd" in line:
            return "satirical_meta"
        elif "Cultural / Humorous" in line:
            return "cultural_humorous"
        return None
    
    def _create_identity(self, meaning: str, category: str) -> Optional[Identity]:
        """Create Identity object from meaning and category"""
        meaning = meaning.strip()
        
        # Skip empty lines or lines that are just formatting
        if not meaning or len(meaning) < 3:
            return None
            
        category_info = self.CATEGORIES.get(category, self.CATEGORIES["foundational_tech"])
        
        return Identity(
            acronym="GOB",
            meaning=meaning,
            category=category,
            traits=category_info["traits"].copy(),
            style=category_info["style"],
            description=self._generate_description(meaning, category_info),
            emoji=category_info["emoji"]
        )
    
    def _generate_description(self, meaning: str, category_info: Dict) -> str:
        """Generate personality description for identity"""
        return f"{category_info['emoji']} {meaning} - {category_info['description']}"
    
    def get_random_identity(self, category_filter: Optional[List[str]] = None) -> Identity:
        """Get random identity with optional category filtering"""
        if not self.identities:
            self.parse_acronyms()
            
        available = self.identities
        if category_filter:
            available = [i for i in self.identities if i.category in category_filter]
            
        if not available:
            # Fallback to any identity if filter excludes everything
            available = self.identities
            
        return random.choice(available)
    
    def get_category_counts(self) -> Dict[str, int]:
        """Get count of identities per category"""
        if not self.identities:
            self.parse_acronyms()
            
        counts = {}
        for identity in self.identities:
            counts[identity.category] = counts.get(identity.category, 0) + 1
        return counts
    
    def validate_database(self) -> Dict[str, any]:
        """Validate acronym database and return stats"""
        if not self.identities:
            self.parse_acronyms()
            
        total_count = len(self.identities)
        category_counts = self.get_category_counts()
        
        return {
            "total_identities": total_count,
            "category_breakdown": category_counts,
            "categories": list(self.CATEGORIES.keys()),
            "validation": {
                "has_all_categories": len(category_counts) == len(self.CATEGORIES),
                "sufficient_variety": total_count >= 100,  # Reasonable minimum
                "balanced_categories": min(category_counts.values()) >= 10 if category_counts else False
            }
        }

def main():
    """Demo usage of AcronymParser"""
    parser = AcronymParser()
    
    print("🎭 Randomized GOB Identity System - Acronym Parser Demo")
    print("=" * 60)
    
    try:
        # Parse identities
        identities = parser.parse_acronyms()
        print(f"✅ Parsed {len(identities)} identities from database")
        
        # Show validation stats
        stats = parser.validate_database()
        print(f"\n📊 Database Statistics:")
        print(f"   Total Identities: {stats['total_identities']}")
        print(f"   Categories: {len(stats['category_breakdown'])}")
        
        for category, count in stats['category_breakdown'].items():
            emoji = parser.CATEGORIES[category]["emoji"]
            print(f"   {emoji} {category}: {count} identities")
        
        # Show some random identities
        print(f"\n🎲 Random Identity Examples:")
        for i in range(5):
            identity = parser.get_random_identity()
            print(f"   {identity.emoji} {identity.meaning}")
            print(f"      Category: {identity.category}")
            print(f"      Traits: {', '.join(identity.traits[:3])}")
            print()
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure the acronym database exists at the expected location.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
