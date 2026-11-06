# EvidenceTwin V1 — Separate Job and Execution Attempt transition tables

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner approved both transition tables for planning on 2026-11-06. This section approval does not close any gate or authorize implementation. All **24 gates remain OPEN**. This bounded refinement proposes state names, transitions and invariants for the [first coding scope](FIRST_CODING_SCOPE.md); it does not approve implementation, deployment or capability enablement. Existing architecture, scientific boundaries and development-only defaults remain unchanged. PostgreSQL is selected; provider/region/deployment remain open. Partially Supported remains an unresolved proposed scientific verdict.

## 1. Scope and proposed state inventories

A Job represents one accepted execution request against pinned inputs. An Execution Attempt represents one dispatch opportunity for that job. A retry creates another attempt within the same nonterminal job; terminal jobs never reopen. A later researcher-requested rerun creates a new linked job with fresh admission/authorization, not another attempt hidden inside an old job. These are proposed lifecycle semantics for review, not existing runtime behavior or a new rerun feature implementation.

Scientific check-execution status, claim verdict, report verification, queue readiness, provider settlement and job execution state are separate. In particular, `succeeded` means the requested workflow produced an accepted, valid output under its pinned contract; it does not mean scientifically Verified or Supported. A truthful incomplete scientific report can be a valid workflow output only if its approved output contract allows it. Missing mandatory Council phases cannot masquerade as a completed Full Council execution.

| Entity | Proposed state | Meaning | Terminal? |
| --- | --- | --- | --- |
| Job | `queued` | Accepted with one pending attempt, awaiting capacity. | No |
| Job | `running` | One current attempt has claimed execution. | No |
| Job | `retry_wait` | Previous attempt ended; one replacement pending attempt awaits its retry deadline/capacity. | No |
| Job | `reconciliation_required` | Execution is stopped and prior attempt ended; uncertain external operations prevent automatic replacement. | No |
| Job | `cancellation_requested` | Cancellation won the guarded race; further scientific publication/dispatch is prohibited, local shutdown is being finalized. | No |
| Job | `succeeded` | Final workflow output accepted atomically. | Yes |
| Job | `failed` | Execution cannot continue under this job's policy/budget/attempt limits. | Yes |
| Job | `cancelled` | Logical cancellation finalized; external settlement may remain outstanding. | Yes |
| Attempt | `pending` | Allocated durably but never claimed; no worker lease. | No |
| Attempt | `running` | Claimed with current owner, fencing epoch and database-time lease. | No |
| Attempt | `cancellation_requested` | Cancellation prohibits execution/publication; cleanup acknowledgement or controller finalization remains. | No |
| Attempt | `succeeded` | Accepted final workflow output from this attempt. | Yes |
| Attempt | `failed` | Current worker reported a validated execution failure or inability to continue. | Yes |
| Attempt | `abandoned` | Control authority retired ownership after lease expiry or other explicitly authorized revocation. | Yes |
| Attempt | `cancelled` | Attempt logically cancelled, including never-claimed attempts. | Yes |

Reconciliation is job-level blocking plus separate external-operation records; it does not resurrect or mutate a terminal attempt. Finalized here means the state machine has no outgoing state transition, not that authorized retention/deletion or append-only settlement records cease to exist.

## 2. Actors, common guards and atomic effects

Actors below are logical responsibilities, not newly selected services/frameworks: API admission/cancellation handler, dispatcher, current worker, recovery controller and authorized reconciliation operator. The same executable may host several responsibilities; workers cannot grant themselves control-plane authority.

Every row requires **G0**: current action/resource authorization, exact job/analysis revision and expected predecessor versions, a recognized event/profile, pinned input/configuration identity, scoped idempotency and attributable audit. Every mutating writer uses the same short atomic database protocol. Unlisted transitions are rejected. Caller assertions alone never establish a guard.

