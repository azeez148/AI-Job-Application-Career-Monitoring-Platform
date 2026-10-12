# AI Job Application & Career Monitoring Platform
Phase 0 foundation implementation. This repository does not yet contain a running web application.

Start with [the phased delivery plan](docs/ROADMAP.md), [current progress](docs/PROGRESS.md), and [Phase 0 results](docs/phases/00-foundations.md).

## Docker (recommended)
Docker Engine with Compose v2 is required. From this checkout:
```sh
docker compose config --quiet
docker compose build foundations
docker compose run --rm foundations
```
For this cloud machine, use the documented [cloud build fallback](docs/DOCKER.md), which downloads dependencies on the host before building.

This runs the Phase 0 unit/integration suite in an isolated Python 3.12 container. It does not start a web application. See [Docker development](docs/DOCKER.md) for scope and the Phase 1 service plan.

## Native development
Python 3.12 is validated. From this checkout:
```sh
python -m venv /workspace/career-platform-venv
/workspace/career-platform-venv/bin/python -m pip install -r requirements-dev.txt
PYTHONPATH=src /workspace/career-platform-venv/bin/python -m unittest discover -s tests -v
```
Policy defaults live in `config/policy.json`. Contract schemas live in `schemas/`. No credentials, external services or database are required for Phase 0. See `data/evaluation/README.md` to prepare the real evaluation set.

## Delivery rules
Strict phase gates: implement, test, document outcomes and rationale, gather exit evidence, then advance. A passing software test does not replace real user evaluation. Unit and integration tests start in Phase 0; Playwright browser tests start when Phase 1 provides an Angular UI. Public-site browser automation remains deferred and conditional.
