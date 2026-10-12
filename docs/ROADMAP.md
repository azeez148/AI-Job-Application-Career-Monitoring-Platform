# Phased delivery plan

Version 0.3, 12 October 2026. Source: `source-roadmap-v0.2.txt`. Estimates assume 1–2 engineers; they are not commitments.

## Operating model

Strict gates confirmed by the owner. Finish each phase in order; do not start the next phase before its gate passes. A phase can be implementation-complete while its evidence gate remains pending. Every unit has a stable ID, one bounded responsibility, tests, documentation and an explicit status. Track `not_started`, `in_progress`, `implemented`, `validated`, `blocked`, or `skipped_with_reason`; never equate implemented with gate-passed.

Architecture: modular monolith with Angular, FastAPI and PostgreSQL from Phase 1. Modules: identity, profiles/claims, jobs/intake, assessment, tailoring/approval, applications/events, delivery, discovery, contacts, evaluation and administration. Providers are replaceable adapters with versioned contracts. Every candidate-owned row has tenant/user ownership; server identity determines scope. Postgres is the single source of workflow truth. No microservices, LinkedIn/Indeed scraping, guessed email addresses, CAPTCHA bypass or unapproved sending.

No Celery/Redis before Phase 4; no mandatory LangGraph or provider failover. Services communicate through application interfaces and transactional database updates. Resume approval and sending authorization remain separate; changes invalidate relevant approval. Browser UI testing begins in Phase 1 even though discovery browser automation is deferred.

## Configurable and manageable units

`config/policy.json` records initial defaults: strict gates, single tenant, owner evaluator, one pilot user, USD 0.25/application, USD 10/month/user, 30-day company cooldown, 90-day no-reapply window, 24-hour scan interval, 50 scans/day global cap, 90-day retention, 30-day deletion SLA, in-app notifications. These are planning defaults rather than measured or legal commitments. Sending stays disabled (daily cap zero) until Phase 3 defines and validates an enabled policy. Region remains undecided until real personal-data hosting is selected.

Phase 1 must add typed runtime validation and authenticated settings management: deployment-only infrastructure settings, admin policy caps, and user preferences bounded by caps. Log policy version on decisions and events; migrations preserve history. Do not expose credentials in config or logs. Invalid/unset mandatory safety settings fail closed. Later changes require tests for the affected unit and documented rationale, without silently reopening completed gates.

## Repeated delivery procedure

1. Confirm previous gate and pick the next work unit.
2. Define contracts, failure behavior and acceptance examples.
3. Implement with unit tests and integration tests against relevant real local services.
4. Add Playwright coverage when a user-facing browser flow exists; use provider fakes in CI.
5. Run required tests, record actual counts and failures, inspect repository changes.
6. Complete a phase report: completed work, logic, evidence, limitations, pending work, decisions and next gate.
7. Obtain required real-world evidence and record gate acceptance before advancing.

## Phases

### Phase 0: Foundations and decisions (1 week)

Are scope, rules and thresholds agreed?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 0.1 | Architecture and policy | Record modular monolith, tenant ownership, safety invariants and configurable defaults. |
| 0.2 | Contracts | Version verified claims and evaluation schemas; fail closed on invalid records and ownership mismatch. |
| 0.3 | Evaluation intake | Collect 50–100 real JDs, owner ratings, tier coverage and dataset provenance. |
| 0.4 | Safety and privacy review | Accept claims schema, checklist, retention/consent posture and provisional budget. |

**Required exit gate:** Real evaluation set validated; owner accepts claims schema and safety/privacy checklist.

**Testing:** Unit: schemas, ownership, verified-only filtering, duplicates and evaluation boundaries. Integration: JSONL CLI and exit codes. Playwright: not applicable until a UI exists.

### Phase 1: JD to approved tailored resume (3–4 weeks)

