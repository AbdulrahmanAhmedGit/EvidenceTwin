# EvidenceTwin Council

A bilingual React/TypeScript/Vite + Flask research workspace. Save a scientific question and supporting files as a real case, preserve evidence revisions, inspect supported tables, and explicitly authorize an exploratory Council review when an operator has configured a provider. Case saving does not require a provider.

The current runtime is local SQLite/private files with a single-process threaded worker. Optional invite-only accounts provide server-side ownership boundaries. This is not the hosted scientific verification pilot: all 24 scientific/operating gates remain OPEN, and no hosted deployment is claimed.

Start with the [documentation map](docs/DOCUMENTATION_MAP.md), [development setup](docs/DEVELOPMENT.md), [researcher workflow](docs/PRODUCT_WORKFLOWS.md), [API](docs/API.md) and [scientific scope](docs/SCIENTIFIC_SCOPE.md). The approved requirements remain [concepts_brief.md](concepts_brief.md); [DESIGN.md](DESIGN.md) captures the implemented visual system.

For local development, start Flask from `backend/` and Vite from `frontend/` using the commands in the development guide. Accounts-disabled mode must stay loopback. Never place credentials in `VITE_*` values. Read [deployment and rollback](docs/DEPLOYMENT_ROLLBACK.md) before changing runtime or account modes.

Historical verification records retain their dates and scope. Current focused checks and browser evidence are recorded under `output/transformation/`; neither compilation nor fixture screenshots establish scientific validation or owner acceptance. Official artwork remains unchanged under `frontend/public/brand/`.

See the [implementation handoff and manual acceptance checklist](output/transformation/IMPLEMENTATION_REPORT.md) for this transformation's exact changes, checks, documentation archive and remaining blockers.
