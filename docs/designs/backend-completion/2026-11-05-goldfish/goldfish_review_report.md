# Goldfish Brainstorm Review Report

**Target:** `docs/designs/backend-completion/2026-11-05-goldfish/review_input.md` (255 lines), immutable review snapshot dated 2026-11-05.

**Mode:** BRAINSTORM. This is upstream concept synthesis, not an implementation-design approval or a runtime/security/scientific certification. Findings describe requirements for the subsequent design and hosted pilot. The current local exploratory implementation intentionally leaves scientific services unavailable; the report does not treat their absence as a built-feature defect.

## Reviewer status and evidence boundary

| Reviewer | BRAINSTORM dimension | Actual status | Raw report |
| --- | --- | --- | --- |
| egm-design | Cost, Quota & Token Economics | completed; complete required reads | [design_raw.md](design_raw.md) |
| egm-codebase-details | Observability & Operational SRE Debuggability | completed; complete required reads | [codebase_raw.md](codebase_raw.md) |
| egm-zoom-out | Contrarian / YAGNI & Code Minimization | completed; complete required reads | [zoomout_raw.md](zoomout_raw.md) |
| egm-comprehension | UX & Developer Ergonomics | completed; complete required reads | [comprehension_raw.md](comprehension_raw.md) |
| egm-implementation-readiness | Migration & Backward Compatibility | completed; complete required reads | [readiness_raw.md](readiness_raw.md) |
| egm-structural | Long-Term Tech Debt & Maintainability | completed; complete required reads | [structural_raw.md](structural_raw.md) |

All six returned actual final reports. No reviewer failed, so no review retry was required. Zoom-out and readiness provided receipt-only follow-ups naming their exact installed standards. Each receipt reports all ten required public/source files, the target, its installed persona and Heilmeier standard fully read; zoom-out additionally read zoom-out-standard.md and readiness read implementation-readiness-standard.md. All report no inaccessible required file and no private configuration, database/upload, memory/history, test or provider access.

The four live-agent slots included the primary and synthesizer, leaving two reviewer slots. Six separate general-purpose reviewers therefore ran in successive batches: design + codebase, zoom-out + comprehension, readiness + structural. Each was launched with `fork_turns: "none"`, the same immutable target and original reading list; later batches received no earlier findings. Parent-turn isolation was requested. Host-instruction exclusion remains unverified; no independent isolation probe was performed. Read receipts are reviewer attestations, not external runtime verification.

**Deduplicated result:** 0 Blocker, 14 Major, 1 Nit. Zero brainstorm blockers means the concept can proceed to refinement; it does not establish implementation or pilot readiness. Sources below use actual project-relative paths; all `services` and `contracts` references are normalized under `backend/evidencetwin_backend/`.

## Prioritized findings

### M01 — Bound scientific coverage with explicit supported combinations — Major

**Lenses:** zoom-out, structural, design. **Target:** V1 scientific scope; Source verification policy; Remaining scope decisions.

Broad categories do not define reliable methods. Require a claim-category × input-shape × procedure × source-type matrix with prerequisites, exact outputs, mandatory/applicable checks, failure/insufficiency behavior and reference cases. Define source-content extraction support without implying a general unstructured-document pipeline. Keep all five user-established categories visible while staging their supported combinations. The exact statistical allowlist, source-type matrix, notice semantics and Blind Optics/Neutral Twin criteria remain unresolved.

**Evidence/consequence:** `backend/evidencetwin_backend/services/runtime.py:111–170` contains bounded current ingestion, while `:215–222` exposes unavailable source/check behavior. Extending a fixed workflow without explicit adapters and method versions could produce broad verification labels over narrow actual coverage. Propose bounded source-policy, ingestion, deterministic-procedure and visualization interfaces, not an unrestricted plugin platform.

### M02 — Define one canonical scientific record and explicit contract transition — Major

**Lenses:** all six. **Target:** Required report outputs; Minimum end-to-end acceptance; Clarified claim assessment; API compatibility.

Define versioned Core inputs/results for assertions, evidence versions, typed check definitions/executions and assessments, independent of Flask, Werkzeug, browser URLs and presentation DTOs. A check records applicability, required inputs, execution outcome, scientific result, policy/procedure version, omission/failure reason and evidence/artifact references. Generate panels, filters, comparisons and reports from the same persisted records. Document claim-level assessment, mixed-claim aggregation and wire/schema migration. Do not silently equate historic `unsupported` with Contradicted or automatically promote exploratory records.

