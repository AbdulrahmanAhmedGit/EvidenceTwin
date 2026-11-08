# Documentation authority

Organized 2026-11-08. The [documentation index](README.md) is the entry point for current guidance. This map establishes precedence and separates implementation from proposals and historical evidence.

## Authority order

1. [concepts_brief.md](../concepts_brief.md) is the approved requirements baseline. It remains unchanged.
2. Explicit owner approvals apply within their recorded scope. The [visualization focus clarification](decisions/2026-11-08-visualization-focus.md) prioritizes misleading scientific plots, initially in healthcare and public health. [PRODUCT.md](../PRODUCT.md) summarizes that purpose.
3. Current verified source and API behavior establish what the application implements. They do not approve scientific procedures or close gates.
4. Current guides describe that implementation. [Architecture](ARCHITECTURE.md), [Development](DEVELOPMENT.md), [API](API.md), [Workflow](PRODUCT_WORKFLOWS.md), [Evidence processing](EVIDENCE_PROCESSING.md), [Scientific scope](SCIENTIFIC_SCOPE.md) and [Deployment/rollback](DEPLOYMENT_ROLLBACK.md) each own their named subject. [DESIGN.md](../DESIGN.md) defines the visual system, with CSS as the runtime source of actual values. [Brand integration](BRAND_INTEGRATION.md) preserves artwork provenance.
5. [design_draft.md](../design_draft.md) and [backend design documents](designs/backend-completion/README.md) contain scoped approvals, proposals and unresolved decisions. Draft procedures and planned tests are not executed scientific evidence.
6. [Historical reports and guides](archive/README.md) retain their original dates and limits. An old acceptance result applies only to its recorded scope.

## Conflicts to resolve explicitly

| Earlier assumption | Current interpretation and guide |
| --- | --- |
| URLs are metadata and never retrieved | Newly authorized runs can retrieve supported public sources, with bounded access and recorded failures. Saving or previewing a case does not retrieve them. See [Evidence processing](EVIDENCE_PROCESSING.md). |
| Reviewers only receive the first 200 table rows | Complete accepted tables remain retained. Selected context and bounded exact queries expose relevant records with explicit limits. See [Evidence processing](EVIDENCE_PROCESSING.md). |
| Prompt-first entry forwards to a preparation wizard | The unified composer saves a real case and immutable revision. Image-first entry also supports an optional question. See [Workflow](PRODUCT_WORKFLOWS.md). |
| XLSX selection or a UI panel establishes scientific support | XLSX is currently unavailable. Blind Optics and scientific source/statistical verification remain unavailable. See [Scientific scope](SCIENTIFIC_SCOPE.md). |
| Provider settings belong to every researcher | Shared provider configuration requires server-authorized operator access. See [Development](DEVELOPMENT.md) and [API](API.md). |
| PostgreSQL infrastructure tests establish hosted execution | Current HTTP execution uses local SQLite/private files and one threaded process. Isolated PostgreSQL infrastructure remains separate. See [Architecture](ARCHITECTURE.md). |
| A historical tool-availability statement describes every environment | Earlier reports retain the tools available for their own checks. Discover tools in the current session and record actual use. See [Development](DEVELOPMENT.md). |

All 24 scientific/operating gates remain OPEN in the [gate register](designs/backend-completion/TECHNICAL_PLAN_GATES.md). Scoped local implementation does not establish hosted readiness, scientific validation, confirmed detection accuracy or owner acceptance. Legacy and local ownership must not be silently assigned to new accounts.

## Preservation and organization

The [archive index](archive/README.md) separates earlier technical guides, design passes and verification evidence from the active reading path. Old top-level report paths remain short pointers for existing references. Runtime prompts stay beside the backend code because they are executable research instructions with per-attempt snapshots. Frozen Goldfish reviews, the Ember investigation, scientific drafts and approval histories remain in their existing directories.

The [2026-11-07 consolidation record](archive/2026-11-08/DOCUMENTATION_MAP.md) preserves the earlier review scope, conflict inventory and incremental history. The [2026-11-08 archive manifest](archive/2026-11-08/manifest.json) records original/archive paths and hashes. Only relative Markdown link destinations were rebased in archived records. No historical verification claim was refreshed by moving it.

Remaining decisions include scientific procedure acceptance, Blind Optics, XLSX semantics, historical source identity, hosted identity/team roles, durable execution cutover, retention/deletion, quotas, coordinated hosted recovery and pilot approval. Use the [design index](designs/backend-completion/README.md) to locate their decision records.
