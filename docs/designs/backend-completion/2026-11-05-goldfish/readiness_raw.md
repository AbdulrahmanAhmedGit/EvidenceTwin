BRAINSTORM assessment: the concept identifies the principal migration concerns correctly. The findings below are requirements for the subsequent design, not defects claimed against an already implemented hosted service. No Blocker is asserted against this upstream concept.

1. **Major — Migration & Backward Compatibility: ownership must be assigned before imported records become accessible.**

   **Scope:** Concept “Migration implications” and “Access and privacy requirements”; `services/store.py:34–67`; `services/runtime.py:72–73`, `:182–190`, `:259–270`, `:292–296`; `__init__.py:48–51`.

   **Hazard:** Current persisted records have no owner column, and record lookup, lists, reports and activity read the workspace collectively. A new account system cannot safely infer ownership from an analysis ID, uploader filename, first login or the presence of authentication. File authorization must follow the same migrated ownership as its analysis. List totals, activity and comparisons can disclose another account’s research even if detail pages are protected.

   **Migration requirement:** Specify an explicit legacy-data ownership manifest or quarantined import state; preserve IDs and evidence relationships; reject ambiguous assignment; and keep unassigned records inaccessible to pilot users. Define authorization at the repository/service boundary for reads, writes, list aggregation, comparisons, files and workers. Require migration reconciliation and negative cross-account checks before hosted access opens. Choose account/team boundaries explicitly rather than deriving supervisor permissions from the audience list.

2. **Major — Migration & Backward Compatibility: scientific statuses require a coordinated wire-schema transition and historical interpretation policy.**

   **Scope:** Concept “Required report outputs,” “Source-level statuses,” “Clarified claim assessment requirements” and “Remaining scope decisions”; `contracts/common.py:23–25`; `contracts/analyses.py:72–73`, `:86`; `contracts/inspection.py:12–21`; `services/workflow.py:177–178`; `docs/FRONTEND_API_CONTRACT.md`, analysis inspection and report-filter contracts.

   **Hazard:** Existing verdicts include `unsupported` but not `contradicted`; source statuses include `unavailable` but not `inaccessible`. Adding the requested strings can fail strict current clients and backend DTO validation. Conversely, silently translating a historic `unsupported` outcome into `Contradicted` would invent scientific semantics. Existing exploratory records deliberately remain `not_evaluated`.

   **Migration requirement:** Define versioned canonical semantics and an explicit compatibility strategy covering backend contracts, frontend parsers, labels, list filters, comparisons, report exports and saved records. Preserve historical exploratory classifications and original model outputs. Define claim-level assessment and check coverage independently, including mixed-claim aggregation. Never map source authenticity directly to claim support, or missing evidence to contradiction.

3. **Major — Migration & Backward Compatibility: replacing local execution needs an explicit cutover protocol and billable-call recovery policy.**

   **Scope:** Concept “System responsibilities” and “Migration implications”; `services/workflow.py:24–42`, `:44–83`, `:94–101`; `services/runtime.py:196–207`; Backend Implementation Guide “Architecture and data ownership.”

   **Hazard:** Today the process lock and in-memory semaphore enforce a single local worker process; restarts mark queued/running work failed rather than replaying provider calls. Distributed workers cannot inherit those guarantees. Old and new workers operating during cutover could duplicate work, overwrite cancellation or consume provider budget twice. A crash after a provider accepted a request but before the result was persisted creates an ambiguous outcome.

   **Migration requirement:** Define drain/freeze/cutover steps; durable enqueue and execution ownership; attempt IDs, leases/fencing and cancellation semantics; retry rules for uncertain provider calls; and how old queued/running attempts are represented. Specify whether rollout rollback drains new work, pauses it or preserves it for compatible workers. Do not promise exactly-once remote generation without supporting provider semantics.

4. **Major — Migration & Backward Compatibility: private-file migration must preserve evidence identity and remain reversible alongside database changes.**

   **Scope:** Concept “Private file storage,” “Migration implications,” reproducibility requirement 7 and retention/deletion decisions; `services/store.py:28–35`; `services/runtime.py:107–108`, `:149–152`, `:188–193`, `:273–280`, `:373–380`.

   **Hazard:** Existing file references rely on local analysis/file IDs and generated filesystem paths. Moving records without their corresponding bytes, or changing assets independently of records, can produce inaccessible evidence or misleading provenance. Database rollback alone cannot restore deleted or moved objects. Current report deletion preserves the analysis; analysis deletion removes its uploads.

   **Migration requirement:** Specify an inventory of record IDs, file IDs, hashes and byte counts; ownership-aware object-key mapping; integrity reconciliation; and a staged copy/switch strategy retaining recovery material. Preserve immutable evidence identity and authorized API asset routes. Define deletion across originals, generated assets, source snapshots, retry history and backups, including the period during which rollback remains possible. Distinguish reproducibility retention from user-visible report deletion.

