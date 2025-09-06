# GOBV1 Reference Materials

This directory contains reference materials for GOBV1 development.

## Contents

### Agent Zero (Original Framework)
- **Directory**: `agent-zero/`
- **Source**: https://github.com/agent0ai/agent-zero.git
- **Purpose**: Official Agent Zero repository that GOBV1 is based on
- **Usage**: Reference for original architecture, features, and implementation patterns

### Other References
- **File**: `acronyms.md` - Agent naming expansion references
- **File**: `architechture.md` - Architecture documentation
- **File**: `development.md` - Development notes

## Using References

### Comparing Changes
```bash
# Compare file structures
diff -u references/agent-zero/agent.py agent.py

# Compare directories
diff -r references/agent-zero/python/ python/

# Find GOBV1-specific additions
find . -name "*.py" | grep -v references | xargs grep -l "GOBV1\|General Orchestrator Bot"
```

### Understanding Original Features
- Study `references/agent-zero/` to understand base functionality
- Compare with GOBV1 implementation to see customizations
- Use as reference for bug fixes and feature development

### Development Workflow
1. **Before making changes**: Check original implementation in `agent-zero/`
2. **Adding features**: See if similar exists in original framework
3. **Bug fixes**: Compare with original to identify regressions
4. **Architecture decisions**: Reference original design patterns

## Key Differences from Agent Zero

GOBV1 modifications include:
- Native conda setup (removed Docker complexity)
- CLI management tool (`gob` command)
- Automatic setup script (`setup.sh`)
- Simplified documentation structure
- Custom branding and naming
- Enhanced error handling and user feedback

## Updating References

To update the Agent Zero reference:
```bash
cd references/agent-zero/
git pull origin main
```

---

**Note**: The `agent-zero/` directory is read-only for reference purposes.
All GOBV1 development happens in the main project directories.
