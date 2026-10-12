# Risk register
| Risk | Mitigation / evidence | Owner | Phase |
|---|---|---|---|
| Invented claims | Source maps, verified-only output, deterministic checks and approval tests | Engineering + candidate | 1, 6 |
| JD prompt injection | Untrusted labeling, no parsing tools, validated outputs; adversarial fixtures | Engineering | 1 |
| Weak scoring | 50–100 real owner labels and held-out evaluation | Project owner | 0, 1 |
| Email underperforms | Compare observed reply rates; condition contact discovery | Project owner | 3, 5 |
| Duplicate/unauthorized sends | Version-bound authorization, transactional idempotency, unknown-state reconciliation | Engineering | 3 |
| Reputation and provider rules | Caps, cooldowns, draft-first and OAuth review | Project owner | 2, 3 |
| Discovery noise/cost | Public APIs, prefilters, budgets and measured engagement | Engineering | 4 |
| Privacy/data exposure | Consent, access control, redaction, deletion, residency and legal review | Project owner + reviewer | 0, 7 |
| Workflow state drift | Postgres authority and recovery tests | Engineering | 4, 6 |
| Arbitrary URL/file intake | SSRF protections, content/size validation, safe parsing | Engineering | 1 |
| Production isolation defects | Server-scoped ownership and adversarial multi-tenant tests | Engineering + security reviewer | 1, 7 |
