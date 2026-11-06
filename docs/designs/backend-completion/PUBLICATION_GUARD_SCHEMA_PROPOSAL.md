# EvidenceTwin V1 — Candidate publication guard schemas

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** All **24 gates remain OPEN**. This is a candidate refinement of the owner-selected conditional/version-guarded publication direction, following the [guard-coverage contract](VERSION_GUARDED_PUBLICATION_DRAFT.md). Names, discriminants, transition rules, storage types and API projections below are proposed, not formally approved. No production implementation, deployment or capability enablement is authorized. PostgreSQL was a candidate when this proposal was drafted; it is now owner-selected, with Core/Psycopg 3/Alembic selected for refinement. Provider/region/deployment remain open. No statistical method or implementation library is selected. Partially Supported remains a proposed, unresolved claim verdict. Acceptance examples remain unexecuted specifications.

## 1. Trust and type boundaries

A worker supplies expected identities and a candidate result. It cannot supply authoritative permissions, assign its own fencing epoch, declare itself current, or decide that a mandatory scientific requirement is waived. Treat all incoming fields as untrusted until validated.

The following are conceptual types, not Python models, wire DTOs or database tables:

| Candidate type | Meaning and constraints |
| --- | --- |
| `Ref<T>` | Stable typed identifier for a particular entity; identifiers from different entity classes are not interchangeable. |
| `RevisionRef<T>` | Exact immutable revision identity, with its parent entity relation validated. No implicit latest-version lookup. |
| `FenceEpoch` | Trusted, ordered ownership epoch; exact storage representation, allocation scope and exhaustion handling remain open. Equality with current ownership is required for worker writes. |
| `ContentIdentity<T>` | Identity of validated content under an approved canonicalization/digest procedure; that procedure remains open. A digest alone establishes neither authorization nor scientific validity. |
| `Expected<T>` | Untrusted caller assertion about the predecessor/current context. It becomes a comparison operand, never authoritative state. |
| `Required<T>` | Explicit value required by the selected operation profile. Unknown or absent is a rejection, not a default. |
| `NotApplicableToOperation` | Explicit, profile-defined guard exemption with a profile/rule reference; distinct from scientific Not Applicable. Callers cannot invent exemptions. |

Nullable values must not erase a required guard. A profile specifies whether a field is required or explicitly not applicable. Unknown tags, extra incompatible branches and missing required references fail validation. Scientific typed absence continues to follow the [separate contract](EXPLICIT_ABSENCE_CONTRACT_DRAFT.md).

## 2. Candidate request family

Proposed discriminated family: `PublicationCommand = WorkerPublication | ControlTransition | LateResponseRecord`. This separates authority and purpose; it does not select final tags or legal job states.

Common candidate fields:

| Field | Required meaning |
| --- | --- |
| `command_contract_ref` | Exact command schema revision. |
| `operation_id` | Stable logical operation identity, scoped to the authorized owner/resource/action under an approved idempotency policy. |
| `operation_profile_ref` | Versioned server-recognized guard/transition profile; server authorizes its use. |
| `target` | Exact case, analysis revision, job and publication target references. |
| `expected_predecessor` | Expected job state/version and publication/record predecessor appropriate to the profile. Explicit initial-publication branch prevents ambiguous null-as-no-predecessor. |
| `payload_ref` | Exact immutable prepared payload, where this operation carries one; content identity and schema reference are bound to it. |

`WorkerPublication` additionally requires expected attempt and execution-step references, ownership epoch, immutable evidence manifest revision, classification revision when required, scientific policy bundle revision and execution configuration revision. Its proposed purpose distinguishes checkpoint, final result and execution failure. Each uses a complete candidate record; failure is not an unguarded status patch.

`ControlTransition` carries the expected prior attempt/ownership context and a requested retry, recovery, cancellation or other reviewed control action. Replacement attempt identity and fencing epoch are allocated by trusted state, not accepted as worker-chosen values. Control authority is checked independently from worker ownership.