Is fit scoring and verified tailoring good?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 1.1 | Portal, auth and storage | Docker Compose for Angular, FastAPI and PostgreSQL, persistent development volume, health checks and a separate disposable test database; PostgreSQL migrations; authenticated identity determines tenant/user scope; negative isolation tests. |
| 1.2 | Profile and claims | Preferences, immutable source resume storage, hash/provenance, upload limits and reviewed claim lifecycle. |
| 1.3 | JD intake | Paste, file and URL adapters, extraction, snapshots, dedup; URL fetching rejects private addresses and unsafe redirects. |
| 1.4 | Assessment and tailoring | Three tiers and evidence per requirement; single provider adapter, validated outputs, no tools during parsing, prompt versions and token/cost ledger. |
| 1.5 | Exports and approval | Claim-to-source map, change summary, DOCX/PDF export, approval of a specific immutable resume version; editing invalidates approval. |

**Required exit gate:** At least 80% agreement against owner labels; zero unverified claims in approvable output; measured per-application cost within USD 0.25 provisional ceiling.

**Testing:** Unit: scoring boundaries, claims, costs, injection/output validation. Integration: real disposable Postgres, migrations, auth/isolation, upload/export and mocked provider failure paths. Playwright: sign in, profile, JD, review, export, approve; reject unverified evidence. Live model evaluation is separate from deterministic CI.

### Phase 2: Drafts, tracking and manual send (2–3 weeks)

Do users trust and use the output?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 2.1 | Email drafting | Application-specific options; salary/notice off by default; verified claims only. |
| 2.2 | Tracker and audit | Postgres dashboard, append-only event history, source snapshots and notes. |
| 2.3 | Manual workflow | Copied and user-reported sent/reply/interview/rejection states; distinguish user reports from provider-confirmed Applied. |
| 2.4 | Reapplication controls | Company cooldown and no-reapply policies with deterministic reasons. |

**Required exit gate:** One-user pilot completes real applications for two weeks; record trust, time saved, draft edits and issues.

**Testing:** Unit: transitions, options, cooldown boundaries. Integration: transactional events and duplicate actions. Playwright: draft, copy, track, annotate and policy errors.

### Phase 3: Gmail drafts and gated sending (3–4 weeks)

Do sent applications get replies?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 3.1 | Draft-only OAuth | Per-user minimum scopes, draft creation, token protection; start Google verification planning. |
| 3.2 | Authorized send | Separate single-application send authorization bound to resume/message/recipient version, cap enforcement, idempotency and transactional reservation. |
| 3.3 | Unknown outcome recovery | Persist UNKNOWN_SEND_STATUS on ambiguous timeout; reconcile before retry; only provider confirmation marks Applied. |
| 3.4 | Reply and channel evidence | Thread/message IDs, suggested status updates, measure email versus manually submitted ATS applications. |

**Required exit gate:** 30–50 real confirmed sends, reply-rate comparison with ATS and documented channel decision; API send safety tests pass.

**Testing:** Unit: invalidated authorization, limits and retry rules. Integration: Gmail stub responses, timeouts/reconciliation, concurrency and idempotency. Playwright: draft and separate send approval using test transport, never real sends in CI. Live send requires explicit per-application authorization.

### Phase 4: Public ATS watchlists (3–4 weeks)

Can discovery avoid excessive noise?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 4.1 | Watchlists and provenance | Company and bulk entry, official careers resolution. |
| 4.2 | Adapters and identities | Greenhouse/Lever public APIs with canonical job IDs, edits/reposts and snapshots. |
| 4.3 | Scheduling | Introduce Celery, Redis and Beat only now; per-company intervals, global cap, leases and retry policies. |
| 4.4 | Filtering and health | Rules/embeddings before LLM, budgets, in-app match notifications, scan health; browser fallback disabled unless separately justified. |

**Required exit gate:** Users act on at least 50% of surfaced strong matches; monthly measured cost remains within configurable USD 10/user target.

