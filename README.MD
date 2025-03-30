# Python Sprint Zero

## Architecture

The architectural structure and design rules for this project uses a combination of Hexagonal Architecture and Domain-Driven Design (`DDD`) principles. The architecture is organized into clearly separated domain, application, infrastructure, and interface layers, following clean architecture principles. The domain layer encapsulates entities and business rules, the application layer manages orchestration through use cases, infrastructure contains data persistence implementations with repositories, and the interface layer provides `RESTful` `API` routes. The structure emphasizes high test coverage, maintainability, and security by design.

---

### Project Structure Overview

```
project/

 application/                       # Use cases
    use_cases/
        import_data_use_case.py
        get_data_use_case.py
        check_health_use_case.py
    services/
        auth_service.py

 domain/                            # Business logic
    auth/
        user_identity.py
    health/
        health_status.py
    model/
       data_record.py
    repository/
       data_repository.py
    service/
       data_import_service.py
    enums/
       user_role.py

 infrastructure/                    # Adapters, drivers
    observability/
        logger.py
        metrics.py
        tracing.py
    persistence/
       in_memory_repository.py
    caching/
        cache_provider.py
    messaging/
        message_producer.py
        message_consumer.py
    file_importer/
       csv_data_importer.py
       base_importer.py
    security/
       auth_backend.py
       token_provider.py
    audit/
       audit_logger.py
    system/
        health_checker.py

 interface/                         # APIs and CLI
    api/
        main.py
        controllers/
           health_controller.py
        dtos/
            health_status_dto.py
    cli/

 shared/                            # Cross-cutting concerns
     configuration.py
     resilience/
         retry.py
         circuit_breaker.py
     formatters/
```

---

### Design Principles

#### Domain

- `models/` contain pure domain entities (e.g., `DataRecord`)
- `repositories/` define interfaces for persistence (abstract base classes)
- `services/` contain stateless domain logic (business rules)

#### Application

- Use cases (`_use_case.py`) orchestrate logic/delegate
- Should not directly depend on e.g. `FastAPI`, database, or file system

#### Infrastructure

- Implements interfaces from `domain.repositories`
- `file_importer` handles imports
- `security/` provides token-based auth
- `system/` contains diagnostics (e.g., disk, database checks)
- `observability/` provides logging, tracing decorators

#### Interface

- `api/controllers/` expose `FastAPI` routes and depend on use cases
- `api/dtos/` define `Pydantic` models for request/response shaping
- `cli/` optionally runs scripts or command-line tools

#### Shared

- `formatters/` contains reusable utility classes for formatting (e.g., date/time conversion)
- `configuration.py` loads settings

---

### Enhancing System Quality

#### Performance and Scalability

- Implement caching strategies (`Redis`) for frequently accessed data.
- Use message queues (`Pub/Sub`) for asynchronous tasks.

#### Reliability and Fault Tolerance

- Explicitly define retry and circuit breaker strategies.
- Clearly document error handling and recovery procedures.

#### Maintainability and Modularity

- Clearly define module boundaries and use explicit interfaces (`ABC`).

#### Observability and Monitoring

- Structured logging with `correlation-id`.
- Metrics collection and distributed tracing.

#### Security

- Auditing of key domain events.
- Secure management of secrets (`Vault`).

#### Availability

- Explicit fall-back or degraded-service strategies.
- Robust health-check mechanisms.

#### Testability

- Include integration and end-to-end tests for core functionality.
- Contract testing for integrations.

#### Portability

- Containerization strategy (`Docker`).
- Infrastructure as code (`Terraform`, `Ansible`, `Packer`).

---

### Coding Conventions

#### General

- No comments: code should be self-documenting and expressive
- Descriptive naming: variables, functions, and classes should clearly communicate their intent
- Include `__init__.py` files in each Python package to clearly define module boundaries and support tools like `linters`, test runners, and code navigation.

#### Testing

- 100% test coverage is expected
- Tests should be meaningful and not just aim to increase coverage
- Mocks/stubs should be used where necessary to isolate behaviour
- Tests must include only one assertion per test case
- Test names should be phrased as a sentence clearly reflecting the behaviour being asserted.
  - **Example:** `test_should_return_404_when_resource_not_found()`
- Consumer Driven Contract Testing (`CDCT`) consumer tests are required for any internal services called, and producer tests for `API` routes provided by the project.
- Architectural Unit Testing should be used to assert that the code aligns with the principles defined in this document.

#### Static Analysis

Code must pass the following tools before merging:

| Tool                | Purpose                                            |
|---------------------|----------------------------------------------------|
| `flake8`            | `Linting` and style checking                       |
| `black`             | Code formatting                                    |
| `bandit`            | Security scanning for common issues                |
| `xenon`             | Maintainability and complexity limits              |
| `mypy`              | Static type checking                               |
| `safety`            | Dependency vulnerability scanning                  |
| `semgrep`           | Static analysis for code patterns and security     |
| `dependency-check`  | Dependency vulnerability scanning                  |

##### Xenon Configuration

```
xenon --max-absolute A --max-modules A --max-average A
```

This enforces an "A" grade for complexity across all modules.

---

By following these conventions, the code remains:

- Clean and easy to reason about
- Secure by default
- Readable by both humans and tools
- Easy to `refactor` and scale with confidence