**Evidence/consequence:** `backend/evidencetwin_backend/contracts/common.py:22–26` lacks requested `contradicted`/`inaccessible` literals; `backend/evidencetwin_backend/contracts/analyses.py:59–80` has one analysis assessment; `backend/evidencetwin_backend/contracts/inspection.py:119–133` uses optional generic fields and findings for checks. Narrative-only extensions risk conflicting scientific meanings or strict-client failures. Keep job completion, provenance status, reproduced calculation, coverage, claim outcome and AI interpretation separate.

### M03 — Separate private research cases, evidence revisions, attempts and report versions — Major

**Lenses:** structural, readiness, comprehension. **Target:** Primary V1 experience; Migration implications.

Define stable resource identities and relationships before choosing routes. `/cases` and creation `caseId` currently denote illustrative educational samples; they must not silently become ownership-bearing research cases. A revised evidence packet needs an attributable revision, while retry repeats the same immutable inputs/configuration under defined execution rules. Preserve report-version links and prior results.

**Evidence/consequence:** `backend/evidencetwin_backend/services/runtime.py:33–37,153–174,195–211,318–325`; `backend/evidencetwin_backend/contracts/analyses.py:31`; `backend/evidencetwin_backend/services/workflow.py:195–209`. Reusing these identities would confuse real research, examples, revised evidence and historical conclusions. Preserve explicit sample provenance and document compatibility mappings.

### M04 — Enforce tenancy through repository, artifact and worker boundaries — Major

**Lenses:** design, zoom-out, readiness, structural. **Target:** Access/privacy; Migration implications.

Require an explicit principal and owner/case-scoped operations for direct reads, collections/totals, activity, reports, comparison, audit, files, exports and jobs. Opaque IDs and frontend permission flags are not authorization. Define legacy ownership using an explicit manifest or quarantine; unresolved records remain inaccessible rather than belonging to the first account. Team/supervisor/institution sharing remains a user decision.

**Evidence/consequence:** `backend/evidencetwin_backend/__init__.py:48–51` provides the optional hook; `backend/evidencetwin_backend/services/store.py:34,50–69` keys globally by kind/ID; `backend/evidencetwin_backend/services/runtime.py:72–73,182–186,252–313` uses global collections. Login alone would not provide hosted account isolation. Require negative cross-account acceptance checks throughout the resource graph.

### M05 — Make provider authority, credential lifecycle and private processing explicit — Major

**Lenses:** design, readiness, comprehension, codebase. **Target:** Operator-only configuration; Access/privacy.

Define server-enforced operator roles for settings read/save/test, hosted secret storage/rotation, worker access and immutable non-secret configuration references. A rotated or unavailable pinned credential needs explicit behavior. Disclose to researchers which evidence categories leave the service, the applicable provider/handling boundaries and the path for evidence that cannot be transmitted. No particular consent model or vendor is approved by this review.

**Evidence/consequence:** `backend/evidencetwin_backend/services/runtime.py:41–63,364–372` changes shared configuration; `backend/evidencetwin_backend/services/workflow.py:54–58,145–161` binds execution configuration and transmits packets/images; `frontend/src/features/settings/AIProviderSettings.tsx:27,32–47` presents workspace settings and private-file storage. Hiding navigation alone does not restrict the API; private server storage alone does not describe external processing.

### M06 — Specify durable execution and uncertain paid-call recovery — Major

**Lenses:** design, zoom-out, readiness, structural, codebase. **Target:** Workers; Migration implications.

Define atomic acceptance/enqueue, persisted attempt/step identities, leases/fencing, checkpoints, cancellation, stale-result rejection and duplicate-delivery behavior. Distinguish safe deterministic recomputation from an ambiguous provider request accepted before a crash. Preserve no-silent-replay semantics; do not promise exactly-once remote generation. Persist an immutable manifest of inputs, procedure/policy/software versions and non-secret provider configuration.

**Evidence/consequence:** `backend/evidencetwin_backend/services/workflow.py:23–83,94–128,184–185` uses process-local execution and attempt guards; `backend/evidencetwin_backend/services/runtime.py:196–207` retries attempts. A queue substitution alone could duplicate charges or overwrite newer/cancelled results.

### M07 — Budget the whole execution, including failed and cancelled calls — Major

