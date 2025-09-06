# GOB Platform Development Environment

> **GOB Network Intelligence Platform** - Development Hub  
> Lead Developer Guidelines & Project Organization  
> **Version**: 2.0  
> **Last Updated**: 2025-01-06

---

## 🎯 Mission Statement

**GOB** is evolving into the **Network Intelligence Platform** - a revolutionary multi-device AI deployment system built on Agent Zero foundations. This development environment supports our transformation from a single-interface agent to a network-wide intelligence ecosystem.

---

## 📁 Development Structure

```
dev/
├── README.md                    # This file - development hub overview
├── architecture/                # System design, ADRs, technical blueprints
├── documentation/               # Complete developer documentation
├── projects/                    # Active development initiatives
├── standards/                   # Development standards & conventions
├── tools/                       # Development utilities & scripts
└── resources/                   # References, research, external docs
```

---

## 🚀 Current Active Projects

### **Priority 1: Terminal UI Migration**
- **Path**: `projects/terminal-ui/`  
- **Status**: Phase 0 - Architecture & Planning  
- **Goal**: Migrate from legacy WebUI to terminal-style interface  
- **Timeline**: 12 weeks  

### **Priority 2: Randomized GOB Identity System**
- **Path**: `projects/randomized-gob/`  
- **Status**: Ready for Implementation  
- **Goal**: Daily identity rotation and personality variation  
- **Timeline**: 2-3 days  

### **Priority 3: Agent Zero Integration**  
- **Path**: `projects/agent-zero-core/`  
- **Status**: Research & Integration Planning  
- **Goal**: Deep Agent Zero framework integration  
- **Timeline**: 8 weeks  

### **Priority 4: Network Intelligence Platform**
- **Path**: `projects/network-platform/`  
- **Status**: Future - Post UI Migration  
- **Goal**: Multi-device AI deployment system  
- **Timeline**: 24 weeks

---

## 📋 Development Standards

### **Code Quality Requirements**
- [ ] **TypeScript**: All new code must use TypeScript for type safety
- [ ] **Testing**: Minimum 80% test coverage for new features  
- [ ] **Documentation**: All public APIs must be documented  
- [ ] **Review Process**: All changes require peer review  
- [ ] **Performance**: No regressions in load time or memory usage

### **Architecture Principles**
- [ ] **Agent Zero Compatibility**: All changes must preserve Agent Zero patterns
- [ ] **Network-Ready**: Components must be extractable for device templates  
- [ ] **Event-Driven**: Loose coupling via event bus communication
- [ ] **Progressive Enhancement**: Core functionality without JavaScript
- [ ] **Security First**: CSRF protection, input validation, secure defaults

### **Documentation Standards**  
- [ ] **ADRs**: All architectural decisions must be documented
- [ ] **API Docs**: OpenAPI specs for all endpoints
- [ ] **User Guides**: Step-by-step instructions for features  
- [ ] **Developer Onboarding**: Complete setup instructions
- [ ] **Change Logs**: Semantic versioning with detailed changelogs

---

## 🛠️ Developer Workflow

### **1. Setup & Environment**
```bash
# Clone and setup
git clone <repo>
cd GOB
mamba env create -f environment.yml  # Python 3.13 + dependencies
mamba activate gob

# Frontend development (terminal UI)
cd dev/projects/terminal-ui
npm install
npm run dev
```

