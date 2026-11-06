# EvidenceTwin V1 — Lease, retry and reconciliation rules

**Status: Recommended for owner approval.** Date: 2026-11-06. This is the next bounded planning section after approval of the [Job and Attempt tables](JOB_ATTEMPT_TRANSITIONS_DRAFT.md). All **24 gates remain OPEN**. The owner approved this section for planning on 2026-11-06; no production code, deployment or capability enablement is authorized. No new scientific procedure, product or infrastructure value is selected.

## 1. Lease and heartbeat rules proposed for review

Use the same authoritative database-time basis for claiming, renewal, expiry, retry eligibility and publication. Exact PostgreSQL expression/isolation remains an implementation-planning item: it must evaluate current acceptance time rather than a stale worker timestamp or transaction-start value after a prolonged wait.

| Event | Required rule |
| --- | --- |
| Claim | In one short atomic operation acquire eligible pending attempt and shared analysis capacity, allocate a strictly later trusted fence, assign owner and set expiry to authoritative acceptance time plus the configured 30-second development lease. |
| Renew | Every configured five seconds, request renewal for exact job/attempt/owner/fence and expected lease revision. Renew only while running, uncancelled and unexpired. Proposed expiry is acceptance time plus lease duration, not repeatedly adding duration to the prior expiry. |
| Renewal timeout | The configured two seconds is proposed to cover the entire heartbeat database operation, including waiting for a connection/lock and commit acknowledgement. Deadline enforcement/cancellation must be supported by the eventual driver configuration. Timeout is an unknown outcome until reconciled, not evidence that no commit happened. |
| Missed renewal | No trustworthy acknowledgement by the deadline counts as one consecutive miss. Two consecutive misses trigger local stop-new-work and a diagnostic/reconciliation attempt. A definitive ownership/cancellation rejection triggers immediate stop without waiting for two misses. |
| Uncertain ownership | From the first uncertain renewal, pause new provider dispatch and step initiation until authoritative ownership is confirmed; do not publish using a cached lease. An in-flight call is tracked through settlement. The two-miss threshold escalates local shutdown; it does not authorize work during uncertainty. |
| Reconnect | Reconcile the current owner/fence, state, lease and renewal operation. Resume only if the same running attempt remains authoritative and the lease is valid. At/after expiry, renewal is rejected; recovery must use a new attempt. |
| Publication | Require the current database-time lease and all publication guards atomically. Preparing output before expiry does not grant publication after expiry. |
| Recovery | Controller uses J07/J08/J10 only after exact predecessor and database-time expiry or separately authorized revocation. Missed heartbeat count is diagnostic, not a substitute for this guard. |

No database transaction spans a five-second heartbeat interval, calculation or provider call. No process-local timer grants ownership. Delayed/duplicated heartbeat messages cannot renew a replaced attempt or roll expiry backward. Duplicate renewal acknowledgement must refer to the same committed renewal; it must not extend the lease again as an accidental replay.

## 2. Retry rules proposed for review

The existing defaults remain three total allocated attempts, two-second base delay, fifteen-second cap, exponential backoff with full jitter. Attempt one is initial execution; only attempts two and three are available as replacements. Claim contention and equivalent request replays do not allocate attempts. Allocation and attempt-limit enforcement are atomic.

Proposed precise convention: for a replacement after attempt ordinal n, draw one delay uniformly from zero through `min(15 seconds, 2 seconds × 2^(n−1))`, subject to the final selected duration precision. Thus the first replacement has a two-second upper bound and the second a four-second upper bound under current defaults. The fifteen-second cap remains configurable for larger separately authorized attempt limits. Record the selected delay once and persist the database-time eligibility deadline; controller restarts must not redraw it to bring a job forward.

This formula is a proposal for approval, not an executed statistical procedure. Tests would inject a controlled random source rather than asserting exact production random outcomes. A validated provider Retry-After/cooldown may delay eligibility further; it must not be shortened to the local fifteen-second jitter cap. Maximum wait/deadline policy remains open rather than silently retrying earlier.

