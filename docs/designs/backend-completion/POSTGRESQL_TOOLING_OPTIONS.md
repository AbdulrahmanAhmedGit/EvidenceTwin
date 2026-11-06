# EvidenceTwin V1 — PostgreSQL access and migration tooling choice

**Status: Recommended for owner approval.** Date: 2026-11-06. All **24 gates remain OPEN**. The first implementation file/test mapping has received owner section approval for planning. The owner selected B — SQLAlchemy Core + Psycopg 3 + Alembic for refinement on 2026-11-06. The comparison below is retained as decision history; A is not the selected runtime direction. No dependency installation, implementation, deployment or capability enablement is authorized.

## Decision to make

PostgreSQL is already selected. Choose the application access layer and migration approach together. Both options below use synchronous operations inside short transactions, separately runnable workers, typed internal contracts and actual PostgreSQL concurrency tests. Neither requires an ORM, new backend framework, broker or cloud vendor.

| | A — Direct Psycopg access; Alembic migrations | B — SQLAlchemy Core over Psycopg; Alembic migrations |
| --- | --- | --- |
| Mechanism | Runtime repository uses parameterized PostgreSQL SQL through Psycopg and explicit transaction scopes. Alembic uses its SQLAlchemy connection only for versioned schema migration. | Runtime repository uses SQLAlchemy Core Engine/Connection with Psycopg as driver. PostgreSQL-specific conditional statements remain explicit where required. Alembic manages revisions. |
| Schema ownership | Reviewed migrations own the physical schema; internal typed contracts remain separate. No migration autogeneration is assumed. | Core metadata can describe tables/constraints, with reviewed migrations as the authoritative evolution history. Generated migration suggestions, if used later, still require review. |
| Pool ownership | Psycopg pooling, if selected, is the sole runtime pool. Alembic's migration connection has a separate lifecycle. | SQLAlchemy Engine pooling is the sole runtime pool; do not add a second Psycopg pool below it. |
| Trade-off | Direct visibility of SQL and transaction boundaries; more manual query/result mapping and discipline to keep schema/contracts aligned. Alembic still introduces SQLAlchemy as a tooling dependency. | Shared schema/query abstractions and managed connection lifecycle; adds application-level SQLAlchemy concepts and requires reviewing transaction behavior and generated SQL. |
| Failure conditions | Unreviewed SQL, ad-hoc commits, inconsistent row mappings or leaked implicit transactions can defeat the guarded repository. | Hidden implicit transactions, ORM-style assumptions, or treating Core abstractions as automatic race protection can defeat the guarded repository. |
| Fit | When the owner wants the queue repository expressed primarily as explicit PostgreSQL statements. | When the owner wants Core table/query abstractions for future application persistence as well as the execution repository. |

These trade-offs and fit statements are design judgments; they are not measured performance findings. Neither option makes all-writer guard coverage, ownership checks, lease validity or provider settlement automatic. No isolation level, claim statement or PostgreSQL server version is selected here.

## File-map impact of either choice

Replace the provisional standalone `backend/migrations/0001_execution.sql` allocation with reviewed Alembic files: `backend/alembic.ini`, `backend/migrations/env.py`, `backend/migrations/script.py.mako` and `backend/migrations/versions/0001_execution.py`. Existing environment secrets must not be written into migration configuration. No migration runs at import or worker startup by surprise.

Option A keeps runtime SQL inside the repository/database modules already mapped. Option B additionally proposes `backend/evidencetwin_backend/execution/tables.py` for Core metadata; this is a specific conditional addition to the approved file map, subject to the tooling selection. No production files are created by documenting these paths.

Exact stable compatible package versions, installation variant, supported Python/PostgreSQL versions and lock updates must be checked before authorized installation. The Psycopg documentation source consulted below identifies itself as a development documentation build; that is not a recommendation to install a development release.

## Primary documentation consulted

- [Psycopg transaction management](https://www.psycopg.org/psycopg3/docs/basic/transactions.html): implicit transaction behavior, explicit transaction scopes and commit/rollback responsibilities.
- [SQLAlchemy Core connections and transactions](https://docs.sqlalchemy.org/en/20/core/connections.html): Engine/Connection lifecycle and transaction interfaces. This is a 2.0 documentation reference, not selection of that release line.
- [Alembic documentation](https://alembic.sqlalchemy.org/en/latest/): migration tooling built for SQLAlchemy, including revision environments and reviewed migration operations.

B is selected for refinement only. SQLAlchemy Core is the exclusive runtime database abstraction, with centralized metadata and explicit repositories; Psycopg 3 is the driver. ORM, mapped entities, Sessions, lazy loading and relationship persistence are excluded. Core expressions are the default, with reviewed parameterized PostgreSQL-specific SQL permitted for specialized operations through the Core connection boundary. Reviewed Alembic migrations are explicit administrative operations; no automatic production schema creation. Scientific and business logic remain outside persistence. Coding still requires separate authority. All existing architecture decisions and development defaults remain unchanged.