### **2. Branch Strategy**
- **main**: Production-ready code, protected branch
- **develop**: Integration branch for features  
- **feature/***: Individual feature development
- **hotfix/***: Critical production fixes

### **3. Commit Standards**
```
type(scope): description

feat(ui): add terminal command parser
fix(api): resolve websocket connection issue  
docs(architecture): add terminal UI ADR
test(chat): add message streaming tests
```

### **4. Pull Request Process**
1. **Create Feature Branch**: `git checkout -b feature/terminal-commands`
2. **Develop & Test**: Write code + tests, ensure CI passes
3. **Update Documentation**: Add/update relevant docs
4. **Submit PR**: Use PR template, request reviews
5. **Address Feedback**: Make requested changes
6. **Merge**: Squash merge after approval

---

## 🔧 Tools & Utilities

### **Development Tools**
- **Code Editor**: VS Code with GOB workspace settings
- **Package Manager**: Mamba for Python, npm for JavaScript
- **Testing**: pytest (Python), Vitest (JavaScript), Playwright (E2E)
- **Linting**: ruff (Python), ESLint (JavaScript)
- **Formatting**: black (Python), Prettier (JavaScript)

### **Build & Deployment**
- **Build System**: Vite for frontend, setuptools for Python
- **CI/CD**: GitHub Actions with automatic testing  
- **Containers**: Docker for consistent environments
- **Monitoring**: Built-in performance metrics

---

## 📚 Knowledge Base

### **Essential Reading**
1. **[Architecture Overview](architecture/README.md)** - System design principles
2. **[Development Standards](standards/README.md)** - Coding conventions  
3. **[Agent Zero Integration](resources/agent-zero/README.md)** - Framework patterns
4. **[API Documentation](documentation/api/README.md)** - Endpoint specifications
5. **[Deployment Guide](documentation/deployment/README.md)** - Production setup

### **Quick References**
- **[Command Reference](documentation/commands.md)** - Terminal UI commands
- **[API Quick Reference](documentation/api-quick-ref.md)** - Common endpoints
- **[Troubleshooting](documentation/troubleshooting.md)** - Common issues
- **[Performance Guide](documentation/performance.md)** - Optimization tips

---

## 🏗️ Architecture Overview

### **Current System**
```
GOB v1.x (Legacy WebUI)
├── Python Backend (Agent Zero Framework)
├── Alpine.js Frontend (Complex Modal UI)  
├── WebSocket Streaming
└── REST API Layer
```

### **Target System**
```
GOB v2.x (Network Intelligence Platform)
├── Agent Zero Core (Enhanced)
├── Terminal UI (Command-Driven)
├── Network Sync Layer  
├── Device Template Generator
└── Multi-Device Deployment
```

### **Migration Strategy**
- **Phase 1**: Terminal UI with full feature parity
- **Phase 2**: Agent Zero deep integration  
- **Phase 3**: Network intelligence capabilities
- **Phase 4**: Multi-device template generation

---

## 🔍 Code Review Guidelines

### **Review Checklist**
- [ ] **Functionality**: Does the code work as intended?
- [ ] **Agent Zero Compatibility**: Does it break existing patterns?
- [ ] **Performance**: Are there any performance regressions?
- [ ] **Security**: Are inputs validated, outputs sanitized?
- [ ] **Tests**: Are there adequate tests for new functionality?
- [ ] **Documentation**: Is the code and API documented?

### **Review Process**
1. **Automated Checks**: CI must pass before review
2. **Peer Review**: At least one senior developer approval
3. **Architecture Review**: For significant changes
4. **Security Review**: For security-sensitive changes
5. **Performance Review**: For performance-critical changes

---

## 📈 Success Metrics

### **Development Velocity**
- **Sprint Completion Rate**: >90% of planned work completed
- **Bug Resolution Time**: <24 hours for critical, <1 week for minor
- **Code Review Time**: <48 hours for standard PRs
- **Documentation Coverage**: 100% for public APIs

### **Quality Metrics**
- **Test Coverage**: >80% for all new code
- **Performance**: No regressions in page load or API response times
- **Security**: Zero known vulnerabilities in dependencies
- **User Experience**: Feature parity with legacy UI

---

## 🤝 Contributing

### **For Core Team**
- Full access to all projects and documentation
- Expected to follow all development standards
- Responsible for code review and mentoring
- Must maintain Agent Zero compatibility

### **For Contributors**
- Fork repository and submit PRs
- Must sign Contributor License Agreement  
- Follow coding standards and review process
- Focus on assigned project areas

### **Communication Channels**
- **Daily Standups**: Progress updates and blockers
- **Weekly Architecture Reviews**: Design decisions
- **Monthly Retrospectives**: Process improvements
- **Quarterly Planning**: Roadmap and priorities

---

## 🚨 Emergency Procedures

### **Critical Bug Response**
1. **Immediate**: Assess impact and severity
2. **Hotfix**: Create hotfix branch from main  
3. **Fix & Test**: Minimal fix with focused testing
4. **Deploy**: Emergency deployment process
5. **Post-Mortem**: Root cause analysis and prevention

### **Security Incident Response**
1. **Isolate**: Disable affected systems if necessary
2. **Assess**: Determine scope and impact
3. **Patch**: Apply security fix immediately  
4. **Communicate**: Notify stakeholders appropriately
5. **Review**: Security audit and improvements

---

## 📞 Support & Escalation

### **Technical Issues**
- **Level 1**: Individual developer troubleshooting
- **Level 2**: Team lead or senior developer assistance  
- **Level 3**: Architecture team or external experts
- **Level 4**: Vendor support or community help

### **Process Issues**
- **Development Process**: Team lead
- **Architecture Decisions**: Architecture review board
- **Resource Conflicts**: Project manager  
- **Strategic Direction**: Product owner

---

**GOB Platform Development Team**  
*Building the future of network-wide AI intelligence*

---

*For detailed information on any topic, refer to the specific documentation in the respective directories.*
