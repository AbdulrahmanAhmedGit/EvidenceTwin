# Documentation map and authority

Consolidated 2026-11-07 after the researcher-workspace transformation. Seven guides below describe current behavior. Historical records keep their original dates and evidence limits; neither old approvals nor a new application review establish scientific or hosted readiness.

| Active guide | Responsibility |
| --- | --- |
| [Documentation map](DOCUMENTATION_MAP.md) | Authority, conflicts, reviewed families and archive paths. |
| [Architecture](ARCHITECTURE.md) | Actual frontend/services/storage and execution boundaries. |
| [Development](DEVELOPMENT.md) | Setup, accounts/provider administration, focused checks and fixture preview. |
| [API](API.md) | Current session/case/revision/run contracts and retained endpoints. |
| [Researcher workflow](PRODUCT_WORKFLOWS.md) | Question → saved case/revisions → consent → recorded Council/report. |
| [Scientific scope](SCIENTIFIC_SCOPE.md) | Implemented exploratory scope, unavailable science and open gates. |
| [Deployment/rollback](DEPLOYMENT_ROLLBACK.md) | Local runtime, data preservation, ownership modes and safe reversal. |

[Root DESIGN.md](../DESIGN.md) and `.impeccable/design.json` describe the implemented slate/cobalt system. CSS is the runtime authority for actual visual values. [BRAND_INTEGRATION.md](BRAND_INTEGRATION.md) remains the authoritative artwork-provenance/usage supplement. Root/module READMEs are entry points rather than competing specifications. [AGENTS.md](../AGENTS.md) carries current agent rules.

## Requirements and decisions

1. [concepts_brief.md](../concepts_brief.md) is the approved requirements baseline; it is preserved unchanged. [PRODUCT.md](../PRODUCT.md) explains durable product intent, including planned capabilities, rather than asserting hosted/scientific completion.
2. [design_draft.md](../design_draft.md) contains approved sections, selected directions and unresolved designs. Read scoped approvals with their dates. Nested [designs/backend-completion](designs/backend-completion/) includes frozen review inputs, proposals, selected technical choices and acceptance research. These are not replacements for the approved brief.
3. [TECHNICAL_PLAN_GATES.md](designs/backend-completion/TECHNICAL_PLAN_GATES.md) keeps all **24 gates OPEN**. Later scoped decisions select PostgreSQL, SQLAlchemy Core/Psycopg/Alembic and Read Committed for the bounded infrastructure path; earlier candidate/unselected wording remains historical chronology. The [coding-readiness report](designs/backend-completion/CODING_READINESS_REPORT.md) and [preserved implementation guide](../BACKEND_IMPLEMENTATION_GUIDE.md) distinguish planning, isolated infrastructure evidence and current HTTP runtime.
4. Current implemented behavior is verified against source by these active guides. It does not silently amend scientific requirements, approve a pilot, assign old ownership or migrate HTTP execution to PostgreSQL.

## Reviewed document families and conflicts

Review depth: all inventory paths/headings were discovered; current READMEs, product context, previous DESIGN, implementation entry points and relevant case/access/ingestion source were read directly. Scientific and dated review families were sampled by status, introduction, decision/approval notes and relevant boundaries; no claim of line-by-line revalidation of every historical document is made. The per-file [review manifest](../output/transformation/documentation-review-manifest.json) records every inventoried path and treatment. Pre-task hashes are in [the inventory](../output/transformation/documentation-inventory.json).

| Family | Treatment and resolved conflict |
| --- | --- |
| Root/module README and service README | Rewritten for actual Flask, optional accounts, provider-independent case saving and current guide links. Old “No Flask backend”/“authentication unavailable” statements removed from current entry points. |
| Root DESIGN and Impeccable sidecar | Refreshed from semantic CSS and actual components; green/sage system superseded. Prior identity preserved in source snapshot and historical design records. Inherited modal overlay literals are documented honestly. |
| FRONTEND_ARCHITECTURE, INTEGRATION_GUIDE, DESIGN_SYSTEM, BACKEND_SKELETON_REFERENCE, DEVELOPMENT_STAGES, FRONTEND_API_CONTRACT | Archived with original prose/dates and rebased Markdown links; compact old-path pointers retained. Current guides consolidate overlapping technical direction. |
| BACKEND_IMPLEMENTATION_GUIDE | Original body preserved unchanged, with a current-guidance context notice. Its unique PostgreSQL completion/recovery evidence remains. Pre-case settings/auth/workflow language is historical. |
| AI_PROVIDER_CONFIGURATION | Retained as historical provider storage/wire evidence. Current operator/session authority is in API/development guides; ordinary researchers cannot administer providers. |
| BRAND_INTEGRATION | Preserved artwork identity and provenance supplement. Historical placement/check counts retain their original scope. |
| BACKEND_RUNTIME_VERIFICATION; PHASE_2/3/4/5_ACCEPTANCE; QUICK_FIVE_PHASE_AUDIT; ACCESSIBILITY_REVIEW; FRONTEND_STABILIZATION | Preserved dated verification snapshots. Their fixture/test counts and scope are not present-day whole-product acceptance. |
| FRONTEND_COLOR_TYPOGRAPHY_REVIEW, FRONTEND_MOTION_REFINEMENT, FRONTEND_REDESIGN, LANDING_REDESIGN, PROMPT_FIRST_REDESIGN, SAAS_DASHBOARD_REDESIGN | Preserved historical design/implementation history. Prior palette, local-only XLSX, preparation-wizard handoff and backend deferrals are superseded for current behavior. Current scientific/brand constraints still apply. |
| `.impeccable/critique`, `.impeccable/surfaces`, `output/impeccable-review` | Preserved prior direction, review and finish evidence; original scope/date governs. The new transformation records live separately under `output/transformation`. |
| Scientific/source/numerical/statistical/decimal/confirmation/Council/acceptance-corpus/check-axis/absence/publication drafts | Preserved in place, classified as draft/specification/decision history. Their examples and planned tests are not executed scientific results. All open-gate statuses retained. |
| Core/transaction/lease/job/attempt/schema/SQL/tooling/dependency/readiness/test plans | Preserved selected bounded infrastructure design and chronology. Isolated PostgreSQL is not current local HTTP execution. Earlier “no code authorized” notes retain their original moment and do not invalidate later scoped implementation evidence. |
| Frozen Goldfish package (`2026-11-05-goldfish`) | Preserved frozen intake, raw six-lens findings and review report. Nested concepts brief is historical review input, not the current approved baseline. |
| Ember acceptance case and associated artifacts | Preserved manual investigation, pinned bytes/provenance and incomplete historical identity/original-chart boundary. No backend scientific acceptance is claimed. |
| Runtime packaged prompts and `snippets/prompts` | Preserved without rewriting; runtime instructions versus source/reference copies remain distinct. Prompt text is not independent scientific verification. |

