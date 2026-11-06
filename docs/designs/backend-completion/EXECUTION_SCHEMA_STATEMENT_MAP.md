# EvidenceTwin V1 — Execution metadata, constraints and statement map

**Status: Recommended for owner approval.** Date: 2026-11-06. All **24 gates remain OPEN**. Read Committed is owner-selected as the V1 default, with SQLAlchemy Core exclusively, Psycopg 3 and reviewed Alembic migrations. This bounded document recommends the concrete coordination design for the first coding scope. Recommendations are not production implementation authority. No runtime files, migrations or dependencies are changed.

## 1. Recommended persistence model

Use centralized Core metadata with named constraints and explicit repositories. Recommend UUID identifiers for new internal execution entities; preserve existing external case/analysis/revision identifiers as opaque references rather than coercing them or importing local data. Use timezone-aware PostgreSQL timestamps, positive BIGINT record versions and per-job fencing epochs with explicit exhaustion rejection. Do not reuse an execution job ID or reset its fencing counter; a linked rerun has a separate immutable job identity.

| Metadata group | Required columns/relations | Recommended database enforcement |
| --- | --- | --- |
| Jobs | ID, trusted owner/case references, immutable analysis/input/policy/configuration references, lifecycle state, record version, current attempt reference, fence counter and timestamps | Primary key; positive version/nonnegative fence; state allowlist; exact same-job attempt relationship enforced by composite FK where applicable. Immutable scope cannot be patched during execution. |
| Attempts | ID, job ID, positive ordinal, lifecycle state, owner instance, fence, lease expiry, record version and failure reason | Unique job/ordinal and job/ID; one partial unique index per job for pending/running/cancellation_requested states combined; state and lease-field checks. Pending has no worker/lease; running has all ownership fields; terminal ownership cannot authorize work. |
| Queue entries | Stable job reference, pending attempt reference where eligible, eligibility deadline, enabled/terminal scheduling flags and version | Exactly one retained queue row per job; queue/attempt belongs to same job. Retain the row after execution for coordination; terminal is ineligible. Paired lifecycle validity is transactional, not a cross-table CHECK. |
| Steps and outputs | Job/attempt/step logical key, exact input/validation identity, status, immutable payload/output references and accepted publication relation | Unique accepted logical step per attempt; accepted outputs append immutable records. Reuse links identify the original step and dependency binding rather than copying a success flag. |
| Publication operations | Trusted owner/resource/action/key scope, canonical command bytes/digest/schema, outcome, publication reference and timestamps | Unique scoped operation key; command identity immutable; conflicting duplicate rejects. No upsert overwrites a prior result. |
| Publications | Job/attempt, output kind/key/revision, predecessor, validated content identity, validation/provenance/artifact manifest references | Unique final workflow publication per job and unique step publication key/revision; accepted links must reference the exact owning job/attempt. |
| Guard rows | Stable authority/resource/policy/configuration/artifact identifiers, eligibility, version and authoritative references | Primary keys and positive versions. Version changes accompany every relevant mutable fact change. Missing guard is ineligible, never implicitly allowed. |
| Capacity scopes and reservations | Scope ID/type, configured limit, active reservations, exact job/attempt/call linkage and settlement/release facts | Unique live reservation identity; nonnegative counters/limits. Counter/reservation agreement is maintained under a locked scope row. No count-then-insert race. |
| Scheduler coordination | Singleton coordination identity, per-account last-dispatch order and versioned dispatch sequence | Short claim-only scheduler lock; stable account identity and deterministic ordering. No queue/entity holder may acquire this earlier-order lock. |
| External operations | Logical request ID, original attempt/step/fence, pinned provider reference, dispatch intent, request identifier, observed outcome, settlement and reservation links | Unique logical dispatch identity; no automatic duplicate request after uncertain outcome. State is separate from terminal Job/Attempt state. |
| Audit/reconciliation history | Event ID, safe actor/action/target references, outcome, correlation and timestamps | Append-only through repository interfaces; no private payload/credential logging. Rejection history does not require a forbidden lifecycle update. |

These groups may map to several physical tables where FK/uniqueness requires it; the migration review must enumerate the final columns and constraint names before coding authorization. The partial unique index enforces at most one executable attempt, while the paired transition transaction enforces exactly one where required. PostgreSQL CHECK constraints must not be used as cross-row assertions.

No account system, scientific verdict tables, source-verification engine or production object-storage implementation is introduced here. Guard rows are an internal coordination interface with future authoritative application services, not a fake identity provider or a permissive authorization cache. In this increment unconfigured production authorizers/validators/artifact adapters reject; controlled implementations exist only in test fixtures.

## 2. Recommended coordination order

