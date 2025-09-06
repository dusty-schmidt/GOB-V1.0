# GOB Randomized Personality System - Installation Guide

## 🚀 **Quick Installation**

The randomized personality system is **already integrated** into your GOB setup! Here's how to activate it:

### **Prerequisites**
- ✅ **GOB Agent Zero** - Already installed
- ✅ **Python 3.8+** - Available via your conda environment
- ✅ **Configuration system** - Already created

### **Activation Steps**

1. **Verify Installation**
   ```bash
   cd /home/ds/GOB/dev/projects/randomized-gob
   python tools/personality_manager_cli.py --status
   ```

2. **Test the System**
   ```bash
   python tools/personality_manager_cli.py --test
   ```

3. **Start GOB** - The personality system will automatically activate!

---

## 🎭 **What You Get**

### **Dynamic Daily Personalities**
- **7 Different Personas** with unique behaviors
- **Weighted Probability System** (Professional: 25%, Friendly: 20%, etc.)
- **Consistent Daily Identity** - Same personality all day, changes at midnight

### **Personality-Aware Greetings**
Instead of: *"Hello! I'm GOB, your AI assistant."*

You'll see: *"Hey there! 😄 I'm **GOB** - the Grandmaster Of Backups! Fair warning: I'm in Humorous Jokey mode today, so expect some puns and jokes mixed in with my help."*

### **Dynamic Acronym System**
- **600+ Acronym Meanings** from your existing database
- **Category-Based Selection** matching today's mood
- **Expandable** - easily add your own custom meanings

---

## 🔧 **Customization**

### **Add New Personas**
```bash
cd /home/ds/GOB/dev/projects/randomized-gob
./tools/personality_manager_cli.py --add-persona
```

Interactive prompts will guide you through:
- Persona name and description
- Probability percentage
- Greeting style and personality prompt

### **Add Custom Acronyms**
```bash
./tools/personality_manager_cli.py --add-acronym
```

Example custom acronyms:
- "Galactic Operations Bot" (ai_intelligence)
- "Guardian Of Binary" (foundational_tech)
- "Giggly Optimistic Bot" (cultural_humorous)

### **Adjust Probabilities**
```bash
# Make GOB Bluth mode more common
./tools/personality_manager_cli.py --update gob_bluth 15

# Auto-normalize to ensure 100% total
./tools/personality_manager_cli.py --normalize
```

---

## 🛠️ **Advanced Configuration**

### **Configuration File Location**
```
/home/ds/GOB/dev/projects/randomized-gob/config/personality_config.json
```

### **Manual Configuration**
Edit the JSON directly for bulk changes:
```bash
cd /home/ds/GOB/dev/projects/randomized-gob
./tools/personality_manager_cli.py --export backup.json  # Backup first
nano config/personality_config.json  # Edit manually
./tools/personality_manager_cli.py --normalize  # Fix probabilities
```

### **Memory and State Management**
Personality state is stored in Agent Zero's memory:
```
{agent_memory_path}/
├── personality_state.json      # Current daily profile
├── personality_history.json    # Last 30 days history
└── behaviour.md               # Agent Zero behavior prompt
```

---

## 🧪 **Testing & Verification**

### **Test Different Personalities**
```bash
cd /home/ds/GOB/dev/projects/randomized-gob

# View current configuration
./tools/personality_manager_cli.py --status

# Test personality generation
./tools/personality_manager_cli.py --test

# List all personas with details
./tools/personality_manager_cli.py --list
```

### **Debug Agent Zero Integration**
```bash
# Test the Agent Zero integration directly
cd /home/ds/GOB/dev/projects/randomized-gob
python src/agent_zero_integration.py
```

### **Check Integration Status**
When you start GOB, look for:
```
[DEBUG] Personality system not available, using standard greeting: [error]
```

If you see this, the system fell back to standard greetings. Check that all dependencies are in place.

---

## 🎯 **Persona Types**