**Lenses:** design, codebase, zoom-out. **Target:** Pilot usage/budgets; Access/privacy.

Specify per-role token/image limits, accumulated context bounds, per-attempt/account reservations, global provider concurrency/rate limits and an operator spending stop. Account separately for dispatch, failure, cancellation, discarded late outputs and unknown usage. Distinguish measured tokens, estimated price and unavailable billing data; set workload/budget assumptions with the user.

**Evidence/consequence:** `backend/evidencetwin_backend/services/workflow.py:142–161` runs four initial Council calls plus cross-review and judge with growing context; `:95–98,119–128` shows why cancellation and accepted successful results alone cannot account for external work. Job counts cannot bound total provider expenditure.

### M08 — Define lossless bounded ingestion and show exact processing scope — Major

**Lenses:** design, comprehension, readiness, structural. **Target:** Input formats; Metadata; XLSX.

Retain original bytes and version parsed tables/transformations. Define numeric and missing-value parsing, sheet/range selection, formula/cached values, cross-sheet dependencies, external links/macros and workbook cell lineage. Bound expanded bytes, sheets/cells and CPU/memory/runtime. Explicitly preserve or restrict legacy exploratory WebP/JSON/PDF behavior. Show limits before launch and exact dataset/range/row selection per calculation and reviewer; the AI preview must never silently become the scientific dataset.

**Evidence/consequence:** `backend/evidencetwin_backend/services/runtime.py:112–147,153–170` currently preserves CSV strings and sends at most 200 rows to review; `backend/evidencetwin_backend/contracts/inspection.py:33–49` is flat-table shaped. Silent coercion or workbook selection would change numerical meaning and hide incomplete coverage.

### M09 — Treat source retrieval as a new network and untrusted-content boundary — Major

**Lenses:** design, zoom-out. **Target:** Source verification policy.

Require destination/IP validation, redirect revalidation, restricted egress, credential isolation, time/byte/type/decompression limits, request quotas and bounded retries in the retrieval design. Specify which original source formats can actually be inspected. Record inaccessible/failed/unperformed checks honestly; network failure is not contradiction or proof of inauthenticity.

**Evidence/consequence:** `backend/evidencetwin_backend/services/runtime.py:101–104,215–216` currently treats URLs as metadata and performs no retrieval. Reusing that URL validation for fetching would not protect internal/cloud metadata destinations or bound resource consumption.

### M10 — Define reproducibility artifacts and lifecycle retention/deletion — Major

**Lenses:** design, zoom-out, structural, readiness, comprehension. **Target:** Verification requirement 7; Retention/export.

Specify immutable manifests resolving exact input/source versions, retained bytes or their availability limits, transformations, software/environment/procedure parameters, prompt content or recoverable versions, outputs and report versions. Distinguish replayable deterministic computations from inspection of historical stochastic AI output. Define authorized lifecycle rules for originals, snapshots, derivatives, historical attempts, exports, worker copies and backups; do not promise reproducibility after required evidence is deleted.

**Evidence/consequence:** `backend/evidencetwin_backend/services/store.py:50–75` rewrites JSON records; `backend/evidencetwin_backend/services/runtime.py:188–200,268–278` has different analysis/report deletion and retry history behavior; `backend/evidencetwin_backend/services/workflow.py:54–56,195–209` stores hashes and narrative reports. Hashes alone do not preserve reproducible contents, and visible report deletion may leave historical copies.

### M11 — Plan reversible data, file and worker cutover together — Major

**Lenses:** readiness, structural. **Target:** Migration implications.

Define persisted-schema/scientific-policy versions, supported reader ranges, staged new-reader/new-writer rollout and rollback boundaries. Inventory record/file IDs, hashes and byte counts; reconcile ownership and relationships, copy/switch storage with recovery material, and drain/freeze old execution before new workers accept work. Specify rollback treatment of newly written records and accepted jobs; database rollback cannot restore deleted objects. Re-evaluation creates attributable new results, not rewritten historical conclusions.

**Evidence/consequence:** `backend/evidencetwin_backend/services/store.py:28–67`; `backend/evidencetwin_backend/services/runtime.py:149–152,171–175,188–207,373–380`; `backend/evidencetwin_backend/services/workflow.py:24–42`. Independent cutovers could lose evidence identity or run both worker generations.

### M12 — Design safe operational diagnostics and actionable errors — Major

