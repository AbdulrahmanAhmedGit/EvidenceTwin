# EvidenceTwin V1 — Check lifecycle and guarded publication

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R01 after approval to continue from the [typed dimensions/validity matrix](TYPED_CHECK_AXES_DRAFT.md). Separate Typed Axes remains the recommended direction. Exact enum names, legal transitions, persistence/API projections, locking and validation implementations are proposals, not final selections. **All 24 gates remain OPEN.** Partially Supported remains a proposed/unresolved verdict. Acceptance obligations are unexecuted; no production code, method/library selection, deployment or enablement is authorized.

## 1. Four operations that must not be confused

| Operation | Contract and permissible output |
| --- | --- |
| Admit a canonical check record | Whole-record shape, scope, applicability and state predicates pass. Valid Pending/Blocked/Error/Unresolved records can be retained and shown with their actual meaning. Validity does not imply scientific satisfaction. |
| Admit a scientific finding | Its specific procedure/proof/assurance predicates pass for the declared finding. A reproducible computation can be visible with an unverified source limitation; it cannot claim assurance it does not have. |
| Produce a report/progress view | May truthfully show incomplete work, missing evidence, failed gates and retained assessments. This does not authorize unconfirmed final aggregation or a Complete verification label. |
| Publish an active final assessment/version | Current authorization, attempt/revision/fencing, confirmation and assessment eligibility guards hold. A report marked Complete additionally satisfies every mandatory claim/report requirement; an eligible Incomplete report preserves its blockers. |

The prohibition is against **invalid or misrepresented publication**, not against displaying valid incomplete scientific work. Missing mandatory evidence blocks Complete verification; it does not require hiding all results. Unconfirmed materiality/roles still block final report-level aggregation, while independent assessments and progress remain inspectable.

This distinction clarifies the earlier phrase “unresolved-mandatory publication”: unresolved mandatory requirements prohibit representing verification as Complete, but a valid report can explicitly be Incomplete. No existing coverage/report/conclusion rule is relaxed.

## 2. Candidate operation contracts

These are semantic operations for review, not finalized endpoint names or an approved transition graph. Every operation validates the complete candidate record through the centralized contract, including unchanged dimensions. Forbidden transitions cannot be made possible by patching one dimension at a time.

| Operation | Preconditions to specify/enforce | Candidate result and audit facts |
| --- | --- | --- |
| Accept/check requested | Authorized exact scope, declared policy/procedure and truthful availability status; accepted attempt identity if scheduled. | Pending or explicit Blocked record; no Satisfied determination. Record requested scope/configuration. |
| Start scientific work | Current valid claim/ownership, allowed applicability and satisfied dispatch prerequisites. | Running facts with actual start/attempt/fence; requirement remains unestablished. No transaction held during long work. |
| Record checkpoint | Current ownership/scope and whole-record validity; explicitly provisional observations if any. | Progress/diagnostics without final satisfaction or claim verdict inferred from partial output. |
| Record blocked prerequisite | Explicit unavailable input/method/authorization context and actual performed scope. | Blocked-before-performance or performed-unresolved as applicable, not an interchangeable generic failure. |
| Finalize performed result | Complete procedure output, identity/provenance and positive/negative/unresolved proof predicates; current publication guards. | Performed facts plus Satisfied, Not satisfied or no established determination, according to the actual requirement. |
| Record technical error | Actual error/performed scope and safe reason; no invented final output. | Error record with diagnostics and approved recovery eligibility, not scientific contradiction. |
| Cancel work | Authorized cancellation and exact target attempt; shared execution policy applies. | Logical cancellation and dispatch prevention for work not yet sent. In-flight call settlement remains separate. |
| Establish Not Applicable | Approved rule and evidence justify applicability for this scope. | Separate applicability proof and no falsely performed scientific procedure. An unavailable method is not sufficient justification. |
| Retry/re-evaluate | Approved safe-replay/replacement authority, inputs/policy/configuration pinned and uncertainty reconciled where required. | Attributable attempt/result revision under the approved recovery contract; no overwritten historical outcome. |
| Amend evidence/classification | Authorized correction/confirmation and an exact parent revision. | New immutable scope/revision and explicit affected-result eligibility; old report remains historical. |

The exact conditions for resuming an unfinalized blocked candidate versus creating a new step/attempt remain OPEN. Already finalized results cannot be silently edited either way. Updating attempt cancellation does not retroactively convert a previously performed historical check into “never performed.”

