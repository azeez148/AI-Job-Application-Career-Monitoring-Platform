# Docker development

## Current Phase 0 runner
Requirements: Docker Engine and Compose v2. Run from the repository root:
```sh
docker compose config --quiet
docker compose build foundations
docker compose run --rm foundations
```
The final command propagates the test runner's exit code and removes the one-off container. Rebuild after changing source, schemas, configuration or tests: code is copied into the image, not bind-mounted. Dependency installation is cached separately. The official Python 3.12 image is pinned by digest; update the digest deliberately and rerun tests for security updates.

The runner uses a non-root user, read-only root filesystem, temporary writable `/tmp`, no runtime network and no host ports. The build requires access to Docker Hub and Python package registries. An allowlist-based `.dockerignore` excludes Git metadata, local credentials and evaluation datasets. No personal dataset or secrets belong in an image layer.

In the current cloud environment, the default Docker client config directory is read-only. Before these commands, use:
```sh
mkdir -p /workspace/docker-client
export DOCKER_CONFIG=/workspace/docker-client
```
Build containers in this cloud machine cannot resolve the registry/proxy DNS, even though host downloads work. Use the optional offline dependency stage:
```sh
/workspace/career-platform-venv/bin/python -m pip download --only-binary=:all: --dest .docker-wheels -r requirements-dev.txt
docker compose -f compose.yaml -f compose.cloud.yaml config --quiet
docker compose -f compose.yaml -f compose.cloud.yaml build foundations
docker compose run --rm foundations
```
The host downloads wheels with normal HTTPS verification; BuildKit mounts that ignored cache only during installation. No verification is disabled. Run the download with Python 3.12 on the same Linux architecture as the image (the current cloud machine is Linux AMD64). If targeting another architecture, obtain wheels for that target rather than reusing this cache. The base image still requires Docker Hub access or a local image cache. Normal connected machines can use the default online build.

This is a client configuration workaround, not a new Docker daemon. Regular machines with a writable Docker config directory do not require it. The daemon and image cache must not be assumed to survive environment restoration; rerun the build when needed.

## Phase 1 application services (planned, not implemented)
Unit 1.1 adds Angular, FastAPI and PostgreSQL Compose services alongside the first working application slice. Include development reload, application/database health checks, readiness dependencies, explicit migration commands and a persistent development database volume. Add a separate test database with disposable storage and independent credentials; tests must never target development data. Application secrets are injected at runtime, never baked into images. Configure browser tests to wait for readiness and use Playwright against the UI/API stack.

Phase 0's strict evidence gate still applies; this Docker runner does not advance or accept it. Redis, Celery and Beat remain scheduled for Phase 4. Compose is a development/test workflow; production deployment is designed in Phase 7.
