"""
GOB State Manager
Centralized state management for daily and session state.
Provides single source of truth for UI, personality, and system state.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, Any, Optional
import os


class GOBStateManager:
    """Manages centralized state for GOB system"""
    
    # GOB title variations
    GOB_TITLES = [
        "GOB: the Grandmaster Of Backups",
        "GOB: Guardian Of Bytes",
        "GOB: Genius Of Backends",
        "GOB: Governor Of Bits",
        "GOB: Gladiator Of Bandwidth",
        "GOB: Guru Of Binary"
    ]
    
    def __init__(self, state_dir: str = "./state"):
        self.state_dir = Path(state_dir)
        self.state_dir.mkdir(exist_ok=True)
        self.state_file = self.state_dir / "gob_state.json"
        self._state = self._load_or_create_state()
    
    def _load_or_create_state(self) -> Dict[str, Any]:
        """Load existing state or create new one"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                    # Check if state is from today
                    if state.get('date') == self._get_today_str():
                        return state
            except:
                pass
        
        # Create new daily state
        return self._create_daily_state()
    
    def _create_daily_state(self) -> Dict[str, Any]:
        """Create new state for today"""
        today = datetime.datetime.now()
        day_of_year = today.timetuple().tm_yday
        
        # Select today's GOB title
        title_index = day_of_year % len(self.GOB_TITLES)
        gob_title = self.GOB_TITLES[title_index]
        gob_acronym = gob_title.split(": ")[1]  # Extract just the acronym part
        
        state = {
            "date": self._get_today_str(),
            "day_of_year": day_of_year,
            "gob_title": gob_title,
            "gob_acronym": gob_acronym,
            "gob_title_index": title_index,
            "connection_status": "online",  # online, offline, away
            "session_id": self._generate_session_id(),
            "personality": self._get_personality_state(),
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat()
        }
        
        self._save_state(state)
        return state
    
    def _get_today_str(self) -> str:
        """Get today's date as string"""
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def _get_personality_state(self) -> Optional[Dict[str, Any]]:
        """Get personality state if randomized GOB is available"""
        try:
            import sys
            from pathlib import Path
            gob_personality_path = Path(__file__).parent.parent.parent / "dev" / "projects" / "randomized-gob" / "src"
            if gob_personality_path.exists():
                sys.path.insert(0, str(gob_personality_path))
                from enhanced_personality_manager import EnhancedPersonalityManager
                
                manager = EnhancedPersonalityManager()
                profile = manager.get_daily_personality()
                
                return {
                    "identity": profile.identity,
                    "mood": profile.mood,
                    "mood_description": profile.mood_description,
                    "traits": profile.traits
                }
        except:
            return None
    
    def _save_state(self, state: Dict[str, Any]) -> None:
        """Save state to file"""
        state["updated_at"] = datetime.datetime.now().isoformat()
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
        self._state = state
    
    def get_state(self) -> Dict[str, Any]:
        """Get current state, refreshing if needed"""
        # Check if we need new daily state
        if self._state.get('date') != self._get_today_str():
            self._state = self._create_daily_state()
        return self._state.copy()
    
    def get_gob_title(self) -> str:
        """Get today's GOB title"""
        return self.get_state()["gob_title"]
    
    def get_gob_acronym(self) -> str:
        """Get just the acronym part (e.g., 'the Grandmaster Of Backups')"""
        return self.get_state()["gob_acronym"]
    
    def get_connection_status(self) -> str:
        """Get current connection status"""
        return self.get_state()["connection_status"]
    
    def set_connection_status(self, status: str) -> None:
        """Update connection status (online, offline, away)"""
        if status in ["online", "offline", "away"]:
            self._state["connection_status"] = status
            self._save_state(self._state)
    
    def get_personality(self) -> Optional[Dict[str, Any]]:
        """Get personality state if available"""
        return self.get_state().get("personality")
    
    def get_state_for_ui(self) -> Dict[str, Any]:
        """Get state formatted for UI consumption"""
        state = self.get_state()
        return {
            "gobTitle": state["gob_title"],
            "gobAcronym": state["gob_acronym"],
            "connectionStatus": state["connection_status"],
            "sessionId": state["session_id"],
            "personality": state.get("personality", {}),
            "updatedAt": state["updated_at"]
        }


# Global singleton instance
_state_manager = None

def get_state_manager() -> GOBStateManager:
    """Get or create the global state manager instance"""
    global _state_manager
    if _state_manager is None:
        _state_manager = GOBStateManager()
    return _state_manager
