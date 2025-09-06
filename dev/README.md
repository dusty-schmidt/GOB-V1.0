# GOBV1 Development Hub

This directory contains all development work, planning, and progress tracking for GOBV1.

## 🚨 **IMPORTANT: Use Agent Zero Reference**

Before modifying any core functionality code, **ALWAYS** consult the Agent Zero reference:

```bash
# Check original Agent Zero implementation first
ls dev/references/agent-zero/
diff -u dev/references/agent-zero/[file] [file]
```

### **Development Rules:**
1. **📖 Reference First** - Study `dev/references/agent-zero/` before changing core code
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
- `dev/` - Development organization

---

## 📁 Directory Structure

### **Development Work**
- **`worklogs/`** - Development session tracking and progress logs
- **`ui-migration/`** - Terminal-style UI migration project  
- **`ideas/`** - Project concepts, feature ideas, and experimental plans
- **`references/`** - Reference materials and upstream Agent Zero codebase

### **Development Process**
1. **Quick Reference** - Check `worklogs/worksummary.md` for recent activity
2. **Detailed History** - Review relevant daily worklogs for context
3. **Agent Zero Check** - Compare with `references/agent-zero/` before core changes
4. **Development** - Work on features with proper documentation
5. **Documentation** - Update worklogs and project status

---

## 📋 Work Tracking

### **Work Summary** 
- **File**: `worklogs/worksummary.md` 
- **Purpose**: High-level timeline with timestamps and brief descriptions
- **Format**: One-line summaries linking to detailed worklogs
- **Update**: After every development session (every few hours)

### **Detailed Worklogs**
- **Directory**: `worklogs/YYYY-MM-DD-description.md`
- **Purpose**: Complete technical details, decisions, and impact assessment  
- **Template**: Session info, objectives, technical changes, next steps
- **Update**: Create new worklog for significant development sessions

### **Worklog Template**
Each detailed worklog should include:
1. **Session Info** - Date, time, duration, objectives
2. **Accomplishments** - What was completed and why
3. **Technical Details** - Files changed, key decisions, testing
4. **Impact Assessment** - Developer experience, code quality, operational benefits
5. **Next Steps** - Future opportunities and identified issues

---

## 💡 Ideas & Planning

### **Ideas Directory** (`ideas/`)
- **Purpose**: Experimental concepts, feature brainstorming, future planning
- **Structure**: Organized by topic with planning documents and prototypes
- **Status**: Ideas → Development → Integration or Archive

### **Reference Materials** (`references/`)
- **Agent Zero Base**: Complete upstream codebase for comparison
- **Documentation**: Architecture notes and development references
- **Usage**: Study before making changes to understand original implementation

---

## 🔄 Current Projects

### **UI Migration** (`ui-migration/`)
**Status**: Planning → Implementation  
**Goal**: Migrate from feature-rich interface to minimalist terminal-style UI  
**Reference**: Compare with Agent Zero's `webui/` before making changes

### **Development Infrastructure** 
**Status**: Complete ✅  
**Achievement**: Professional development workflow with tracking and guidelines

---

## 🎯 Development Philosophy

> **GOBV1 maintains Agent Zero's core functionality** with these enhancements:
> - Better setup experience (`setup.sh`, `gob` CLI)
> - Improved documentation and user guidance
> - Development organization tools
> - Simplified deployment (native conda vs Docker)

**Core agent orchestration, LLM handling, and web UI logic remain largely unchanged from Agent Zero.**

---

## 🚀 Getting Started

### **New Contributors**
1. Read this README for development guidelines
2. Check `worklogs/worksummary.md` for project context
3. Study Agent Zero reference in `references/agent-zero/`
4. Review relevant detailed worklogs for specific areas

### **Development Session**
1. Check latest work summary for context
2. Reference Agent Zero if touching core functionality  
3. Work on features with proper testing
4. Document session in new worklog
5. Update work summary with brief entry

### **Feature Development**
1. **Ideation** - Add concepts to `ideas/` directory
2. **Planning** - Create detailed plans and prototypes
3. **Reference** - Compare with Agent Zero implementation
4. **Development** - Implement with proper testing
5. **Documentation** - Update worklogs and guides

---

*Development work on GOBV1 focuses on enhancing user experience while preserving Agent Zero's proven core functionality.*
