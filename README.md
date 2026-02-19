# devops-lab-app

Application source repository for the DevOps Hybrid Lab.

## Purpose

This repository contains the application code, quality checks, and container build inputs used by CI pipelines.

## Documentation

- [Documentation Home](docs/README.md)
- [Architecture](docs/architecture.md)
- [Development Workflow](docs/development-workflow.md)
- [Runbook](docs/runbook.md)

## Upstream/Downstream Integration

- CI builds and publishes container images from this repository
- Deployment manifests in `devops-lab-deploy` consume released image tags
- Project-level guidance is maintained in `devops-lab-hub`