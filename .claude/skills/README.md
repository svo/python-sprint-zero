# Claude Code Skills for Python Sprint Zero

This directory contains custom Claude Code skills tailored to this project's strict architectural and coding standards.

## Installed Skills (Tier 1 - Highest Value)

### 1. Hexagonal Architecture Feature Scaffolder
**Directory:** `hexagonal-architecture-scaffolder/`
**Trigger phrases:** "create a new feature", "scaffold a feature", "add a new domain entity", "create a new API endpoint"

**Purpose:** Guides Claude through creating complete features across all hexagonal architecture layers (domain → application → infrastructure → interface) with proper dependency injection, layer boundaries, and test coverage.

**Key features:**
- Step-by-step scaffolding across all layers
- Enforces layer boundary rules
- Generates repository interfaces in domain, implementations in infrastructure
- Creates use cases with dependency injection
- Generates DTOs and controllers
- Creates corresponding test files
- References existing coconut feature as example

**Supporting files:**
- `references/existing-coconut-example.md` - Complete example from codebase
- `references/layer-dependency-rules.md` - Import dependency rules

---

### 2. Test Generator with One-Assertion Rule
**Directory:** `test-generator/`
**Trigger phrases:** "generate tests", "create tests for", "write test cases", "add test coverage"

**Purpose:** Generates tests following the project's mandatory one-assertion-per-test rule with proper naming (`test_should_X_when_Y`), Arrange-Act-Assert structure, and appropriate mocking.

**Key features:**
- Enforces one assertion per test (critical project rule)
- Generates descriptive test names following pattern
- Creates Arrange-Act-Assert structure
- Provides testing patterns by layer (domain, application, infrastructure, interface)
- Shows how to properly mock dependencies
- Includes examples of exception testing, fixtures, and HTTP testing

**Supporting files:**
- `references/test-examples-from-codebase.md` - Actual test examples from project

---

### 3. Self-Documenting Code Refactorer
**Directory:** `self-documenting-refactor/`
**Trigger phrases:** "remove comments", "make code self-documenting", "refactor to eliminate comments", "improve code clarity"

**Purpose:** Enforces the project's strict NO COMMENTS policy by helping refactor code to be self-explanatory through expressive naming instead of comments.

**Key features:**
- Identifies comments in code
- Suggests refactoring strategies (extract to well-named function, expressive variables, boolean conditions, named constants)
- Provides before/after examples
- Teaches naming conventions for functions, variables, constants, booleans
- Includes common refactoring patterns

**Supporting files:**
- `scripts/find_comments.py` - Executable script to scan for comments in codebase

**Usage:**
```bash
# Find all comments in source code
python .claude/skills/self-documenting-refactor/scripts/find_comments.py src/

# Expected output: 0 comments
```

---

### 4. Observability Pattern Injector
**Directory:** `observability-injector/`
**Trigger phrases:** "add logging", "add observability", "add metrics", "add tracing", "implement correlation-id"

**Purpose:** Provides complete observability patterns including structured logging with correlation IDs, metrics collection, and distributed tracing. Creates the infrastructure that's documented but not yet implemented.

**Key features:**
- Complete logger infrastructure with JSON structured logging
- Correlation ID propagation across requests
- Metrics collection (counters, gauges, histograms)
- Distributed tracing with decorators
- FastAPI middleware for correlation IDs
- Usage patterns for each layer
- Testing patterns for observability

**Supporting files:**
- `templates/logger_template.py` - Complete logger implementation
- `templates/metrics_template.py` - Complete metrics collector implementation
- `templates/tracing_template.py` - Complete tracing decorator implementation

**Note:** This infrastructure doesn't exist yet in the project but is claimed as a key feature. This skill provides complete reference implementations.

---

## How Claude Code Uses Skills

### Automatic Invocation
Claude Code automatically loads and applies skills when trigger phrases are detected in user requests. For example:
- User: "Create a new user feature" → Loads Hexagonal Architecture Scaffolder
- User: "Generate tests for the UserService" → Loads Test Generator
- User: "This code has comments, make it clearer" → Loads Self-Documenting Refactorer

### Manual Invocation
You can also explicitly invoke skills:
- `/hexagonal-architecture-scaffolder` - Load architecture scaffolding guidance
- `/test-generator` - Load test generation guidance
- `/self-documenting-refactor` - Load code refactoring guidance
- `/observability-injector` - Load observability patterns

### Progressive Disclosure
Skills use progressive disclosure:
- Main `SKILL.md` contains core guidance (1,500-2,000 words)
- `references/` directory contains detailed examples and patterns
- `templates/` directory contains ready-to-use code templates
- `scripts/` directory contains executable helper scripts

Claude Code loads the main skill first, then references supporting files as needed.

## Skill Development Guidelines

These skills follow Claude Code best practices:

1. **Clear trigger phrases** - Specific, concrete phrases users would naturally say
2. **Imperative writing** - Direct instructions ("Create", "Add", "Use")
3. **Progressive disclosure** - Main guidance is concise, details in references
4. **Project-specific** - Tailored to this project's unique rules and patterns
5. **Complementary to testing** - Skills teach generation, automated tests validate

## Project-Specific Rules Enforced by Skills

All skills enforce these critical project rules:

- **NO COMMENTS** - Code must be self-documenting
- **One assertion per test** - Each test function has exactly ONE assertion
- **Layer boundaries** - Respect hexagonal architecture import restrictions
- **Dependency injection** - Always use Lagom DI, never direct instantiation
- **100% test coverage** - Every function must have tests
- **Type hints** - All function signatures must have type hints
- **`__init__.py` required** - All Python packages must have this file

## Testing Skills

To test if skills are working:

1. **Try trigger phrases in Claude Code:**
   - "Create a new product feature"
   - "Generate tests for ProductService"
   - "Remove comments from this code"
   - "Add logging to this use case"

2. **Verify skill loads:**
   - Claude should reference the skill in its response
   - Guidance should match skill content

3. **Check skill is applied:**
   - Generated code follows skill patterns
   - Layer boundaries respected
   - Tests have one assertion
   - No comments in generated code

## Extending Skills

To add more skills:

1. Create directory: `.claude/skills/skill-name/`
2. Add `SKILL.md` with YAML frontmatter and instructions
3. Optionally add `references/`, `templates/`, `scripts/` subdirectories
4. Use specific trigger phrases in description
5. Keep main skill body concise (1,500-2,000 words)
6. Update this README

## Additional Recommended Skills (Tier 2)

Future skills to consider:

- **CDCT Test Generator** - Consumer-Driven Contract Testing patterns
- **Dependency Injection Scaffolder** - Lagom container setup patterns
- **API Route Generator** - Complete endpoint scaffolding
- **Test Coverage Analyzer** - Identify untested code gaps

## Resources

- [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills)
- [Official Skills Repository](https://github.com/anthropics/skills)
- [Awesome Agent Skills](https://github.com/VoltAgent/awesome-agent-skills)
- Project coding standards: `.claude/CLAUDE.md`

## Verification

Check all skills are present:
```bash
ls -la .claude/skills/*/SKILL.md
```

Expected output: 4 SKILL.md files (one for each Tier 1 skill)