## 3. Whole-record mutation contract

A mutation request supplies the intended complete candidate change and the predecessor/scope it was based on. Exact fields, operation-key format and error DTOs remain OPEN. The canonical validator must:

1. Authenticate/authorize the operation against trusted application scope; do not trust owner/role/validity flags supplied by a client or model.
2. Resolve the expected predecessor, exact evidence/classification revision, attempt ownership and approved policy references. A mismatch is a conflict/blocker, not a command to edit the newest available record.
3. Form the complete candidate record, retaining dimensions not intentionally changed.
4. Validate all typed dimensions, the whole-record validity matrix, allowed operation semantics and scientific provenance/eligibility.
5. Guard the authoritative commit against concurrent changes to the relevant permission, predecessor, cancellation, scope and fence.
6. Retain attributable mutation/result/audit facts under the approved transaction and artifact-consistency design; publish no success acknowledgement until the corresponding authoritative acceptance occurred.

An invalid candidate does not become an authoritative partial record. Safe rejected-operation diagnostics may be retained separately under approved access/logging policy. Operator and recovery utilities obey the same scientific validity rules; elevated operational authority is not a scientific bypass.

### Duplicate requests and uncertainty

The eventual idempotency contract must scope a repeated operation to the authorized actor/case/attempt/operation identity and candidate content. Equivalent repeats may resolve to the same accepted logical operation under a reviewed rule; conflicting content under the same identity cannot silently replace it. Authorization is checked before exposing an earlier acknowledgement, so replay lookup cannot leak another account's record.

The operation identity storage/commit mechanism remains OPEN. Idempotent local writes do not promise exactly-once LLM execution. A lost acknowledgement after acceptance must be reconciled against durable state; it does not authorize a replacement paid call.

## 4. Guarded publication predicate

Before an active result/report version is committed, validate the whole record and establish all relevant predicates against authoritative current state:

| Predicate | Meaning |
| --- | --- |
| Authorized | The actor/execution principal still has permission for this case, resource and action. Identity possession or an old permission read is insufficient. |
| Exact scope | Case, claim/evidence/classification revisions and temporal layer match the target assessment. No historical/current substitution or implicit newest-version lookup. |
| Current ownership | Attempt, worker ownership/fence and active publication target are valid; cancelled/superseded work cannot overwrite the active version. |
| Approved version use | The pinned policy/procedure/configuration is admissible for this attempt under the approved version-use policy. “Newest” is not automatically required or scientifically equivalent. |
| Canonical validity | Complete candidate satisfies dimension types, matrix, operation constraints and evidence/provenance correspondence. |
| Assessment eligibility | Approved verdict predicates and citations hold. Partially Supported remains an unresolved proposal and cannot enter final aggregation through a fallback mapping. |
| Confirmation | Required confirmed roles/materiality, scope/bindings and processing authorization refer to this exact revision; preparatory proposals do not count. |
| Honest verification label | Coverage and mandatory report gates justify the claimed status. Incomplete work remains Incomplete with explicit blockers; no label inferred from job/model completion. |

These predicates require a guarded commit, not merely an earlier validator call. The owner subsequently selected [conditional/version-guarded publication](VERSION_GUARDED_PUBLICATION_DRAFT.md) as the recommended primary refinement direction, with short atomic transactions, monotonic fencing and comprehensive write-path guards. Exact predicate/schema/transaction/isolation and external authorization/artifact coordination remain OPEN. No engine-specific SQL, locking library or API token scheme is selected; long-lived pessimistic locking is not the primary strategy.

The resulting authoritative publication must be attributable to the exact validated scope. If a required guard cannot be established, fail safely with an explicit reason and retain permitted evidence rather than claiming publication. Audit atomicity, object finalization and public visibility timing require concrete D01/D02/D05/D06 specifications; they are not solved by this prose.

## 5. Concurrency and race specifications

All rows are unexecuted specifications for review. They express invariants rather than observed behavior or a selected database concurrency algorithm.

