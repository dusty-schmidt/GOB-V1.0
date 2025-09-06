# ADR-001: Terminal UI Technology Stack

> **Status**: Accepted  
> **Date**: 2025-01-06  
> **Author**: Lead Developer  
> **Reviewers**: Architecture Team

---

## Context

GOB is migrating from a complex Alpine.js-based WebUI to a terminal-style interface as part of the Network Intelligence Platform evolution. We need to select technologies that:

1. Maintain full Agent Zero compatibility
2. Support network-wide deployment
3. Enable device template generation  
4. Provide excellent performance
5. Facilitate easy maintenance and development

## Decision

We will use the following technology stack for the Terminal UI:

### **Frontend Framework**
- **Primary**: Vanilla JavaScript with Alpine.js 3.x
- **Rationale**: 
  - Maintains compatibility with existing Agent Zero patterns
  - Lightweight and performant
  - Minimal build complexity
  - Excellent for reactive terminal interfaces

### **CSS Architecture**  
- **Primary**: CSS Custom Properties + CSS Grid
- **Build**: PostCSS with Tailwind CSS for utilities
- **Rationale**:
  - Terminal aesthetic requires precise control
  - Custom properties enable theming
  - Grid provides responsive terminal layouts
  - Tailwind speeds development without bloat

### **Build System**
- **Primary**: Vite with TypeScript
- **Testing**: Vitest + Playwright
- **Rationale**:
  - Fast development and hot reload
  - TypeScript for better code quality
  - Excellent testing ecosystem
  - Production-ready optimization

### **State Management**
- **Primary**: Event-driven architecture with Alpine stores
- **Persistence**: LocalStorage + WebSocket sync  
- **Rationale**:
  - Aligns with Agent Zero event patterns
  - Enables network synchronization
  - Simple but scalable
  - No heavy framework overhead

### **Communication Layer**
- **WebSocket**: Existing Agent Zero WebSocket channels
- **REST API**: Existing GOB REST endpoints with CSRF protection
- **Rationale**:
  - Zero breaking changes to backend
  - Preserves all Agent Zero streaming capabilities
  - Maintains security patterns

## Alternatives Considered

### **React + TypeScript**
- **Pros**: Strong ecosystem, excellent TypeScript support
- **Cons**: Heavy runtime, would require significant Agent Zero adaptation, overkill for terminal UI
- **Verdict**: Rejected - too heavy for terminal aesthetic

### **Vue 3 + Composition API**  
- **Pros**: Good performance, nice developer experience
- **Cons**: Another learning curve, not aligned with existing Agent Zero patterns
- **Verdict**: Rejected - doesn't leverage existing knowledge

### **HTMX + Server-Side Rendering**
- **Pros**: Minimal JavaScript, server-driven
- **Cons**: Would require major backend changes, limited for real-time features
- **Verdict**: Rejected - too disruptive to current architecture

### **Pure Vanilla JavaScript**
- **Pros**: Zero dependencies, maximum control
- **Cons**: Significant development overhead, no reactivity patterns
- **Verdict**: Rejected - too much reinventing the wheel

## Implementation Plan

### **Phase 1: Foundation (Weeks 1-2)**
- Set up Vite + TypeScript build system
- Create terminal CSS design system
- Implement command parser and router
- Set up testing infrastructure

### **Phase 2: Core Features (Weeks 3-6)**  
- Migrate chat system with WebSocket streaming
- Implement command-based settings
- Port file browser as terminal commands
- Add notification system

### **Phase 3: Advanced Features (Weeks 7-10)**
- Complete task scheduler migration
- Implement chat history and context switching
- Add help system and documentation
- Performance optimization and testing

### **Phase 4: Polish & Deploy (Weeks 11-12)**
- Accessibility improvements
- Cross-browser testing
- Production deployment
- Legacy UI sunset planning

## Consequences

### **Positive**
- ✅ Maintains full Agent Zero compatibility
- ✅ Lightweight and fast terminal UI
- ✅ Network-ready architecture from day one
- ✅ Familiar development patterns for the team
- ✅ Easy to extract components for device templates

### **Negative**
- ❌ Some learning curve for advanced TypeScript patterns
- ❌ Need to maintain two UIs during transition period
- ❌ Limited rich UI components (by design for terminal aesthetic)

### **Risks & Mitigations**
- **Risk**: WebSocket streaming complexity
  - **Mitigation**: Reuse existing Agent Zero streaming patterns
- **Risk**: State synchronization across devices
  - **Mitigation**: Build network sync layer incrementally
- **Risk**: Terminal UI learning curve for users
  - **Mitigation**: Comprehensive help system and gradual migration

## Success Metrics

### **Technical Metrics**
- [ ] Bundle size ≤ 200KB (current: ~500KB)
- [ ] Page load time ≤ 500ms (current: ~800ms)  
- [ ] Memory usage ≤ 50MB (current: ~80MB)
- [ ] Test coverage ≥ 80%

### **Functional Metrics**
- [ ] 100% feature parity with legacy UI
- [ ] All Agent Zero WebSocket channels preserved
- [ ] All REST API endpoints unchanged
- [ ] Zero regressions in core workflows

### **User Experience Metrics**
- [ ] Command completion time ≤ 100ms
- [ ] Terminal response time ≤ 50ms
- [ ] Keyboard-only navigation 100% functional
- [ ] Help system coverage 100%

## Implementation Details

### **Project Structure**
```
dev/projects/terminal-ui/
├── src/
│   ├── components/          # Terminal components
│   ├── commands/           # Command implementations  
│   ├── stores/             # Alpine.js stores
│   ├── styles/             # CSS and design tokens
│   └── utils/              # Shared utilities
├── tests/
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── e2e/                # End-to-end tests
├── docs/
│   ├── commands.md         # Command reference
│   ├── architecture.md     # Technical architecture
│   └── deployment.md       # Deployment guide
└── tools/
    ├── build.js            # Build scripts
    └── generate-commands.js # Command generation
```

### **Development Environment**
```bash
# Setup
cd dev/projects/terminal-ui
npm install

# Development
npm run dev              # Start dev server
npm run build            # Production build  
npm run test             # Run all tests
npm run test:watch       # Watch mode testing
npm run lint             # Code linting
npm run format           # Code formatting
```

### **Architecture Principles**
1. **Command-First**: Every user action maps to a terminal command
2. **Event-Driven**: Components communicate via event bus  
3. **Network-Ready**: State and components are serializable
4. **Performance-First**: Minimize DOM manipulation and memory usage
5. **Accessibility**: Full keyboard navigation and screen reader support

## Review and Approval

### **Technical Review**
- [ ] **Architecture Team**: Approved architecture and technology choices
- [ ] **Backend Team**: Confirmed API and WebSocket compatibility  
- [ ] **UI/UX Team**: Approved terminal interface design
- [ ] **Security Team**: Reviewed security implications

### **Implementation Readiness**
- [ ] Development environment set up
- [ ] Build system configured
- [ ] Testing framework ready
- [ ] Documentation structure created
- [ ] Team training completed

---

**Decision Status**: ✅ **Accepted**  
**Implementation Start**: 2025-01-06  
**Expected Completion**: 2025-04-06  

---

*This ADR will be reviewed quarterly and updated as the implementation progresses.*
