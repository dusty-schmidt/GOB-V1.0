# GOB Development Standards

> **Unified development standards for the Network Intelligence Platform**  
> These standards ensure consistency, quality, and maintainability across all GOB projects.  
> **Last Updated**: 2025-01-06

---

## 📋 Standards Overview

All GOB development must adhere to these standards to maintain code quality, security, and Agent Zero compatibility.

| Standard | Scope | Compliance |
|----------|-------|------------|
| **[Coding Standards](coding/README.md)** | TypeScript, Python, CSS | Mandatory |
| **[Documentation](documentation/README.md)** | APIs, Architecture, User Guides | Mandatory |
| **[Testing](testing/README.md)** | Unit, Integration, E2E | Mandatory |
| **[Security](security/README.md)** | Input validation, Auth, CSRF | Mandatory |

---

## 🎯 Core Principles

### **1. Agent Zero Compatibility First**
- All changes must preserve existing Agent Zero patterns
- WebSocket streaming capabilities must be maintained
- Tool system integration must remain functional
- Context management must work seamlessly

### **2. Network Intelligence Ready**
- Components must be extractable for device templates
- State must be serializable for cross-device sync
- Event-driven architecture for loose coupling
- Progressive enhancement for different device capabilities

### **3. Performance & Security**
- No regressions in load time or memory usage
- All inputs validated, outputs sanitized
- CSRF protection on all state-changing operations
- Secure defaults for all configurations

### **4. Developer Experience**
- Clear, consistent APIs and interfaces
- Comprehensive documentation and examples
- Fast feedback loops with testing and linting
- Minimal setup and onboarding friction

---

## 🔧 Tool Configuration

### **Code Quality Tools**
All projects must use these tools with the provided configurations:

#### **TypeScript Configuration**
```json
// tsconfig.json - Standard configuration
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  }
}
```

#### **ESLint Configuration**
```json
// .eslintrc.json - Standard linting rules
{
  "extends": [
    "@typescript-eslint/recommended",
    "@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "prefer-const": "error",
    "no-var": "error"
  }
}
```

#### **Python Configuration** 
```toml
# pyproject.toml - Python project configuration
[tool.ruff]
target-version = "py313"
select = ["E", "F", "UP", "B", "SIM", "I"]
ignore = ["E501"]  # Line length handled by formatter

[tool.ruff.format]
quote-style = "double"
line-ending = "lf"
```

### **Git Configuration**
```bash
# .gitmessage - Commit message template
# Type: feat, fix, docs, style, refactor, test, chore
# Scope: ui, api, core, docs, test
# 
# feat(ui): add terminal command parser
# 
# - Implement command parsing with colon and slash prefixes
# - Add argument extraction and validation
# - Support command aliases and help text
# 
# Closes #123
```

---

## 📏 Quality Gates

### **Pre-Commit Requirements**
Every commit must pass these checks:

```bash
# Run quality gates
npm run lint          # ESLint checks
npm run type-check    # TypeScript compilation
npm run test:unit     # Unit tests
npm run format:check  # Code formatting
```

### **Pre-Push Requirements**  
Every push must pass these checks:

```bash
# Extended quality gates
npm run test:all      # All tests including integration
npm run build         # Production build succeeds
npm run audit         # Security audit passes
npm run perf:check    # Performance regression check
```

### **Pull Request Requirements**
Every PR must satisfy:

- [ ] All automated checks pass (CI/CD)
- [ ] Code coverage ≥ 80% for new code
- [ ] Performance meets defined benchmarks
- [ ] Security review completed (if applicable)
- [ ] Documentation updated
- [ ] At least one peer review approval

---

## 🏗️ Architecture Standards

### **File Structure Standards**
```
project-name/
├── src/                     # Source code
│   ├── components/         # Reusable components
│   ├── stores/             # State management
│   ├── utils/              # Shared utilities
│   └── types/              # TypeScript type definitions
├── tests/                   # Test files (mirrors src/)
├── docs/                    # Project documentation  
├── tools/                   # Build and dev tools
└── config/                  # Configuration files
```

### **Naming Conventions**
- **Files**: `kebab-case.ts`, `PascalCase.vue`
- **Directories**: `kebab-case`
- **Variables**: `camelCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Classes**: `PascalCase`
- **Functions**: `camelCase`

### **Import Standards**
```typescript
// Import order and style
import { type ComponentProps } from 'react';        // Types first
import { useState, useEffect } from 'react';        // External libraries
import { Button, Input } from '@/components/ui';    // Internal components  
import { useStore } from '@/stores/app';             // Internal utilities
import type { User } from '@/types/user';           // Local types
```

---

## 🧪 Testing Standards

### **Test Coverage Requirements**
- **Unit Tests**: 80% minimum coverage for all new code
- **Integration Tests**: All API endpoints and component interactions
- **E2E Tests**: Critical user workflows and edge cases

### **Test Organization**
```typescript
// Standard test structure
describe('ComponentName', () => {
  describe('when condition', () => {
    it('should behave as expected', () => {
      // Arrange
      const input = 'test data';
      
      // Act  
      const result = functionUnderTest(input);
      
      // Assert
      expect(result).toBe('expected output');
    });
  });
});
```

### **Test Naming Conventions**
- **Unit Test Files**: `component-name.test.ts`
- **Integration Test Files**: `feature-name.integration.test.ts`  
- **E2E Test Files**: `user-workflow.e2e.test.ts`

---

## 📖 Documentation Standards

### **Code Documentation**
```typescript
/**
 * Parses terminal commands and extracts arguments
 * 
 * @param input - Raw user input from terminal
 * @param context - Current terminal context
 * @returns Parsed command with arguments and metadata
 * 
 * @example
 * ```typescript
 * const result = parseCommand(':files ls /home', context);
 * console.log(result.command); // 'files'
 * console.log(result.args);    // ['ls', '/home']
 * ```
 */
