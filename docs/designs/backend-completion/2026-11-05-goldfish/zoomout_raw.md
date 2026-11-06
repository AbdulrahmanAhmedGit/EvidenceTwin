BRAINSTORM result: the objective is clear and useful. No concept-level Blocker identified. The main risk is treating “complete the backend” as one deliverable spanning scientific methods, hosted tenancy, durable execution and evaluation. The following are design requirements and reuse opportunities, not claims that the current exploratory implementation is defective.

1. **Major — Contrarian / YAGNI & Code Minimization: stage scientific coverage by explicitly supported combinations.**

   **Affected scope:** FeatureConcept, “V1 scientific scope established by the user,” “Source verification policy,” and “Remaining scope decisions.”

   Five claim categories, XLSX, charts, arbitrary source URLs, source authenticity/content matching and a hosted pilot create several interacting validation problems. A broad category label cannot establish which methods are reliable. Source-content inspection also needs a clear boundary against the exclusion of arbitrary unstructured documents.

   **Consequence:** implementation could deliver a convincing workflow whose actual supported scientific coverage is unclear, or spend most effort constructing a general research-document ingestion system.

   **Requirement / simpler alternative:** specify a bounded matrix of claim category × input shape × supported procedure × source type. Define preconditions, exact outputs, failure/insufficiency behavior and reference examples for each supported combination. Explicitly identify unsupported content types and manual evidence requests. Stage delivery within the user’s established scope; do not silently drop categories or imply all category combinations are verified.

   **Reuse:** `runtime.py:create_analysis` already distinguishes retained PDFs from extracted evidence and preserves user-supplied metadata; `get_analysis_evidence` already exposes an evidence contract and computed-fact placeholder. Extend that boundary rather than inventing a separate ingestion product.

2. **Major — Contrarian / YAGNI & Code Minimization: “independent Scientific Core” should mean dependency independence before deployment independence.**

   **Affected scope:** FeatureConcept, “System responsibilities” and “API and future clients.”

   The required Core separation does not inherently require another network service, another API or a separately deployed microservice. Those add authentication between services, serialization, version skew and distributed failure modes before their necessity is demonstrated.

   **Consequence:** infrastructure work could dominate scientific implementation and create duplicated scientific behavior across Flask, workers and future integrations.

   **Requirement / reuse opportunity:** define a Python package boundary with explicit inputs, check records and result objects, callable by asynchronous workers without Flask request/session objects. Keep Flask responsible for account authorization and HTTP serialization. Choose separate service deployment only if a concrete operational requirement warrants it.

   Existing `workflow.py:Workflow.run`, provider review schemas/reference validation, `store.py:Store`, and `contracts/` provide reusable pieces. Reuse their responsibilities selectively: `workflow.py` currently imports Werkzeug errors and uses local files/store state, so copying that class wholesale would not establish framework independence.

3. **Major — Contrarian / YAGNI & Code Minimization: use one structured verification record as the reporting backbone.**

   **Affected scope:** FeatureConcept, “Required report outputs,” “Per-source verification record,” “Required fields for every claim”; `contracts/common.py:Verdict, SourceStatus`; `contracts/analyses.py:Analysis`; `contracts/inspection.py:Source, SectionResponse`; `workflow.py:finish, report`.

   Current contracts hold a single analysis assessment, optional source status, generic findings and textual report sections. They do not yet define the requested first-class per-claim/check/source relationships. The current workflow intentionally places AI judgment outside the verified badge.

   **Consequence:** independently extending every panel and report could produce inconsistent verdicts, source statuses and coverage summaries. A later adapter might collapse “Contradicted” into existing “unsupported,” or mistake source verification for claim support.

   **Requirement / reuse opportunity:** define one structured result model linking each assertion to applicable checks, completion/results, evidence references, calculations, limitations and assessment. Generate existing panel DTOs and report prose from that model through explicit compatibility mappings. Preserve Contradicted versus Insufficient Evidence, provenance versus claim support, and job completion versus scientific coverage. Reuse existing `Finding`, `SectionResponse`, evidence contract and report adapters instead of building parallel report engines.

4. **Major — Contrarian / YAGNI & Code Minimization: tenancy belongs at shared data-access boundaries.**

   **Affected scope:** FeatureConcept, “Access and privacy requirements” and “Migration implications”; `__init__.py:infrastructure_boundary`; `store.py:Store.get, all, put`; `runtime.py:record, list_analyses, list_reports, list_activity, compare_analyses, file_asset`.

   The existing optional authentication hook and global record store are explicitly local-workspace foundations. Adding account checks separately to each route would duplicate policy and leave list, comparison, audit, worker or asset paths easy to overlook.

   **Consequence:** a superficially authenticated deployment could expose another account’s existence, metadata or files.

   **Requirement / simpler alternative:** establish account ownership and operator role semantics first, then require ownership-aware access for direct reads, collections, linked resources, exports and worker actions through a shared repository/application boundary. Treat team/supervisor sharing as unresolved. Define how legacy records obtain an owner before exposing them in the pilot.

   Reuse existing opaque IDs and record-aware asset routes, but do not treat those as authorization. Restrict provider configuration in both HTTP handlers and navigation; `AIProviderSettings.tsx` currently represents workspace-wide provider management.