| Race | Required semantic behavior |
| --- | --- |
| Cancellation versus worker start | Respect authoritative ordering; no start/dispatch after a cancellation that has become effective under the approved contract. If dispatch already happened, track the remote outcome instead of pretending cancellation revoked it. |
| Cancellation versus final result | A cancellation effective before publication prevents active publication by that attempt. Already finalized historical work remains visible with its original meaning where authorized. |
| Lease expiry/reclaim versus old-worker response | Old ownership/fence cannot publish into the reclaimed attempt. Lease expiry does not prove the old provider request ended or authorize blind replay. |
| Evidence/classification amendment versus result commit | Reject publication into a superseded target; preserve correct historical scope. Creating a new revision does not rewrite unrelated immutable historical results. |
| Account suspension/revocation versus publication | Enforce the approved authorization consistency/revocation contract at publication. Exact ordering and any bounded propagation policy remain OPEN; do not claim instantaneous global revocation without a mechanism. |
| Duplicate finalization | At most one accepted logical publication for the same protected operation/version; equivalent acknowledgement replay is scoped/authorized, conflicting payload is rejected. |
| Object write versus database acceptance | Do not publish a report whose required accepted artifact references cannot resolve. Missing/orphan objects require explicit acceptance/reconciliation states under the eventual storage design. |
| New policy/configuration versus running attempt | Use the pinned version under an approved admissibility policy; no silent method/model substitution or assumption that “latest” can reproduce the same result. |
| Operator repair versus scientific result | Repair may create an attributable revision/correction under approved authority; it cannot bypass a mandatory scientific check or overwrite the original audit. |

## 6. Failure and read/projection contract

Keep invalid shape/combination, unauthorized scope, stale predecessor/attempt, unresolved prerequisite, technical failure and genuine conflicting evidence distinct. Their public code names/HTTP mappings remain OPEN. A safe explanation identifies the affected check/claim/range and the next action without secrets, private cross-account existence or raw provider errors.

Read/report/export projections must not infer scientific satisfaction from a valid stored record alone. Validate representability and authorization, then expose actual dimensions, completeness and limits. An old client unable to represent the state receives defined incompatibility/adapter handling, never silently fabricated certainty.

An incomplete report can be a valid published artifact if its prerequisites for that **incomplete** view are met; the scientific verification field remains Incomplete. An unconfirmed-scope preliminary view must not masquerade as final overall aggregation. Deletion/revocation affects access according to the actual lifecycle policy without retroactively falsifying a computation's historical content.

## 7. Acceptance obligations — unexecuted specifications

| ID | Required future observable behavior |
| --- | --- |
| LP01 | Every operation validates the complete candidate; an isolated dimension patch cannot bypass validity. |
| LP02 | A checkpoint/provisional observation cannot become a final Satisfied requirement or final claim by projection. |
| LP03 | Performed-unresolved and blocked-before-performance retain different execution/provenance facts. |
| LP04 | Cancellation/current-fence checks reject active publication after the relevant authoritative state changes. |
| LP05 | Concurrent evidence/classification changes cannot publish a result under the wrong snapshot. |
| LP06 | Revoked or cross-account actors cannot publish or learn protected state through duplicate-acknowledgement lookup. |
| LP07 | Lost acknowledgement does not trigger duplicate local finalization or blind replacement paid calls. |
| LP08 | Required missing artifacts prevent falsely complete publication; orphan writes enter the approved reconciliation path. |
| LP09 | A valid incomplete report remains inspectable without being labeled Verified or hiding completed claim evidence. |
| LP10 | Unconfirmed scope blocks final aggregation while permitted independent assessments remain labeled. |
| LP11 | A pinned admissible old method/configuration is not silently replaced by the newest version. |
| LP12 | Partially Supported remains an unresolved verdict proposal, separate from Partial coverage and source Partially Verified. |

No LP obligation has executed inputs/results, a passing status or reviewer certification. They refine TA/RC/AC cases rather than replace the original capability acceptance gates.

## 8. Remaining specifications and progression

- Exact field names/enums, operation legality and transition graph remain OPEN. The matrix and operations above are proposals for review, not finalized transitions.
- Choose and approve guarded mutation/publication and idempotency mechanisms only after concrete database/authorization/object design comparison. No mechanism or product is selected here.
- Define policy-version admissibility, account-revocation ordering and incomplete/preliminary report DTOs explicitly; do not choose them during implementation by convenience.
- R02 can next refine numerical type/precision/undefined-result contracts against these publication rules. R03–R07 retain their unresolved scientific method, source, confirmation, review and acceptance decisions.

**Status remains Recommended for owner approval. All 24 gates remain OPEN.** Further design approval does not authorize production implementation, deployment, testing claims or capability enablement.
