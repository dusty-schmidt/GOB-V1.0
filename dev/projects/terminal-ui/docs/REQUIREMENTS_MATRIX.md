# GOB UI Migration - Requirements Triage & Preservation Matrix

> **Purpose**: Define exactly which behaviors must survive, be simplified, or be retired in the terminal UI migration
> 
> **Status**: Phase 0 - Migration Planning  
> **Aligned with**: Strategic Framework & Agent Zero patterns  
> **Last Updated**: 2025-01-06

---

## Migration Strategy Framework

### **Preservation Categories**

| Symbol | Category | Action | Justification |
|--------|----------|---------|---------------|
| 🟢 **PRESERVE** | Keep exactly as-is | Direct port with terminal styling | Core functionality, zero compromise |
| 🟡 **SIMPLIFY** | Streamline but maintain | Reduce complexity, keep essence | Important but overly complex |
| 🔄 **REDESIGN** | Rethink for terminal UX | Terminal-native approach | Good feature, poor current UX |
| 🔴 **RETIRE** | Remove from terminal UI | Not implemented | Redundant or obsolete |

---

## Core Chat System - **100% PRESERVE**

### **Chat Input & Output** 🟢 **PRESERVE**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Message input textarea | Terminal command line with multiline support | Essential - must support same input patterns |
| Enter/Shift+Enter behavior | Same keyboard shortcuts | User muscle memory critical |
| Auto-resize input | Terminal prompt expansion | Essential UX behavior |
| Message streaming | Character-by-character terminal output | Core Agent Zero pattern |
| Message types (user/assistant/system) | Terminal prompt differentiation (`$` vs `>` vs `#`) | Visual hierarchy essential |
| Auto-scroll management | Terminal scroll with user preference | Core usability feature |

### **Attachment System** 🟢 **PRESERVE**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| File drag & drop | Terminal drag & drop to command line | Essential functionality |
| Attachment preview | Terminal-styled file listing | User needs preview |
| Multiple file upload | Same batch upload capability | Core workflow |
| File type validation | Same validation with terminal feedback | Security requirement |

### **WebSocket Streaming** 🟢 **PRESERVE**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Real-time message updates | Character streaming to terminal output | Agent Zero core pattern |
| Connection status indicators | Terminal connection indicator | User needs connection awareness |
| Auto-reconnect logic | Same reconnect with terminal feedback | Reliability requirement |
| Progress indication | Terminal progress bars | User needs progress feedback |

---

## Settings Management - **SIMPLIFY**

### **Settings Interface** 🟡 **SIMPLIFY**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Multi-tab modal interface | Terminal command-based settings (`:settings agent`, `:settings mcp`) | Too complex for terminal UX |
| Dynamic field types | Terminal-friendly form fields | Maintain functionality, simpler UI |
| Real-time validation | Same validation with terminal feedback | Essential for UX |
| Settings persistence | Same backend persistence | Data integrity requirement |

### **Settings Commands** 🔄 **REDESIGN**
- **Agent Settings**: `:config agent` or `:agent-config`
- **External Services**: `:config external` or `:external-config`  
- **MCP/A2A**: `:config mcp` or `:mcp-config`
- **Developer**: `:config dev` or `:dev-config`
- **Task Scheduler**: `:scheduler` or `:tasks`
- **Backup & Restore**: `:backup` or `:restore`

---

## File System - **REDESIGN FOR TERMINAL**

### **File Browser** 🔄 **REDESIGN**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Modal tree interface | Terminal file explorer with `ls`, `cd` commands | Terminal-native navigation |
| File operations | Terminal commands (`rm`, `mv`, `cp`, `mkdir`) | Familiar terminal patterns |
| Upload interface | Drag & drop to terminal or `:upload` command | Simplified but functional |
| Download links | `:download <file>` command | Terminal-appropriate |

### **File Commands** 🔄 **REDESIGN**
- **Browse Files**: `:files` or `:ls`
- **Navigate**: `:cd <path>`
- **Upload**: `:upload` or drag & drop
- **Download**: `:download <file>`
- **Delete**: `:rm <file>`
- **New Folder**: `:mkdir <name>`

---

## Task Scheduler - **SIMPLIFY & REDESIGN**

### **Task Management** 🟡 **SIMPLIFY**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Complex task creation modal | Command-based task creation | Overly complex current UI |
| Visual cron builder | Text-based cron with help | Terminal-appropriate |
| Multiple task types | Same types, simpler creation | Functionality preserved |
| Task state management | Terminal status indicators | Visual feedback needed |

### **Scheduler Commands** 🔄 **REDESIGN**
- **List Tasks**: `:tasks` or `:scheduler`
- **Create Task**: `:task create <name>`
- **Edit Task**: `:task edit <id>`
- **Delete Task**: `:task delete <id>`
- **Run Task**: `:task run <id>`
- **Task Status**: `:task status <id>`

---

## Chat History & Context - **PRESERVE**

### **Context Management** 🟢 **PRESERVE**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Multiple chat contexts | Terminal context switching | Essential workflow |
| Chat creation/deletion | Terminal commands for chat management | Core functionality |
| Context persistence | Same backend persistence | Data integrity |
| Chat naming | Terminal-based naming | User organization need |