5. **Major — Migration & Backward Compatibility: format expansion needs a lossless import policy rather than replacing the existing dataset representation.**

   **Scope:** Concept “Input formats” and XLSX design questions; `services/runtime.py:112–147`, `:153–170`; `contracts/inspection.py:33–49`; Backend Implementation Guide “Input and upload policy.”

   **Hazard:** Current CSV values remain strings; structured JSON permits typed cells; only one dataset is accepted; reviewer context is limited to 200 rows; retained datasets are limited to 5,000 rows. Existing exploratory WebP/JSON/PDF acceptance differs from the new verified input list. XLSX introduces sheets, formulas and relationships that the present single-table shape cannot represent without policy decisions. Coercing legacy strings or using a preview as the computation input could change numerical meaning.

   **Migration requirement:** Define stable original-byte retention plus versioned parsed datasets and transformations. Specify XLSX sheet selection, formula/cached-value policy, external-link behavior and handling of cross-sheet dependencies. Decide explicitly which legacy formats remain exploratory. Deterministic checks must reference the complete approved dataset or record an explicit bounded scope; the reviewer preview must never silently become the scientific calculation dataset. Preserve original units, missing-value representation and numeric parsing provenance.

6. **Major — Migration & Backward Compatibility: provider configuration must change authority without changing accepted-job provenance.**

   **Scope:** Concept operator-only configuration requirement; `services/runtime.py:41–63`; `services/workflow.py:54–58`; `frontend/src/features/settings/AIProviderSettings.tsx:27`, `:39`, `:46–47`; `__init__.py:48–51`.

   **Hazard:** The current settings flow changes the backend-wide provider. Hosted researchers must not inherit that authority. Hiding the React page alone leaves settings and probe endpoints as server operations requiring independent authorization. Migrating credentials or rotating them while jobs are accepted can also make “retained initial configuration” ambiguous.

   **Migration requirement:** Specify operator roles and server-enforced access for settings read/save/test; secret migration and rotation; worker access to credentials; and immutable, non-secret job configuration references. Preserve the submitted model/provider/prompt version as execution provenance. Define behavior when a pinned credential becomes unavailable, without storing credential values inside audit records or research exports. The current page’s private-file storage notice must match the selected hosted implementation.

7. **Major — Migration & Backward Compatibility: “research case” is currently a sample-catalog namespace, not a user case resource.**

   **Scope:** Concept primary experience and Flask case-management responsibility; `services/runtime.py:33–37`, `:153–166`, `:318–325`; `contracts/analyses.py:31`; Backend Implementation Guide case endpoint handoff.

   **Hazard:** `/cases` currently returns authored educational samples `a1`–`a3`, and creation `caseId` selects those samples. Reusing those fields/routes for account-owned research cases would change their meaning and could accidentally attach illustrative values to real research or reinterpret existing analyses.

   **Migration requirement:** Decide explicitly whether account-owned cases receive a distinct resource/identifier or a versioned replacement. Keep educational sample IDs and sample-data provenance distinct from user research identifiers. Specify migration of existing `educational_case`/`caseId` references and compatibility for the current React sample library.

8. **Major — Migration & Backward Compatibility: persistence and scientific-policy versions need a forward/backward compatibility boundary.**

   **Scope:** Concept reproducibility requirements, “Key Decisions & Staging” and “Remaining scope decisions”; `services/store.py:34`, `:50–63`; `services/runtime.py:171–175`, `:200`; `services/workflow.py:195–209`; `contracts/common.py:9–10`.

   **Hazard:** The current store persists whole JSON snapshots without an explicit record-schema version. New ownership, source checks, calculation records and report structures will exceed the old reader’s assumptions. A code rollback could therefore fail to read new records, discard new state on writes, or regenerate a report under different rules. Prompt hashes alone do not version parsers, source policies, calculation code or scientific acceptance criteria.

   **Migration requirement:** Introduce explicit persisted-schema and scientific-policy versions, supported-reader ranges, reversible/irreversible migration boundaries and immutable historical result versions. Define when re-evaluation creates a new attempt/result instead of altering the old scientific record. Stage deployment so new readers precede new writes where needed; establish rollback behavior for records that an older release cannot understand. Keep verified capabilities disabled until their corresponding policy versions and acceptance checks are implemented; historical exploratory work must not be promoted automatically.

Read completeness: fully read the immutable `review_input.md` (255 lines), both standards and the readiness persona, and every required public file:

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

No required file was inaccessible. Truncated combined output was supplemented with targeted reads. No writes, tests, provider calls, private configuration, database contents, uploads, memory or session-history reads were performed. Parent-turn isolation and host-instruction exclusion were not independently verified.

---

Receipt clarification (actual reviewer follow-up):

Confirmed fully read:

- Persona: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/agents/implementation_readiness.md`
- Heilmeier standard: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/resources/document_standards/heilmeier-standard.md`
- Implementation Readiness standard: `/home/abdulrahman/.codex/plugins/cache/egm/egm/0.1.0/resources/document_standards/implementation-readiness-standard.md`
