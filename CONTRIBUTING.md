# Contributing Guide

Thank you for contributing to the DevOps Hybrid Lab.

## Branching Model

- Use short-lived feature branches from `main`
- Open pull requests for all changes
- Keep branches focused on one concern

## Commit Messages

Use clear, action-oriented commits.

Suggested prefixes:

- `feat:` new functionality
- `fix:` bug fix
- `docs:` documentation updates
- `chore:` maintenance tasks
- `refactor:` internal code improvements

## Pull Request Expectations

- Link to relevant issue/task when applicable
- Keep scope small and reviewable
- Include tests or validation evidence
- Update docs when behavior changes

## Quality Checks

Before opening a PR:

1. Run local tests
2. Run lint/format checks
3. Validate container build (if applicable)

## Security and Secrets

- Do not commit credentials or tokens
- Use environment variables and secret stores
- Report security concerns privately