- **G1 — worker ownership:** exact active attempt/step and current fencing epoch; matching worker owner; database time strictly before lease expiry; no cancellation/terminal/supersession blocker. At exact expiry, the lease is expired.
- **G2 — claim/admission:** valid confirmed immutable input snapshot where required, pinned policy/configuration, authorized provider-processing constraints, available shared capacity, pending-attempt eligibility and database-time retry deadline. Claims allocate a trusted epoch strictly later than prior ownership of the protected target.
- **G3 — publication:** G1 plus full candidate validation, exact evidence snapshot/manifest, scientific policy/configuration/schema, publication predecessor and staged-artifact eligibility under PG01–PG12. Accepted result, artifact relations, transition, operation decision and audit relation commit atomically.
- **G4 — safe replacement:** approved retryable failure/recovery cause, permitted attempt budget, admissible unchanged pinned context, durable completed-step inventory, and no unresolved external-call/permit uncertainty. Never infer safe replacement from lease expiry alone.
- **G5 — control ownership change:** exact current attempt/epoch and control authority; database-time expiry when expiry is the reason. Invalidate old ownership and prevent all later active writes from it. A new claim must allocate a strictly later epoch; no reset/reuse.
- **G6 — reconciliation:** attributable external-operation evidence or explicit replacement authorization, usage/reservation disposition and duplicate-cost risk recorded. An authorization to replace is not proof the original call ended and cannot free an unsettled concurrency permit.

All event payloads and cross-entity candidates undergo centralized whole-record validation. No status-only patch, operator override or retry endpoint may skip these guards. No transaction remains open during a scientific calculation or network/provider request.

## 3. Complete Job transition table — proposed

Each row below is an allowed edge with its own event and guards. `CREATE` is an initial creation event, not a stored state. Braced source sets explicitly enumerate the allowed sources for that row. There are no other state-changing edges.

