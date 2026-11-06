# EvidenceTwin V1 — Core repository and transaction contract

**Status: Recommended for owner approval.** Date: 2026-11-06. All **24 gates remain OPEN**. B — SQLAlchemy Core + Psycopg 3 + Alembic is selected for refinement. The owner approved this bounded transaction plan for planning on 2026-11-06; it is not implementation or deployment authority. Existing development defaults, approved transition tables and scientific exclusions remain unchanged.

## 1. Fixed access boundary

Centralize all execution table definitions, foreign keys, indexes and named constraints in `execution/tables.py`. Keep internal contracts separate from Core rows and public DTOs. Repositories alone execute persistence operations; they receive explicit validated commands and trusted actor/context references rather than derive scientific conclusions.

Use SQLAlchemy Core Engine/Connection exclusively, with Psycopg 3 as driver and a single runtime pool managed by the Engine. No ORM, mapped entities, Session, lazy loading or relationship persistence. Do not bypass Core using direct driver connections for application writes. Use Core expressions and bound parameters by default; specialized parameterized PostgreSQL SQL may run through a Core Connection when its predicates are clearer to audit. Never interpolate caller-controlled values or identifiers into SQL.

Explicitly scoped transactions begin and end inside repository operations. Return detached contract values, never live connections/cursors or objects that require later queries. A lower-level helper must not commit a caller-owned transaction. No transaction crosses scientific execution, object upload, network dispatch, provider response wait or heartbeat sleep.

Use reviewed Alembic revisions for schema evolution. No production `create_all`, startup migration or metadata-driven schema repair. Schema incompatibility produces a safe readiness error. Migrations are reviewed against metadata and exercised on disposable PostgreSQL before approval; migration generation is not proof of correctness.

## 2. Repository operation plan

| Operation | Short atomic unit and inspectable postcondition |
| --- | --- |
| Submit | Validate pinned references and current authority; reserve scoped operation identity; create job, initial attempt and queue entry together. No partially accepted job if any write fails. |
| Claim | Select an eligible pending attempt under a reviewed PostgreSQL claim protocol, recheck state/deadline/authority, acquire shared analysis capacity, increment trusted ownership epoch, establish attempt/owner/lease and pair job transition. Exactly one claimant wins. |
| Heartbeat | Conditional renewal on running state, owner, attempt, fence, expected version, cancellation and unexpired database-time lease. Acknowledge only a committed operation; duplicate replay must not extend again. |
| Record checkpoint | Bind complete validated step payload to current ownership, pinned versions and exact predecessor. Persist step/output acceptance metadata and audit together. Provisional output remains provisional. |
| Publish final | Verify PG01–PG12 and G3 against exact context; atomically accept output/artifact relations, paired job/attempt terminal transition, operation outcome and audit. No result pointer appears before commit. |
| Fail/retry/recover | Enforce approved J/A edges and failure classification, prior ownership, total-attempt limit and external-settlement blockers. Retire prior attempt and allocate at most one pending replacement/deadline where allowed. |
| Cancel | Compare exact expected predecessor, set cancellation guard, pair attempt transition and queue eligibility changes atomically. Never reopen terminal states; settlement records remain separate. |
| Reconcile external call | Append attributable evidence and adjust only justified reservations/settlement facts. Any job transition still passes its ordinary guards. No direct promotion of late output. |

Scientific applicability, verdict eligibility and business retry policy are validated outside persistence by explicit services; repositories enforce the resulting approved command and immutable validation binding plus current mutable guards. Missing validation/authorization/artifact evidence fails closed. A test-only principal or validator never becomes a permissive production default.

## 3. Guard participation and write inspection

The acceptance protocol must protect every mutable dependency, not just the publication row. Inventory owner permissions/suspension, target revision, job/attempt/fence/lease/cancellation, evidence acceptance/deletion, policy/configuration admissibility, predecessor and artifact readiness. For each dependency, the concrete transaction specification must name its authoritative row/version and every writer that can invalidate it.

A pre-read followed by a guarded job update is insufficient if permission or evidence deletion can change without participating in that protocol. Short database locks or validated version updates may be needed. This plan does not select a blanket isolation level, lock ordering or claim statement; those require a concrete all-writer consistency proof before coding. Long-lived pessimistic locks remain prohibited.