### **Built-in Personas**
| Persona | Probability | Description |
|---------|-------------|-------------|
| **Professional** | 25% | Focused, systematic, business-like |
| **Friendly Chatty** | 20% | Warm, conversational, helpful |
| **Direct Efficient** | 20% | No-nonsense, straight to the point |
| **Humorous Jokey** | 15% | Can't help but make jokes and puns |
| **Wise Oracle** | 10% | Deep insights, philosophical |
| **GOB Bluth** ⭐ | 5% | Overconfident, dramatic (special) |
| **Quirky Eccentric** | 5% | Creative, unconventional approaches |

### **Greeting Styles**
- **Formal** - Professional, systematic
- **Warm** - Friendly, enthusiastic  
- **Brief** - Direct, concise
- **Playful** - Humorous, witty
- **Dramatic** - Over-the-top, theatrical
- **Mystical** - Wise, philosophical
- **Whimsical** - Creative, quirky

---

## 🔄 **Daily Rotation**

### **How It Works**
- **Consistent per day** - Same personality from midnight to midnight
- **Date-based randomization** - Uses current date as random seed
- **Weighted selection** - Higher probability personas appear more often
- **Automatic updates** - Changes at midnight without restart

### **Forcing a New Personality** (for testing)
```python
cd /home/ds/GOB/dev/projects/randomized-gob
python -c "
import sys; sys.path.insert(0, 'src')
from enhanced_personality_manager import EnhancedPersonalityManager
manager = EnhancedPersonalityManager()
# Force regeneration by clearing current profile
manager.current_profile = None
profile = manager.get_daily_personality()
print(f'New personality: {profile.identity[\"meaning\"]} ({profile.mood})')
"
```

---

## 🚨 **Troubleshooting**

### **Common Issues**

#### **"Acronym file not found"**
```bash
# Check if acronym files exist
ls -la /home/ds/GOB/dev/resources/references/acronyms.md
ls -la /home/ds/GOB/python/data/acronyms.md

# The system will auto-detect the correct path
```

#### **"Personality system not available"**
```bash
# Check Python path integration
cd /home/ds/GOB
python -c "
import sys
from pathlib import Path
gob_path = Path('./dev/projects/randomized-gob/src')
print(f'GOB personality path exists: {gob_path.exists()}')
sys.path.insert(0, str(gob_path))
try:
    from enhanced_personality_manager import EnhancedPersonalityManager
    print('✅ Personality manager importable')
except Exception as e:
    print(f'❌ Import error: {e}')
"
```

#### **Standard greeting still showing**
This is normal - the system has graceful fallback. Check the console for debug messages when starting Agent Zero.

### **Reset to Defaults**
```bash
cd /home/ds/GOB/dev/projects/randomized-gob
rm -f config/personality_config.json
python src/personality_config.py  # Regenerates defaults
```

---

## 📚 **API Reference**

### **PersonalityConfig Class**
```python
from personality_config import PersonalityConfig

config = PersonalityConfig()
config.add_persona(name, probability, description, tone, categories, greeting_style, prompt)
config.add_custom_acronym(meaning, category, notes)
config.update_persona_probability(persona_name, new_probability)
```

### **EnhancedPersonalityManager Class**
```python
from enhanced_personality_manager import EnhancedPersonalityManager

manager = EnhancedPersonalityManager(agent_memory_path, acronym_file_path, config_file)
profile = manager.get_daily_personality()
summary = manager.get_personality_summary()
greeting = manager.get_personality_greeting()
```

### **Agent Zero Integration**
```python
from agent_zero_integration import PersonalityAgentZeroIntegration

integration = PersonalityAgentZeroIntegration(memory_path)
message = integration.get_enhanced_initial_message()
```

---

## 🎉 **You're All Set!**

The randomized personality system is now active! Every day GOB will:

1. **🎲 Roll for personality** based on configured probabilities  
2. **🎭 Select matching acronym** from the appropriate category
3. **👋 Greet you** with personality-aware message
4. **🤖 Maintain character** throughout the conversation
5. **📝 Update behavior** to reflect the day's persona

**Next steps:**
- Start a new GOB session to see the personality system in action
- Customize personas and acronyms to your liking  
- Share your configuration with `--export` for backup
- Monitor `personality_history.json` to see the variety over time

---

*Made a huge mistake? No problem - there's always tomorrow for a new personality! 🎭*