| Failure class | Scheduling action |
| --- | --- |
| Proven transient failure before external acceptance, or safe settled transient failure | J05/J07 if all G4 guards and attempt budget pass. |
| Invalid input, incompatible contract/configuration, forbidden access or unsupported operation | No automatic retry; J06/J08 or J18/J19 as applicable. |
| Possibly accepted paid request, lost provider result or uncertain publication commit | Reconcile before scheduling replacement. Database commit uncertainty first queries the durable operation record; it must not trigger provider replay. |
| Attempt limit exhausted | No replacement allocation. Fail with explicit exhaustion reason unless uncertainty first requires J09/J10. |

Transient classification must be explicit in the future adapter error contract. Generic timeout or HTTP 5xx alone does not prove a paid operation was not accepted. Replacement uses unchanged pinned inputs/configuration; fixing inputs or changing provider/model requires a new authorized execution scope, not silent retry mutation.

## 3. Reconciliation actions proposed for review

Persist external dispatch intent and capacity/spend reservation before sending the request. Track original attempt/step/fence, stable logical request identity, provider configuration reference, request identifier where available, send/observation timestamps, safe failure metadata and reservation relationships. Do not log credentials or private evidence payloads as diagnostics.

| Established situation | Permitted action |
| --- | --- |
| Existing committed publication found after lost acknowledgement | Return its currently authorized outcome; do not publish again or replay the provider call. |
| Provider proves request was not accepted, with no surviving local execution | Record attributable evidence; release only justified reservations; consider G4/J11 safe replacement. |
| Request completed and late result is available | Retain authorized late result/usage as historical settlement evidence. Under the approved tables it does not revive a terminal attempt or directly move reconciliation_required to succeeded. Any later reuse requires separately approved exact dependency/reuse validation. |
| Provider proves terminal failure/settlement | Record outcome and actual/unknown cost separately. Release request concurrency only with evidence the call ended; financial reconciliation may remain open. Consider replacement only if retryable and within all bounds. |
| Acceptance/completion cannot be established | Keep explicit uncertainty, retain applicable permits/reservations, and require attributable operator replacement authorization before any replacement paid request. Such authorization cannot release concurrency permits or waive budgets. |
| Researcher cancels or operator terminates | Use J15/J12, respectively. Logical termination preserves unresolved external records and blocks replacement under the terminal job. |

Unknown provider settlement does not become settled just because the worker lease expires, a new worker starts, an operator acknowledges an alert or the job becomes terminal. Provider-supported cancellation must itself be observed/reconciled; sending a cancellation request is not confirmation. No automatic provider fallback is introduced.

Analysis-execution capacity and provider-request permits have separate release proofs. Local worker process termination/isolation may establish that local execution stopped; it does not establish external settlement. If execution termination cannot be established, preserve its capacity reservation and block unsafe replacement. This deliberately favors bounded execution over automatic throughput.

## 4. Planned verification and remaining limits

Future PostgreSQL concurrency tests must cover acknowledgement loss, renewal/expiry boundary, renewal-versus-recovery, concurrent replacement allocation, deterministic retry deadlines across restarts, cancellation during renewal/provider calls, stale result rejection, durable completed steps, and held permits for uncertain calls. Test clocks/randomness may be controlled through explicit test interfaces; real production lease decisions still use database time. No tests are executed by this document.

Unresolved items remain visible: controller-finalization/intervention deadlines; exact polling choice within 1–3 seconds; provider-specific settlement evidence and idempotency support; resource termination/isolation proof; driver/database timeout mechanics; short-transaction implementation; audit persistence under outage; and per-step reuse approval. These do not change the existing defaults or close gates. Until resolved, affected behavior cannot be represented as implemented or pilot-ready.

Review this section before proceeding to the implementation-file and PostgreSQL-test mapping. The broader scientific design remains paused.

**Section review record:** Owner section approval received on 2026-11-06. This approves the rules for planning only; it closes no gate and does not authorize implementation, deployment or scientific capability enablement.
