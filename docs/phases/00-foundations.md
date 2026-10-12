# Phase 0: foundations and decisions
Status: implementation delivered; exit gate pending. Updated 12 October 2026.

## Completed
- 0.1: preserved the supplied roadmap and expanded it into bounded units, dependencies, test strategy, progress tracking and provisional policy defaults.
- 0.2: claim/evaluation JSON Schemas, verified-only claim filtering, ownership/duplicate rejection and a JSONL validation CLI.
- 0.3: documented real-data intake and built its validator; real dataset collection remains pending.
- 0.4: documented decisions, risk register and proposed privacy posture; acceptance remains pending.
- Added pinned development dependencies and GitHub Actions test workflow. The workflow file exists; hosted CI has not run.

## Logic and rationale
Claims carry tenant/user ownership, immutable-source identifiers, source hashes and locators, and explicit review metadata. Malformed records fail validation; only verified claims survive filtering. This checks structure, not the truth of a claim or integrity of stored bytes. Authentication, trusted review persistence and actual document storage belong to Phase 1.

Evaluation validation requires distinct records, all three tiers and 50–100 records; synthetic records are rejected as gate evidence. Software fixtures marked as real solely to exercise this branch are isolated in tests and do not constitute an actual dataset. The owner must establish real provenance and honest ratings.

Configuration separates safety, budgets, quality, discovery and privacy. Owner-authorized defaults are provisional; sending is disabled. The architecture defers services until their phase warrants them.

## Verification
Executed locally on 12 October 2026, Python 3.12.14:
```sh
PYTHONPATH=src /workspace/career-platform-venv/bin/python -m unittest discover -s tests -v
/workspace/career-platform-venv/bin/python -m pip check
```
Result: 14 tests passed (10 unit, 4 subprocess integration); dependency check passed. Initial testing exposed a missing optional timestamp-format dependency; installed format validators, pinned resolved dependencies, and reran successfully. Coverage includes ownership rejection, unverified exclusion, required review metadata, invalid timestamps/hashes, evaluation count boundaries, tier coverage, synthetic/duplicate rejection, CLI exit codes and validation-error redaction.

Playwright: not run; no UI exists. Phase 1 requires browser tests from its first user flow. No live model calls, real JD evaluation, provider integration or production claims were tested.

## Exit checklist: pending owner evidence/acceptance
- [ ] Supply 50–100 distinct real JDs rated strong/maybe/skip against the candidate profile; follow `data/evaluation/README.md` and validate locally.
- [ ] Accept the claims schema and provenance/reviewer requirements.
- [ ] Accept separate resume and send authorization gates, no guessing and confirmation-only Applied status.
- [ ] Accept or revise provisional consent/retention/deletion posture and select appropriate storage region before real personal-data hosting.
Defaults for budget and pilot size are recorded under the owner's instruction to choose defaults; these will be calibrated rather than treated as measured results.

## Pending and next step
Phase 0 is not gate-complete. No phase beyond 0 has started because the owner chose strict gates. Once evidence and checklist acceptance exist, record acceptance here and start unit 1.1. Do not publish a final project achievement report until the full phase sequence has been resolved.

## Docker follow-up (12 October 2026)
Owner requested Docker support. Added a digest-pinned Python test image, Compose runner, restricted build context, non-root/read-only execution and a Docker CI job. Phase 1 unit 1.1 now explicitly includes Angular/FastAPI/PostgreSQL containers, health checks, persistent development storage and an isolated test database.

Validation: Compose configuration passed; the image built using `compose.cloud.yaml`; all 14 tests executed and passed inside Docker (10 unit, 4 integration). Container build dependency checking also passed. The default online build could not resolve registry/proxy DNS in this cloud environment. The documented fallback downloads wheels on the host with normal HTTPS verification and installs them without build-network access. Initial non-root test discovery found zero tests because copied subdirectories retained restrictive ownership; explicit copy ownership fixed it. The zero-test run was a failure and is not counted as validation.

The default online build is retained for normally connected machines and hosted CI; its success in those environments has not been verified here. See `docs/DOCKER.md` for exact cloud commands. This follow-up does not accept the Phase 0 evidence gate or implement Phase 1 application services.
