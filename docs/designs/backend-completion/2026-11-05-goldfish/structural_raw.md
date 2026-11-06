BRAINSTORM findings — Structural / Long-Term Tech Debt & Maintainability

These are requirements for the implementation design, not claims that the intentionally unavailable scientific features are defective. No concept-level Blocker identified; the following Major risks should be resolved before implementation or hosted release.

1. **Major — Define a domain model independent of both Flask and existing wire DTOs.**

   **Scope:** Concept, “System responsibilities,” “API and future clients,” “Required fields for every claim”; `services/runtime.py:94–176`; `services/workflow.py:100–209`; `contracts/analyses.py:38–90`; `contracts/inspection.py:119–133`.

   **Risk and consequence:** The existing runtime creates an application-specific nested record, while the workflow edits its HTTP-facing analysis fields and directly constructs report sections. Extending this structure into the Scientific Core would couple scientific calculations, job persistence and React presentation. Future clients would inherit a browser-oriented result structure or require parallel scientific logic.

   **Maintainability requirement:** Define versioned Core input/result models for claims, evidence versions, check executions, findings and assessment decisions; keep them independent of Flask, Werkzeug exceptions, browser links and presentation sections. Flask adapters should translate those models into documented HTTP contracts. Report presentation should consume the same persisted scientific results rather than recompute assessment.

2. **Major — Represent scientific check execution separately from findings and overall job state.**

   **Scope:** Concept, “Minimum end-to-end acceptance,” “Source-level statuses,” “Required fields for every claim”; `contracts/inspection.py:12–20,119–133`; `contracts/analyses.py:38–58`; `services/workflow.py:162–185`.

   **Risk and consequence:** Existing `checks` uses the `Finding` shape, while sources expose a status and free-text `checked` field. Neither alone expresses mandatory versus optional checks, applicability, prerequisites, unperformed checks, policy version or the exact assertion evaluated. Encoding these in narrative or arbitrary JSON would produce brittle assessment rules and inconsistent coverage.

   **Maintainability requirement:** Introduce typed check definitions and executions with stable IDs, subject/claim IDs, policy or procedure version, prerequisite inputs, applicability decisions, execution outcome, evidence/result references and reasons for omission or failure. Define coverage and assessment as separate outputs with explicit derivation rules. Source provenance verification must remain distinct from claim support; absence must remain distinct from contradiction.

3. **Major — Specify an immutable execution manifest and checkpoint protocol before replacing the local worker.**

   **Scope:** Concept, “Asynchronous workers,” “Migration implications,” “Reproducibility”; `services/workflow.py:23–63,71–98,142–160`; `services/runtime.py:49–55`; `services/store.py:20–60`.

   **Risk and consequence:** The local implementation uses a process file lock, in-memory futures/semaphore and an attempt token; restart recovery marks accepted work failed. Provider selection is captured as a live object when submitting. These are reasonable local boundaries, but simply substituting a queue would leave duplicate delivery, crash-after-provider-response, lease expiry, cancellation races and configuration changes underdefined.

   **Maintainability requirement:** Persist a complete immutable execution manifest, including evidence versions, supported procedures/policies, software/prompt versions and non-secret provider configuration references. Define durable acceptance, atomic enqueue/persistence, worker ownership, fencing/checkpoints, cancellation and retry semantics. Record uncertain external-call outcomes explicitly; do not claim exactly-once paid generation or silently replay an uncertain call. Scientific results and billing/accounting records need identifiable attempt and step boundaries.

4. **Major — Make ownership enforcement a repository and worker boundary, not only an HTTP hook.**

   **Scope:** Concept, “Access and privacy requirements,” “Migration implications”; `__init__.py:25–27,48–51`; `services/runtime.py:72–73,182–186,252–313`; `services/store.py:50–69`.

   **Risk and consequence:** Current records are keyed by kind/ID, global lists load every record, and authorization is an optional request hook. A hosted design that only adds a login check or filters individual route results would be easy to bypass through list/activity/report/comparison paths or background jobs.

   **Maintainability requirement:** Define an explicit authenticated principal and case ownership boundary; require scoped repository operations and worker execution authorization. Specify access to every derived artifact, report, source snapshot and audit record. Legacy records without ownership need an explicit migration/quarantine rule rather than automatic exposure. Decide team/supervisor roles separately; the audience list does not grant permissions.

5. **Major — Separate research cases, evidence versions, analysis attempts and reports as independently identified resources.**

   **Scope:** Concept, “Primary V1 experience,” “Persistent database,” “Migration implications”; `services/runtime.py:33–37,153–174,195–211`; `services/workflow.py:195–209`; `services/store.py:50–60`; implementation guide, “Endpoint handoff.”

   **Risk and consequence:** `/cases` currently denotes educational examples; the runtime packet uses its analysis ID as `case_id`; reports use the analysis ID; retry replaces current results while embedding attempt history. Reusing these identities for persistent researcher cases would make evidence updates, reruns, report citation and deletion ambiguous, and could silently change the meaning of existing case APIs.

   **Maintainability requirement:** Define stable identities and relationships for researcher cases, educational catalog entries, immutable evidence revisions, analysis configurations, execution attempts and report versions. Specify which report/version a link cites and how legacy endpoints map. Preserve educational samples as explicitly illustrative input. A retry must retain attributable prior results without allowing current evidence or configuration to rewrite their provenance.