| ID | From → To | Trigger | Responsible actor | Additional guards and atomic effects |
| --- | --- | --- | --- | --- |
| J01 | CREATE → `queued` | Submission accepted | API admission | Validate admission and immutable manifest; atomically create job, initial pending attempt and pending queue entry. Duplicate equivalent submission returns the existing authorized outcome. |
| J02 | `queued` → `running` | Initial claim wins | Dispatcher | G2; atomically claim pending attempt, allocate ownership/fence and lease, acquire analysis capacity and update queue eligibility. |
| J03 | `retry_wait` → `running` | Eligible retry claim wins | Dispatcher | G2; retry deadline reached and attempt budget already reserved; claim the replacement pending attempt atomically. No intermediate queued state required. |
| J04 | `running` → `succeeded` | Final valid output accepted | Current worker | G3; attempt becomes succeeded in the same transaction; finalize queue state and release only settled/releasable capacity. |
| J05 | `running` → `retry_wait` | Validated transient failure, safe retry | Current worker via transition handler | G1 and G4; end current attempt as failed; allocate exactly one replacement pending attempt, counted toward total limit, and durable retry deadline. |
| J06 | `running` → `failed` | Permanent failure or exhausted attempt/budget policy | Current worker via transition handler | G1; record safe execution reason and failed attempt; no scientific contradiction inferred. If external outcome is uncertain use J09 instead. |
| J07 | `running` → `retry_wait` | Abandoned owner, safe recovery | Recovery controller | G4 and G5; mark prior attempt abandoned, revoke lease, allocate one replacement pending attempt and retry deadline. |
| J08 | `running` → `failed` | Abandoned owner, replacement prohibited | Recovery controller | G5; preserve completed steps; record exhaustion/permanent blocker. If external outcome is uncertain use J10 instead. |
| J09 | `running` → `reconciliation_required` | Worker reports uncertain external outcome | Current worker via transition handler | G1; end attempt as failed with explicit uncertainty reason, revoke ownership, retain external request/reservation records; create no replacement. |
| J10 | `running` → `reconciliation_required` | Owner abandoned with possibly accepted external call | Recovery controller | G5; end attempt as abandoned; retain external uncertainty and permits; create no replacement. |
| J11 | `reconciliation_required` → `retry_wait` | Safe continuation/replacement authorized | Reconciliation operator via controller | G4 and G6; no scientific output promoted from late history; allocate one new pending attempt and retry deadline. Unsettled calls keep permits and may still block dispatch. |
| J12 | `reconciliation_required` → `failed` | No safe/authorized continuation | Reconciliation operator via controller | G6 or explicit attributable termination decision; retain unsettled external records without describing them as resolved. No new attempt. |
| J13 | `queued` → `cancelled` | Pending cancellation accepted | Authorized cancellation handler | Cancel pending attempt and queue entry atomically; no claim can subsequently succeed. |
| J14 | `retry_wait` → `cancelled` | Retry cancellation accepted | Authorized cancellation handler | Cancel replacement pending attempt/queue entry; preserve older attempts and steps. |
| J15 | `reconciliation_required` → `cancelled` | Cancellation accepted | Authorized cancellation handler | End logical job; preserve all unsettled external operations/permits and prior terminal attempt history. |
| J16 | `running` → `cancellation_requested` | Running cancellation wins publication race | Authorized cancellation handler | Set cancellation guard and attempt cancellation_requested atomically; revoke execution lease and forbid further provider dispatch/scientific publication. |
| J17 | `cancellation_requested` → `cancelled` | Local stop acknowledged or forced logical finalization | Cancellation/recovery controller | Exact pending cancellation revision; retire attempt as cancelled and clear active execution ownership. Worker acknowledgement is evidence, not independent authority. External settlement remains separate. |
| J18 | `queued` → `failed` | Nonrecoverable admission/configuration/authorization blocker discovered before claim | Authorized controller | Cancel never-claimed pending attempt with scheduling-stop reason; terminal job reason distinguishes failure from researcher cancellation. No retry under silently changed configuration. |
| J19 | `retry_wait` → `failed` | Nonrecoverable blocker discovered before replacement claim | Authorized controller | Cancel replacement pending attempt with scheduling-stop reason; preserve failed/abandoned predecessors. No implicit fallback. |

J17 must be controller-finalizable without worker cooperation; an unavailable worker cannot leave cancellation permanently dependent on an acknowledgement. The numeric intervention deadline and its operational alert remain open. J18/J19 distinguish a failed job from a cancelled never-executed attempt; `pending → failed` is intentionally not permitted because no execution occurred.

## 4. Complete Execution Attempt transition table — proposed

Attempt state changes must match the corresponding job transition in the same short transaction. There is no successful attempt publication followed by a separately attempted job-state update.

| ID | From → To | Trigger | Responsible actor | Guards and paired effect |
| --- | --- | --- | --- | --- |
| A01 | CREATE → `pending` | Accepted submission or authorized replacement allocation | Admission/transition/recovery controller | J01, J05, J07 or J11 only; unique next attempt ordinal within total budget, pinned snapshots, one pending replacement and durable queue relation. |
| A02 | `pending` → `running` | Claim wins | Dispatcher | G2; J02 or J03; trusted strictly later fence, owner, lease and capacity established atomically. |
| A03 | `running` → `succeeded` | Accepted final workflow result | Current worker | G3 and J04; durable accepted output, no unsettled required operation that blocks successful workflow completion. |
| A04 | `running` → `failed` | Validated execution error or uncertain-call report | Current worker via transition handler | G1; J05, J06 or J09 selected by safe retry/permanent failure/uncertainty classification. Preserve completed outputs. |
| A05 | `running` → `abandoned` | Expired/revoked ownership retired | Recovery controller | G5; J07, J08 or J10; append reason and invalidate ownership, without claiming provider failure. |
| A06 | `running` → `cancellation_requested` | Running cancellation accepted | Authorized cancellation handler | J16; atomically revoke execution permission and block publication/dispatch. |
| A07 | `cancellation_requested` → `cancelled` | Logical cancellation finalized | Cancellation/recovery controller | J17; exact cancellation predecessor; late data may be recorded only as history/settlement. |
| A08 | `pending` → `cancelled` | Pending job cancellation or scheduling stop | Authorized cancellation/controller handler | J13, J14, J18 or J19; prohibit later claim; retain allocated ordinal/history. |