**Lenses:** codebase, comprehension. **Target:** Traceable execution; Actual states; Hosted experience.

Require analysis/attempt/operation correlation, typed safe error causes/retryability and researcher actions tied to file/sheet/column/claim where relevant. Separate web liveness, dependency readiness and worker progress; observe queue age/depth, stage latency, lease loss and recovery. Keep researcher scientific audit and operator telemetry independently authorized and retained, with emission allowlists and privileged configuration-change records. Choose thresholds from pilot assumptions and measured behavior, not invented SLAs.

**Evidence/consequence:** `backend/evidencetwin_backend/services/store.py:71–75` accepts generic event metadata; `backend/evidencetwin_backend/services/workflow.py:132–140,186–191` sanitizes distinct failures into broad messages; `backend/evidencetwin_backend/services/runtime.py:251–252,334–340` exposes audit and configuration-derived availability. Generic retry advice cannot distinguish researcher corrections from operator failures and may waste paid calls.

### M13 — Make claim bindings and evidence requests an explicit researcher journey — Major

**Lenses:** comprehension, structural. **Target:** Identify claims; Metadata; Required next steps.

Before relying on an assertion, show its scope, units, time/population/denominator and source/sheet/row/column bindings. Distinguish supplied from extracted values; unresolved essential bindings remain insufficient. Define missing-item requests, acceptable responses, conflicting metadata resolution and new evidence revisions with linked prior reports. Separate same-input retry from amendment/resubmission in UI and API.

**Evidence/consequence:** `backend/evidencetwin_backend/services/runtime.py:159–164` uses shared evidence packets; `backend/evidencetwin_backend/contracts/analyses.py:18–31` has submission metadata; `backend/evidencetwin_backend/services/runtime.py:196–205` retries an existing packet. Without an amendment path, an insufficiency report cannot reliably lead to stronger evidence.

### M14 — Size hosted persistence and polling from a pilot workload envelope — Major

**Lenses:** design, zoom-out. **Target:** Database; Workload limits.

Define expected users, concurrent jobs, polling load, evidence size and retained attempts before vendor/capacity selection. Separate indexed authorized summaries from large artifacts and page/filter within scoped queries. Bound history/audit retrieval and validate the chosen architecture against the stated envelope.

**Evidence/consequence:** `backend/evidencetwin_backend/services/store.py:50–64` loads complete JSON collections; `backend/evidencetwin_backend/services/runtime.py:75–86,182–183,259–267,292–296` filters after loading; `docs/FRONTEND_API_CONTRACT.md:75` establishes polling. Small pages do not bound full-workspace deserialization cost.

### N01 — Reuse current transport and keep optional integrations staged — Nit

**Lens:** zoom-out. **Target:** API/future clients.

Prefer one framework-independent Python Core package before deciding a separate deployed service. Reuse polling, inspection routes, opaque asset identifiers and truthful unavailable capabilities where semantics fit. A full benchmark management UI, SSE, MCP, SDKs, expanded exports or event sourcing need a concrete requirement before entering the critical path. This is a simplification proposal, not a newly approved exclusion or a reason to skip scientific acceptance checks.

## Proposed examinations and unresolved decisions

Propose reference cases with documented provenance and known calculations, including the user's 20% versus reproduced 5% contradiction and missing-treatment-data insufficiency. Add mixed claims, comparability mismatch, inaccessible source, retraction/correction semantics, unsupported methods, workbook scope, visual-only limitations and genuine disagreeing reviewers. These are future checks, not executed validation or measured success rates. A small acceptance suite can precede a full benchmark product; independent reference judgments and rubric ownership still need specification.

Operational examinations should cover cross-account denial (including totals/files/jobs), operator-only settings, crash before/after external dispatch, redelivery/cancellation, amended evidence versus retry, storage reconciliation/rollback, stalled workers with healthy HTTP and retained accounting for cancelled calls. Define expectations from selected policies and pilot volume before asserting pass criteria.

Unresolved user/product decisions: complete claim taxonomy/aggregation; first procedure and source-policy support matrix; Neutral Twin/Blind Optics semantics; workbook formula/sheet policy; team/supervisor/institution permissions; legacy ownership assignment; privacy/provider processing and retention/deletion policy; pilot workload, budgets, operators and timeline. Infrastructure/authentication/database/storage/queue choices remain design decisions under those requirements. No reviewer selected a vendor, supplied an approved budget/timeline or established scientific accuracy.
