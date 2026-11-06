# EvidenceTwin V1 — FD02 publication and idempotency options

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner subsequently selected **A — Conditional / Version-Guarded Publication as the recommended refinement direction only**. The [guard-coverage/fencing draft](VERSION_GUARDED_PUBLICATION_DRAFT.md) develops it. B remains comparison history, not the primary direction. All **24 gates remain OPEN**. Engine/isolation, guard schema, clock/revocation rules, API contracts and acceptance criteria remain unresolved. No implementation, statistical method/library, deployment or capability enablement is authorized. All examples are unexecuted specifications.

Separate Typed Axes, Decimal and explicit typed absence remain recommended refinement directions. Partially Supported remains a proposed/unresolved claim verdict. Neither option can bypass whole-record validity or mandatory scientific/report requirements.

## 1. Acceptance boundary and shared facts

A logical publication binds the exact authorized actor/service, case, claim/evidence/classification/temporal revisions, attempt/step/fence, result version and pinned policy/procedure/configuration. Define its authoritative acceptance ordering relative to cancellation, reassignment, amendment, permission changes and competing publication. A valid payload or earlier successful read is insufficient.

Long-running calculations, retrieval, rendering and LLM requests occur outside the guarded transaction. Publication consumes validated immutable results/proofs and re-establishes mutable acceptance predicates; it never waits for scientific/provider work while holding database locks.

| Protected fact | Required coherence |
| --- | --- |
| Account/session/service permission | Trusted current EvidenceTwin authorization under an explicit revocation consistency contract, not an old client/identity assertion. |
| Case/resource access | Scope-specific grants, suspension/deletion/support-access expiry and all affected resource classes. |
| Predecessor/active target | Competing finalization or new active scope cannot be overwritten silently; historical targets remain distinct. |
| Evidence/classification/processing | Exact immutable scope and required confirmations/authorization, not mutable latest settings. |
| Attempt/cancellation/fence | Reclaimed, cancelled or superseded work cannot actively publish; lease expiry does not establish remote settlement. |
| Policy/configuration | Pinned versions remain admissible under the approved version-use rule, not automatically replaced by newest. |
| Artifact state | Required exact objects are accepted/available under the storage/deletion contract; pending/orphan references are not assumed usable. |

Every writer affecting these facts must participate in the guard protocol, including API, worker, operator, recovery, suspension/deletion and migration paths. Publisher-only version increments cannot protect unversioned permission/cancellation changes. External identity events, object availability and provider settlement require explicit coordination; no instantaneous global revocation or distributed atomicity is promised.

## 2. A — Conditional/version-guarded publication

### Candidate mechanism

1. Validate the complete immutable candidate, scientific proof and exact trusted scope/version context.
2. Enter bounded authoritative acceptance under a reviewed database isolation contract.
3. Conditionally accept only if all protected predecessor/permission/attempt/fence/revision/artifact-state predicates still hold.
4. Ensure publication itself participates in the guard protocol so competing changes obey the intended order.
5. Record result/publication relation, operation outcome and required audit identity atomically under the approved DB contract.
6. On conflict, reconcile durable state and reevaluate under bounded policy; never silently rebase inputs or repeat paid scientific work.

Conditional does **not** mean lock-free or “read everything, then check only the result row.” A multi-record scope needs a complete coherent guard/version protocol for every relevant writer. No schema or engine-specific algorithm is selected here.

### Tradeoffs and failure conditions

Can bound protected write duration and expose stale conflicts directly. Requires complete guard coverage and carefully bounded retries. Fails if permission/fence/artifact changes do not invalidate acceptance, a snapshot read is mistaken for current state, or conflict retries merge into a new unconfirmed scope.

Guard granularity, atomic compare/update semantics, isolation, clock predicates and retry limits remain OPEN. A single version field without those definitions is not proof of correctness.

## 3. B — Bounded transactional locking

### Candidate mechanism

1. Validate immutable candidate/proof outside long-running work.
2. Enter a short transaction and acquire the reviewed actor/case, target, attempt/fence and metadata guards in an explicit order.
3. Revalidate mutable permission/scope/predecessor/cancellation/version predicates under the selected future isolation/locking contract.
4. Record accepted publication, operation outcome and required audit relation; commit and release locks.
5. Handle deadlock, timeout, transaction failure and lost acknowledgement through bounded durable-state reconciliation, not model replay.

Locks must protect all necessary changing facts, not just the destination report row. Missing/deleted guards and every competing writer require explicit treatment. No lock scope/order, table-wide lock, isolation level, SQL or library is selected.

### Tradeoffs and failure conditions

Makes the protected acceptance section explicit and can simplify some orderings. Adds contention/deadlock and bounded-wait responsibilities. Fails if another permission/cancellation path uses different guards, scientific/network work holds locks, or database locks are treated as control over external objects, identity systems or paid calls.