Review each specialized statement with: purpose, bound inputs, affected tables, exact expected states, guard predicates, authoritative time evaluation, expected returned row count, unique-constraint behavior, rollback path and safe error outcome. Zero affected rows means rejection or reconciliation, never implicit success. Multi-row updates that violate a single-target contract roll back.

Queue claim mechanisms such as `FOR UPDATE SKIP LOCKED` are candidates for this concrete specification, not yet selected by this document. Skipping locked rows does not itself enforce fair per-account dispatch, shared capacity, authorization or publication safety. Those remain explicit proof obligations.

## 4. Idempotency and rejection outcomes

Use a database-enforced unique scoped operation key plus immutable command/context identity. Equivalent retries read the committed authorized outcome; conflicting key reuse rejects without overwrite. The exact canonicalization, unique scope and retention still need concrete schema review. Never treat hash equality as permission or scientific equivalence.

Accepted operation/result/audit relations commit together. Guard rejections must preserve authorized safe rejection history without attempting the forbidden job mutation. Serialization/deadlock/connection failures and unknown commit acknowledgements require separate classification; a rolled-back or uncertain audit write is not a durable rejection record. Reconcile operation history before repeating writes, and never rerun a paid provider call to resolve database uncertainty.

## 5. Database time and resource boundaries

Lease validation uses authoritative time evaluated after relevant waits inside the acceptance protocol. PostgreSQL transaction-start time cannot silently substitute for current lease time after contention. A reviewed statement must bind a consistent authoritative acceptance timestamp for its expiry comparison and renewed expiry. Exact SQL evaluation remains subject to the forthcoming statement/transaction review.

Each process constructs/disposes its own Engine; live pooled connections must not be shared across worker process boundaries. Numeric pool bounds, PostgreSQL version, statement/lock limits, isolation and deployment topology are still open; development lease/heartbeat/retry values remain exactly as approved. SQL parameters and database connection strings must not leak into ordinary diagnostics where they contain private data or secrets.

## 6. Verification required before implementation acceptance

Inspect emitted parameterized statements and transaction boundaries; verify no ORM/Session/direct-driver write paths or automatic schema creation. Test migrations on empty and prior disposable schemas, rollback of partial submission, concurrent claims/capacity, renewal/recovery/cancellation races, duplicate/conflicting operation keys, stale publication and uncertain commit reconciliation using actual PostgreSQL processes. Prove permission/revision/deletion races across every writer. No test was executed by drafting this plan.

Remaining bounded work: concrete metadata/constraints, operation-key identity, all-writer guard strategy, claim/fairness algorithm, isolation/lock order and database-time SQL; safe audit/outage protocol; approved package/server versions and disposable test provisioning. These remain explicit D02/other existing-gate obligations, not new gates. Do not proceed to coding from this section approval alone.

## Primary references

- [SQLAlchemy Core Engine/Connection transactions](https://docs.sqlalchemy.org/en/20/core/connections.html): connection and transaction behavior; reference only, not a selected release line.
- [SQLAlchemy PostgreSQL dialect](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html): PostgreSQL-specific expression and driver facilities.
- [PostgreSQL SELECT locking clauses](https://www.postgresql.org/docs/current/sql-select.html): queue-related SKIP LOCKED behavior and its limited consistency guarantees.
- [PostgreSQL date/time functions](https://www.postgresql.org/docs/current/functions-datetime.html): transaction/statement time versus actual clock time.

**Section approval:** Owner planning approval received on 2026-11-06. Concrete isolation/guard coordination, metadata/constraints and statement-level proof remain unresolved. No gate closes.

## Current readiness package — 2026-11-06

The remaining bounded preparation is consolidated in the [Coding Readiness Report](CODING_READINESS_REPORT.md), [concrete schema/SQL review](EXECUTION_POSTGRESQL_SCHEMA_REVIEW.md), [dependency compatibility review](DEPENDENCY_COMPATIBILITY_REVIEW.md) and [test environment/EX01–EX46 specification](EXECUTION_TEST_SPECIFICATION.md). These supersede earlier statements that routine tooling/isolation/schema/test defaults are still awaiting A/B/C selection. The concrete additions are assistant recommendations, not silently approved decisions. Owner-approved architecture and development defaults are preserved.

Preparation for the isolated execution-infrastructure increment is ready for coding-scope review; actual SQL/migrations/dependency/runtime/concurrency validation is explicitly unexecuted. All 24 gates remain OPEN and status remains Recommended for owner approval. No production code/migration/dependency/service changes are authorized without the separate coding-stage notification and explicit owner authorization.
