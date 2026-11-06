# EvidenceTwin V1 — Coding Readiness Report

**Status: Recommended for owner approval.** Prepared 2026-11-06. All **24 existing gates remain OPEN**. **Ready for owner review and explicit authorization of the bounded execution-infrastructure coding stage.** This is not readiness of the whole backend for deployment, scientific capability enablement or pilot use. No implementation authorization is inferred from design approvals.

## 1. Completed design deliverables and decisions

The preparation tasks are complete for the isolated first increment; there are no unselected fundamental architectural decisions within that scope. Assistant recommendations below remain recommendations until the owner reviews this scope; they do not become final decisions through documentation.

- [First coding scope](FIRST_CODING_SCOPE.md) and [exact file/test mapping](FIRST_IMPLEMENTATION_FILE_MAP.md).
- [Job and Attempt tables](JOB_ATTEMPT_TRANSITIONS_DRAFT.md): 19 Job and eight Attempt edges, actors, guards, terminality, invalid transitions, recovery and paired invariants; owner planning approval recorded.
- [Lease/retry/reconciliation rules](LEASE_RETRY_RECONCILIATION_DRAFT.md): owner planning approval recorded; development defaults preserved.
- [Core transaction contract](CORE_TRANSACTION_PLAN_DRAFT.md): owner planning approval recorded; Core-only/Psycopg 3/Alembic and Read Committed are owner-selected refinement directions.
- [Concrete PostgreSQL schema and statement review](EXECUTION_POSTGRESQL_SCHEMA_REVIEW.md): 16-table schema, composite identities, unique/partial indexes, SQL templates, lock ordering, admission/fairness, time semantics, idempotency, database retry policy and security review.
- [Dependency compatibility findings](DEPENDENCY_COMPATIBILITY_REVIEW.md): official package metadata and documentation; no installation or runtime compatibility claim.
- [PostgreSQL test environment and acceptance matrix](EXECUTION_TEST_SPECIFICATION.md): isolated server, roles, process crash/recovery harness and EX01–EX46, all unexecuted.

Standing instructions are incorporated: recommend routine decisions with rationale/trade-offs, escalate only owner-specific or irreversible commitments, notify coding readiness with concrete scope, and wait for explicit coding authorization.

## 2. Final proposed schema and repository boundaries

Propose qualified schema et_execution with tables: control, dispatch_accounts, guards, snapshots, jobs, attempts, queue_entries, operations, publications, steps, artifacts, publication_artifacts, capacity_scopes, external_operations, reservations and audit_events. The complete column/type/FK/CHECK/index proposals and conditional SQL are in the schema review. Core metadata is centralized; Alembic revisions, not startup create_all, evolve it.

Responsibilities: contracts/transitions validate complete internal candidates; database owns bounded Core connections/transactions; repository owns atomic persistence; capacity owns shared reservations; recovery owns guarded retirement/retry/reconciliation; supervisor proves local process stop; worker orchestrates bounded task execution without embedding scientific policy in SQL. Immutable input/configuration and validation/authorization/artifact interfaces are explicit and fail closed when absent.

The first increment has no live paid/scientific task adapter or new HTTP endpoint. Controlled tasks exist only in tests. Production CLI without supported configured tasks reports unavailable and does not claim successful work. Existing local Flask/SQLite uploads/settings/Workflow, frontend, prompts and provider transports remain unchanged and are not silently migrated or rerouted.

## 3. Lifecycle and immutable output guarantees

Job states: queued, running, retry_wait, reconciliation_required, cancellation_requested, succeeded, failed, cancelled. Attempt states: pending, running, cancellation_requested, succeeded, failed, abandoned, cancelled. All unlisted transitions reject; terminal jobs/attempts do not reopen. A researcher rerun would create a separate linked job, not reset attempt history.

At most one executable attempt per job is enforced through a partial unique index; exact required Job/Attempt/queue relations are validated and committed together. Replacement attempts preserve accepted steps and require same-snapshot dependency validation for reuse. Pending claims do not become ownership until committed. A successful workflow is not scientific verification or confirmation that a claim is true.

## 4. Transaction, publication and recovery guarantees proposed

Read Committed is the default, with atomic conditional writes, explicit short row locks and appropriate FOR UPDATE SKIP LOCKED queue claims. Permission/revision/evidence/configuration writers participate in the guard protocol. Cross-row invariants are enforced by composite FKs, uniqueness and reviewed transactional validation; Read Committed alone is not considered sufficient.