Recommend one retained queue coordination row per accepted job. Every lifecycle mutation first locks that job's queue row, including heartbeat, publication, cancellation and recovery. Claims choose eligible queue rows using FOR UPDATE SKIP LOCKED. This keeps the supported claim mechanism and subsequent lifecycle mutations in a consistent order, rather than claiming queue-first while cancellation locks the same job in reverse order.

After queue coordination, acquire only required guard/capacity/entity rows in this fixed category order, then stable identifier order within each category:

1. Authority guards, including account suspension and case/action permissions.
2. Analysis/evidence-snapshot and policy/configuration/artifact eligibility guards.
3. Shared capacity scope rows.
4. Job, attempt, external operation and step rows.
5. Operation/publication and accepted-artifact relation rows.

All existing-row locks are short and end with commit/rollback. Dependency IDs come from pinned immutable references and are revalidated after locking. Do not discover new lower-order locks after acquiring later categories. An operation affecting multiple jobs must acquire all required queue rows in stable order before proceeding, or split into independently guarded operations where that preserves semantics.

An authority/evidence/configuration revocation may update its own guard rows without acquiring job queues, but must not then acquire queue rows in that same transaction. Follow-up cancellation uses a new queue-first transaction. Therefore publication either precedes the guarded revocation or observes it and rejects. Every writer must participate; arbitrary direct table writes cannot be declared safe. Future migration/import/operator tools receive no bypass.

Trade-off: queue coordination briefly serializes a job's heartbeat and publication; shared capacity rows serialize small reservations across jobs. At the two-analysis pilot planning limit, recommend this explicit protocol over a more elaborate lock-free design. This is a design judgment, not a throughput guarantee. Keep transactions short, measure contention, and never hold a queue lock while preparing evidence or waiting for a provider.

## 3. Statement-level operation map

All statements use bound values via Core. Reviewed PostgreSQL-specific text is permitted through Core Connection where expressions obscure the guard. No generated statement is considered reviewed merely because it compiles.

| Operation | Required statement sequence and guarded result |
| --- | --- |
| Submission | Reserve idempotency scope under its unique constraint; create job, pending attempt and queue row atomically. Initial rows are created within one transaction without acquiring other jobs' locks. Collision resolves to exact authorized command comparison, never duplicate allocation. |
| Claim | Lock eligible queue candidate using FOR UPDATE SKIP LOCKED; lock required guards and capacity; load/lock job/attempt, then reevaluate queue readiness and exact pending predecessor. Conditional job/attempt updates reserve capacity, advance trusted fence and establish owner/lease. If any check fails, roll back the candidate claim. |
| Heartbeat | Lock queue and required current authority/context; conditionally update running attempt on exact owner/fence/version and database-time unexpired lease, paired with immutable heartbeat operation outcome. Duplicate acknowledgement does not renew twice. |
| Step/final publication | Prepare validated immutable payload outside transaction. Lock queue, guards and required capacity/entities; validate exact input/configuration/authority and all PG guards. Conditional predecessor update and inserts atomically establish publication, accepted artifact links, paired lifecycle state, idempotency outcome and audit. Any row-count mismatch rolls back acceptance. |
| Cancellation | Lock same queue and required authority/context; compare expected Job/Attempt states and versions, atomically set cancellation/terminal guards and queue eligibility. Cancellation cannot follow a committed successful terminal job by reopening it. |
| Recovery | Lock same queue/context/capacity/job/attempt; compare lease expiry/revocation and exact fence. Retire old attempt, preserve uncertain-call records and reservations; allocate at most one pending replacement only when G4 permits. New claim, not the old worker, allocates the next execution epoch. |
| External dispatch intent | Lock queue/context/capacity/job/call rows; check current running owner and lease, reserve per-analysis/global/provider capacity and approved spend where available, persist logical intent. Commit before the external call. No intent commit means no dispatch. Uncertain intent acknowledgement must reconcile before sending. |
| Settlement/history | Record an attributable observation under current settlement authority and original request identity; release only proven-releasable reservations under scope locks. No stale worker may use settlement to publish an active result or reopen a terminal attempt. |

The first coding increment has no live paid-provider dispatch adapter or spending policy. Its reservation/uncertainty behavior can be tested with controlled tasks only; no missing spend guard becomes default approval.

## 4. Time, fairness and idempotency recommendations

Recommend clock_timestamp() sampled after required waits and used consistently for the atomic ownership decision. Do not substitute transaction-start now() or a worker clock. Retain explicit time/fence/state predicates on conditional writes even when short locks already serialize the job. A lease valid at the protected ownership decision is not a promise of validity after commit; the worker must reconfirm before new work. Physical PostgreSQL statement shape must demonstrate the timestamp is sampled at the intended point, not hoisted before lock acquisition.

