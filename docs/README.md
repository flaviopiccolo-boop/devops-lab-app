# devops-lab-app Documentation

This repository contains application source code and quality controls for the DevOps Hybrid Lab.

## Documentation Index

- [Architecture](architecture.md)
- [Development Workflow](development-workflow.md)
- [Runbook](runbook.md)

## Main Responsibilities

- Implement application features
- Provide tests and linting
- Build container image inputs for CI
- Expose health and readiness endpoints

## Integration Points

- CI pipelines consume this repository to build and publish images
- Deploy repository consumes produced image tags
- Hub repository is the authoritative project guidance source