Publication binds exact job/state, active attempt/worker, monotonic fencing epoch, database-time lease, pinned analysis/evidence/manifest/classification/policy/configuration, current authority, validated complete candidate, artifact eligibility and operation/predecessor identity. Validated result/accepted artifact links, paired transitions and required operation/audit relations commit atomically. Stale success/error/checkpoint cannot overwrite newer/terminal state.

No database transaction includes source retrieval, uploads, process execution or LLM calls. Database-only retries are three total executions for known rolled-back 40P01/40001, with separate subsecond jitter/deadline; heartbeat uses one transaction per scheduled operation. Unknown COMMIT/class-08 failures reconcile durable operation identity before repeating mutation. Never replay paid work from a database retry.

Capacity is separate from logical state. Local process exit/isolation proof gates analysis reservation release; unresolved provider calls retain per-analysis/global/provider permits after lease loss/cancellation. The same-host supervisor recommendation is explicit; remote automatic kill/failover is not claimed. Uncertain external outcomes require attributable reconciliation/replacement authorization and cannot bypass concurrency/spend limits.

## 5. Dependency compatibility findings

Recommend Python 3.14.4; PostgreSQL 18.6; existing Flask 3.1.3 and pytest 9.2.0; new SQLAlchemy 2.1.8, psycopg[binary] 3.3.8 and Alembic 1.20.1, with Mako 1.4.3 as migration transitive. Exact resolver/lock results must be checked during authorized implementation, retaining existing unrelated pins where compatible. No greenlet/async extras, ORM, Flask-SQLAlchemy or second Psycopg pool.

Research observed compatible Requires-Python metadata, matching driver/binary pins, CPython-3.14 Linux wheels and 15 compatible active direct dependency edges. The installed backend interpreter was read-only verified as 3.14.4. The shell inspection interpreter is 3.15.0 and must not accidentally be used for backend dependency resolution.

This is metadata-level feasibility, not a successful full resolver, import, ABI, migration or live database test. Those checks are deliberately deferred because installation and migration execution are prohibited before coding authorization. Recheck current security/patch notices when authorized; do not invent image digests or wheel lock hashes.

## 6. Test infrastructure and acceptance coverage

Recommend an explicitly invoked disposable local PostgreSQL 18.6 test profile, restricted to loopback, random per-run credentials, no production mounts or networks and per-case et_test_* databases. Separate migration administrator and DML-only worker roles. Fixture safeguards reject real/unknown DSNs and validate recorded teardown identities. No test service starts during import/collection or design preparation.

EX01–EX46 cover migrations/constraints, all lifecycle pairs, atomic submission, concurrent claims, fairness/admission, shared limits, worker crash, durable steps, lease/renewal/recovery races, cancellation, stale publication, idempotency, uncertain calls, pool/timeouts, authorization/revocation/deletion, fail-closed adapters and existing runtime regressions. Use actual PostgreSQL with independent worker processes and controlled barriers. No scientific, provider, security-isolation or throughput claim follows from fixture success alone.

Existing 150 overlapping scientific contract rows remain unchanged and unexecuted; the new 46 EX rows are infrastructure specifications, not passed tests. No live-provider/scientific acceptance tests were performed. Required integration CI cannot report skipped PostgreSQL tests as success.

## 7. Design risks and owner-dependent decisions

| Item | Effect on this coding increment | Effect beyond it |
| --- | --- | --- |
| Explicit coding authorization and approval of this bounded recommended design | Required before any runtime/migration/dependency work. | Does not close gates or authorize deployment. |
| Local test provisioning | Scope requests permission to provision only an isolated local test service after authorization, or use a supplied disposable PostgreSQL. If no supported local runner is available, report blocker; do not alter host services silently. | No cloud vendor/region commitment. |
| All-writer guard discipline and transaction contention | Mandatory implementation tests; no architectural choice left implicit. | Hosted application/auth/storage bridges must join the same protocol before use. |
| Real authentication/ownership, artifact readiness and scientific validators | Production interfaces reject while missing; tests provide explicit controlled implementations. | Blocks integrated production submissions/results until independently implemented/accepted. |
| Actual provider settlement, budgets and processing consent | No paid-provider adapter/calls in this increment. | Owner provider configuration, budget/currency and processing/privacy approval required. |
| Local process-stop proof versus remote host loss | Test same-host supervisor; hold permits on uncertain loss. | Hosting orchestration/remote recovery must supply reviewed proof. |
| Actual dependency resolution, SQL syntax/plans and race outcomes | First coding-stage verification obligations; currently unproven. Stop if fundamental incompatibility appears. | No performance/capacity guarantee before representative load measurements. |
| Retention, deletion, backups, RPO/RTO and legacy ownership import | No destructive migration/import/deletion of real data. | Explicit owner values, source rights, restore tests and cutover approval required. |

