"""
GOB Naming Service

This module provides centralized naming for agents with daily identity changes
for the main agent and task-based acronyms for subordinate agents.
"""

import datetime
import hashlib
import random
import os
import re
from typing import Dict, List, Optional
from enum import Enum


class AgentTask(Enum):
    """Task categories for subordinate agents"""
    DEVELOPMENT = "development"
    RESEARCH = "research" 
    HACKING = "hacking"
    ANALYSIS = "analysis"
    WRITING = "writing"
    COMMUNICATION = "communication"
    GENERAL = "general"


class NamingService:
    """Centralized naming service for GOB agents"""
    
    # Default fallback acronyms if file loading fails
    _DEFAULT_MAIN_AGENT_ACRONYMS = [
        "GOB",  # Default fallback
        "GAB",  # General Autonomous Bot
        "GIB",  # General Intelligence Bot  
        "GUB",  # General Utility Bot
        "GEB",  # General Executive Bot
        "GRB",  # General Response Bot
        "GSB",  # General Service Bot
        "GTB",  # General Task Bot
        "GHB",  # General Helper Bot
        "GWB",  # General Worker Bot
        "GXB",  # General eXecution Bot
        "GYB",  # General Yielding Bot
        "GZB",  # General Zone Bot
        "GAC",  # General Autonomous Core
        "GIC",  # General Intelligence Core
        "GUC",  # General Utility Core
        "GEC",  # General Executive Core
        "GRC",  # General Response Core
        "GSC",  # General Service Core
        "GTC",  # General Task Core
        "GHC",  # General Helper Core
        "GWC",  # General Worker Core
        "GXC",  # General eXecution Core
        "GYC",  # General Yielding Core  
        "GZC",  # General Zone Core
    ]
    
    # Task-specific acronym pools for subordinate agents
    TASK_ACRONYMS = {
        AgentTask.DEVELOPMENT: [
            "DEV", "COD", "BLD", "ARC", "SYS", "APP", "WEB", "API", "DBA", 
            "OPS", "SEC", "TST", "DBG", "PKG", "GIT", "ENV", "CFG", "LIB",
            "FWK", "CLI", "GUI", "IDE", "SDK", "VCS", "REP", "MRG", "DEP"
        ],
        AgentTask.RESEARCH: [
            "RES", "ANA", "DIG", "SCN", "SRC", "DOC", "REP", "SUM", "SYN",
            "VER", "CHK", "FAC", "DAT", "INF", "KNW", "LEA", "STU", "EXP",
            "OBS", "HYP", "THR", "MOD", "SIM", "PRD", "TRN", "PAT", "COR"
        ],
        AgentTask.HACKING: [
            "HAK", "PEN", "SEC", "VUL", "EXP", "SCN", "FUZ", "BRK", "CRK",
            "ROT", "SHL", "PWN", "ESC", "PRV", "ELV", "INJ", "XSS", "SQL",
            "RCE", "BOF", "ROP", "JOP", "GDB", "HEX", "ASM", "REV", "DCM"
        ],
        AgentTask.ANALYSIS: [
            "ANL", "EVL", "ASS", "REV", "INS", "STA", "MTR", "MSR", "CAL",
            "CMP", "DIF", "TRD", "PAT", "COR", "REG", "CLS", "GRP", "SEG",
            "FLT", "AGG", "RED", "MAP", "VIS", "CHR", "GRP", "HIS", "FOR"
        ],
        AgentTask.WRITING: [
            "WRT", "DOC", "EDT", "PUB", "AUT", "DRF", "REV", "PRF", "STY",
            "GRM", "SPL", "FMT", "LAY", "STR", "NAR", "REP", "ART", "BLG",
            "MRK", "HTM", "TXT", "PDF", "MDN", "TEX", "RTF", "CSV", "JSON"
        ],
        AgentTask.COMMUNICATION: [
            "COM", "MSG", "CHT", "TLK", "SPK", "LSN", "REP", "REL", "UPD",
            "NOT", "ALR", "LOG", "BRD", "SIG", "SND", "RCV", "TRN", "FWD",
            "EML", "SMS", "API", "WEB", "IRC", "TCP", "UDP", "WSS", "SSH"
        ],
        AgentTask.GENERAL: [
            "GEN", "UTL", "HLP", "AST", "SVC", "TSK", "JOB", "WRK", "EXE",
            "RUN", "OPR", "MGR", "CTL", "MON", "SUP", "SUB", "AUX", "MID",
            "HUB", "NOD", "LNK", "BRG", "RTR", "PRX", "GAW", "FLT", "BUF"
        ]
    }
    
    _instance: Optional['NamingService'] = None
    _current_date_cache: Optional[str] = None
    _main_agent_name_cache: Optional[str] = None
    _main_agent_acronyms_cache: Optional[List[str]] = None
    _gob_expansions_cache: Optional[Dict[str, str]] = None
    _gob_expansions_list: Optional[List[str]] = None
    
    def __init__(self):
        """Initialize the naming service"""
        pass
    
    @property
    def MAIN_AGENT_ACRONYMS(self) -> List[str]:
        """Get main agent acronyms, loading from file if needed"""
        if self._main_agent_acronyms_cache is None:
            self._load_acronyms_from_file()
        return self._main_agent_acronyms_cache or self._DEFAULT_MAIN_AGENT_ACRONYMS
    
    @property
    def GOB_EXPANSIONS(self) -> Dict[str, str]:
        """Get GOB acronym expansions, loading from file if needed"""
        if self._gob_expansions_cache is None:
            self._load_acronyms_from_file()
        return self._gob_expansions_cache or {}
    
    def _load_acronyms_from_file(self) -> None:
        """Load GOB acronyms and expansions from the acronyms.md file"""
        try:
            # Get the directory where this module is located
            current_dir = os.path.dirname(os.path.abspath(__file__))
            acronyms_file = os.path.join(current_dir, '..', 'data', 'acronyms.md')
            # Normalize the path to handle .. properly
            acronyms_file = os.path.normpath(acronyms_file)
            
            # Debug info (can be removed later)
            # print(f"DEBUG: Looking for acronyms file at: {acronyms_file}")
            
            if not os.path.exists(acronyms_file):
                # Try alternative path as fallback
                alt_path = os.path.join(os.getcwd(), 'python', 'data', 'acronyms.md')
                if os.path.exists(alt_path):
                    acronyms_file = alt_path
                else:
                    # Fallback to defaults
                    self._main_agent_acronyms_cache = self._DEFAULT_MAIN_AGENT_ACRONYMS.copy()
                    self._gob_expansions_cache = {}
                    return
            
            with open(acronyms_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple approach: Just use "GOB" as the acronym and all the creative
            # expansions from the file as the possible full names
            expansions = {}
            gob_expansions = []
            
            # Split by lines and process each line
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                
                # Skip empty lines and emoji headers
                if not line or line.startswith('🧠') or line.startswith('📡') or \
                   line.startswith('⚙️') or line.startswith('🛰️') or \
                   line.startswith('🧪') or line.startswith('🎭'):
                    continue
                
                # Add this as a possible GOB expansion
                if line and len(line) > 3:  # Only meaningful expansions
                    gob_expansions.append(line)
            
            if len(gob_expansions) > 50:  # We have enough expansions from file
                # Always use "GOB" as the main acronym, but pick a random expansion each day
                self._main_agent_acronyms_cache = ["GOB"]
                # Store all expansions indexed by line number for deterministic selection
                for i, expansion in enumerate(gob_expansions):
                    expansions[f"GOB_{i}"] = expansion
                self._gob_expansions_cache = expansions
                # Store the list of expansions for selection
                self._gob_expansions_list = gob_expansions
            else:
                # Not enough expansions, fall back to defaults
                self._main_agent_acronyms_cache = self._DEFAULT_MAIN_AGENT_ACRONYMS.copy()
                self._gob_expansions_cache = {}
                
        except Exception as e:
            # If anything goes wrong, fall back to defaults
            self._main_agent_acronyms_cache = self._DEFAULT_MAIN_AGENT_ACRONYMS.copy()
            self._gob_expansions_cache = {}
    
    @classmethod
    def get_instance(cls) -> 'NamingService':
        """Get singleton instance of naming service"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_main_agent_name(self, date: Optional[datetime.date] = None) -> str:
        """
        Get the main agent's daily identity name
        
        Args:
            date: Specific date to get name for (defaults to today)
            
        Returns:
            The main agent's acronym for the given date
        """
        if date is None:
            date = datetime.date.today()
        
        date_str = date.strftime("%Y-%m-%d")
        
        # Use cache if same date
        if (self._current_date_cache == date_str and 
            self._main_agent_name_cache is not None):
            return self._main_agent_name_cache
        
        # Generate deterministic random seed from date
        seed_string = f"gob_main_agent_{date_str}"
        seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
        seed = int(seed_hash[:8], 16)  # Use first 8 hex chars as seed
        
        # Set random seed and select acronym
        random.seed(seed)
        selected_name = random.choice(self.MAIN_AGENT_ACRONYMS)
        
        # Cache result
        self._current_date_cache = date_str
        self._main_agent_name_cache = selected_name
        
        return selected_name
    
    def get_subordinate_agent_name(self, 
                                   agent_type: str, 
                                   context_id: Optional[str] = None) -> str:
        """
        Get a subordinate agent's acronym (always GOB)
        
        Args:
            agent_type: The agent type/profile (e.g., 'developer', 'researcher')
            context_id: Optional context identifier for consistent naming
            
        Returns:
            Always returns "GOB" - all agents use the same acronym
        """
        # All agents use GOB as their acronym
        return "GOB"
    
    def get_full_agent_identity(self, 
                               agent_type: str = "main",
                               context_id: Optional[str] = None,
                               date: Optional[datetime.date] = None) -> Dict[str, str]:
        """
        Get complete agent identity information
        
        Args:
            agent_type: Type of agent ('main' or specific subordinate type)
            context_id: Context identifier for subordinate agents
            date: Date for main agent (defaults to today)
            
        Returns:
            Dictionary with agent identity information
        """
        if agent_type.lower() == "main":
            name = self.get_main_agent_name(date)
            return {
                "acronym": name,
                "full_name": self._expand_main_acronym(name, date),
                "type": "main",
                "date": (date or datetime.date.today()).strftime("%Y-%m-%d")
            }
        else:
            name = self.get_subordinate_agent_name(agent_type, context_id)
            return {
                "acronym": name,
                "full_name": self._expand_subordinate_acronym(name, agent_type, context_id),
                "type": agent_type,
                "context": context_id or agent_type
            }
    
    def _expand_main_acronym(self, acronym: str, date: Optional[datetime.date] = None) -> str:
        """Expand main agent acronym to full name"""
        # For GOB, use daily selection from loaded expansions
        if acronym == "GOB" and hasattr(self, '_gob_expansions_list') and self._gob_expansions_list:
            if date is None:
                date = datetime.date.today()
            
            # Generate deterministic random seed from date for expansion selection
            seed_string = f"gob_expansion_{date.strftime('%Y-%m-%d')}"
            seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
            seed = int(seed_hash[:8], 16)
            
            # Select expansion deterministically based on date
            random.seed(seed)
            expansion_index = random.randint(0, len(self._gob_expansions_list) - 1)
            return self._gob_expansions_list[expansion_index]
        
        # Try to get expansion from loaded file cache
        file_expansions = self.GOB_EXPANSIONS
        if acronym in file_expansions:
            return file_expansions[acronym]
        
        # Fall back to default expansions
        default_expansions = {
            "GOB": "General Operations Bot",
            "GAB": "General Autonomous Bot",
            "GIB": "General Intelligence Bot",
            "GUB": "General Utility Bot", 
            "GEB": "General Executive Bot",
            "GRB": "General Response Bot",
            "GSB": "General Service Bot",
            "GTB": "General Task Bot",
            "GHB": "General Helper Bot",
            "GWB": "General Worker Bot",
            "GXB": "General eXecution Bot",
            "GYB": "General Yielding Bot",
            "GZB": "General Zone Bot",
            "GAC": "General Autonomous Core",
            "GIC": "General Intelligence Core",
            "GUC": "General Utility Core",
            "GEC": "General Executive Core",
            "GRC": "General Response Core",
            "GSC": "General Service Core",
            "GTC": "General Task Core",
            "GHC": "General Helper Core",
            "GWC": "General Worker Core",
            "GXC": "General eXecution Core",
            "GYC": "General Yielding Core",
            "GZC": "General Zone Core",
        }
        return default_expansions.get(acronym, f"General Operations Bot ({acronym})")
    
    def _expand_subordinate_acronym(self, acronym: str, agent_type: str, context_id: Optional[str] = None) -> str:
        """Expand subordinate agent acronym based on context"""
        # For GOB, use context-based selection from loaded expansions
        if acronym == "GOB" and hasattr(self, '_gob_expansions_list') and self._gob_expansions_list:
            # Generate deterministic selection based on agent type and context
            context_str = f"{agent_type}_{context_id or agent_type}"
            seed_string = f"gob_subordinate_{context_str}"
            seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
            seed = int(seed_hash[:8], 16)
            
            # Select expansion deterministically based on context
            random.seed(seed)
            expansion_index = random.randint(0, len(self._gob_expansions_list) - 1)
            return self._gob_expansions_list[expansion_index]
        
        # Fall back to generic expansion
        return f"{acronym} Specialist ({agent_type.title()})"
    
    def get_display_name(self, agent_type: str = "main", **kwargs) -> str:
        """
        Get agent display name for UI elements
        
        Args:
            agent_type: Type of agent
            **kwargs: Additional arguments for identity generation
            
        Returns:
            Display-ready agent name
        """
        identity = self.get_full_agent_identity(agent_type, **kwargs)
        return identity["acronym"]
    
    def refresh_main_agent_cache(self):
        """Force refresh of main agent name cache"""
        self._current_date_cache = None
        self._main_agent_name_cache = None


# Convenience functions for easy access
def get_naming_service() -> NamingService:
    """Get the global naming service instance"""
    return NamingService.get_instance()


def get_main_agent_name(date: Optional[datetime.date] = None) -> str:
    """Get main agent name for date"""
    return get_naming_service().get_main_agent_name(date)


def get_subordinate_agent_name(agent_type: str, context_id: Optional[str] = None) -> str:
    """Get subordinate agent name"""
    return get_naming_service().get_subordinate_agent_name(agent_type, context_id)


def get_agent_display_name(agent_type: str = "main", **kwargs) -> str:
    """Get agent display name"""
    return get_naming_service().get_display_name(agent_type, **kwargs)
