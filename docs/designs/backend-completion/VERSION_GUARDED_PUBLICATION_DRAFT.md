# EvidenceTwin V1 — Conditional publication, monotonic fencing and guard coverage

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner selected **A — Conditional / Version-Guarded Publication as the recommended V1 direction for refinement only**. This refines [FD02](PUBLICATION_IDEMPOTENCY_OPTIONS.md). All **24 gates remain OPEN**. Exact guard schema, transaction/isolation implementation, time/permission consistency and legal job transitions remain unresolved. No implementation, deployment, statistical method/library selection or capability enablement is authorized. All coverage/race obligations are unexecuted specifications.

Separate Typed Axes, Decimal and explicit typed absence remain recommended directions. Partially Supported remains a proposed/unresolved claim verdict. No publication guard can waive unresolved scientific requirements or fabricate a valid canonical result.

## 1. Acceptance operation and atomicity

Result publication must be accepted or rejected through atomic conditional database operations inside a **short transaction**. Checking conditions in an earlier read followed by an unconditional write is invalid. The authoritative operation binds exact scope/versions and uses the centralized complete-record contract.

Prepare scientific outputs, artifacts and immutable proof references outside the transaction. Within the bounded acceptance transaction, validate all applicable current guards and atomically record the accepted result/publication relation, applicable job/attempt transition, operation outcome, artifact acceptance metadata and required audit relation. Exact physical tables/queries and the transaction strategy remain OPEN.

No transaction or lock remains open during scientific execution, source retrieval, rendering or external LLM requests. Internal short-lived database locking may be necessary for atomic persistence, but long-lived pessimistic locking is not the primary concurrency-control direction. Conditional publication does not mean lock-free or weaker authorization.

## 2. Guard set — required meaning, not final schema

The following guard labels are document identifiers, not new gates or selected field names. Unknown required guard facts block acceptance; no default-to-true behavior.

| Guard | Protected fact and required predicate |
| --- | --- |
| PG01 — Job identity/state | Exact authorized logical job identity and the expected state eligible for the requested operation. Never apply to another job or whichever job is latest. |
| PG02 — Attempt identity | Exact expected execution attempt/step and its relation to the job; old attempts cannot act on a replacement. |
| PG03 — Monotonic fence | Worker ownership token equals the current authoritative token and is valid for that attempt/operation. Ownership/recovery/retry allocation must maintain strict monotonic order over transitions that can publish to the same protected target. |
| PG04 — Analysis revision | Expected analysis/claim/classification revision and active publication target match the request. New scope cannot inherit an old result silently. |
| PG05 — Evidence identity | Exact immutable evidence snapshot/data/source/selection references match the accepted attempt, not just a URL/title/hash or numerically equal output. |
| PG06 — Cancellation/terminal state | Current cancellation/terminal/supersession facts permit this operation. Stale worker results cannot overwrite newer results or change terminal job/attempt state. |
| PG07 — Scientific policy | Exact pinned scientific policy/procedure/schema versions remain admissible for the attempt under the approved version-use rule; no latest-version substitution. |
| PG08 — Execution configuration | Exact pinned role/model/prompt/protocol/context/configuration references match; no silent reconfiguration or fallback. Secret material never enters the public guard record. |
| PG09 — Authorization | Trusted current internal actor/service and case/resource/action permission, including suspension/deletion/revocation handling under an explicit consistency contract. |
| PG10 — Canonical/assessment validity | Complete candidate, typed absence/applicability proof, scientific observations/provenance and verdict/report eligibility meet their approved contracts. No individual-field bypass. |
| PG11 — Artifact acceptance | Required uploaded/derived object identities and staging/deletion/integrity state are eligible for acceptance under the reviewed DB/object protocol. |
| PG12 — Operation/predecessor | Expected record/publication predecessor and scoped idempotent operation/content identity are consistent; no conflicting duplicate active acceptance. |

Guard coverage includes every writer that can change these facts, not only the worker's success path. Application endpoints, administrative tools, recovery/import tasks and deletion/suspension must use the same protocol. A version changed only by publication cannot protect an unguarded cancellation or permission update.

## 3. Monotonic fencing contract

An execution ownership epoch is assigned by trusted authoritative state through an atomic operation. A worker cannot choose, reuse or advance its own token by asserting a larger value in a result. Publication compares the exact current token, not merely “greater than or equal to” an old token.