export function parseCommand(input: string, context: Context): ParsedCommand {
  // Implementation...
}
```

### **API Documentation**
All REST endpoints and WebSocket events must be documented with:
- Purpose and behavior description
- Request/response schemas with examples
- Error conditions and codes
- Authentication requirements
- Rate limiting information

### **Architecture Documentation**
All significant architectural decisions must be documented as ADRs (Architecture Decision Records) with:
- Context and problem statement
- Decision and rationale
- Alternatives considered
- Consequences and trade-offs

---

## 🔒 Security Standards

### **Input Validation**
```typescript
// Standard input validation pattern
import { z } from 'zod';

const CommandSchema = z.object({
  command: z.string().min(1).max(100),
  args: z.array(z.string()).max(10),
  context: z.string().uuid()
});

export function validateCommand(input: unknown): CommandInput {
  return CommandSchema.parse(input);
}
```

### **Output Sanitization**
```typescript
// Standard output sanitization
import DOMPurify from 'dompurify';

export function sanitizeHtml(content: string): string {
  return DOMPurify.sanitize(content, {
    ALLOWED_TAGS: ['p', 'br', 'strong', 'em', 'code', 'pre'],
    ALLOWED_ATTR: ['class']
  });
}
```

### **Authentication & Authorization**
- All API endpoints must validate CSRF tokens
- User sessions must be validated on each request  
- Sensitive operations require re-authentication
- Proper error messages that don't leak information

---

## 🚀 Performance Standards

### **Performance Budgets**
- **Page Load Time**: ≤ 500ms (75th percentile)
- **Bundle Size**: ≤ 200KB compressed
- **Memory Usage**: ≤ 50MB peak
- **API Response Time**: ≤ 200ms (95th percentile)

### **Performance Monitoring**
```typescript
// Standard performance monitoring
export function trackPerformance(event: string, data?: Record<string, unknown>): void {
  performance.mark(`${event}-start`);
  
  // Operation...
  
  performance.mark(`${event}-end`);
  performance.measure(event, `${event}-start`, `${event}-end`);
  
  const measure = performance.getEntriesByName(event)[0];
  if (measure.duration > PERFORMANCE_THRESHOLD) {
    console.warn(`Performance threshold exceeded: ${event} took ${measure.duration}ms`);
  }
}
```

---

## 🔄 Continuous Integration

### **Pipeline Stages**
1. **Code Quality**: Linting, formatting, type checking
2. **Testing**: Unit, integration, and E2E tests
3. **Security**: Vulnerability scanning and security tests
4. **Performance**: Bundle size and performance regression tests
5. **Build**: Production build and artifact generation
6. **Deploy**: Deployment to staging and production environments

### **Quality Gates**
- All tests must pass (100% success rate)
- Code coverage ≥ 80% for changed files
- No high or critical security vulnerabilities
- Performance budgets must be met
- All documentation must be up to date

---

## 📈 Metrics & Monitoring

### **Code Quality Metrics**
- **Technical Debt Ratio**: ≤ 5%
- **Code Coverage**: ≥ 80%  
- **Duplication**: ≤ 3%
- **Maintainability Index**: ≥ 70

### **Development Metrics**
- **Lead Time**: Feature to production ≤ 7 days
- **Deployment Frequency**: ≥ 1 per day
- **Mean Time to Recovery**: ≤ 1 hour
- **Change Failure Rate**: ≤ 10%

---

## 🤝 Code Review Standards

### **Review Checklist**
- [ ] **Functionality**: Code works as intended
- [ ] **Architecture**: Follows established patterns
- [ ] **Performance**: No performance regressions
- [ ] **Security**: Proper validation and sanitization
- [ ] **Testing**: Adequate test coverage
- [ ] **Documentation**: Code and APIs documented
- [ ] **Maintainability**: Code is readable and maintainable

### **Review Process**
1. **Author Self-Review**: Check your own code first
2. **Automated Checks**: Ensure CI passes
3. **Peer Review**: At least one team member approval
4. **Architecture Review**: For significant changes
5. **Merge**: Squash merge with clear commit message

---

## 📞 Getting Help

### **Standards Questions**
- Check this documentation first
- Ask in team chat for clarifications
- Escalate to architecture team for interpretations

### **Tool Setup Issues**
- Follow the setup guides in each standard
- Check the troubleshooting section
- Ask for help from senior developers

### **Process Improvements**
- Suggest improvements via GitHub issues
- Discuss in retrospective meetings
- Propose changes through RFC process

---

**GOB Development Standards Team**  
*Ensuring quality and consistency across the Network Intelligence Platform*
