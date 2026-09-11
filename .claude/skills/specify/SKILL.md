---
name: specify
description: Defines a feature specification for Python Sprint Zero using spec-driven development. Produces structured requirements with user stories, acceptance criteria, hexagonal layer impact, API and CLI contracts, and Lagom wiring. Invoke as /specify <feature-description> before any code is written; run /plan on the result.
disable-model-invocation: true
allowed-tools: Read Glob Grep Write Bash
argument-hint: "[feature-description]"
---

# Specify

Define feature specifications before implementation. This follows a spec-driven development approach where requirements are fully articulated before any code is written. A spec describes **what** the feature does; `/plan` later describes **how** it is built.

## Usage

`/specify <feature-description>`

The full description is available as `$ARGUMENTS`.

## Process

1. **Read the project CLAUDE.md** (`.claude/CLAUDE.md`) for the non-negotiables: no comments, one assertpy assertion per test, layer boundaries, 100% coverage, prefer editing over creating.

2. **Derive `<feature-name>`** from `$ARGUMENTS` as a kebab-case slug (for example "add coconut deletion" → `coconut-deletion`). This slug is the argument to `/plan`.

3. **Scan the existing codebase** under `src/python_sprint_zero/` and `tests/python_sprint_zero/` for the closest existing feature (the `coconut` vertical slice is the reference) and for files this feature will extend rather than duplicate.

4. **Identify affected hexagonal layers** — which of domain, application, infrastructure, interface, or shared will this feature touch?

5. **Produce a specification document** saved to `.specs/<feature-name>/SPEC.md` with this structure:

```markdown
# Feature: <name>

## Overview
One-paragraph summary of the feature and its value.

## User Stories
- As a <role>, I want <goal> so that <benefit>
- ...

## Acceptance Criteria
- [ ] Given <context>, when <action>, then <outcome>
- ...

## Out of Scope
What this feature deliberately does not do.

## Hexagonal Layer Impact

### Domain Layer (`src/python_sprint_zero/domain/`)
New or modified Pydantic entities (`model/`), query and command repository interfaces as ABCs (`repository/`), domain services (`service/`), authentication rules (`authentication/`), health rules (`health/`).
List files that change or are created.
No imports from application, infrastructure, interface, or FastAPI.

### Application Layer (`src/python_sprint_zero/application/`)
New or modified use cases, one class per use case exposing `execute()` (`use_case/`), and application services (`service/`).
List files that change or are created.
No imports from infrastructure or interface.

### Infrastructure Layer (`src/python_sprint_zero/infrastructure/`)
New or modified repository implementations (`persistence/in_memory/`), authentication adapters (`security/`), health checks (`system/`), structured logging, metrics and tracing (`observability/`).
List files that change or are created.

### Interface Layer (`src/python_sprint_zero/interface/`)
New or modified FastAPI controllers (`api/controller/`), Pydantic DTOs (`api/data_transfer_object/`), container wiring and router registration (`api/main.py`), Click commands (`cli/main.py`).
List files that change or are created.
DTOs must not import `domain.model`; they convert via `from_domain_model()`.

### Shared Layer (`src/python_sprint_zero/shared/`)
Configuration settings (`configuration.py`), resilience patterns, formatters.
No imports from application, infrastructure, or interface.

## API Contracts
For each new or modified FastAPI endpoint: method, path, request DTO, response DTO, status codes, and whether HTTP Basic authentication is required.
Every response is a Pydantic DTO, never a plain dict.

## CLI Contracts
For each new or modified Click command in `interface/cli/main.py`: name, options, and output.

## Dependency Injection
New Lagom registrations for `get_container()` in `interface/api/main.py`.
Which abstract interface maps to which concrete implementation.

## Observability
Required structured log entries (with correlation-id), metrics, and tracing additions.

## Open Questions
List any ambiguities or decisions that need resolution.
```

6. **Cross-reference** the spec against existing specs in `.specs/` for consistency and conflicts.

7. Present the spec for review before proceeding to `/plan <feature-name>`.

## Additional resources

- For architecture rules and coding standards, see [CLAUDE.md](../../CLAUDE.md)
- For the enforced layer rules, see `tests/python_sprint_zero/test_architecture.py`
- For the reference vertical slice, see [existing-coconut-example](../hexagonal-architecture-scaffolder/references/existing-coconut-example.md)
- For the next step, see [plan](../plan/SKILL.md)