`LateResponseRecord` identifies the original call/attempt/epoch and observed response artifact. It may record settlement or rejection history under current authorization, but cannot mutate the active scientific result or reopen a terminal job. Acceptance of a historical observation does not accept its scientific output.

The authenticated actor is derived from trusted request/session/service context, not an actor ID supplied in this command. Provider secrets and raw credentials are excluded.

## 3. Authoritative guard facts and validation binding

`GuardFacts` is a conceptual server-side view, not a public response or caller-supplied object. It includes current target ownership and authorization, job state/revision, active attempt/step and epoch, analysis and evidence revisions, cancellation/terminal/supersession state, pinned policy/configuration, publication predecessor and operation history, and eligible artifact metadata. Every fact has an identified authority and consistency requirement.

Facts read before preparation may become stale. Only the facts protected by the atomic acceptance protocol decide publication. Comparing an old permission snapshot or locking only the result row does not protect a concurrent permission or cancellation change. Every writer of protected facts must participate in the same reviewed consistency protocol.

A proposed `ValidationBinding` ties the full candidate's content identity to exact validator/schema/policy revisions and its observation/provenance/artifact references. It records what was validated, not permission to publish later. An ordinary worker-supplied “valid” flag is insufficient. The trusted publication boundary must independently validate, or verify a trusted validation record whose provenance and exact binding satisfy an approved protocol. Final mutable guards are always checked again at acceptance.

Separate observations and provenance remain separate records. A completed execution does not establish scientific satisfaction. Performed-but-unresolved, blocked, errored, cancelled, pending/running and justified Not Applicable must retain their canonical semantics. No field-level update bypasses whole-record validation.

## 4. Candidate operation profiles

All profiles enforce exact target identity, current authority, schema validity, operation identity/content and applicable predecessor guards. PG labels refer to the [existing twelve guards](VERSION_GUARDED_PUBLICATION_DRAFT.md); these rows are not additional gates.

| Profile | Ownership and context | Permitted effect and additional requirements |
| --- | --- | --- |
| Worker checkpoint | Current job/attempt/step/epoch and expected state; exact pinned input/policy/configuration | Persist a validated provisional record, explicitly ineligible as a final finding/report. |
| Worker final result | Same current ownership plus eligible cancellation/terminal state and publication predecessor | Accept exact candidate and artifacts only after all applicable PG01–PG12 checks. Final aggregate and Complete report have additional scientific eligibility predicates. |
| Worker execution failure | Same current ownership and pinned context | Record the actual execution error and permitted transition. Cannot overwrite a newer success or fabricate a scientific Contradicted verdict. |
| Retry/recovery | Current control authority, exact predecessor state/attempt/epoch and approved retry/recovery condition | Atomically establish replacement ownership and later epoch. Preserve old attempt. External-call settlement is a separate prerequisite where required. |
| Cancellation | Current control authority and exact target/state/revision | Record cancellation under the reviewed transition policy; invalidate conflicting publication atomically. In-flight external calls remain tracked until settlement. |
| Late response/history | Authorized historical target/call relation; original identities retained | Append permitted audit/settlement facts only. Never claim current ownership or attach late output to a replacement attempt. |
| Revision/operator/deletion change | Current specific authority and exact affected revision/predecessor | Apply only the reviewed mutation; invalidate or advance all affected guard facts. No administrative bypass of scientific validity. |

A retry request is not a replacement allocation. A worker may request retry but cannot advance its fence. Exact legal state transitions, retry eligibility and epoch allocation scope remain open. Artifact requirements apply to actual payloads; an error without generated artifacts must not invent artifacts to satisfy a profile.

## 5. Atomic decision and outcome family

The proposed durable `OperationDecision` family has Accepted, Rejected and ConflictingReplay branches. Acknowledgement replay refers to an already committed decision and rechecks current response authorization. An unknown commit outcome is a transport/reconciliation state, not a fabricated durable decision.