When ownership is replaced, any new token must be strictly later than the prior protected ownership epoch. Scope and allocation/storage format remain to be specified, but no reset/reuse/wraparound may allow an earlier owner to match a newer execution capable of writing the same target. Overflow/resource limits require explicit failure handling, not silent counter rollover.

Attempt identity and fencing are both required: a matching token with the wrong attempt, or a matching attempt with an obsolete token, cannot publish. A new attempt/recovery ownership decision must persist its relation to the expected predecessor atomically. No cross-job total ordering or particular integer width/increment algorithm is selected here.

Lease expiry is not proof an external call ended. Recovery may replace ownership only through the guarded recovery policy and must separately reconcile provider settlement/reservations. The old worker's late response remains fenced from active result/job mutation even if its output is scientifically plausible.

## 4. Write-path guard coverage

Every path enforces the common applicable PG guards. “Applicable” is an explicit reviewed operation profile, not a per-endpoint exemption from validation. Control-plane operations use their own current authority and exact predecessor context; they do not impersonate worker ownership to bypass it.

| Write path | Required guarded behavior |
| --- | --- |
| Worker success/final result | Validate PG01–PG12 for the exact completed candidate and active target; scientific validity does not override stale ownership. |
| Worker failure/insufficient input | Check the same job/attempt/fence/revision/state/configuration/authority context before recording an authoritative failure or changing active state. A stale error cannot replace newer success or reopen a terminal job. |
| Worker progress/checkpoint | Full candidate validity and current identity/attempt/fence/state/revision; provisional output cannot become final satisfaction or bypass later guards. |
| Worker retry request | Record proposed retry only under current authority/state; safe replay/replacement authorization is explicit. A worker cannot reset the job or advance its fence unilaterally. |
| Authorized retry acceptance | Match expected eligible job/attempt/state/fence and immutable input/configuration; create attributable new attempt/ownership under the future legal-transition policy. Old terminal attempt history is not rewritten. |
| Abandoned-work recovery | Compare exact current ownership/attempt/state and approved recovery conditions; atomically establish replacement identity and strictly later fence. No blind uncertain paid-call replay. |
| Pending/running cancellation | Current authorized control-plane actor and exact target/predecessor; atomically record cancellation state. Concurrent worker publication must obey the same accepted ordering. |
| Late/duplicate response | Old/noneligible context cannot mutate active or terminal state. Retain permitted rejected-response/settlement history without presenting it as newly accepted scientific output. |
| Evidence/classification amendment | Exact authorized parent revision, confirmation and dependency context; new revision/target affects future guards without rewriting history. |
| Suspension/deletion/operator repair | Explicit current authority and consistent guard/version updates. No administrative path may force scientific validity or silently change protected scope. |
| Projection/export/public link issuance | Reads do not overwrite job state, but current access and accepted-result visibility rules apply. No acceptance access through object keys or replay cache. |

Exact operation-profile membership and state transitions remain OPEN. This table does not decide whether a retry reuses a logical job or creates a new one; either must preserve old attempt history and prevent stale terminal-state writes.

## 5. Transaction outcomes and rejected publication audit

| Outcome | Required persistence/public behavior |
| --- | --- |
| Accepted | Guards and publication occur atomically with the applicable state/operation/audit/acceptance metadata; only then may the service acknowledge accepted publication. |
| Conditional rejection | No active result/job/terminal mutation. Persist attributable rejection facts for audit/reconciliation under the short database protocol. |
| Equivalent acknowledgement replay | After current authorization, return the existing accepted logical outcome under the reviewed idempotency contract; do not perform a new terminal-state mutation or republish artifacts. |
| Conflicting replay | Preserve conflict/rejection; never overwrite the earlier outcome or merge changed content into another revision. |
| Database failure/unknown commit outcome | Do not claim acceptance or a durably recorded rejection without evidence. Reconcile durable operation/result/audit state before retry decisions; no scientific/LLM replay from uncertainty alone. |

A rejection record must identify the publication operation, trusted actor/component, proposed job/attempt/revision/fence/configuration references, safe guard-rejection reason, observed time and reconciliation/late-call references where applicable. Preserve only authorized safe metadata; do not leak another account's existence, secret credentials or raw private evidence through the failure response/log.

The rejection audit must not depend on the forbidden worker state mutation succeeding. Exact atomic rejection-event/idempotency recording and database-outage recovery are OPEN design items; they must meet the audit requirement before FD02 can be formally accepted. If commit/audit persistence is uncertain, retain that uncertainty explicitly rather than pretending the rejected attempt was safely logged or replaying paid work.

## 6. Staged artifacts and accepted visibility

