Mode: **BRAINSTORM — Skeptical Architect**. Findings below are requirements to resolve in the Concepts Brief/PRD, not a full implementation-design audit. No blocker to continuing brainstorming was identified; the proposed hosted service requires the safeguards below before pilot deployment.

Paths below are relative to `/home/abdulrahman/Desktop/Evidence Twin/`. `review_input.md` refers to `docs/designs/backend-completion/2026-11-05-goldfish/review_input.md`.

1. **Major — Cost, Quota & Token Economics: Council cost multiplies beyond the initial reviews.**

   **Target:** “System responsibilities,” “Remaining scope decisions,” `review_input.md:27–36, 230–233`.

   **Evidence:** `services/workflow.py:142–161` performs four initial Council calls, cross-review and judging. Cross-review receives all initial reports; judging additionally receives cross-review. Images accompany these calls. `services/runtime.py:167–170` bounds the initial dataset context, but that does not establish a complete token budget for subsequent expanded packets. `BACKEND_IMPLEMENTATION_GUIDE.md:90–92, 253–256` records timeout, response and local queue bounds, not a pilot spending ceiling.

   **Consequence:** One accepted Council analysis can incur six generation calls, repeatedly transmit images and evidence, and accumulate reviewer outputs in later prompts. Job-count limits alone cannot bound token expenditure or provider quotas. Failed or cancelled calls may still cost money.

   **Mitigation requirement:** Define input/output token and image limits per role, maximum accumulated reviewer context, per-attempt and per-account budgets, global provider concurrency/rate limits, and a global spending stop. Reserve budget at admission, reconcile actual usage where available, and specify treatment of unknown usage. Estimate focused/Council workloads separately using stated pilot-volume assumptions; do not invent a user-approved budget.

2. **Major — Cost, Quota & Token Economics: Durable execution needs explicit handling of ambiguous paid-call outcomes.**

   **Target:** “Migration implications” and infrastructure decisions, `review_input.md:53–55, 231`.

   **Evidence:** `services/workflow.py:23–42` uses a process lock and local executor; restart recovery marks queued/running analyses failed. `services/workflow.py:100–128` sends a provider request before persisting its validated result. `services/runtime.py:196–205` restarts an attempt rather than resuming individual stages. `BACKEND_IMPLEMENTATION_GUIDE.md:126–135` explicitly describes local execution and the no-silent-replay policy.

   **Consequence:** Replacing the executor with a durable queue does not alone prevent duplicate model charges. A worker can disappear after the provider accepted work but before completion was persisted. Automatic redelivery could then repeat a billable operation. Conversely, continuing the current restart behavior would not provide resumable hosted execution.

   **Mitigation requirement:** Specify durable stage records, atomic job admission/enqueue behavior, worker leases and fencing, checkpoint boundaries, cancellation propagation and stale-result rejection. Distinguish safe deterministic recomputation from an uncertain provider-call outcome. Define reconciliation or explicit retry semantics for that outcome; preserve the existing protection against silent duplicate billing.

3. **Major — Cost, Quota & Token Economics: Ownership must be part of storage/query execution, including administrative provider controls.**

   **Target:** “Access and privacy requirements,” `review_input.md:38–47`.

   **Evidence:** `__init__.py:22–24, 48–51` offers an optional request hook without a principal-bearing repository interface. `services/runtime.py:72–73, 182–186, 259–267, 292–296` retrieves records and global collections without owner criteria. `services/store.py:34, 55–64` stores `(kind, id, body)` and enumerates complete kind collections. `services/runtime.py:46–55, 364–372` exposes shared provider configuration through the general endpoint mechanism. `AIProviderSettings.tsx:27, 39–47` supplies the global configuration UI.

   **Consequence:** Adding sign-in around the existing routes would leave account isolation dependent on ad hoc checks. Lists, activity, comparisons, reports, files and workers could accidentally access cross-account data. An ordinary authenticated user must also not gain global provider-selection or credential-management authority.

   **Mitigation requirement:** Define a principal and explicit owner/case scope in repository operations, jobs and artifact access. Require server-enforced operator authorization on provider settings and diagnostics. Document ownership migration for legacy records; unresolved ownership must not silently assign records to newly registered users. Keep team/supervisor access unresolved until its permission model is selected.

