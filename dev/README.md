# GOB Development Projects

This directory contains active development work that's beyond the experimental/ideas phase but not yet integrated into the main production codebase.

## 🚨 **IMPORTANT: Use Agent Zero Reference**

Before modifying any core functionality code, **ALWAYS** consult the Agent Zero reference:

```bash
# Check original Agent Zero implementation first
ls references/agent-zero/
diff -u references/agent-zero/[file] [file]
```

### **Development Rules:**
1. **📖 Reference First** - Study `references/agent-zero/` before changing core code
2. **🔍 Compare Implementations** - Understand how features work in original Agent Zero
3. **⚠️ Preserve Core Logic** - GOBV1's value is in UX improvements, not core rewrites
4. **🧪 Test Thoroughly** - Changes to core files can break agent orchestration

### **Core Files to Reference:**
- `agent.py` - Main agent orchestration logic
- `models.py` - LLM provider configurations  
- `python/` - Framework core functionality
- `webui/` - Web interface components
- `agents/` - Agent definitions and prompts

### **Safe to Modify:**
- `gob` - CLI tool (GOBV1-specific)
- `setup.sh` - Setup script (GOBV1-specific)  
- `docs/` - Documentation (GOBV1-specific)
- `dev/`, `ideas/`, `worklogs/` - Development organization

---

## Current Projects

### `ui-migration/`
**Status**: Planning → Implementation  
**Goal**: Migrate GOB's webui from feature-rich interface to minimalist terminal-style UI  
**Timeline**: 15 weeks (estimated)  
**Lead**: [Your name]

#### Structure:
- `docs/` - Migration plan, progress tracking, requirements
- `prototypes/` - UI mockups, experimental implementations  
- `tests/` - Regression tests for UI migration
- `assets/` - Design assets, screenshots, mockups

## Guidelines

- Each project should have its own README with current status
- Use branches for active development: `feature/project-name`
- Move completed projects to appropriate locations in main codebase
- Archive completed projects that don't merge to main
- **Always reference Agent Zero before modifying core functionality**

## Project Lifecycle

1. **Ideas** → Experimental concepts in `/ideas/`
2. **Development** → Active projects move here with structure
3. **Reference Check** → Compare with Agent Zero original implementation
4. **Integration** → Features merge into production code  
5. **Archive** → Completed projects archived with documentation

## Agent Zero vs GOBV1

**GOBV1 maintains Agent Zero's core functionality** with these enhancements:
- Better setup experience (`setup.sh`, `gob` CLI)
- Improved documentation and user guidance
- Development organization tools
- Simplified deployment (native conda vs Docker)

**Core agent orchestration, LLM handling, and web UI remain largely unchanged.**