Terminal attempts (`succeeded`, `failed`, `abandoned`, `cancelled`) have no outgoing state transitions. Recovery never returns an abandoned attempt to running. A cancelled pending attempt still counts as an allocated attempt; cancellation ends its job, so it cannot be used to evade the total-attempt cap.

## 5. Cross-state invariants

| Job state | Required attempt relationship |
| --- | --- |
| `queued` | Exactly one pending initial attempt; no running/cancellation_requested attempt. |
| `running` | Exactly one active running attempt; no pending replacement; an expired lease can exist until recovery, but authorizes no execution/publication. |
| `retry_wait` | Exactly one pending replacement; all predecessors terminal. |
| `reconciliation_required` | No pending/running/cancellation_requested attempt; latest execution attempt failed or abandoned; at least one explicit unresolved external operation or replacement-authorization blocker. |
| `cancellation_requested` | Exactly one corresponding cancellation_requested attempt with execution permission revoked; no pending replacement. |
| `succeeded` | Exactly one successful terminal attempt and accepted final publication; no executable attempt. |
| `failed` | No executable attempt; latest attempt failed, abandoned or cancelled with explicit job failure reason. |
| `cancelled` | No executable attempt; latest attempt cancelled, failed or abandoned according to cancellation path; no post-cancellation accepted final result. |

Additional invariants:

1. Job identity, analysis revision, evidence snapshot/manifest, classifications, policy and execution configuration remain pinned. Amendments do not mutate an executing snapshot; a superseded target blocks further publication and requires authorized cancellation/new execution scope.
2. At most one executable attempt per job. A reserved pending replacement is not current execution ownership. Attempt ordinals never reset; default cap is three total attempts, not three retries.
3. Ownership epochs strictly increase over replacements capable of writing the same protected target. A worker token must equal current trusted ownership; a larger submitted token is not authority. Terminal history cannot be overwritten by late workers.
4. Analysis-capacity reservations are shared across processes and not inferred from state counts alone. They cover running execution, cancellation cleanup and any uncertain surviving local execution until safe release. Recovery cannot free capacity merely because a lease expired; explicit termination/isolation evidence or retained reservations are required before replacement starts.
5. External requests require durable intent/reservation before dispatch. A crash after dispatch intent but before outcome persistence is potentially accepted/paid until reconciled. Separate provider/global and per-analysis permits persist across logical cancellation/ownership loss until settlement allows release. A new attempt cannot overlap an unresolved call by relabeling it as another attempt.
6. External settlement, logical state and cost reconciliation are separate. A terminal job may retain unsettled calls, but cannot launch replacement calls. Operator replacement authorization cannot waive concurrency/spending limits or scientific guards.
7. Completed step records and accepted outputs remain durable and immutable. New attempts may reference them only after explicit validation of all input/policy/configuration dependencies and reuse eligibility. Late/rejected/staged artifacts never become accepted steps automatically.
8. All paired job/attempt/queue/capacity changes and required operation/audit relations are atomic; storage bytes and provider operations are not made atomic by database transactions. Unknown database commit outcomes require reconciliation, not a new execution.
9. Current ownership and authorization are required even for error/checkpoint writes. Invalid/stale transitions produce safe rejection/audit/reconciliation, never a fallback state change.

## 6. Events that do not change lifecycle state

Successful heartbeat renewal keeps running/running, conditioned on G1, database time and exact owner/fence. Renewal after expiry is rejected, not resurrection. Checkpoints keep running/running under publication guards and persist complete validated provisional step records. Neither consumes another attempt.