5. **Major — Contrarian / YAGNI & Code Minimization: durable workers must preserve the existing no-silent-replay guarantee.**

   **Affected scope:** FeatureConcept, “Asynchronous workers” and “Migration implications”; `workflow.py:recover, submit, update, cancel`; `runtime.py:retry_analysis`.

   Existing execution uses a process lock, in-memory semaphore/futures and explicit interrupted-job failure. It already has valuable attempt fencing, cancellation protection and retained retry history. Moving to a durable queue is required for the requested hosted execution, but a broker alone does not define safe recovery.

   **Consequence:** delivery retries or worker crashes could repeat billable calls, overwrite cancelled/newer attempts or expose completed status without persisted outputs.

   **Requirement / reuse opportunity:** specify persisted attempt identity, execution ownership, duplicate-delivery handling, cancellation/deletion behavior and the policy for uncertain provider-call outcomes. Define how accepted database state and queued work remain consistent. Reuse attempt fencing and explicit retry semantics; do not simply wrap current `Workflow.run` in automatic task retries.

6. **Major — Contrarian / YAGNI & Code Minimization: preserve reproducibility through versioned attempts, not undifferentiated record growth.**

   **Affected scope:** FeatureConcept, verification requirement 7 and “Retention/deletion/export policy”; `store.py:Store.put`; `runtime.py:retry_analysis, delete_analysis, delete_report`; `workflow.py:submit, report`.

   Current persistence rewrites JSON snapshots and keeps retry copies inside the record. This is useful local functionality but is not yet a retention model for private source snapshots, deterministic outputs, method versions and hosted deletion.

   **Consequence:** audit exports may omit necessary replay information, retention costs may expand unpredictably, and deletion may conflict with claimed reproducibility.

   **Requirement / simpler alternative:** define the minimal immutable attempt manifest: authorized input/version references, transformations, check/method versions, actual outputs, provider/model/prompt identity and source retrieval/version information. Specify what export reproduces deterministically versus merely documents a historical AI response. Define deletion, backup expiry and inaccessible-source limitations explicitly. Full event sourcing is unnecessary unless a concrete requirement needs it.

7. **Major — Contrarian / YAGNI & Code Minimization: bound pilot cost and prove scientific behavior before expanding Council infrastructure.**

   **Affected scope:** FeatureConcept, “Minimum end-to-end acceptance” and “Pilot usage expectations”; `workflow.py:run`; `runtime.py:create_benchmark, capabilities`.

   Council currently performs four initial reviews followed by cross-review and judgment when preceding outputs validate. Hosting converts these into shared provider expenditure. The concept acknowledges budgets and benchmark judgments as open, but does not yet establish their release role.

   **Consequence:** a small pilot can consume unpredictable resources, while elaborate agent orchestration provides little evidence that scientific checks are correct.

   **Requirement / reuse opportunity:** define operator-controlled submission/concurrency limits, bounded source retrieval and file processing, provider-call limits and uncertain-call handling before pilot release. Define a small reference suite with known calculations, documented source-policy cases, missing-input cases and contradiction-versus-insufficiency examples. Specify review of reference judgments without inventing accuracy targets. A full benchmark management product need not precede these acceptance checks; the existing benchmark endpoint can remain unavailable until its evaluation protocol exists.

8. **Nit — Contrarian / YAGNI & Code Minimization: preserve current transport and research-tool limits unless a requirement changes.**

   **Affected scope:** FeatureConcept, “API and future clients”; `docs/FRONTEND_API_CONTRACT.md`, processing/polling and Phase 5; `runtime.py:compare_analyses, create_benchmark, list_integrations`.

   The existing polling, inspection sections, report JSON export and explicit unavailable capabilities already support useful integration boundaries.

   **Requirement / reuse opportunity:** retain polling and existing routes while introducing the necessary scientific/ownership contract changes. Keep MCP, external-client SDKs, SSE, benchmark dashboards and expanded export formats outside the critical path unless a concrete pilot requirement emerges. This supports the concept’s existing staging rather than changing user scope.

Read completeness: every required file was fully read successfully, including portions reread after output truncation:

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

Read the supplied persona and both standards. Performed public Python source searches for reuse. No writes, tests, provider calls, private configuration, databases, uploaded data, memory or session-history access. Parent-turn isolation was requested; host-instruction exclusion remains unverified.

---

Receipt clarification (actual reviewer follow-up):

Fully read:

- Persona: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/agents/zoom_out.md`
- Heilmeier standard: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/resources/document_standards/heilmeier-standard.md`
- Zoom-Out standard: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/resources/document_standards/zoom-out-standard.md`

No required files were inaccessible.
