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
- Environment promotions from app repo (`.github/workflows/ci-promote-environment.yml`)
	- Manual `workflow_dispatch` to promote:
		- `dev -> staging`
		- `staging -> prod-blue`
		- `staging -> prod-green`
	- App workflow dispatches `Promote Environment` in `devops-lab-deploy` and waits for completion
	- Deploy workflow opens PR in `devops-lab-deploy` behind the scenes
	- `staging` promotions require approval in app `staging` environment
	- `prod-*` promotions require approval in app `production` environment
- Environment rollback from app repo (`.github/workflows/ci-rollback-environment.yml`)
	- Manual `workflow_dispatch` to rollback to previous stable for:
		- `staging`
		- `prod-blue`
		- `prod-green`
	- App workflow dispatches `Rollback Environment` in `devops-lab-deploy` and waits for completion
	- Deploy workflow opens rollback PR in `devops-lab-deploy` based on the previous stable overlay revision
	- `staging` rollback requires approval in app `staging` environment
	- `prod-*` rollback requires approval in app `production` environment
- Issue-driven deploy operations (`.github/workflows/ci-issue-deploy-operations.yml`)
	- Open issue template **Promote Deploy** or **Rollback Deploy**
	- Workflow routes request and opens an **app PR** for approval (`deploy-operation-request`)
	- After PR approval, `CI - Deploy On App PR Approval` dispatches the corresponding deploy workflow
	- Issue and PR receive run links/status comments for traceability

### Required GitHub Secrets

- `DEPLOY_REPO_TOKEN`
	- Personal access token (or GitHub App token) with permission in `pipeops-platform/devops-lab-deploy` for:
		- dispatching workflows (`actions:write`)
		- reading workflow runs (`actions:read`)
		- pushing branches / creating PRs (used by deploy-side workflow)
	- If missing, image publish still works and deploy promotion steps are skipped
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
- `ENABLE_DEPLOY_AUTO_MERGE` (optional)
	- Set to `true` to request auto-merge on deploy PRs created by workflows
	- Repository protection rules can still require manual approval/merge
- `APP_PR_TOKEN` (recommended when org blocks PR creation by `GITHUB_TOKEN`)
	- Personal access token (or GitHub App token) with permission to create pull requests in `devops-lab-app`
	- Used by issue-driven workflow to open app PRs when repository setting "Allow GitHub Actions to create and approve pull requests" is disabled by policy

### Required GitHub Environments (app repo)

Configure protected environments in the app repository so promotion approvals happen before deploy PR creation:

- `staging`
	- Required reviewers: staging approvers/tech lead
- `prod`
	- Required reviewers: production approvers/release managers

This allows end users to operate only in app repository Actions while keeping deploy repository access transparent.

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