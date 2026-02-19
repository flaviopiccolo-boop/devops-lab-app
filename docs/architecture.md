# Application Architecture

## Objective

Maintain a minimal, production-style application that is easy to test, containerize, and deploy to Kubernetes.

## Planned Structure

- `src/` application code
- `tests/` unit and integration tests
- `Dockerfile` container build definition
- `.dockerignore` build context optimization

## Non-Functional Requirements

- Fast startup time
- Health and readiness endpoints
- Deterministic builds
- Versioned image tags (semantic version + commit SHA)

## Quality Baseline

- Lint checks
- Unit tests
- Optional contract/integration tests