**Testing:** Unit: normalization/dedup/filter/budget. Integration: recorded ATS responses, scheduler and worker restart recovery. Playwright: watchlist, matches and scan errors. Public-site automation needs source policy review.

### Phase 5: Conditional contact research (2–3 weeks)

Does evidence justify email contact research?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 5.1 | Channel gate | Use Phase 3 comparison to build, defer or skip email discovery; document decision. |
| 5.2 | Verified contacts | Official-domain evidence, source URL, observed time, verification status; explicit no-contact result; never guess addresses. |
| 5.3 | ATS assistance | Source guidance, prepared answers and resume for user-controlled manual submission. |

**Required exit gate:** Conditional on Phase 3 evidence; verified provenance for every suggested contact, zero guessed addresses. A justified skip is an accepted outcome.

**Testing:** Unit: provenance and no-contact behavior. Integration: source fixtures and unavailable pages. Playwright: review contact provenance or ATS preparation.

### Phase 6: Orchestration and quality (3–4 weeks)

Does workflow complexity justify orchestration?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 6.1 | Complexity decision | Adopt LangGraph only when branching/loops/checkpoints justify it; Postgres remains state authority. |
| 6.2 | Verification quality | Deterministic dates/numbers/employers, soft-wording LLM checks and evidence reports. |
| 6.3 | Recovery and evaluation | Redacted traces, dead letters, resumable execution, frozen dataset regression runs. |
| 6.4 | Provider evolution | LiteLLM/capability registry when needed; cross-provider failover opt-in with privacy and budget checks. |

**Required exit gate:** No agreed metric regressions for model/prompt changes; recovery preserves state and approvals.

**Testing:** Unit: checks and routing. Integration: crash/resume/dead-letter/provider failures. Playwright: checkpoint review and recovery. Compare frozen dataset metrics with previous accepted baseline.

### Phase 7: Multi-tenant and production hardening (4–6 weeks)

Is it safe to open to other users?

| Unit | Responsibility | Deliverable |
|---|---|---|
| 7.1 | Administration | RBAC, users, provider settings, budgets/quotas, crawler policy and audit exports. |
| 7.2 | Privacy and security | Isolation review, encryption, secrets manager, redaction, deletion/retention workflows and legal review. |
| 7.3 | Operations | AWS object storage/managed Postgres/workers, monitoring, infrastructure configuration and cost alerts. |
| 7.4 | Launch evidence | Penetration/load tests, backup restore drills, legal/data residency and OAuth verification closure. |

**Required exit gate:** Security review, recovery drill, cost targets, legal/privacy and OAuth requirements all pass before public launch.

**Testing:** Unit: RBAC/retention/quotas. Integration: tenant isolation, deletion, backups and restore. Playwright: multi-user role matrix and lifecycle. External security/legal reviews remain explicit external evidence.

## Phase commits

Commit the implementation, tests and updated phase report at each phase completion. Record actual test outcomes and unresolved gate evidence in the commit/report; never describe a pending gate as passed. The owner authorized phase commits on 12 October 2026. The initial Phase 0 implementation commit is a checkpoint while its real-data and acceptance gate remains pending.

## Metrics and measurement

Track preparation time (target <10 minutes), fit agreement (>=80%), unverified claims reaching approval (zero), user edit ratio (<20% of resume lines), reply rates with explicit denominators and observation windows, and actual provider cost. Record model/prompt versions, token counts, pricing version and policy version. The USD targets must be calibrated from measured data. Compare channels with similar jobs and report sample limitations; do not infer causality from small pilots.

## Future progress and final delivery

After Phase 7, publish `docs/FINAL-REPORT.md` with a phase-by-phase achievement/evidence matrix, pending items and reasons, expected versus observed metrics, remaining operational limitations, deployment/recovery instructions and prioritized future plans. Do not label an interim report final. Candidate future work: Workday/generic adapters only with policy review, broader provider support after evaluation, larger pilots, and ATS assistance based on channel evidence. All remain backlog until their prerequisites and budgets are met.