4. **Major — Cost, Quota & Token Economics: Current pagination still reads and deserializes the entire workspace.**

   **Target:** Persistent database, controlled-pilot capacity and workload limits, `review_input.md:32–34, 211, 232`.

   **Evidence:** `services/store.py:50–64` stores and retrieves whole JSON records. `services/runtime.py:75–86, 182–183, 259–267, 292–296` filters, sorts or aggregates after loading complete collections. `services/workflow.py:71–81, 125–128` persists whole record snapshots for stage updates. `services/runtime.py:200` retains previous attempt outputs within the same record.

   **Consequence:** Retained datasets, outputs, audit events and attempts increase the cost of unrelated list/activity requests and status updates. Five-second polling is an established client behavior (`docs/FRONTEND_API_CONTRACT.md:75`), so several active users can amplify read/deserialization load even when the returned page is small.

   **Mitigation requirement:** Separate indexed account/case/job summaries from large evidence and output artifacts; perform filtering/pagination within authorized database queries. Bound audit/attempt retrieval and define retention. Establish pilot assumptions for concurrent users, active jobs, polling QPS, artifact size and retained attempts, then validate the selected architecture against those assumptions. A vendor choice is premature without this envelope.

5. **Major — Cost, Quota & Token Economics: Original-source retrieval creates a new network and ingestion boundary.**

   **Target:** Source verification policy and supported source lookups, `review_input.md:139–168, 224`.

   **Evidence:** `services/runtime.py:101–104` currently checks only that supplied URLs are credential-free HTTP(S) metadata; `services/runtime.py:215–216` explicitly says no retrieval occurred. `BACKEND_IMPLEMENTATION_GUIDE.md:148, 173–174, 190–191` confirms that remote downloads are absent.

   **Consequence:** Reusing current URL validation for server-side retrieval could expose internal services or cloud metadata endpoints and permit costly redirects, oversized downloads or slow responses. Valid publisher/source policies do not themselves bound network consumption or make fetched content safe.

   **Mitigation requirement:** Specify an isolated retrieval component with destination/IP validation, redirect revalidation, restricted egress, credential isolation, time/byte/content-type/decompression limits, source-level request quotas and bounded retries. Record retrieval failures as unavailable/inaccessible checks without converting them into scientific contradictions. Restrict initial source support to an implementable policy matrix.

6. **Major — Cost, Quota & Token Economics: XLSX and scientific tools require limits beyond compressed upload size.**

   **Target:** Input formats and procedure specifications, `review_input.md:97–118, 225–227`.

   **Evidence:** `services/runtime.py:114–147` supports bounded images, CSV, structured JSON and retained PDFs, but not XLSX. `contracts/inspection.py:33–48` defines a flat table; it has no workbook/sheet/formula lineage. Existing transport limits are documented in `BACKEND_IMPLEMENTATION_GUIDE.md:176–187`.

   **Consequence:** Workbook expansion, many sheets, formulas and external relationships introduce CPU/memory and provenance costs that the current flat-table limit does not resolve. Statistical procedures and rendering can similarly monopolize general job workers if execution resources are unbounded.

   **Mitigation requirement:** Define expanded-byte, sheet, row, column, cell and processing-time limits; an explicit formula/cached-value policy; external-link and macro handling; and cell/sheet provenance for derived tables. Give deterministic checks/rendering explicit CPU, memory and runtime ceilings. Preserve a failed/incomplete check record when a resource limit prevents execution rather than reporting scientific completion.

