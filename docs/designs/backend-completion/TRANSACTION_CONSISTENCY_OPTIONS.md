# EvidenceTwin V1 — Short-transaction consistency choice

**Status: Recommended for owner approval.** Date: 2026-11-06. All **24 gates remain OPEN**. This is a bounded implementation dependency within the approved Core transaction plan. The owner selected A — Read Committed as the default isolation direction on 2026-11-06. The alternatives below are retained as history; no implementation or deployment is authorized.

## Fixed requirements

Both options retain conditional/version-guarded publication, current lease and monotonically increasing fencing epochs, complete-record validation, centralized Core metadata, Psycopg 3 and reviewed Alembic migrations. Neither permits long-lived locks, transactions during scientific/provider work, ORM/Session access or automatic production schema creation. This comparison refines the earlier selected publication direction rather than reopening it.

## Comparison retained as decision history

| | A — Read Committed with coordinated conditional guard writes | B — Serializable with coordinated conditional guard writes |
| --- | --- | --- |
| Mechanism | Each protected operation conditionally writes explicit shared guard/version rows and validates current authoritative facts inside one short transaction. All writers of permission, cancellation, evidence eligibility and revision changes participate. PostgreSQL row-write conflicts coordinate concurrent changes; exact statements and deterministic order require review. | Use the same explicit ownership/version/authorization guard participation, plus Serializable isolation for the protected operation group. Serialization failures restart the entire short database operation with fresh guards, never scientific execution or external calls. |
| Why retain shared guard writes? | A check of an unrelated row followed by a result insert cannot protect against changes to the checked fact. The guard must actually coordinate with that fact's writers. | Serializable alone can order overlapping operations before a revocation even when their commits arrive in another order. Explicit guard participation still defines required cancellation/revocation ordering and exact ownership. |
| Trade-off | Directly inspectable conflict points and narrower explicit coordination; greater responsibility to prove the complete read/write dependency inventory and protect missing-row/predicate cases. | Additional protection against serialization anomalies across participating operations; requires whole-operation abort/retry handling and may increase contention/retries. Still requires correct constraints, predicates and guard coverage. |
| Failure conditions | A writer bypasses the shared guard, mutable dependencies are missing, lock/version order is inconsistent or a phantom-dependent condition has no explicit protection. | Some participating operations run at weaker isolation without a reviewed interaction proof, aborted work leaks effects, or retry logic replays an external request. Serializable does not repair missing authorization or wrong scientific policy. |
| Fit | When each relevant invariant can be tied to a finite, explicit set of rows/constraints and the owner wants the consistency proof based on those write conflicts. | When the owner wants Serializable as an additional invariant check and accepts its retry/operational requirements while retaining explicit guard coordination. |

These are design trade-offs, not measured performance results. A does not mean an unconditional write after an earlier read; B does not mean defaulting the entire existing application to Serializable. Exact security-sensitive acceptance ordering must be specified for either option.

## Common review obligations after selection

1. Map every mutable guard to authoritative rows and every writer, including suspension, cancellation, revisions, deletion, recovery and administrative repair. Define a deterministic acquisition/write order and safe handling of absent-row and capacity predicates.
2. Preserve atomic job/attempt/queue/permit/publication/idempotency/audit relationships and evaluate lease time after relevant waits. Verify every affected-row count and unique conflict outcome.
3. Define bounded transaction retries separately from the three execution-attempt budget. A database-only retry does not allocate a new scientific attempt or repeat a provider call; uncertain commit acknowledgement first reconciles the durable operation identity.
4. Review the queue claim statement and per-account fairness separately. SKIP LOCKED, if later selected, is queue acquisition behavior, not an authorization or fairness guarantee.
5. Test actual PostgreSQL processes with races for cancellation, revocation, evidence deletion, revision changes, recovery, duplicate publication and capacity. No option passes merely because sequential tests succeed.

Neither option supplies cross-system atomicity with object storage, identity-provider revocation or external LLMs. Required adapter consistency contracts and unresolved settlement blockers remain in force.

## Scope after this decision

Next, consolidate the selected approach into concrete metadata constraints, operation-key scope and the statement/guard map for the already approved file allocation. Do not expand the scientific design. Exact package/server versions, disposable test provisioning and any remaining publication adapter gaps must be resolved before a separate request to authorize coding. Existing development defaults and all 24 OPEN gates are unchanged.

## Primary references

- [PostgreSQL transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html): Read Committed snapshots, concurrent updates, Serializable behavior and retry obligations.
- [PostgreSQL explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html): row locking, short-transaction coordination and deadlock considerations.

The proposed protocols and trade-offs above are EvidenceTwin design analysis, not claims that PostgreSQL automatically enforces application-specific authorization or verification policy.

**Owner selection and refinement rule:** Read Committed is the V1 default. Use atomic conditional transitions, explicit locks where required, appropriate FOR UPDATE SKIP LOCKED queue claims, reviewed cross-row enforcement and all existing guards. Selective Serializable requires an identified invariant and separate reviewed justification; it is not a silent fallback. Future recommendations are to be selected by the assistant with rationale, trade-offs, assumptions and open gates, without routine A/B/C questions. Owner-specific facts and irreversible commitments still require owner input. Before any production/runtime/migration/dependency change, present the concrete scope, affected files/interfaces/dependencies, unresolved risks and an explicit coding-readiness notification, then wait for separate coding authorization.
