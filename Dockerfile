# Phase 0 foundation runner; application services are introduced in Phase 1.
ARG DEPENDENCY_STAGE=online
FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1 AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements-dev.txt ./

FROM base AS online
RUN python -m pip install --no-cache-dir -r requirements-dev.txt

# Cloud fallback: verified HTTPS downloads occur on the host; no build network.
FROM base AS offline
RUN --mount=type=bind,source=.docker-wheels,target=/wheels \
    python -m pip install --no-cache-dir --no-index --find-links=/wheels -r requirements-dev.txt

FROM ${DEPENDENCY_STAGE} AS foundations
RUN python -m pip check \
    && groupadd --gid 10001 career \
    && useradd --uid 10001 --gid career --no-create-home career
COPY --chown=career:career schemas/ ./schemas/
COPY --chown=career:career config/ ./config/
COPY --chown=career:career src/ ./src/
COPY --chown=career:career tests/ ./tests/
USER career
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