6. **Major — Avoid turning source-type and statistical support into branches inside one workflow.**

   **Scope:** Concept, “Claim categories,” “Input formats,” “Source verification policy,” “Remaining scope decisions”; `services/runtime.py:111–170`; `services/workflow.py:142–160`; `contracts/inspection.py:28–48`.

   **Risk and consequence:** Existing ingestion is a bounded inline file-type switch and the exploratory workflow has a fixed reviewer sequence. Adding publisher lookups, workbook interpretation, deterministic tests and chart transformations directly here would create interdependent conditionals. Each new source type or procedure could alter unrelated behavior and make acceptance coverage hard to audit.

   **Maintainability requirement:** Define bounded interfaces for ingestion, source-policy adapters, deterministic procedures and visualization transformations. Each implementation should declare supported inputs, prerequisites, output schema, version and failure/unsupported semantics. Persist transformations from original bytes to normalized values, including selected workbook sheets/cells and formula policy. Keep the initial allowlists explicit; unsupported methods must produce limited or insufficient assessments rather than fall through to AI inference.

7. **Major — Separate reproducibility artifacts from mutable application records and lifecycle deletion.**

   **Scope:** Concept, “Access and privacy requirements,” “Per-source verification record,” “User-defined verification requirements” item 7; `services/store.py:50–75`; `services/runtime.py:188–194,268–276`; `services/workflow.py:50–56,195–209`.

   **Risk and consequence:** Current persistence replaces complete JSON snapshots; events live inside those records; deleting an analysis removes its record and uploaded directory. Prompt hashes identify versions but do not themselves preserve the prompt content. Extending this arrangement to source snapshots, calculations and exported reports would make retention/deletion and reproducibility accidentally depend on UI resource operations.

   **Maintainability requirement:** Specify a versioned artifact manifest linking retained inputs, transformations, exact procedures/software, prompt contents or resolvable immutable versions, results and reports. Define authorized retention/deletion across originals, derivatives, worker copies, exports and backups, including what reproducibility information remains after permitted deletion. Do not promise exact reproduction of stochastic or externally updated models; distinguish replayable deterministic calculations from inspection of recorded AI executions.

8. **Major — Version contract evolution explicitly rather than overloading existing enums or free-text reports.**

   **Scope:** Concept, “Required report outputs,” “Clarified claim assessment requirements,” “Remaining scope decisions”; `contracts/common.py:22–26`; `contracts/analyses.py:61–80`; `contracts/inspection.py:106–133`; frontend contract, “Analysis record and processing,” “Audit and report.”

   **Risk and consequence:** Existing assessment includes `unsupported` but no `contradicted`; source status includes `unavailable` rather than the requested `Inaccessible`; analysis has one assessment, while claim results and structured provenance are not first-class report fields. An implicit string substitution or narrative-only extension risks old clients rejecting responses or displaying scientific distinctions inaccurately.

   **Maintainability requirement:** Specify canonical internal semantics and a documented API migration/version strategy, including per-claim results, mixed-claim aggregation, source-status mappings and machine-readable report content. Retain compatibility only where its semantics are accurate. The report, filters, detail view and exports must use the same assessment records. AI agreement or an authenticated source must never automatically produce a supported claim.

Required-read completion:

- Fully read: persona `agents/structural.md`.
- Fully read: standard `resources/document_standards/heilmeier-standard.md`.
- Fully read: immutable `docs/designs/backend-completion/2026-11-05-goldfish/review_input.md`.
- Fully read: `BACKEND_IMPLEMENTATION_GUIDE.md` — 318 lines.
- Fully read: `docs/FRONTEND_API_CONTRACT.md` — 252 lines.
- Fully read: `backend/evidencetwin_backend/__init__.py` — 69 lines.
- Fully read: `backend/evidencetwin_backend/services/runtime.py` — 380 lines.
- Fully read: `backend/evidencetwin_backend/services/workflow.py` — 213 lines.
- Fully read: `backend/evidencetwin_backend/services/store.py` — 75 lines.
- Fully read: `backend/evidencetwin_backend/contracts/analyses.py` — 90 lines.
- Fully read: `backend/evidencetwin_backend/contracts/inspection.py` — 133 lines.
- Fully read: `backend/evidencetwin_backend/contracts/common.py` — 69 lines.
- Fully read: `frontend/src/features/settings/AIProviderSettings.tsx` — 48 lines.

Initial tool output truncations were addressed with subsequent bounded reads. No required file was inaccessible. No writes, tests, provider calls, private configuration, databases, uploads, memory or session-history reads were performed. Parent-turn isolation and exclusion of host instructions could not be independently verified.
