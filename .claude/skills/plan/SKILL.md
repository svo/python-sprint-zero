---
name: plan
description: Creates a technical implementation plan from a Python Sprint Zero feature specification. Produces a step-by-step plan organized by hexagonal architecture layers, with an ordered TDD task list, Lagom wiring, and the tox quality gates each task must pass. Invoke as /plan <spec-name> after /specify has produced .specs/<spec-name>/SPEC.md.
disable-model-invocation: true
allowed-tools: Read Glob Grep Write Bash
arguments: spec-name
argument-hint: "[spec-name]"
---

# Plan

Create a technical implementation plan from a feature specification. This bridges the gap between "what" (the spec) and "how" (the code).

## Usage

`/plan <spec-name>`

Where `<spec-name>` matches a directory under `.specs/`. The argument is available as `$spec-name`.

## Process

1. **Read the spec** at `.specs/$spec-name/SPEC.md`.

2. **Read the project CLAUDE.md** (`.claude/CLAUDE.md`) for the non-negotiables: no comments, one assertpy assertion per test, layer boundaries, 100% coverage, prefer editing over creating.

3. **Scan the existing codebase** — identify files to edit (prefer editing over creating), the existing patterns to follow (the `coconut` slice: CQRS repository ABCs, `execute()` use cases, class-based controllers with a `create_<feature>_controller` factory, DTOs with `from_domain_model()`), and `__init__.py` files that new packages need under both `src/python_sprint_zero/` and `tests/python_sprint_zero/`.

4. **Produce a plan document** saved to `.specs/$spec-name/PLAN.md` with this structure:

```markdown
# Plan: <feature-name>

## Implementation Strategy
High-level approach and key architectural decisions.
Identify which existing files to modify vs. new files to create.

## Layer Changes

### Domain Layer (`src/python_sprint_zero/domain/`)
- New or modified Pydantic entities (`model/`)
- New or modified query and command repository interfaces using ABC (`repository/`)
- New or modified domain services (`service/`), authentication rules (`authentication/`), health rules (`health/`)
- No imports from application, infrastructure, interface, or FastAPI

### Application Layer (`src/python_sprint_zero/application/`)
- New or modified use cases, one class per use case with `execute()` (`use_case/`)
- New or modified application services (`service/`)
- Dependencies received via constructor injection as domain abstractions
- No imports from infrastructure or interface

### Infrastructure Layer (`src/python_sprint_zero/infrastructure/`)
- Repository implementations (`persistence/in_memory/`)
- Authentication adapters that import `domain.authentication` (`security/`)
- Health checks (`system/`)
- Structured logging with correlation-id, metrics, tracing (`observability/`)
- Implements domain interfaces

### Interface Layer (`src/python_sprint_zero/interface/`)
- FastAPI controller class with `_register_routes()` and a `create_<feature>_controller(container, authentication_dependency)` factory (`api/controller/`)
- Pydantic DTOs with `from_domain_model()` that do not import `domain.model` (`api/data_transfer_object/`)
- Lagom registrations in `get_container()` and `app.include_router(...)` in `api/main.py`
- Click commands (`cli/main.py`)

### Shared Layer (`src/python_sprint_zero/shared/`)
- Settings added to `configuration.py`
- New resilience patterns or formatters
- No imports from application, infrastructure, or interface

## Dependency Injection
- New Lagom registrations in `get_container()` (`interface/api/main.py`)
- Abstract-to-concrete mappings
- `Mock(spec=<Abstraction>)` fixtures in `tests/python_sprint_zero/conftest.py` for each new abstraction

## Task List

Ordered list of implementation tasks. Each task is independently committable and pairs one source module with its mirrored test module under `tests/python_sprint_zero/`.
Follow inside-out order: domain → application → infrastructure → interface → wiring.
Each task starts with a failing test (`test-driven-development`).

1. [ ] domain: <module> + <test module>
2. [ ] application: <module> + <test module>
3. [ ] infrastructure: <module> + <test module>
4. [ ] interface: <module> + <test module>
5. [ ] wiring: `get_container()` registration, router or CLI registration + `test_main*.py` updates
6. [ ] architecture: new pytest-archon rules in `tests/python_sprint_zero/test_architecture.py` if a new boundary is introduced
...

## Testing Strategy
- One assertion per test, using assertpy (`assert_that`), never bare `assert`
- Test names follow `test_should_<behaviour>_when_<condition>`
- Tests mirror the source tree under `tests/python_sprint_zero/<layer>/`
- Unit tests per layer with `Mock(spec=<Abstraction>)` doubles for every injected dependency
- Controller tests via FastAPI `TestClient`, including a `@pytest.mark.benchmark` case when a new route is added
- Architectural tests via pytest-archon validate layer boundaries
- CDCT producer tests for every new API route
- Tests must pass under `--random-order`; no shared mutable state between tests
- Verify with `tox` (not pytest directly) — enforces flake8, black, bandit, semgrep, pip-audit, radon, xenon, mypy, and 100% coverage
- Target: 100% coverage

## Observability Plan
- Structured log entries with correlation-id
- Metrics to collect (counters, gauges, histograms)
- Tracing decorators for use cases

## Risks and Mitigations
- Risk: a function exceeds xenon complexity grade A → Mitigation: extract well-named helpers
- Risk: <description> → Mitigation: <approach>
```

5. **Validate** the plan against the spec — confirm every acceptance criterion is covered by at least one task and every new file has a mirrored test file.

6. Present the plan for review before implementation. Implement with `hexagonal-architecture-scaffolder` and `test-driven-development`; gate completion with `verification-before-completion` (`tox`).

## Additional resources

- For the spec this plan is based on, see `.specs/$spec-name/SPEC.md`
- For architecture rules and coding standards, see [CLAUDE.md](../../CLAUDE.md)
- For the enforced layer rules, see `tests/python_sprint_zero/test_architecture.py`
- For scaffolding guidance, see [hexagonal-architecture-scaffolder](../hexagonal-architecture-scaffolder/SKILL.md)
- For the previous step, see [specify](../specify/SKILL.md)