### **History Commands** 🔄 **REDESIGN**
- **List Chats**: `:chats` or `:history`
- **New Chat**: `:new` or `:new-chat`
- **Load Chat**: `:load <id>` or `:switch <id>`
- **Save Chat**: `:save <name>`
- **Delete Chat**: `:delete <id>`

---

## Notifications - **REDESIGN FOR TERMINAL**

### **Notification System** 🔄 **REDESIGN**
| Current Feature | Terminal Implementation | Rationale |
|-----------------|-------------------------|-----------|
| Toast notifications | Terminal status line messages | Terminal-appropriate feedback |
| Notification stack | Rolling status messages | Terminal-native approach |
| Auto-dismiss | Same timing behavior | UX consistency |
| Error/success types | Color-coded terminal messages | Visual hierarchy |

---

## Features to **RETIRE** in Terminal UI

### **Legacy Features** 🔴 **RETIRE**
- **Multiple modal systems**: Redundant implementations
- **Complex tooltip system**: Terminal help text is sufficient
- **Fancy animations**: Terminal UI should be fast and simple
- **Image modal**: Terminal can display images inline
- **Complex responsive breakpoints**: Terminal is inherently responsive

### **Nice-to-Have Features** 🔴 **RETIRE** *(Phase 1)*
- **Speech integration**: Focus on core functionality first
- **Agent naming system**: Can be added later
- **Tunnel management**: Specialized feature for later
- **Advanced accessibility features**: Basic terminal accessibility first

---

## Terminal UI Design Principles

### **Core Principles** 
1. **Command-Driven**: Every action should have a terminal command
2. **Keyboard-First**: Minimal mouse interaction required
3. **Monospace Aesthetic**: Consistent terminal look and feel
4. **Fast & Responsive**: No heavy animations or transitions
5. **Network-Ready**: Built for multi-device deployment

### **Command Syntax Standards**
- **Settings**: `:config <category>` or `:set <key>=<value>`
- **File Operations**: `:files`, `:cd`, `:ls`, `:upload`, `:download`
- **Chat Management**: `:new`, `:load`, `:save`, `:delete`, `:chats`
- **Task Management**: `:tasks`, `:task <action>`
- **Help System**: `:help` or `:help <command>`

### **Visual Hierarchy**
- **User Input**: `$ command` (prompt style)
- **Assistant Output**: `> response` (response style)  
- **System Messages**: `# status` (system style)
- **Error Messages**: `! error` (error style)
- **Success Messages**: `✓ success` (success style)

---

## Implementation Phases

### **Phase 1: Core Terminal** (Weeks 1-4)
🟢 **PRESERVE**: Chat system, WebSocket streaming, basic settings  
🔄 **REDESIGN**: File browser, notification system  
🔴 **RETIRE**: Legacy modals, complex animations  

### **Phase 2: Advanced Features** (Weeks 5-8)
🟡 **SIMPLIFY**: Task scheduler, complex settings  
🔄 **REDESIGN**: Chat history, context management  
🟢 **PRESERVE**: API layer, state management  

### **Phase 3: Polish & Integration** (Weeks 9-12)
🟡 **SIMPLIFY**: Advanced settings, edge cases  
🔄 **REDESIGN**: Help system, error handling  
🟢 **PRESERVE**: All core functionality  

---

## Success Criteria

### **Functional Parity**
- [ ] All Essential features work identically to current UI
- [ ] All Important features work with simplified but complete functionality  
- [ ] All API endpoints and WebSocket channels preserved
- [ ] All keyboard shortcuts maintained or improved

### **Performance Requirements**  
- [ ] Page load time ≤ current UI
- [ ] Message streaming ≥ current speed
- [ ] Memory usage ≤ current UI
- [ ] Bundle size ≤ 50% of current assets

### **User Experience Goals**
- [ ] Zero learning curve for existing power users
- [ ] Faster common operations via keyboard shortcuts
- [ ] Consistent terminal aesthetic throughout
- [ ] Network deployment readiness

---

## Risk Assessment

### **High Risk** 🔴
- **WebSocket streaming**: Complex real-time state management
- **File upload system**: Large files and error handling
- **Settings persistence**: Complex form state management

### **Medium Risk** 🟡  
- **Task scheduler**: Complex cron syntax and datetime handling
- **Chat context switching**: State management between contexts
- **Responsive design**: Terminal UI at different screen sizes

### **Low Risk** 🟢
- **Basic chat functionality**: Well-understood patterns
- **Simple file operations**: Standard terminal commands
- **Notification system**: Simple terminal feedback

---

## Stakeholder Approval

### **Required Sign-offs**
- [ ] **Product Owner**: Feature priority and retirement decisions
- [ ] **Technical Lead**: Architecture and implementation approach  
- [ ] **Users**: Terminal command syntax and workflow approval
- [ ] **DevOps**: Deployment and build system requirements

---

*This matrix serves as the definitive scope for the GOB terminal UI migration. Any changes require stakeholder approval and documentation updates.*