## Archive and merge record

Archive date: 2026-11-07. No unique requirements, prompts, approval records, scientific drafts or dated verification reports were deleted. No persisted research or screenshot was changed by this consolidation. Six redundant guides were merged into current architecture/development/API/workflow/design guidance. Old paths remain pointers, preserving source comments and external references. Relative Markdown targets inside archived guides were rebased to their original destinations; prose, dates and historical claims remain intact. The [archive manifest](../output/transformation/documentation-archive-manifest.json) records original/archive hashes and paths.

- `docs/FRONTEND_ARCHITECTURE.md` → [FRONTEND_ARCHITECTURE.md](archive/2026-11-07/FRONTEND_ARCHITECTURE.md).
- `docs/INTEGRATION_GUIDE.md` → [INTEGRATION_GUIDE.md](archive/2026-11-07/INTEGRATION_GUIDE.md).
- `docs/DESIGN_SYSTEM.md` → [DESIGN_SYSTEM.md](archive/2026-11-07/DESIGN_SYSTEM.md).
- `docs/BACKEND_SKELETON_REFERENCE.md` → [BACKEND_SKELETON_REFERENCE.md](archive/2026-11-07/BACKEND_SKELETON_REFERENCE.md).
- `docs/DEVELOPMENT_STAGES.md` → [DEVELOPMENT_STAGES.md](archive/2026-11-07/DEVELOPMENT_STAGES.md).
- `docs/FRONTEND_API_CONTRACT.md` → [FRONTEND_API_CONTRACT.md](archive/2026-11-07/FRONTEND_API_CONTRACT.md).

## Unresolved questions and evidence limits

Scientific procedure/schema/source acceptance, historical Ember identity/chart access, hosted identity integration, team/supervisor/institution roles, retention/deletion rules, durable HTTP-worker cutover, spend/quota controls, coordinated hosted restore and pilot approval remain unresolved under the gate register. Local invite-only accounts do not settle the external hosted-auth design. Local records owned by `local` and legacy unassigned rows need explicit reviewed migration before account ownership changes.

The broad older Playwright specs need deliberate adaptation to the new workflow; do not delete/disable them or cite prior pass counts as new acceptance. Transformation checks are focused application evidence only. Dedicated Playwright MCP, Context7 MCP and Chrome DevTools MCP were unavailable; installed Playwright CLI with Brave supplied browser feedback. No hosted/scientific, paid-provider, physical-device, screen-reader or cross-browser acceptance was performed. The finish review's SHIP verdict applies to its reviewed fix list; final product acceptance belongs to the owner.

## 2026-11-08 evidence-processing increment

[EVIDENCE_PROCESSING.md](EVIDENCE_PROCESSING.md) describes actual complete-table queries, descriptive Decimal calculations, public-source retrieval, per-role evidence access and results/report composition. Earlier statements in dated reports that URLs were metadata and packets contained only 200 rows remain accurate for their original scope. Current workflow, architecture, API and scientific-scope guides now link this implementation. All scientific gate and historical approval records remain unchanged. No documents were merged, removed or archived in this increment.

## 2026-11-08 source connectors and unified results increment

The current [evidence guide](EVIDENCE_PROCESSING.md), [API](API.md), [setup](DEVELOPMENT.md), [workflow](PRODUCT_WORKFLOWS.md) and [scientific scope](SCIENTIFIC_SCOPE.md) include the multi-source, caption and translated-report boundaries. The [connector implementation record](../output/source-connectors/IMPLEMENTATION.md) and [unified results implementation record](../output/unified-results/IMPLEMENTATION.md) contain dated engineering evidence. The independent finish review and its scoped verdict remain separate files under `output/unified-results/`.

This increment does not supersede scientific decisions or historical verification. No historical guides were deleted, merged or archived again. Existing archive paths and dated records remain intact. Documentation now distinguishes successful public caption access, source retrieval failures, exact descriptive arithmetic, machine translation safety fallback and unavailable scientific verification.