Development defaults remain exactly 30-second lease, 5-second heartbeat, 2-second heartbeat timeout, threshold two missed heartbeats, polling within 1–3 seconds, maximum three total attempts, retry base two seconds and cap fifteen seconds, exponential backoff with full jitter. These are not pilot/production settings. Two missed heartbeats require the worker to stop initiating work and report uncertainty where possible; they do not shorten the authoritative 30-second lease or prove the external request ended. Exact timeout coverage, retry-index/jitter formula, polling selection and intervention deadlines remain bounded planning items; no new values are chosen here.

Equivalent operation replays return the existing authorized outcome without another transition. Conflicting replay is rejected. Late responses append authorized historical/settlement observations only; they cannot change terminal attempt/job states. Lost publication acknowledgements are reconciled against the durable operation record before any retry.

## 7. Invalid transitions and race ordering

Every edge not listed in J01–J19/A01–A08 is invalid, including terminal-to-running, running-to-queued, reconciliation-to-succeeded, abandoned-to-running and pending-to-succeeded. Invalid actor, guard failure, missing required fact or incompatible job/attempt pairing rejects even a listed edge. Report scientific status must never be used as a job-state command.

Concurrent claimers compare the same pending predecessor; one may win. Claim versus pending cancellation has one atomic winner: if claim wins, cancellation must be reevaluated as running cancellation, not applied using a stale pending snapshot. Final publication versus cancellation similarly has one atomic winner: accepted success prevents later cancellation from rewriting it; accepted cancellation prohibits success. Repeated cancellation returns the existing authorized outcome without advancing epochs or creating attempts again.

Recovery versus renewal compares authoritative lease/state/version atomically. A renewal committed before expiry can prevent recovery; renewal at/after expiry cannot restore the lease. Recovery/cancellation races cannot allocate a runnable replacement after cancellation wins. Stale worker failure cannot replace newer success. A lease boundary is evaluated using database time inside the short acceptance operation, not the worker clock or a precomputed timestamp.

Suspension/deletion/revocation prevents new dispatch and scientific publication; an authorized controller then applies only listed cancellation/failure edges. Restoring access does not reopen a terminal job. Permission removal and publication must participate in the same guard protocol. No override endpoint may force a transition that bypasses ownership or whole-record validity.

## 8. Recovery and review obligations — unexecuted

| Scenario | Expected contract observation |
| --- | --- |
| Crash before claim | Pending attempt remains eligible; no duplicate accepted claim. |
| Crash after claim, no uncertain operation | Expiry/revocation retires attempt; safe recovery allocates at most one replacement within budget and capacity. |
| Crash during provider dispatch or response persistence | Job enters reconciliation_required, with no automatic paid replay and no premature permit release. |
| Lost final commit acknowledgement | Durable accepted operation is returned after authorized reconciliation; no second final result. |
| Completed steps then crash | New attempt references only reuse-eligible accepted outputs; previous records stay intact. |
| Cancellation with dead worker | Controller finalizes logical cancellation without waiting forever for acknowledgement; uncertain calls remain tracked. |
| Two concurrent recovery controllers | One predecessor transition/replacement wins; other rejects or returns the same authorized idempotent outcome. |
| Retry exhaustion | Third allocated attempt is the last under development defaults; no fourth allocation or terminal reopening. |
| Stale success/error/checkpoint | All reject active mutation even if scientific payload is valid. |
| Every source/destination pair | Future tests enumerate all job/attempt pairs, listed triggers, actor/guard failures and forbidden edges; no unlisted edge succeeds. |

These are refinements of existing lifecycle/publication obligations, not executed tests or additional gates. Both tables and their paired invariants received owner section approval for planning on 2026-11-06. Implementation, formal gate closure and capability enablement remain unauthorized. Later changes to these approved planning semantics require review.
