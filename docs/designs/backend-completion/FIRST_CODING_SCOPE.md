# EvidenceTwin V1 — First coding scope and readiness decisions

**Status: Recommended for owner approval.** Updated 2026-11-06. All **24 gates remain OPEN**. This records the owner's latest pre-implementation direction. It authorizes focused technical refinement and implementation planning, not production coding, deployment, scientific capability enablement or pilot use. Broad design expansion remains stopped.

## Decisions incorporated

PostgreSQL is selected as the V1 database engine for this planning baseline, superseding the earlier candidate-only position. Development and hosted testing must use PostgreSQL to exercise real transaction/concurrency behavior. Managed provider, hosting region, deployment configuration, supported engine version and database driver/migration tooling remain open. Engine selection alone does not close D02.

Job and Execution Attempt must have separate state machines. Retain existing proposed states where applicable; do not reuse scientific check-execution states as job states. Define every permitted transition and reject unlisted transitions. The inspected publication documents leave exact legal job/attempt transitions open; a complete enumerated transition table still needs reconciliation before implementation approval. No new state set is silently selected here.

Conditional publication must validate current attempt identity, monotonic fencing epoch, valid lease ownership using database time, cancellation/terminal state, exact evidence snapshot/manifest, pinned scientific policy/configuration, authorization, predecessor and scoped idempotency. Persist validated results and their accepted artifact relations atomically in short transactions. Never hold transactions during scientific or external calls. Completed steps and outputs remain durable; reuse requires exact dependency/version validation, not merely a matching step name.

## Development-testing defaults only

| Setting | Value |
| --- | --- |
| Lease duration | 30 seconds |
| Heartbeat interval | 5 seconds |
| Heartbeat operation timeout | 2 seconds |
| Consecutive missed-heartbeat threshold | 2 |
| Queue polling interval | Configurable within 1–3 seconds; exact initial selection/scheduling remains to be specified |
| Maximum execution attempts | 3 total, including the initial attempt |
| Retry base delay | 2 seconds |
| Retry maximum delay | 15 seconds |
| Retry strategy | Exponential backoff with full jitter |

These are development settings, not validated pilot/production settings or performance promises. The heartbeat timeout's precise operation coverage and the action at the missed threshold require explicit definition. Missed heartbeats indicate loss of contact; they must not themselves prove lease expiry or provider-call completion. Database time determines lease eligibility. A worker losing renewal certainty must stop launching new work and cannot publish without satisfying current lease/fence guards.

Specify the retry-index convention and exact jitter bounds before implementation. Apply retries only to approved transient failures; an uncertain paid request requires reconciliation rather than automatic replacement. Lease recovery must preserve external-call/permit settlement records.

Existing shared configurable caps remain: two executing analyses, one LLM request per analysis and two global requests. Multiple worker processes must share enforcement rather than multiply capacity.

## First implementation scope, after separate coding authorization

1. PostgreSQL migrations and explicit repositories for jobs, attempts, queue entries, completed steps, publication records, audit and shared concurrency controls. Preserve existing local data; migration/cutover is a separate approval.
2. Atomic submission, atomic claiming, leases/heartbeats, monotonic fencing and guarded step/result publication.
3. Bounded retries, cooperative cancellation, recovery and explicit uncertain-provider reconciliation records. No blind replay or premature permit release.
4. Configurable development settings and independently runnable workers, preserving the existing Flask/Core boundary.
5. Structural and concurrency tests using controlled test tasks, plus startup and recovery instructions. No live paid provider call or scientific verification is required to test this infrastructure.

Excluded: scientific calculations, source verification, agent/prompt changes, claim-verdict implementation, authentication implementation, cloud deployment and capability enablement.

## Required test evidence — planned, not executed

| Scenario | Required observation |
| --- | --- |
| Concurrent claims | One authoritative owner per attempt; global capacity holds across worker processes. |
| Worker crash and restart | Queue/steps survive; recovery preserves completed work and external-call uncertainty. |
| Lease expiry and stale worker | Database-time lease/fence guards reject renewal/publication by obsolete ownership. |
| Cancellation race | Only permitted atomic ordering commits; cancellation cannot be undone by a late result. |
| Duplicate publication/lost acknowledgement | Equivalent replay does not duplicate results; conflicting reuse is rejected. |
| Revision/configuration mismatch | Stale evidence, policy, manifest or execution configuration cannot publish. |
| Retry and recovery | At most three total attempts under development settings; only eligible failures retry; uncertain paid calls do not replay automatically. |
| Durable outputs | Accepted completed-step outputs persist, while staged/rejected artifacts never appear as accepted results. |

