BRAINSTORM review complete. The concept already requires traceable execution without secrets, truthful check coverage, durable workers and explicit budgets. The following are operational requirements to carry into the brief/design, not contradictions of those intentions or evidence of a production incident. No Blocker identified at this concept stage.

Paths below are relative to `/home/abdulrahman/Desktop/Evidence Twin/` unless stated otherwise.

1. **Major — Observability & Operational SRE Debuggability: define correlation across API acceptance, worker attempts and scientific operations.**

   **Target:** review_input.md, “System responsibilities” lines 29–34, “Access and privacy requirements” lines 40–44, “Migration implications” line 55.

   **Evidence:** `services/store.py:71–75` creates events with independent IDs, timestamps, component, type and status. `services/workflow.py:51–58` records an attempt token on the queue event, but stage/completion/failure events at lines 83–88 and 127–138 do not explicitly carry that token or an operation/span relationship. `contracts/inspection.py:95–105` permits timing and input/output references but has no explicit attempt/trace relationship. `__init__.py:35–57` supplies request boundaries and response headers without request-correlation handling.

   **Operational risk:** A hosted run spans HTTP requests, durable workers, source retrieval, deterministic checks and model calls. Analysis identity alone cannot reliably distinguish retries, redeliveries, a stale worker and the operation producing a particular outcome.

   **Mitigation requirement:** Specify stable analysis, attempt and operation identities, propagation across queue delivery and Core calls, parent-child relationships and a support-visible correlation reference. Record execution/configuration versions and input/output artifact references without research contents. Decide the tracing mechanism during design; no particular vendor is required.

2. **Major — Observability & Operational SRE Debuggability: sanitized failures need machine-readable causes.**

   **Target:** review_input.md, “Primary V1 experience” line 23, “System responsibilities” line 34, “Minimum end-to-end acceptance” lines 131–133.

   **Evidence:** `services/workflow.py:132–140` groups provider and structured-response failures under one generic failed review message and event. Lines 186–191 also collapse broad execution failures into “No usable review was produced” and provider-configuration retry advice. `services/runtime.py:355–370` converts several validation failures into HTTP 422. The guide correctly prohibits raw remote error bodies (`BACKEND_IMPLEMENTATION_GUIDE.md:89–92`).

   **Operational risk:** Operators cannot distinguish exhausted provider quota, timeout, malformed output, invalid references, parser failure, storage failure or a programming error from the saved failure event. Retrying all such cases can waste money and conceal persistent defects.

   **Mitigation requirement:** Define bounded internal error categories, failing operation, retryability, safe provider status category, elapsed time and correlation reference. Keep safe user messages separate from restricted operator diagnostics. Do not log arbitrary exception bodies or provider payloads. Include triage paths for each category and terminal/degraded outcomes.

3. **Major — Observability & Operational SRE Debuggability: define worker health and stalled-work detection separately from API availability.**

   **Target:** review_input.md, “System responsibilities” lines 32–34, “Migration implications” line 55, “Remaining scope decisions” line 231.

   **Evidence:** `services/runtime.py:334–340` derives job availability from provider configuration rather than queue capacity or worker progress. `services/workflow.py:25–42` uses a process lock and marks queued/running work failed on restart; lines 44–69 maintain local queue slots and futures. `BACKEND_IMPLEMENTATION_GUIDE.md:126–135` explicitly documents these local limitations; line 205 describes health as liveness.

   **Operational risk:** A responsive API and configured provider can coexist with a stalled worker, aging queue, storage outage or abandoned lease. Researchers may keep submitting while no work progresses.

   **Mitigation requirement:** Define separate web liveness, dependency readiness and worker-progress signals. Require queue depth, oldest queued age, queue wait, operation duration, active/stalled attempts, lease loss/redelivery and recovery outcomes. Specify ownership of alerts and recovery procedures. Choose thresholds from pilot expectations and measured behavior; do not invent an approved SLA or timeout.

4. **Major — Observability & Operational SRE Debuggability: measure check execution distinctly from scientific outcomes.**

   **Target:** review_input.md, “Minimum end-to-end acceptance” lines 131–133, “Source-level statuses” lines 150–155, “Required fields for every claim” lines 186–192.

   **Evidence:** The concept already mandates applicability/completion per check and distinguishes missing evidence from contradiction. Existing `Stage` status (`contracts/analyses.py:49–54`) and `AuditEvent` (`contracts/inspection.py:95–105`) are generic execution records; `checks` is currently a list of findings (`inspection.py:125`, `analyses.py:38–45`). Runtime currently returns no scientific checks (`services/runtime.py:219–222`).

   **Operational risk:** A source-fetch outage, unavailable notice registry or deterministic-tool failure could become indistinguishable from legitimate insufficient inputs when aggregated into final reports. Conversely, a technically successful HTTP/tool call can be mistaken for a passed scientific check.

   **Mitigation requirement:** Define a versioned check-result record containing check/procedure ID, policy version, applicability, required inputs, execution state, scientific result, reason code and evidence/artifact references. Measure retrieval failures, validation failures, incomplete mandatory checks and degraded coverage separately from claim assessments. Operational dashboards must never label completion rates, source authentication or model agreement as scientific accuracy.