7. **Major — Cost, Quota & Token Economics: Reproducibility and deletion need an artifact lifecycle, not only record retention.**

   **Target:** Privacy, reproducibility and retention, `review_input.md:43–44, 71, 157–168, 210, 233`.

   **Evidence:** `services/runtime.py:188–193` deletes the record and upload directory; report deletion clears the current report (`272–278`). Retry archives prior reports and outputs inside `attemptHistory` (`200`). `services/workflow.py:54–56` retains prompt hashes, while its report is primarily narrative sections (`195–209`). The current provider UI states keys are stored without application-level encryption (`AIProviderSettings.tsx:39`).

   **Consequence:** Hosted snapshots, derived tables, calculation artifacts, reports, previous attempts, backups and provider-held inputs can have different lifetimes. Deleting the visible report may leave historical copies. Retaining hashes without recoverable code/prompt/artifact versions does not by itself enable reproduction.

   **Mitigation requirement:** Define immutable artifact/version identifiers and a reproducibility manifest covering exact inputs, transformations, calculation code/environment, procedure parameters, model/prompt versions and results. Specify retention/deletion/export for each artifact class and backup, including historical attempts and source snapshots. Define which private evidence can be sent to selected providers and disclose applicable retention boundaries. Choose credential storage and rotation for hosted operation explicitly.

8. **Major — Cost, Quota & Token Economics: The compatibility boundary must carry check-level results without collapsing scientific meanings.**

   **Target:** Claim/report requirements and compatibility decisions, `review_input.md:73–83, 129–133, 174–192, 205, 234`.

   **Evidence:** `contracts/common.py:23–25` contains `unsupported` but no explicit `contradicted`, and `unavailable` rather than `inaccessible`. `contracts/analyses.py:59–78` provides a single optional analysis assessment with string claims. `contracts/inspection.py:119–133` allows optional section fields, with checks represented as findings rather than typed applicability/execution results. `docs/FRONTEND_API_CONTRACT.md:24` explicitly leaves required section shapes unresolved.

   **Consequence:** A new Core could perform valid checks but lose the required distinctions when adapting them into the existing aggregate DTO. Optional generic JSON can carry additional facts, but it does not establish a validated, stable contract for per-claim coverage, required checks or mixed outcomes.

   **Mitigation requirement:** Define canonical Core records for claims, assertions, evidence links, check applicability, execution outcome and claim assessment before selecting compatibility mappings. Version or explicitly extend the wire contract and frontend parsing where necessary. Document how legacy exploratory records render. Keep provenance status, completed computation and evidence support as independent dimensions; never derive support from authenticated sources or model consensus.

**Read completeness**

Every required file was fully read, including follow-up reads where combined output was truncated:

- `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/agents/design_critic.md` — 63 lines.
- `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/resources/document_standards/heilmeier-standard.md` — 30 lines.
- `docs/designs/backend-completion/2026-11-05-goldfish/review_input.md` — 255 lines.
- `BACKEND_IMPLEMENTATION_GUIDE.md` — 318 lines.
- `docs/FRONTEND_API_CONTRACT.md` — 252 lines.
- `backend/evidencetwin_backend/__init__.py` — 69 lines.
- `backend/evidencetwin_backend/services/runtime.py` — 380 lines.
- `backend/evidencetwin_backend/services/workflow.py` — 213 lines.
- `backend/evidencetwin_backend/services/store.py` — 75 lines.
- `backend/evidencetwin_backend/contracts/analyses.py` — 90 lines.
- `backend/evidencetwin_backend/contracts/inspection.py` — 133 lines.
- `backend/evidencetwin_backend/contracts/common.py` — 69 lines.
- `frontend/src/features/settings/AIProviderSettings.tsx` — 48 lines.

**Inaccessible required files:** None.

No writes, tests, provider calls, private configuration, databases, uploads, memory or session history were accessed. Review isolation is limited to the delegated context; exclusion of inherited host instructions was not independently verifiable.
