# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common Commands

### Setup and Installation
```bash
# Initial setup (automatic - recommended)
./setup_new.sh

# Manual environment setup if needed
conda create -n gob python=3.13 -y
conda activate gob
pip install -r requirements.txt
```

### Development Workflow
```bash
# Start GOB server
scripts/gob start

# Check server status
scripts/gob status

# View logs (last 50 lines by default)
scripts/gob logs

# Follow logs in real-time
scripts/gob logs follow

# Restart server (after code changes)
scripts/gob restart

# Stop server
scripts/gob stop

# Open web interface
scripts/gob url
# Or manually: http://localhost:50080
```

### Development Commands
```bash
# Activate development environment
conda activate gob

# Run server directly with debug mode
python run_ui.py --host 0.0.0.0 --port 50080 --debug

# Run single test or script
python scripts/test_simple.sh

# Check environment
python -c "import flask, models, agent"
```

### Testing and Monitoring
```bash
# Test phases
./test_phases.sh

# Monitor server health
scripts/gob status

# Check specific functionality
python initialize.py
python agent.py
```

## Architecture Overview

### Core System Design
GOB is an advanced AI agent orchestration system with the following key architectural components:

**Agent System (`agent.py`)**
- Central `Agent` class that manages AI interactions and tool execution
- `AgentContext` for managing conversation sessions and state
- `AgentConfig` for model and system configuration
- Dynamic agent naming system that changes daily for variety
- Extension system for modular functionality

**Model Management (`models.py`)**
- Unified interface for multiple LLM providers via LiteLLM
- Support for chat, utility, browser, and embedding models
- Rate limiting and API key management
- Streaming response handling with reasoning separation
- Custom wrappers for browser compatibility

**Initialization (`initialize.py`)**
- Configuration loading from settings
- Model setup and validation
- MCP (Model Context Protocol) server initialization
- Environment and runtime configuration

### Key Directories Structure
```
GOB/
├── agent.py              # Core agent orchestration
├── models.py             # LLM model management
├── initialize.py         # System initialization
├── scripts/gob           # CLI management tool
├── python/               # Framework core libraries
├── webui/               # Web interface (HTML/CSS/JS)
├── agents/              # AI agent profiles/configurations
├── prompts/             # System and agent prompts
├── conf/                # Configuration files
├── docs/                # Documentation
├── monitoring/          # System monitoring tools
└── requirements.txt     # Python dependencies
```

### Agent Orchestration Flow
1. **Context Creation**: Each conversation creates an `AgentContext` with unique ID
2. **Agent Instantiation**: Main agent (Agent 0) created with configuration
3. **Message Processing**: User messages trigger the monologue loop
4. **Tool Execution**: Agents can call tools and create subordinate agents
5. **Response Generation**: Streaming responses with reasoning separation
6. **State Management**: History and context maintained across interactions

### Model Integration
- **Chat Model**: Primary conversational AI (GPT, Claude, etc.)
- **Utility Model**: Lightweight tasks and tool assistance
- **Browser Model**: Specialized for web automation
- **Embedding Model**: Vector storage and retrieval
- **Rate Limiting**: Per-provider request/token management

### Extension System
The codebase uses an extension system for:
- Custom tool integration
- Response processing
- History management
- Stream filtering
- Error handling

## Development Guidelines

### Code Organization
- **Core Logic**: Keep agent logic in `agent.py`, model management in `models.py`
- **Tools**: Add new tools in `python/tools/` directory
- **Agents**: Create specialized agents in `agents/` subdirectories
- **Prompts**: Store prompt templates in `prompts/` with markdown format
- **Configuration**: Use `conf/` for YAML configuration files

### Agent Development
- Extend `Agent` class for specialized behavior
- Use `AgentConfig` for model and system settings
- Implement tools by extending the base `Tool` class
- Utilize the extension system for modular functionality
- Follow the naming convention system for consistency

### Model Integration
- Use `models.py` functions to get model instances
- Configure rate limits in model configs
- Handle streaming responses with proper callbacks
- Support multiple providers through LiteLLM
- Test model changes with different providers

### Testing Approach
- Use `scripts/gob status` to verify server health
- Test new features by starting/restarting the server
- Monitor logs with `scripts/gob logs` for debugging
- Use the web interface at localhost:50080 for interactive testing
- Run test scripts in the root directory

### Configuration Management
- Environment variables in `.env` file
- Model configurations in `conf/model_providers.yaml`
- Agent profiles in `agents/` subdirectories
- Use `initialize.py` for reading and validating configs

### Web Interface
- Built with vanilla HTML/CSS/JavaScript
- Located in `webui/` directory
- Communicates with backend via API endpoints
- Supports real-time updates and streaming responses

### Memory and Knowledge
- `memory/` directory for agent memory persistence
- `knowledge/` directory for agent knowledge base
- Vector embeddings for semantic search
- History management for conversation continuity

### MCP Integration
- Model Context Protocol servers for external tool integration
- Configured via `mcp_servers` setting
- Fallback to local tools if MCP unavailable
- Dynamic tool loading and execution

## Important Notes

### Server Management
- Always use `scripts/gob` commands for server lifecycle management
- Server runs on port 50080 by default (configurable via .env)
- Conda environment `gob` must be activated for manual operations
- Log files stored in project root as `gob_output.log`

### Development Environment
- Python 3.13+ required
- Miniconda/Anaconda for environment management  
- All dependencies listed in `requirements.txt`
- Setup script handles automatic installation

### Agent Naming System
- Main agent name changes daily for variety
- Subordinate agents have consistent context-based names
- All agents use "GOB" acronym consistently
- Names are deterministic based on date/context

### Extension Points
- `monologue_start/end` - Conversation lifecycle
- `message_loop_start/end` - Per-message processing
- `tool_execute_before/after` - Tool execution hooks
- `response_stream_chunk` - Real-time response processing
- `hist_add_before` - History management

### Error Handling
- `RepairableException` - Errors forwarded to LLM for self-correction
- `InterventionException` - User interruptions during processing
- `HandledException` - Critical errors that stop execution
- Comprehensive logging for debugging

This codebase implements a sophisticated AI agent orchestration system with modular architecture, extensive model support, and robust error handling. Focus on the agent-centric design when making modifications, and always test changes through the web interface.
