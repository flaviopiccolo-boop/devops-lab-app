# Application Runbook

## Local Validation

1. Run tests
2. Run lint
3. Build Docker image
4. Start container and validate health endpoint

## Troubleshooting

- If container fails to start, inspect environment variables and startup logs.
- If tests fail in CI but pass locally, align tool versions and lock dependencies.

## Definition of Done

A change is complete when quality checks pass and the application is ready for image publication in CI.
