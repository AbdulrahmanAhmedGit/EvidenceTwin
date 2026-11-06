# EvidenceTwin V1 — First implementation file and test mapping

**Status: Recommended for owner approval.** Date: 2026-11-06. This bounded section follows planning approval of the [transition tables](JOB_ATTEMPT_TRANSITIONS_DRAFT.md) and [lease/retry/reconciliation rules](LEASE_RETRY_RECONCILIATION_DRAFT.md). All **24 gates remain OPEN**. This is an implementation proposal, not authorization to create the production files listed below. Broad scientific design expansion remains stopped.

## 1. Existing code boundary inspected

`backend/evidencetwin_backend/services/runtime.py` currently creates Store, AISettings, provider and Workflow in the Flask process. `services/store.py` is the local persistence boundary. `services/workflow.py` owns local scheduling, recovery, cancellation and provider calls. The factory installs that runtime when configured. Existing tests explicitly exercise either contract-only or local-runtime behavior.

The first increment should add and test the durable execution infrastructure without switching current HTTP submissions to it. Preserve the local database, uploads, settings, prompts, provider transports and scientific behavior. No data import, hosted cutover or automatic rerouting is included. A separately launched worker remains within the approved Flask/independent-Core architecture; controlled tasks exist only in tests, never as production scientific results.

## 2. Proposed production file changes after separate implementation authority

Paths are relative to the repository root. All new paths are proposed file allocations, not a new framework choice.

| File | Action | Responsibility |
| --- | --- | --- |
| `backend/evidencetwin_backend/execution/__init__.py` | Create | Public internal execution interfaces, with no worker startup or database writes on import. |
| `backend/evidencetwin_backend/execution/contracts.py` | Create | Internal typed job, attempt, transition, pinned-input, external-operation and publication records; distinct from public API DTOs and scientific observations. |
| `backend/evidencetwin_backend/execution/transitions.py` | Create | Central whole-record validation and approved Job/Attempt edge/actor/guard mapping; reject every unlisted edge. |
| `backend/evidencetwin_backend/execution/database.py` | Create | Explicit PostgreSQL connection/short-transaction boundary, safe rollback and database-time access; no global process lock as concurrency protection. |
| `backend/evidencetwin_backend/execution/repository.py` | Create | Atomic submission/claim, attempt allocation, heartbeat, guarded transitions/publication, scoped operation records and rejection audit. |
| `backend/evidencetwin_backend/execution/capacity.py` | Create | Shared analysis/per-analysis/provider permits and reservations; conservative release and crash reconciliation. |
| `backend/evidencetwin_backend/execution/recovery.py` | Create | Lease retirement, retry deadlines, cancellation finalization and explicit uncertain-call reconciliation. No blind replay. |
| `backend/evidencetwin_backend/execution/worker.py` | Create | Independently runnable worker loop, heartbeat lifecycle and bounded task interface. No scientific or paid-provider task enabled by default. Unknown/unconfigured task types must not claim successful work. |
| `backend/evidencetwin_backend/execution/settings.py` | Create | Validated execution settings, exact development defaults and explicit database configuration; no secret logging. |
| `backend/migrations/versions/0001_execution.py` | Create | Versioned schema proposal for queue/job/attempt/step/publication/audit/permit/external-operation records and integrity constraints. Use reviewed Alembic revisions after the owner selection of B; no automatic production schema creation. |
| `backend/pyproject.toml` | Modify | Add only the approved PostgreSQL dependency/tooling and worker entry point; declare PostgreSQL integration-test marker. |
| `backend/requirements.lock` | Modify | Resolve and record the separately selected tested dependency set using the existing locking convention. Never hand-invent version hashes. |
| `backend/README.md` | Modify | Explain explicit worker startup, migrations, development defaults, isolated tests and limits of the increment. |
| `docs/INTEGRATION_GUIDE.md` | Modify | Document the unchanged legacy HTTP path, new internal execution boundary, required future API/auth/storage bridge and absence of automatic cutover. |
| `BACKEND_IMPLEMENTATION_GUIDE.md` | Modify | Record actual implemented infrastructure and remaining owner-owned scientific adapters, after coding/testing establishes their status. |

No existing runtime/workflow/store file, public route, frontend, prompt or scientific procedure needs modification in this increment. If implementation reveals that one is required, revise this scope for review rather than silently enlarging it. Public `/api/v1/` integration is a later bounded change after DTO/authorization/storage alignment; this increment does not pretend the frontend is already using the durable queue.

## 3. Proposed test files and observations