## Remaining bounded planning work

Produce the separate Job/Attempt transition tables and write-path guard mapping; define lease renewal/missed-heartbeat behavior, recovery eligibility, retry indexing/jitter and reconciliation actions; identify concrete implementation files and PostgreSQL test setup. Resolve only decisions needed for this scope. Do not expand scientific design or close gates through this document.

The [gate register](TECHNICAL_PLAN_GATES.md) remains authoritative for open requirements. The [guard schema proposal](PUBLICATION_GUARD_SCHEMA_PROPOSAL.md) remains a proposal; this engine/default selection does not approve every candidate schema field.

**Bounded lifecycle refinement submitted:** the [separate Job and Execution Attempt tables](JOB_ATTEMPT_TRANSITIONS_DRAFT.md) propose explicit allowed edges, actors, guards, terminal behavior, recovery and cross-state invariants. Both tables received owner section approval for planning on 2026-11-06; implementation remains unauthorized. Development defaults are unchanged, status remains Recommended for owner approval, and all 24 gates remain OPEN.

**Next bounded section:** [lease, retry and reconciliation rules](LEASE_RETRY_RECONCILIATION_DRAFT.md) refine the approved transition tables while preserving all development defaults. This new section awaits review; all 24 gates remain OPEN.

**Implementation mapping submitted:** lease/retry/reconciliation received owner section approval for planning on 2026-11-06. The [first implementation file/test map](FIRST_IMPLEMENTATION_FILE_MAP.md) is submitted for review; existing runtime/cutover remains outside the increment, implementation dependencies remain explicit, and no production coding is authorized. Status remains Recommended for owner approval and all 24 gates remain OPEN.

**Tooling choice pending:** owner section approval of the file/test map is recorded. The [PostgreSQL tooling comparison](POSTGRESQL_TOOLING_OPTIONS.md) presents two unselected access/migration combinations and their conditional file changes. No dependency, transaction implementation, production code or gate closure is selected by this comparison. Status remains Recommended for owner approval; all 24 gates remain OPEN.

**Core tooling direction selected:** owner selected SQLAlchemy Core exclusively, Psycopg 3 and reviewed Alembic migrations for refinement. ORM/Session/relationship persistence and automatic production schema creation are excluded. The [repository/transaction plan](CORE_TRANSACTION_PLAN_DRAFT.md) is submitted for review; concrete SQL/isolation/constraints remain open. No implementation or gate closure is authorized; status remains Recommended for owner approval and all 24 gates remain OPEN.

**Transaction-plan section approval:** Owner planning approval recorded on 2026-11-06. The [short-transaction consistency comparison](TRANSACTION_CONSISTENCY_OPTIONS.md) presents Read Committed versus Serializable with explicit shared guard participation in both; neither is selected. No production code, deployment, enablement or gate closure is authorized. Status remains Recommended for owner approval; all 24 gates remain OPEN.

**Read Committed selected:** owner selects Read Committed as V1 default with conditional guards, explicit short row locks and appropriate SKIP LOCKED claims. The [metadata/statement map](EXECUTION_SCHEMA_STATEMENT_MAP.md) records assistant recommendations with rationale/trade-offs. Future routine technical recommendations do not require A/B/C owner selection; owner-specific commitments still do. Mandatory coding-readiness notification and explicit coding authorization remain required. Status remains Recommended for owner approval; all 24 gates remain OPEN.

## Current readiness package — 2026-11-06

The remaining bounded preparation is consolidated in the [Coding Readiness Report](CODING_READINESS_REPORT.md), [concrete schema/SQL review](EXECUTION_POSTGRESQL_SCHEMA_REVIEW.md), [dependency compatibility review](DEPENDENCY_COMPATIBILITY_REVIEW.md) and [test environment/EX01–EX46 specification](EXECUTION_TEST_SPECIFICATION.md). These supersede earlier statements that routine tooling/isolation/schema/test defaults are still awaiting A/B/C selection. The concrete additions are assistant recommendations, not silently approved decisions. Owner-approved architecture and development defaults are preserved.

Preparation for the isolated execution-infrastructure increment is ready for coding-scope review; actual SQL/migrations/dependency/runtime/concurrency validation is explicitly unexecuted. All 24 gates remain OPEN and status remains Recommended for owner approval. No production code/migration/dependency/service changes are authorized without the separate coding-stage notification and explicit owner authorization.