An immutable upload may precede DB publication, but physical existence does not make it an accepted result. Use an explicit staged-to-accepted relationship controlled by successful conditional publication; exact bucket/key/schema/promotion mechanism remains OPEN.

Before acceptance, do not expose the artifact through accepted-result lists, report references, exports or authorized accepted-download links. Retention/inspection of a submitted original upload as input is a separate operation and does not grant acceptance to generated result artifacts.

On guard rejection, preserve permitted staging/rejection/settlement references and reconcile orphaned objects under approved lifecycle rules. Do not attach the artifact to a newer attempt merely because it looks equivalent. On unknown DB outcome, reconcile authoritative acceptance before exposing or deleting it.

Object-store state is not inherently atomic with a DB transaction. The concrete protocol must establish artifact readiness/integrity and protect acceptance/deletion races while the DB controls scientific-result visibility. Original evidence is not overwritten, and no guarded commit can promise permanent artifact availability beyond the retention policy.

## 7. Whole-record validation and scientific boundaries

All writes validate the complete candidate and current guard context. A caller cannot patch only status, fence, determination discriminator or result pointer to evade validation. Explicit Not Applicable absence still needs rationale/policy/evidence; Undetermined applicability or missing/null determination data cannot exempt Mandatory work.

A valid Incomplete report may show completed claims and blockers; it cannot be labeled Complete/Verified with unmet mandatory science/report gates. Partially Supported remains unresolved and cannot become an accepted canonical verdict through a model response or legacy adapter.

Immutable scientific payload checks may be prepared before the transaction, but acceptance must bind the same validated payload/policy references and atomically validate all mutable guards. This is not permission to skip centralized validation at trust boundaries or reuse an old authorization receipt.

## 8. Guard-coverage acceptance specifications — unexecuted

These refine existing LP/TA/CF/CR/AC obligations rather than adding executed tests or a new counted acceptance family.

| Required future scenario | Acceptance invariant / existing obligation |
| --- | --- |
| Stale success and stale failure after a newer result | Neither overwrites active results or changes terminal state. LP04/TA06. |
| Wrong job/attempt with a plausible fence | Reject exact identity mismatch. AC01/CR02. |
| Reclaim/retry produces newer ownership | Strictly later fence; old token cannot publish even if lease/call output arrives later. LP04/TA08. |
| Concurrent analysis/evidence/classification amendment | Reject wrong active revision/snapshot and preserve original history. LP05/CF05/CF08. |
| Cancellation competes with success/error publication | Enforce atomic accepted ordering under common guards, not success-only checks. LP04/CR16. |
| Pinned policy/configuration differs | No silent latest-version/model substitution. LP11/CR14. |
| Conditional rejection | Rejection auditable without changing the protected job/result; unknown audit outcome remains explicit. LP01/AC20. |
| Artifact uploaded before a rejected write | Not visible as accepted report/result/export/download; reconcile staging/orphans. LP08/AC20. |
| Publication committed but acknowledgement lost | Scoped authorized replay returns same accepted outcome without paid-call replay or job mutation. LP07. |
| Operator/recovery/cancellation path skips a guard | Coverage review/test rejects bypass; privileged actor cannot waive scientific validity. TA07. |

Each path needs reviewed test fixtures, actual concurrent failure injection under the selected engine/configuration and audit/artifact observations before acceptance evidence exists. No test has run, no guard implementation is proven and no gate is closed by this matrix.

## 9. Remaining exact design decisions

Still OPEN: guard field/table/ref schema; monotonic fencing allocation/scope/type/bounds; operation and terminal/retry transition profiles; conditional statement/isolation strategy; permission/revocation/clock ordering; result/audit/idempotency atomicity; staging acceptance/deletion/orphan handling; outage reconciliation; public error/visibility projections; exact reviewed fixtures and execution evidence.

The primary direction is conditional/version-guarded publication with bounded atomic transactions, **not long-lived pessimistic locking**. PostgreSQL remains a candidate; no engine, SQL, isolation level, library or production schema is selected. **Status remains Recommended for owner approval; all 24 gates remain OPEN.**

**Candidate schema refinement:** the [publication guard schema proposal](PUBLICATION_GUARD_SCHEMA_PROPOSAL.md) separates untrusted commands, authoritative guard facts, validation bindings, operation profiles, outcomes and artifact acceptance relationships. Exact schemas and transition/transaction mechanisms remain proposals. Status remains Recommended for owner approval; all 24 gates remain OPEN. No implementation or capability enablement is authorized.