| File | Planned verification |
| --- | --- |
| `backend/tests/execution/conftest.py` | Dedicated disposable PostgreSQL fixture, process-safe barriers, explicit test principal/configuration and controlled task/provider simulator; never access real accounts, uploads or provider credentials. |
| `backend/tests/execution/test_transitions.py` | Enumerate all source/destination pairs, approved event/actor combinations and required failures; validate paired Job/Attempt invariants. |
| `backend/tests/execution/test_submission_claims.py` | Transaction rollback, duplicate submissions, concurrent process claims, one active owner and atomic attempt budget. |
| `backend/tests/execution/test_leases_recovery.py` | Heartbeat acknowledgement loss, expiry boundary, crash/restart, renewal versus recovery, stale epoch and safe replacement. |
| `backend/tests/execution/test_capacity.py` | Shared configurable caps across multiple processes; surviving external calls and uncertain local execution retain applicable permits. |
| `backend/tests/execution/test_publication.py` | Stale/wrong identity, pinned-revision mismatch, concurrent cancellation, duplicate/conflicting operation, lost acknowledgement and accepted-artifact visibility. |
| `backend/tests/execution/test_retry_reconciliation.py` | Persisted jitter/deadline, three total attempts, Retry-After precedence, uncertain paid operation and attributable replacement authorization. |
| `backend/tests/execution/test_steps_cancellation.py` | Durable completed outputs, exact dependency reuse checks, pending/running cancellation and controller finalization without worker cooperation. |

Existing contract/local-runtime tests must continue to pass. These new names are planned; no test has been created or executed by this document.

## 4. PostgreSQL testing boundary

Use actual PostgreSQL for repository, atomicity and multiprocess concurrency tests; SQLite and mocked transactions cannot substitute. Keep deployment/provider selection open. The exact supported server version and driver/migration tooling require review before implementation.

Tests require an explicitly supplied disposable test database and a least-privileged test role with authority only over that test namespace. Never derive a test connection from a production database setting. Isolation, cleanup and process-crash handling must be documented before destructive fixture operations are implemented. No database creation, server installation, container startup, live credentials inspection or dependency installation is authorized in this planning section.

Run the existing backend suite plus the dedicated PostgreSQL suite after implementation. CI must treat an unavailable PostgreSQL test database as missing required evidence, not a successful concurrency check. Local opt-out may report skips explicitly; it cannot satisfy acceptance. Include at least two distinct worker processes and process termination/restart, rather than only threads or sequential calls. Use barriers/observed database conditions instead of timing-only sleeps for race assertions where possible.

## 5. Remaining decisions before coding authorization

- Select PostgreSQL driver/access and migration tooling without changing the approved engine or database-backed-queue architecture.
- Approve concrete schema constraints and transaction/claim strategy, including all-writer guard participation and database-time semantics.
- Specify artifact-readiness, authorization and configuration identity interfaces used by publication. Missing required checks must reject publication; they cannot become permissive stubs.
- Define test database/version provisioning and operational proof for terminating/isolation of abandoned local execution. Do not claim a lease alone bounds actual surviving processes.
- Obtain explicit authority for this exact coding increment. Planning section approval alone does not provide it.

The next review should settle only these implementation dependencies. Scientific capabilities, auth implementation, private-object-storage provider selection, hosted migration/cutover and pilot acceptance remain outside this coding increment. No capability may be exposed as operational through infrastructure-only tests.

**Section approval:** The owner approved this file/test mapping for planning on 2026-11-06. This approval does not select unresolved dependencies, authorize production coding or close any gate. Tool-dependent migration paths may be refined after an explicit tooling choice.

**Tooling decision applied:** B — SQLAlchemy Core + Psycopg 3 + Alembic is owner-selected for refinement. Add `backend/evidencetwin_backend/execution/tables.py` for centralized Core metadata, plus `backend/alembic.ini`, `backend/migrations/env.py` and `backend/migrations/script.py.mako` for explicit reviewed migrations. Runtime access stays exclusively through Core Engine/Connection and repositories; no ORM/Session or second driver-level pool. Exact package/server versions and transaction mechanics still require review. No implementation is authorized.

## Current readiness package — 2026-11-06

The remaining bounded preparation is consolidated in the [Coding Readiness Report](CODING_READINESS_REPORT.md), [concrete schema/SQL review](EXECUTION_POSTGRESQL_SCHEMA_REVIEW.md), [dependency compatibility review](DEPENDENCY_COMPATIBILITY_REVIEW.md) and [test environment/EX01–EX46 specification](EXECUTION_TEST_SPECIFICATION.md). These supersede earlier statements that routine tooling/isolation/schema/test defaults are still awaiting A/B/C selection. The concrete additions are assistant recommendations, not silently approved decisions. Owner-approved architecture and development defaults are preserved.

Preparation for the isolated execution-infrastructure increment is ready for coding-scope review; actual SQL/migrations/dependency/runtime/concurrency validation is explicitly unexecuted. All 24 gates remain OPEN and status remains Recommended for owner approval. No production code/migration/dependency/service changes are authorized without the separate coding-stage notification and explicit owner authorization.
