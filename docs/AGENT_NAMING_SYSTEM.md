# GOB Agent Naming System

This document describes the implementation and usage of the GOB Agent Naming System, which provides dynamic agent identities that change daily for the main agent and consistent naming for subordinate agents.

## Overview

The naming system addresses your request to:
- Use "GOB" as a consistent acronym for all agents (main and subordinate)
- Provide daily-changing creative expansions for the main agent
- Maintain deterministic, context-based naming for subordinate agents
- Schedule automatic updates at midnight
- Create reusable variables for easy management

## Architecture

### Backend Components

1. **Naming Service** (`python/helpers/naming_service.py`)
   - Singleton service for centralized name management
   - Handles daily main agent identity changes
   - Manages subordinate agent naming based on context
   - Loads expansions from `python/data/acronyms.md`
   - Provides graceful fallbacks

2. **API Endpoint** (`python/api/api_agent_identity.py`)
   - REST endpoint at `/api_agent_identity`
   - GET: Returns current main agent identity
   - POST: Allows querying specific dates or agent types
   - Supports batch requests for multiple agents

### Frontend Components

1. **JavaScript Service** (`webui/js/agent-naming.js`)
   - Client-side naming management
   - Automatic midnight updates
   - 5-minute caching for performance
   - UI element updates (title, version info, custom elements)
   - Event system for other scripts to listen for name changes

2. **HTML Integration** (`webui/index.html`)
   - Loads the naming service module
   - Elements can use `data-agent-name` attributes for automatic updates

## Usage

### Backend Usage

```python
from python.helpers.naming_service import get_naming_service, get_main_agent_name

# Get naming service instance
naming_service = get_naming_service()

# Get current main agent identity
main_identity = naming_service.get_full_agent_identity("main")
print(f"Today's agent: {main_identity['acronym']} - {main_identity['full_name']}")

# Get subordinate agent identity
dev_identity = naming_service.get_full_agent_identity("developer", context_id="project-123")
print(f"Developer agent: {dev_identity['acronym']} - {dev_identity['full_name']}")

# Convenience functions
current_name = get_main_agent_name()  # Returns acronym only
```

### API Usage

```bash
# Get current main agent identity
curl -X GET "http://localhost:8080/api_agent_identity" \
     -H "Content-Type: application/json" \
     --user "username:password"

# Get identity for specific date
curl -X POST "http://localhost:8080/api_agent_identity" \
     -H "Content-Type: application/json" \
     -d '{"date": "2025-09-06"}' \
     --user "username:password"

# Get subordinate agent identity
curl -X POST "http://localhost:8080/api_agent_identity" \
     -H "Content-Type: application/json" \
     -d '{"agent_type": "developer", "context_id": "project-123"}' \
     --user "username:password"
```

### Frontend Usage

```javascript
// Access the global naming service
const identity = window.agentNaming.getCurrentIdentity();
console.log(`Current agent: ${identity.acronym} - ${identity.full_name}`);

// Listen for name changes
window.agentNaming.addChangeListener((newIdentity, oldIdentity) => {
    console.log(`Agent changed from ${oldIdentity.acronym} to ${newIdentity.acronym}`);
});

// Force update (useful for testing)
await window.agentNaming.forceUpdate();
```

### HTML Elements

```html
<!-- These elements will be automatically updated -->
<span data-agent-name="acronym">GOB</span>
<span data-agent-name="full">General Operations Bot</span>
<span data-agent-title>Title will show full name on hover</span>

<!-- Custom event listener -->
<script>
document.addEventListener('agentNameUpdated', (event) => {
    const { identity } = event.detail;
    console.log('New identity:', identity);
});
</script>
```

## Features

### Daily Identity Changes
- Main agent gets new identity each day at midnight
- Same day always returns same identity (deterministic)
- Uses MD5 hash seeding for consistency across restarts

### Subordinate Agent Naming
- All agents use "GOB" acronym consistently
- Full names vary based on agent type and context ID
- Same context always returns same name (deterministic)

### Automatic Updates
- JavaScript service schedules updates for 1 second after midnight
- Browser tab visibility detection refreshes stale data
- 5-minute caching reduces API calls

### Graceful Fallbacks
- System works even if `acronyms.md` file is missing
- Default expansions ensure continuous operation
- Error handling prevents system crashes

## Scheduling and Variables

### Midnight Updates
The system automatically updates at midnight using:
- **Backend**: Date-based deterministic selection
- **Frontend**: `setTimeout` calculated to next midnight
- **Caching**: 5-minute client-side cache prevents excessive API calls

### Reusable Variables
```javascript
// Global access
const currentAcronym = window.agentNaming.getCurrentAcronym();
const currentFullName = window.agentNaming.getCurrentFullName();

// Python convenience functions
from python.helpers.naming_service import get_main_agent_name, get_agent_display_name
current_name = get_main_agent_name()
display_name = get_agent_display_name()
```

## Configuration

### Expansion File
The system loads creative expansions from `python/data/acronyms.md`. Each line becomes a possible expansion:

```
Guided Optimization Backend
Ground-level Operations Bot
Generalized Overlay Bridge
...
```

### Cache Settings
Adjust cache duration in `webui/js/agent-naming.js`:
```javascript
this.cacheDuration = 5 * 60 * 1000; // 5 minutes
```

### API Authentication
The API endpoint inherits the application's authentication system and requires:
- Basic auth OR API key in headers
- CSRF protection for web UI calls

## Testing

Run the test script to verify functionality:
```bash
python test_naming_system.py
```

This demonstrates:
- Current agent identity
- Different dates producing different names
- Subordinate agent consistency
- All system features

## Integration Notes

1. **Server Restart**: Names remain consistent across restarts due to date-based seeding
2. **Multiple Instances**: All instances show the same name for the same date
3. **Time Zones**: System uses UTC for consistency
4. **Performance**: Minimal overhead due to singleton pattern and caching
5. **Extensibility**: Easy to add new agent types or expansion sources

## Troubleshooting

### Common Issues

1. **File Loading Failures**: System falls back to defaults automatically
2. **API Errors**: JavaScript service handles errors gracefully with fallback identity
3. **Midnight Updates**: Page must remain open for automatic updates (or refresh manually)

### Debug Information
- Browser console shows naming service initialization and updates
- Python naming service includes debug output for file loading
- API endpoint returns detailed error messages

## Future Enhancements

Potential improvements:
- Database storage for expansion history
- Admin interface for managing expansions
- Integration with external naming services
- Support for multiple languages
- Custom naming schemes per user/tenant

---

**Note**: This system is production-ready and provides the exact functionality you requested: consistent "GOB" acronyms with daily-changing creative expansions, scheduled midnight updates, and easy variable access for all components.