Other still-open owner deployment inputs: identity provider, managed database/storage provider, region/residency, pilot workload, production resource limits, support authority and legacy retirement date. They do not block this deliberately isolated infrastructure increment because no real accounts/research data/paid work/hosted deployment are admitted through it.

No missing evidence is treated as false science. Partially Supported remains unresolved. Historical/current evidence remain separate. Source verification/statistical procedures, Neutral Twin, Council independence/scientific acceptance, benchmark rubric and MCP remain outside this coding authority request.

## 8. Proposed implementation phases and dependencies

| Phase | Bounded work | Depends on | Exit evidence |
| --- | --- | --- | --- |
| 1 — Foundation | Resolve/install approved dependency set; Core metadata/internal contracts/settings; explicit reviewed migration and disposable PostgreSQL setup. | Explicit coding authority; safe local test environment. | Import/resolver check, migration/role/constraint tests; no current-runtime change. |
| 2 — Repository | Atomic submission/claim, lifecycle validator, idempotency, ordered guards, database-time leases and admission/fairness. | Phase 1. | Actual PostgreSQL multiprocess claim/transition/race tests. |
| 3 — Execution controls | Shared capacity, worker/supervisor heartbeat, cancellation, bounded retry/recovery and uncertainty interfaces. | Phase 2. | Process crash/expiry/restart tests, retained permits, three-attempt limit. |
| 4 — Publication integrity | Immutable steps/output links, guarded final publication, fail-closed adapters, rejection audit and unknown-commit reconciliation. | Phases 2–3. | Stale/duplicate/cancellation/revocation/artifact tests; no scientific adapter enabled. |
| 5 — Verification/handoff | Full new/existing backend suite, dependency inspection, SQL/privilege review and updated integration/runbooks. | Phases 1–4. | Explicit EX01–EX46 traceability/results/limitations and owner review. |

These are coding subphases of the same bounded infrastructure increment. Successful completion does not switch frontend traffic, migrate existing data, close gates or deploy. A later integrated API/auth/storage bridge requires its own scope and authority.

## 9. Exact expected file changes

Create:

- backend/evidencetwin_backend/execution/__init__.py — import-safe interfaces.
- backend/evidencetwin_backend/execution/contracts.py — typed internal commands/records and explicit adapter contracts.
- backend/evidencetwin_backend/execution/transitions.py — complete paired lifecycle validation.
- backend/evidencetwin_backend/execution/tables.py — centralized Core metadata.
- backend/evidencetwin_backend/execution/database.py — Core Engine/Connection, short transactions/timeouts/retries.
- backend/evidencetwin_backend/execution/repository.py — atomic guarded operations/idempotency/audit.
- backend/evidencetwin_backend/execution/capacity.py — shared reservations and safe release.
- backend/evidencetwin_backend/execution/recovery.py — attempts/leases/uncertain-call control.
- backend/evidencetwin_backend/execution/supervisor.py — same-host child lifecycle/stop proof.
- backend/evidencetwin_backend/execution/worker.py — explicit standalone worker entry point, no enabled scientific task.
- backend/evidencetwin_backend/execution/settings.py — validated development-only configuration.
- backend/alembic.ini — no embedded DSN/secrets.
- backend/migrations/env.py — explicit migration connection/metadata, no Flask startup side effects.
- backend/migrations/script.py.mako — reviewed revision template.
- backend/migrations/versions/0001_execution.py — initial execution schema, named constraints/indexes and two control seeds.
- backend/compose.execution-test.yaml — opt-in disposable PostgreSQL test service only.
- backend/tests/execution/conftest.py — safe isolated DB/role/process fixtures.
- backend/tests/execution/helpers.py — test-only tasks/provider/artifact/authority/validation fixtures.
- backend/tests/execution/test_schema_migrations.py — DDL/constraints/privileges.
- backend/tests/execution/test_transitions.py — enumerated state/actor/guard matrix.
- backend/tests/execution/test_submission_claims.py — admission/idempotency/claim/fairness.
- backend/tests/execution/test_leases_recovery.py — ownership/time/crash/restart.
- backend/tests/execution/test_capacity.py — cross-process capacity/reservations.
- backend/tests/execution/test_publication.py — guarded result/step/artifact publication and replay.
- backend/tests/execution/test_retry_reconciliation.py — bounded retries and uncertain calls.
- backend/tests/execution/test_steps_cancellation.py — durable step reuse and logical cancellation.
- backend/tests/execution/test_security.py — owner isolation/guard/revocation/fail-closed behavior.
- backend/tests/execution/test_timeouts.py — deadline/lock/commit-uncertainty behavior.

