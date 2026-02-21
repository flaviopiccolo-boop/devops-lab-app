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

## CI/CD Automation (Phase 6 MVP)

This repository now includes GitHub Actions workflows for:

- Pull request checks (`.github/workflows/ci-pr-checks.yml`)
	- `ruff check .`
	- `pytest -q`
	- Docker build smoke test
- Main branch publish (`.github/workflows/ci-publish-image.yml`)
	- Build and push image to GHCR with tags:
		- `sha-<commit_sha>`
		- `latest`
	- Open automated PR in `devops-lab-deploy` updating app image tag

### Required GitHub Secrets

- `DEPLOY_REPO_TOKEN`
	- Personal access token (or GitHub App token) with permission to push branch and create PR in `pipeops-platform/devops-lab-deploy`
	- If missing, image publish still works and deploy PR step is skipped
- `ENABLE_DEPLOY_PROMOTION`
	- Must be set to `true` to enable automated PR creation in `devops-lab-deploy`
	- If `false`, image publish runs but no deploy PR is opened
- `RUNTIME_IMAGE_REPO` (recommended)
	- Full image repository used by runtime, e.g. `docker.io/<your-user>/devops-lab-app`
	- The deploy PR updates `apps/devops-lab-app/overlays/dev/kustomization.yaml` with this repo + new tag
	- If omitted, workflow defaults to `ghcr.io/<owner>/<repo>`
- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (required when `RUNTIME_IMAGE_REPO` is not GHCR)
	- Used by publish workflow to login and push image to Docker Hub
	- For GHCR, workflow uses `GITHUB_TOKEN`

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