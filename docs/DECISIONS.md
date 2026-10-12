# Decisions and rationale
- Confirmed by owner: strict phase gates; configurable defaults may be selected now and revisited during delivery.
- Defaults: single-tenant launch; project owner rates the dataset; one pilot user; USD 0.25/prepared application and USD 10/month/user budget targets. These are provisional, not observed costs.
- PostgreSQL becomes authoritative in Phase 1. No database/service is required for the current foundation validators.
- JSON Schema contracts make source provenance and review metadata inspectable independently of UI/provider choices. Reviewed claims need a reviewer and valid timestamp. Hash records identify original sources; Phase 1 must resolve and verify actual stored bytes.
- Approval filtering rejects malformed/cross-owner/duplicate records and excludes pending/rejected claims. It is a foundation utility, not a secure approval service: production must read trusted verification state and authenticated identity from storage.
- No fictional evaluation evidence. Test fixtures exercise contracts only. Human labels, permissions and claim truth cannot be proven by schema validation.
- Playwright starts with Phase 1 UI. This is permitted test automation, distinct from deferred public-site scraping.
- Initial privacy posture: explicit consent, minimum necessary data, immutable source versions, access-scoped storage, no personal data in logs/Git, 90-day provisional retention and 30-day deletion SLA. Immutable means no in-place edits, not exemption from deletion. Hard deletion must cover source files, derived artifacts and provider retention where supported; backup expiry must be documented. No GDPR/UAE PDPL compliance claim; legal review and region selection remain pending.
