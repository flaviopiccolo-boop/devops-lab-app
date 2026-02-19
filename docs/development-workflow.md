# Development Workflow

## Branching

- Use short-lived feature branches
- Merge to `main` via pull requests only

## Pull Request Checklist

- Code compiles and tests pass
- Lint checks pass
- Docker build works locally
- Documentation updated when behavior changes

## Commit Convention

Use clear, action-oriented messages. Suggested prefixes:

- `feat:` new feature
- `fix:` bug fix
- `chore:` maintenance
- `docs:` documentation update
- `refactor:` internal improvements

## Release Inputs

Each merge to `main` should be releasable by CI pipeline.