Recommend fair per-account dispatch based on a durable last-dispatch sequence, then FIFO within an account using immutable submission order. SKIP LOCKED only skips contention; it is not a fairness proof. A scheduler coordination row serializes account selection briefly: acquire it before candidate queue selection; update its dispatch ordering on successful claim only. Only claim scheduling acquires this row; operations already holding queue/entity locks must never acquire it. Capacity-blocked accounts must not prevent eligible other accounts from being considered. Strict finite-wait/starvation guarantees are not claimed without tests and admission bounds.

Recommend idempotency scope `(internal_owner, resource_identity, operation_kind, client_operation_key)`. Store normalized validated command bytes and a versioned SHA-256 digest; include pinned references, attempt/fence where appropriate and payload content identity. Equivalent replay requires exact normalized bytes/context and current response authorization, not hash equality alone. Reject non-finite/unrepresentable JSON and unknown schemas before canonicalization. Canonicalize transport metadata only; never rewrite original scientific number tokens or evidence bytes. Keep keys for the life of the corresponding execution records, subject to the still-open retention/deletion policy; do not silently expire keys and replay old work.

Recommend database-only contention retries have a separate bounded budget from scientific attempts. Defaults for such retries remain to be set in the final readiness configuration; the approved three attempts are not reused for this purpose. Unknown commit outcomes first query durable operation identity and never trigger a paid request replay.

## 5. Accepted, rejected and uncertain writes

Under the queue/guard protocol, an expected predicate rejection may commit a safe rejection operation/audit record without changing active lifecycle/publication fields. The decision must remain attributable and must not reveal unauthorized resource existence. A database exception rolls back the operation; if commit acknowledgement is uncertain, do not claim that either acceptance or rejection audit persisted. Reconcile through a fresh authorized connection.

Durable rejection recording during complete database outage cannot be guaranteed. Report uncertainty through safe operational diagnostics, preserve an opaque correlation reference and reconcile when connectivity returns; do not promise an audit row that was never committed. This limitation remains a pilot operational requirement rather than an invitation to make unguarded writes.

Artifact acceptance is a database relation bound to exact immutable object/hash/version metadata. Unconfigured production readiness or authorization adapters reject. The object deletion path must first mark ineligible under the same guard protocol, then physically delete outside the transaction. Existing accepted references and authorized retention/deletion behavior require explicit lifecycle handling; no database commit guarantees physical availability forever.

## 6. Readiness and verification boundary

The architecture direction is now settled enough to complete one bounded implementation-readiness package, without further routine option questions. Remaining items are concrete engineering checks: final physical columns/FKs and index names, reviewed Core/SQL templates implementing this map, dependency/server compatibility, disposable PostgreSQL provisioning, test fixture safety and transaction retry limits. Recommend resolving them in that package rather than reopening the scientific plan.

No coding stage is declared ready by this document alone. Before coding, present the affected files/dependencies/interfaces, remaining risks and an explicit readiness notification; wait for the owner's explicit coding authorization. No production/runtime code, migration or implementation dependency changes occur before that authorization.

Required future tests include every Job/Attempt edge, duplicate/competing claims, scheduler fairness, admission/capacity predicates, permission/revision/deletion races, renewal/expiry, cancellation/recovery, stale publication, partial transaction rollback and unknown acknowledgement. Use actual PostgreSQL across processes. All are unexecuted specifications; no capability is enabled and no gate closes.

## Primary references

- [PostgreSQL constraints](https://www.postgresql.org/docs/current/ddl-constraints.html): named constraints, uniqueness, foreign keys and limits of CHECK constraints.
- [PostgreSQL SELECT](https://www.postgresql.org/docs/current/sql-select.html): FOR UPDATE SKIP LOCKED and queue-oriented use, not general consistency/fairness proof.
- [PostgreSQL date/time functions](https://www.postgresql.org/docs/current/functions-datetime.html): clock time versus transaction/statement timestamps.

Recommendations for coordination, fairness and metadata above are EvidenceTwin design analysis, not PostgreSQL guarantees.

## Current readiness package — 2026-11-06

The remaining bounded preparation is consolidated in the [Coding Readiness Report](CODING_READINESS_REPORT.md), [concrete schema/SQL review](EXECUTION_POSTGRESQL_SCHEMA_REVIEW.md), [dependency compatibility review](DEPENDENCY_COMPATIBILITY_REVIEW.md) and [test environment/EX01–EX46 specification](EXECUTION_TEST_SPECIFICATION.md). These supersede earlier statements that routine tooling/isolation/schema/test defaults are still awaiting A/B/C selection. The concrete additions are assistant recommendations, not silently approved decisions. Owner-approved architecture and development defaults are preserved.

Preparation for the isolated execution-infrastructure increment is ready for coding-scope review; actual SQL/migrations/dependency/runtime/concurrency validation is explicitly unexecuted. All 24 gates remain OPEN and status remains Recommended for owner approval. No production code/migration/dependency/service changes are authorized without the separate coding-stage notification and explicit owner authorization.