| Outcome | Meaning |
| --- | --- |
| Accepted | Atomic guarded persistence committed: accepted result relation, allowed state transition, operation outcome, artifact acceptance metadata and required audit references agree. |
| Rejected | Applicable guard failed; no active result/job mutation. Record a safe rejection reason and authorized reconciliation reference. |
| Equivalent acknowledgement replay | Return the existing permitted outcome after exact operation scope/content equivalence and current response authorization. No republishing or renewed paid call. |
| Conflicting replay | Same scoped operation identity with incompatible intent/content; reject without overwrite or merge. |
| Commit outcome unknown | Do not report acceptance or durable rejection. Reconcile the authoritative operation record before retrying mutation. Never replay science/paid requests merely to recover an acknowledgement. |

Candidate outcome fields are operation reference, outcome kind, trusted decision timestamp, target/publication references where authorized, safe reason code, correlation reference and audit/reconciliation references. A stale caller must not learn private current revisions or record existence from rejection details.

The physical mechanism for durable rejected-attempt audit, contention and database outage recovery remains unresolved. It must avoid making audit persistence depend on the stale worker's forbidden update. A separate audit write cannot be described as atomically committed with publication unless the chosen protocol actually guarantees that relation. Failure to persist an audit record must remain an explicit operational gap; no successful audit acknowledgement may be invented.

Idempotency retention, canonicalization, operation-key scope, semantic equivalence and replay visibility are still approval items. Same bytes with different evidence/policy/attempt references are not interchangeable scientific publications.

## 6. Candidate artifact relationships

Keep physical object availability separate from acceptance. Proposed metadata branches are Staged, AcceptedForPublication and RejectedOrOrphaned; deletion and integrity are independent constraints rather than assumed success states. Exact names and lifecycle remain proposals.

An artifact reference binds stable artifact ID, exact immutable object/version identity, hash and algorithm, ownership, media/size metadata and producing attempt/step. The accepted relation additionally binds the committed publication and exact manifest revision. Matching a hash does not authorize cross-account reuse.

Before commit, staged derived objects must not appear through accepted-result lists, reports, exports or accepted-result download links. Submitted input inspection is a separate authorized path. Unknown commit outcomes prohibit automatic orphan deletion until reconciliation establishes whether the object is referenced by a committed publication.

Database guards do not create atomicity with the physical object store. The design still needs a reviewed readiness/integrity protocol, deletion coordination, crash recovery and authorized read-time behavior when an accepted object is missing. Never overwrite immutable evidence or expose an unaccepted result to conceal a storage inconsistency.

## 7. Required unexecuted contract examples

These refine existing LP, TA, CF, CR and AC obligations; they do not add a new counted acceptance family or claim executed coverage.

- Reject wrong job/attempt, obsolete epoch, mismatched revision, evidence manifest, policy or configuration; leave accepted state unchanged.
- Race final result with cancellation, recovery, suspension and revision change; only a guard-consistent outcome may commit. Exact legal ordering follows the still-open transition specification.
- Reject a forged validation record, partial field patch or invalid typed-absence proof even when worker ownership is current.
- Recover a lost acknowledgement without duplicate publication; reject operation-key reuse with different context/content.
- Audit late failure/success without overwriting terminal state; retain external settlement obligations.
- Keep staged artifacts out of accepted views; reconcile unknown commit before cleanup; handle missing physical objects without reporting successful export.
- Exercise every non-worker writer against the same guard invariants, including operator repair, import and deletion.

## 8. Remaining formal design work

Before formal approval, resolve exact field/tag definitions and transition tables; authoritative fact ownership and atomicity across all writers; fencing allocation, bounds and ownership scope; validation-record trust; operation equivalence/retention; rejected-attempt audit and unknown-commit recovery; artifact/deletion coordination; authorization consistency; and public error/projection schemas. No candidate database or transaction isolation level is selected by this document.

The next refinement should specify the operation transition and guard-validity matrix, including rejection precedence and safe observable outcomes, before considering any transaction implementation. All 24 gates remain OPEN and all scientific acceptance requirements remain unresolved until their own review and approval.