The initial two-analysis planning cap does not prove contention is harmless. Exact engine/guard semantics still need comparison and validation.

## 4. Shared idempotency contract

Both directions require an operation identity scoped to the authorized actor/case/attempt/purpose and a reviewed immutable candidate-content equivalence rule. Exact key/hash/canonicalization/storage/retention/API formats remain OPEN.

| Condition | Required behavior |
| --- | --- |
| First authorized request | Validate full candidate/current guards; accept durably or give explicit rejection/uncertainty. No success before authoritative acceptance. |
| Equivalent repeat after acceptance | After current authorization, resolve the same logical outcome under the acknowledgement policy; no conflicting second active publication. |
| Same identity, different content/scope | Conflict, not overwrite or automatic changed-input retry. |
| Lost response, unknown outcome | Reconcile authoritative operation state; do not assume failure or launch replacement paid work. |
| Revoked/wrong account replay | Do not reveal acknowledgement/body/protected record existence. |
| Prior rejection/pending state | Preserve actual reason/state; retry/resume/new identity semantics need explicit policy. |

Idempotent local acceptance does not guarantee exactly-once provider generation. Request IDs, uncertain usage/charges, permits/reservations and replacement authorization remain separate recovery records.

## 5. Artifacts, audit and honest incomplete reports

Required objects may need staged/accepted metadata and orphan reconciliation. A DB failure after an object write must not expose an unaccepted report. A missing/deleted required object cannot be assumed usable because its identifier remains in a database row.

Object/DB handoff, integrity/freshness/deletion races and audit atomicity remain OPEN. Neither option alone supplies a distributed transaction. Later outages/deletion are disclosed without silently rewriting history or promising reproducibility without retained content.

Operator recovery cannot bypass canonical validity. Audit must identify accepted operation/scope and outcome without ordinary-log evidence/secret leakage. Valid incomplete reports remain inspectable with blockers; they cannot be labeled Verified. Typed absence still requires rationale/policy/evidence, while undetermined applicability or malformed/null data cannot exempt mandatory work.

## 6. Race obligations — unexecuted specifications

| Race | Required invariant / existing obligation |
| --- | --- |
| Permission changes after prevalidation | Acceptance obeys the explicit current-authority protocol; no stale permission shortcut. LP06/TA06. |
| Cancellation/reclaim before write | Old attempt/fence cannot actively publish or falsely settle provider work. LP04/TA08. |
| Evidence/classification amended | No mixed/latest-substituted scope; history remains bound to original inputs. LP05/CF05/CF06. |
| Duplicate finalization | One protected logical outcome or explicit conflict, not competing active versions. LP07. |
| Accepted but response lost | Reconcile durable state; no duplicate paid execution. LP07. |
| Artifact missing/not accepted/deleted | Enforce readiness/deletion guards and truthful report state. LP08. |
| Operator/import path skips guards | No privileged scientific/authorization bypass. TA07/LP01. |
| Policy/model changes mid-attempt | Use admissible pinned versions; no silent substitution. LP11/CR14. |

These refine existing specifications, not a new counted acceptance family or executed tests. Mechanism approval needs concrete concurrency review and later separately authorized failure/race execution under the selected engine/configuration.

## 7. Decision comparison

| Criterion | A — Conditional/version-guarded | B — Bounded transactional locking |
| --- | --- | --- |
| Coordination | Coherent predicates/versions at conditional acceptance. | Short ordered protection of all required acceptance facts. |
| Main risk | Incomplete guard coverage or unsafe rebase/retry. | Missing lock participation, contention/deadlock or long-held locks. |
| Shared requirement | Complete semantic validation, current permissions, fencing, immutable scope, artifacts and durable outcome. | Same; locks do not replace scientific proof. |
| Engine/product | Unselected; exact semantics must be demonstrated. | Unselected; exact semantics must be demonstrated. |
| External systems | Explicit handoff/settlement/availability contract. | Same; DB locks do not make external systems atomic. |

**A is the owner-selected recommended refinement direction.** Conditional guard validation/publication uses short atomic transactions and comprehensive job/attempt/fence/revision/evidence/state/policy/configuration guards on all applicable paths. Monotonic fencing, rejected-write audit and staged-artifact acceptance are required. Exact schema/transaction/clock/revocation/idempotency details remain OPEN; no gate is closed.

Reference check on 2026-11-06: official PostgreSQL [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html) and [explicit locking](https://www.postgresql.org/docs/current/explicit-locking.html) documentation illustrate why snapshot reads and lock scope need concrete treatment. PostgreSQL remains a candidate. No SQL or runtime implementation was written/tested.

**Status remains Recommended for owner approval; all 24 gates remain OPEN.** Partially Supported remains unresolved; no production implementation/deployment/enablement is authorized.
