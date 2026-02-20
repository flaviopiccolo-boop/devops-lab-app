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

## Phase 3 Quickstart

### Run locally

```powershell
pip install -r requirements-dev.txt
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

By default, local execution persists CRUD data in SQLite at `src/data/app.db`.

To use PostgreSQL instead, configure either `DATABASE_URL` or `DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD`.

Health check:

```powershell
curl http://127.0.0.1:8080/health
```

### Quality checks

```powershell
ruff check .
pytest -q
```

### Build and run container

```powershell
docker build -t pipeops/devops-lab-app:0.3.0 .
docker run --rm -p 8080:8080 pipeops/devops-lab-app:0.3.0
```

Container health check:

```powershell
curl http://127.0.0.1:8080/health
```