Modify:

- backend/pyproject.toml — approved new dependencies, execution-test marker and worker entry point.
- backend/requirements.lock — exact authorized resolver result, preserving unrelated pins where possible.
- backend/README.md — setup, migration, worker/test/safety instructions.
- docs/INTEGRATION_GUIDE.md — actual boundary and still-missing HTTP/auth/storage bridge.
- BACKEND_IMPLEMENTATION_GUIDE.md — infrastructure handoff and scientific owner interfaces.

No production files are deleted. Existing Flask factory/config, local runtime/store/workflow/provider/transports/prompts, frontend, real data/instance files and secrets are not modified. This inventory supersedes older provisional SQL migration/file-map wording. If another production file becomes necessary, report the reason and obtain scope approval before changing it.

## 10. Gates and stopping point

All D01–D09, E01–E07 and P01–P08 remain OPEN. D02 now has a concrete recommended execution design, not a closing approval or passing implementation evidence. Scientific decision/enablement gates prevent claims of verified science. E06/E07 block representing real provider/integrated browser capabilities as accepted. P01–P08 block private pilot use until actual identity isolation, capacity, spend, privacy, recovery, operations, scientific acceptance and transition requirements pass their own reviews.

**CODING STAGE READY FOR SCOPE REVIEW — NOT AUTHORIZED.** The recommended isolated infrastructure scope can proceed to implementation planning without selecting another fundamental architecture mid-build. Its precise runtime guarantees must still be earned by implementation/tests. Owner must explicitly authorize production-code/migration/dependency modifications and isolated local test provisioning before any of them begin. No deployment, cloud provisioning, data cutover, paid requests or scientific capability enablement is requested.

## Evidence and review limitations

Read-only source inspection, official dependency metadata/specifier checks and manual schema/SQL/security/consistency review were performed. This is an author self-review, not an independent Goldfish/domain audit. Document structure/link/inventory checks are performed separately; they are not migration/runtime/scientific tests. Protected backend source/dependency hashes are checked for unchanged content at handoff. No production code, migration files, implementation dependencies or services were created/modified/installed/run.

Sources and version evidence are linked in the dependency and SQL reviews. Recommendations and additional development settings remain Recommended for owner approval. STOP at this report pending explicit coding authorization.

### Additional review findings closed as recommendations

The final self-review added explicit snapshot/command schemas, adapter input/output/default contracts, typed persistence outcomes and safe error rules. It also recorded the physical-send/cancellation limit as a later real-provider integration blocker, not an infrastructure guarantee. This increment keeps all real provider calls disabled and does not pretend that a database transaction can cancel a remote operation atomically.

Recommended file inventory is **28 new files and five existing-file modifications** after coding authorization. Their create/modify status was checked against the live repository; none of the proposed implementation files exists yet. The source/dependency preservation check and document checks are recorded at handoff; they are not execution acceptance evidence.

### Final document and preservation checks

At handoff, ten new/updated design documents passed local-link, formatting and status checks. Structural inventory checks confirmed 16 schema table definitions, all 46 EX IDs exactly once and the unchanged 24-gate register. SHA-256 comparison confirmed all 44 inspected backend source/dependency files unchanged; no execution package or migration directory was created. These checks validate documentation/preservation only. SQL syntax, migrations, runtime integration, process races and scientific capabilities remain unexecuted.

The final review also clarified that authorized equivalent acknowledgement replay is resolved before applying fresh-worker lease/state guards; it returns historical outcome only and cannot mutate current state. This closes the lost-acknowledgement/terminal-state ambiguity without weakening new publication guards.