5. **Major — Observability & Operational SRE Debuggability: budget and cancellation accounting must include already-sent calls and duplicate execution.**

   **Target:** review_input.md, “Access and privacy requirements” line 47, anchored review questions line 61, “Remaining scope decisions” line 232.

   **Evidence:** `services/workflow.py:95–98` acknowledges cancellation while already-sent provider calls can continue. Lines 119–128 save supplied token usage inside completed reviewer reports; stale or failed calls do not follow that successful save path. Lines 184–185 discard stale jobs. Queue events record provider/model/prompt hashes (`workflow.py:54–56`). The guide explicitly avoids fabricated cost and silent billable replay (`BACKEND_IMPLEMENTATION_GUIDE.md:81–92,131–135`).

   **Operational risk:** Summing retained successful reports will undercount external work after cancellation, failed validation or worker loss. Durable redelivery adds potential duplicate billing. Quota enforcement based on that sum can exceed operator budgets.

   **Mitigation requirement:** Specify privacy-safe call accounting independent of scientific-result acceptance: call/attempt identity, reservation, dispatch, response/failure/cancellation, late-result discard and supplied usage. Distinguish measured usage, estimated monetary cost and unavailable billing data. Define budget reconciliation and duplicate-execution detection; explicit retry behavior must preserve prior attempt accounting.

6. **Major — Observability & Operational SRE Debuggability: establish separate access and retention rules for researcher audit records and operator telemetry.**

   **Target:** review_input.md, “Access and privacy requirements” lines 40–47, reproducibility requirement line 71, “Remaining scope decisions” line 233.

   **Evidence:** `services/runtime.py:251–252` returns saved analysis events to the audit inspector; `services/store.py:71–75` accepts arbitrary event metadata without a field allowlist. `services/runtime.py:49–55` changes global provider settings without an explicit settings-change audit event in that method. `frontend/src/features/settings/AIProviderSettings.tsx:27–29,39–41` exposes save/catalog outcomes while correctly explaining their limited meaning. The API contract already says backend logs must exclude private data (`docs/FRONTEND_API_CONTRACT.md:113`).

   **Operational risk:** Reusing one event stream for scientific reproducibility and operator debugging can disclose account, infrastructure or provider details to researchers. Missing privileged-change history makes it harder to connect a sudden failure spike with a model/configuration change. Export/deletion policies can also conflict with operational retention.

   **Mitigation requirement:** Define telemetry field allowlists, redaction at emission, audience/authorization boundaries and retention by event class. Audit privileged configuration changes with actor, timestamp and non-secret version/reference, never key values. Record safe authorization denials and deletion/migration outcomes. Provide a support procedure that uses correlation references without requiring researchers to disclose private evidence.

**Suggested design acceptance exercises:** demonstrate trace continuity across retry/redelivery; distinguish provider timeout from schema rejection; detect a stalled worker while HTTP health succeeds; retain accounting for a canceled in-flight call; and verify that a researcher cannot retrieve another account’s audit/operator records. These are proposed operational examinations, not executed tests or approved success metrics. They fit the Heilmeier standard’s risks, resources and examinations questions (standard lines 25–30).

**Read completeness**

Fully read, including rereads where combined output was truncated:

- Persona: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/agents/codebase_details.md` — followed its BRAINSTORM branch.
- Standard: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/resources/document_standards/heilmeier-standard.md` — all 30 lines.
- `docs/designs/backend-completion/2026-11-05-goldfish/review_input.md` — all 255 lines.
- `BACKEND_IMPLEMENTATION_GUIDE.md` — all 318 lines.
- `docs/FRONTEND_API_CONTRACT.md` — all 252 lines.
- `backend/evidencetwin_backend/__init__.py` — all 69 lines.
- `backend/evidencetwin_backend/services/runtime.py` — all 380 lines.
- `backend/evidencetwin_backend/services/workflow.py` — all 213 lines.
- `backend/evidencetwin_backend/services/store.py` — all 75 lines.
- `backend/evidencetwin_backend/contracts/analyses.py` — all 90 lines.
- `backend/evidencetwin_backend/contracts/inspection.py` — all 133 lines.
- `backend/evidencetwin_backend/contracts/common.py` — all 69 lines.
- `frontend/src/features/settings/AIProviderSettings.tsx` — all 48 lines.

No required files were inaccessible. No writes, tests, provider calls, private configuration, databases/uploads or memory/session history were accessed. This is static source-based observability review; it does not establish live runtime behavior or scientific validity.
