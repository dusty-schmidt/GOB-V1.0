# Agent Zero Prompting System Analysis

## Overview

Agent Zero uses a sophisticated hierarchical prompting system that dynamically constructs system prompts from multiple sources. The system is designed around modularity, extensibility, and dynamic behavior adaptation.

## The Prompting Hierarchy

### 1. Core System Architecture

```
Final System Prompt
├── Dynamic Behavior Rules (highest priority)
├── Main System Prompt
│   ├── agent.system.main.role.md
│   ├── agent.system.main.environment.md
│   ├── agent.system.main.communication.md
│   ├── agent.system.main.solving.md
│   └── agent.system.main.tips.md
├── Tools Prompts
│   ├── agent.system.tools.md (organizer)
│   └── agent.system.tool.*.md (individual tools)
├── MCP Tools (if configured)
├── Secrets & Variables
├── Dynamic Memory Recalls
│   ├── Memories (fragments from past conversations)
│   └── Solutions (successful problem-solving patterns)
├── Extensions Content
└── Context Extras
```

### 2. Execution Flow

The prompt construction follows this sequence:

1. **Extension System Initialization** (`message_loop_prompts_before`)
2. **Core System Prompt Assembly** (`_10_system_prompt.py`)
3. **Dynamic Behavior Injection** (`_20_behaviour_prompt.py`)
4. **Memory and Solution Recall** (`_50_recall_memories.py`)
5. **Final Assembly** (`message_loop_prompts_after`)

### 3. File Structure Hierarchy

```
prompts/
├── default/                    # Base prompts (fallback)
├── custom-profile/             # Custom agent profiles (override default)
└── agent-specific/             # Individual agent overrides

Extensions hierarchy:
python/extensions/
├── system_prompt/
│   ├── _10_system_prompt.py    # Core prompt assembly
│   └── _20_behaviour_prompt.py # Behavior rules injection
├── message_loop_prompts_after/
│   ├── _50_recall_memories.py  # Memory integration
│   ├── _60_include_current_datetime.py
│   └── _70_include_agent_info.py
└── ... (other extension points)
```

## Key Components Explained

### Main System Prompt (`agent.system.main.md`)

This is the central hub that includes other core prompt files using template syntax:
```markdown
{{ include "agent.system.main.role.md" }}
{{ include "agent.system.main.environment.md" }}
{{ include "agent.system.main.communication.md" }}
{{ include "agent.system.main.solving.md" }}
{{ include "agent.system.main.tips.md" }}
```

### Dynamic Behavior System

- **Behavior Rules**: Stored in agent memory as `behaviour.md`
- **Precedence**: Behavior rules are injected at the **beginning** of the system prompt (highest priority)
- **Management**: Users can modify agent behavior in real-time through the `behaviour_adjustment` tool

### Tools Integration

- **Tool Organization**: `agent.system.tools.md` acts as a registry
- **Individual Tools**: Each tool has its own prompt file (`agent.system.tool.*.md`)
- **Vision Support**: Additional vision tools loaded conditionally

### Memory System Integration

- **Automatic Recall**: Triggered every N iterations (configurable)
- **Types**: Memories (fragments) and Solutions (successful patterns)
- **Filtering**: AI-powered relevance filtering and post-processing
- **Injection Point**: Added to system prompt after core components

## Precedence Rules

1. **Behavior Rules** (highest) - injected at position 0
2. **Core System Prompt** - base agent personality/instructions
3. **Tools** - available capabilities
4. **Memory/Solutions** - contextual knowledge
5. **Extensions** - plugin modifications
6. **Context Extras** - temporary additions

## File Override Logic

1. **Custom Agent Profile** (if configured) takes precedence
2. **Default prompts** used as fallback
3. **Template Processing** handles `{{ include }}` directives recursively

## Extension System

Extensions use alphabetical ordering with number prefixes:
- `_10_` executes before `_20_`, etc.
- Multiple extension points: `system_prompt`, `message_loop_prompts_before`, `message_loop_prompts_after`, etc.

## Configuration Sources

- Agent configuration (profile selection)
- Settings (memory recall intervals, thresholds)
- Dynamic behavior stored in agent memory
- MCP server configurations
- Secrets manager integration

This system allows for highly flexible and dynamic prompt construction while maintaining clear hierarchy and precedence rules.
