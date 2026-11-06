# EvidenceTwin V1 — Independent typed check dimensions

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner selected **A — Separate Typed Axes as the recommended V1 representation direction for refinement only**. This does not approve exact field names, enum values, state transitions, persistence layout or API projections. All **24 gates remain OPEN**, including D01. No implementation, library/method selection, deployment or capability enablement is authorized. All examples and acceptance obligations are unexecuted specifications.

Partially Supported remains a **proposed, unresolved claim verdict**. Nothing here approves its meaning, eligibility or aggregation. Partial coverage, Partially Verified sources and provisional check observations are distinct concepts.

**Continued refinement:** the owner approved this working draft for further refinement. The [lifecycle/publication contract](CHECK_LIFECYCLE_PUBLICATION_DRAFT.md) now develops operation preconditions, whole-record mutation, publication guards, races and valid incomplete-report visibility. Exact transitions/mechanisms remain proposals, all gates OPEN, and no production authority is granted.

**Subsequent absence direction:** the owner selected explicit discriminated absence for justified Not Applicable, separately from Not Established and undetermined applicability. The [absence contract](EXPLICIT_ABSENCE_CONTRACT_DRAFT.md) updates the logical types/matrix without selecting exact names or detailed validation rules. This remains Separate Typed Axes; all gates remain OPEN.

## 1. Contract scope and notation

The canonical record composes independent typed Applicability, Execution and Requirement Determination dimensions. Scientific observations, provenance, identity and validation context remain separate typed components. No dimension is inferred solely from another: a performed check may be satisfied, negative or unresolved; a successful calculation may contradict a submitted assertion.

Names below are conceptual type labels and semantic captions, not chosen JSON keys, enum spellings, Python classes or database columns. A concrete schema must preserve these distinctions and whole-record predicates. These are proposed contracts pending review, not production code.

## 2. Explicit logical types

### Applicability dimension

| Typed member | Content and required meaning |
| --- | --- |
| Classification | Resolved Mandatory/Optional/justified Not Applicable, or explicit Undetermined applicability with its blocker. Exact enum values remain open; malformed/missing values do not become Undetermined by default. |
| Policy identity | Policy/rule/version, applicable claim/source/review scope and the input revision evaluated. |
| Justification evidence | Required proof for any Not Applicable decision; explanation and references for other applicability decisions as the policy requires. |
| Decision attribution | Producing component/actor and decision time; distinguish policy evaluation from researcher confirmation where those are separate operations. |

An unavailable implementation, inaccessible source or missing dataset cannot be classified Not Applicable merely to remove a mandatory requirement. New evidence/policy cannot silently rewrite an earlier applicability decision.

### Execution dimension

| Typed member | Content and required meaning |
| --- | --- |
| Lifecycle facts | Enough typed information to distinguish pending, running, blocked before performance, performed, technical execution error, cancellation and no scientific execution required. Exact enum decomposition remains open. |
| Execution ownership | Attempt/step identity, current ownership/fencing references and producing component. These references are not themselves a public authorization token. |
| Timing | Actual observed start/completion/cancellation/error facts when known. Absent times remain absent with the appropriate meaning, not invented durations. |
| Performed scope | Exact input/selection and operation performed, including partial work where relevant. Starting a job does not establish that every check ran. |
| Block/error/cancellation detail | Typed reason category and safe cause, missing prerequisite, performed/unperformed distinction and references to recovery/settlement records where applicable. |

Remote request settlement is a separate execution-accounting concern: local cancellation or lease expiry cannot prove the provider stopped or justify permit release. A cancelled attempt can retain earlier completed checks as historical facts; it cannot publish late work into the active analysis.

### Requirement Determination dimension

| Typed member | Content and required meaning |
| --- | --- |
| Determination slot | Explicit discriminated Present determination (Satisfied/Not satisfied/Not Established) versus justified typed absence for Not Applicable. Absence is not a determination value or ambiguous null; exact names remain OPEN. |
| Requirement identity | The exact predicate evaluated, with scientific procedure/policy version and target assertion. “Compute the quantity” is distinct from “the supplied value matches.” |
| Establishing proof | References/results satisfying the predicate's proof contract for any positive or negative determination. Presence alone is insufficient; correspondence and eligibility are validated. |
| Unresolved basis | What was inspected, what remains unknown and why no determination is established, including missing input versus performed-but-ambiguous evidence. |

A failed identity requirement is not automatically a scientific contradiction. A negative numerical comparison is not a tool exception. The scientific observation and claim-eligibility rules determine the claim implication separately.

### Separate record components

| Component | Typed content |
| --- | --- |
| Identity/scope envelope | Authorized case, claim/classification/evidence revisions, check/result version, attempt and historical/current layer. |
| Scientific observations | Procedure-defined finite/undefined result, units, numerical/visual/methodological observations, exact selection/counts, supporting/conflicting/missing evidence and provisional/final eligibility. No automatic claim verdict. |
| Evidence provenance | Original artifact/source/dataset/range references, hashes/versions, transformations, retrieval facts and procedure/policy/software/model/prompt references relevant to that observation. |
| Diagnostics/blockers | Safe cause, affected requirement and missing evidence/correction/retry prerequisites, separately from observations. |
| Validation context | Current authorized actor/service scope, active attempt/revision/fencing state and the approved specification versions needed to validate publication. Do not accept a caller's assertion that it is current/authorized. |

These components are linked, not duplicated as inconsistent success booleans. Scientific provenance does not contain secret credentials or unrestricted access grants.

## 3. Whole-record validity matrix

**Status: Recommended for owner approval.** This matrix specifies semantic combinations; it does not finalize enum values or transitions. “No established determination” must retain whether work was performed. Every row also requires valid identity, provenance, policy and authorized scope. Invalid or unrecognized combinations are ineligible for publication, not coerced into a nearby valid row.

| Matrix row | Applicability | Execution facts | Requirement determination | Eligible content / mandatory constraint |
| --- | --- | --- | --- | --- |
| MX01 | Mandatory or Optional | Pending, not performed | No established determination | Requested scope/procedure and pending facts only; no eligible final scientific output. |
| MX02 | Mandatory or Optional | Running | No established determination | Progress and explicitly provisional observations only. A progress event cannot satisfy a requirement. |
| MX03 | Mandatory or Optional | Blocked before performance | No established determination | Missing/unavailable prerequisite and next action; no fabricated computation or inspected evidence. |
| MX04 | Mandatory or Optional | Performed | Satisfied | Completed procedure and proof for the exact satisfied requirement; scientific observations may support or contradict the claim. |
| MX05 | Mandatory or Optional | Performed | Not satisfied | Negative requirement proof and actual observations; do not infer every dependent claim is false. |
| MX06 | Mandatory or Optional | Performed but unresolved | No established determination | Actual inspected/performed scope and unresolved evidence. Distinct from MX03 even if both block completion. |
| MX07 | Mandatory or Optional | Technical execution error | No eligible final determination from failed work | Error/performed scope and provisional diagnostics; no manufactured result or final fact inferred from failure. |
| MX08 | Mandatory or Optional | Cancelled before result finalization | No eligible final determination from cancelled work | Cancellation and permitted historical/settlement references; no active publication of late responses. |
| MX09 | Justified Not Applicable | No scientific execution required/performed | Explicit typed absence branch | Rationale/policy/applicability evidence required. No determination value or null-based exemption; record applicability evaluation separately. |
| MX10 | Explicit Undetermined applicability | Pending/blocked applicability resolution | Present Not Established | Preserve unresolved applicability reason; no exemption or final scientific eligibility. Exact preliminary-operation rules remain OPEN. |

The rows are a candidate validity matrix to review for completeness, not a selected state machine. In particular:

- MX04 versus MX05 depends on the **declared requirement**, not on whether the reviewer liked the conclusion.
- A completed result finalized before an attempt was cancelled remains a performed historical check; do not mutate it into MX08. A separate publication guard prevents a cancelled attempt from publishing a new active report.
- Optional means nonmandatory under the approved policy, not unchecked or exempt from record validity.
- Not Applicable with missing justification, Satisfied while Pending/Blocked, and negative determination from an execution error are invalid combinations.
- Unknown applicability or unknown required policy is an explicit schema/policy blocker; do not default to Optional or treat absence as Not Applicable.
- Final scientific observations can be retained without granting final claim/report eligibility. Whole-record validity does not itself establish complete scientific verification.

## 4. Centralized whole-record validation

Define one version-aware canonical validation contract shared by all paths. Its logical input is the **complete candidate record**, its predecessor/revision context where relevant, trusted authorization/ownership context and approved procedure/policy/schema references. The output is either a validated eligible record with its scope/version or structured violations and blockers. Exact API/error classes and implementation library remain open.

Required validation stages:

1. **Shape/types:** all dimensions and separate components conform to the declared contract; no unknown states, missing required proof or nonfinite numerical success.
2. **Identity/authorization:** references resolve to the correct authorized case and exact claim/evidence/attempt revisions; services cannot import arbitrary cross-account findings.
3. **Applicability:** policy/version and proof justify Mandatory/Optional/Not Applicable; no waiver based on unavailability.
4. **Combination:** the complete record matches the validity matrix and provisional/final content rules.
5. **Scientific eligibility/provenance:** outputs and proof match the actual procedure, selection, units, requirement and evidence. Typed payload presence is not proof of correspondence.
6. **Freshness/publication:** active attempt, cancellation state, fence/ownership, authorized scope, input revisions and required confirmation still permit publication.
7. **Projection eligibility:** public/report/export projections retain source/coverage/conclusion/temporal distinctions and cannot admit an unapproved verdict.

The contract must distinguish invalid record structure, valid but scientifically blocked work and valid eligible evidence. Their final serialized representations remain open. An implementation may organize these stages internally, but independent endpoints or workers may not replace them with local partial validation.

### No field-update bypass

Any proposed field/dimension update must be applied to the current complete record to form a candidate, then undergo whole-record and publication-context validation before it can become an authoritative current state. The same rule applies to operator tools and compatibility adapters. Reject stale predecessor/version updates rather than patching whichever record is latest.

Atomic guard/commit behavior is required so another worker cannot change attempt ownership, cancellation or evidence revision between the final check and publication. Exact transactions/locking/version predicates remain a design decision; no database product or persistence layout is selected. Validation performed only before a long-running operation does not protect its final write.

If storage is unavailable, ownership is unknown or proof references cannot be verified, do not publish a trusted scientific result. Retain safe diagnostics and recover according to the approved policy; lack of validation availability is not a successful result.

## 5. Validation at trust boundaries

| Boundary | Required use of the canonical contract |
| --- | --- |
| API intake / updates | Validate full request context, authorized identities and complete resulting record; caller-provided validity flags are not trusted. |
| Persisted records / imports | Validate declared schema/provenance and full record before reuse as eligible evidence. Legacy interpretations remain explicitly unverified; no default upgrade. |
| Queue acceptance / worker claim | Validate bound input/attempt identity and permissions; stale job records do not authorize different evidence or another account. |
| Worker checkpoint / field updates | Reconstruct and validate the complete candidate; checkpoints cannot inject Satisfied into an incompatible execution state. |
| Source/parser/procedure output | Treat external or component output as untrusted; validate scope, types, exact input selection and requirement proof before canonical admission. |
| Model/provider output | Validate references/role/schema and evidence correspondence; model confidence/agreement cannot bypass the scientific predicate or introduce Partially Supported as an approved verdict. |
| Operator/recovery/reconciliation | No privileged bypass of scientific validity or scope/fencing checks; record attributable action and any explicit new attempt/revision. |
| Result/report publication | Revalidate complete result and current guarded publication context; reject stale, cancelled, unauthorized or unresolved-mandatory publication. |
| API/read/report/export projection | Validate that the trusted stored record/projection version can be represented without lost meaning; malformed/unknown states produce explicit incompatibility, not fabricated success. |

Validation must be applied at every trust boundary; implementation may reuse a validated immutable snapshot only under a reviewed integrity/version policy. No such optimization policy is selected here. Final publication guards still need current authorization and ownership checks.

## 6. Stale and unauthorized publication contract

The publication request must bind the exact result, evidence/classification revision, policy/procedure version, attempt and ownership/fence context. The authoritative commit must reject:

- A worker no longer owning the claimed attempt or lease/fence.
- Cancellation or a newer active attempt/revision that supersedes the requested publication scope.
- A caller/service without the necessary current case/resource permission.
- Unconfirmed or mismatched classification/binding needed for aggregation.
- Invalid check combinations, absent proof or an unapproved verdict proposal.
- A report claimed complete while mandatory scientific or report requirements remain unresolved. This blocks misrepresented Complete verification, not a valid explicitly Incomplete report or permitted progress view.

Preserve already finalized historical findings according to lifecycle policy; rejection of active publication does not falsify those findings or erase external-call settlement obligations. Compare-and-commit/locking mechanics and account-revocation concurrency semantics need an explicit D01/D04/D05 design; this document imposes the invariant without pretending to choose that mechanism.

## 7. Acceptance obligations — unexecuted specifications

| Obligation | Proposed expected behavior, requiring later reviewed fixtures and execution |
| --- | --- |
| TA01 | Pending, Running and Blocked cannot publish a Satisfied determination. |
| TA02 | Performed-unresolved retains observed scope and differs from a check never performed. |
| TA03 | Successful reproduction with conflicting numerical observation remains distinct from failed execution and from successful matching. |
| TA04 | Not Applicable without policy/version/justification is invalid; unavailable Mandatory cannot be waived. |
| TA05 | Every individual field update is validated as a whole-record candidate; incompatible partial patches cannot become authoritative. |
| TA06 | Concurrent stale result, cancellation, changed evidence/classification and cross-account publication are rejected at commit. |
| TA07 | All trust-boundary adapters use the same contract and cannot turn a malformed record into scientific success. |
| TA08 | Late provider response retains permitted history/settlement without active publication or false permit release. |
| TA09 | Invalid/unknown dimension values and missing proof cause explicit violations, not coercion or default Optional/zero. |
| TA10 | Partially Supported remains an unresolved proposal and cannot enter an approved final aggregation branch. |
| TA11 | Claim coverage Complete can coexist with report Incomplete under a mandatory report blocker, with original evidence/assessments preserved. |
| TA12 | Public/legacy/export projections preserve separate dimensions and temporal meaning or return explicit incompatibility. |

These extend the existing RC/AC obligations; they are not 12 passing tests or evidence of an implemented validator.

## 8. Open specification items and continuation

| Item | Direction versus unresolved specification |
| --- | --- |
| Representation | Separate Typed Axes is the owner-selected **recommended refinement direction**. No whole-record schema is formally approved. |
| Logical types and matrix | This draft makes the three dimensions, separate observations/provenance and valid-combination constraints explicit; exact names, enum values and matrix completeness need review. |
| Transitions | Exact legal transitions, timestamps and finality/revision operations remain OPEN. The matrix is not a transition graph. |
| Validation | Central contract and trust-boundary/whole-record requirements are specified for review; exact implementation, public errors and guarded-write mechanism remain OPEN. |
| Persistence/API | Data layout, indexing, serialization, projection/caching rules and compatibility contracts remain OPEN. |
| Science | Numerical conventions, all statistical methods/libraries, source/protocol specifications and proposed Partially Supported remain unresolved as recorded in R02–R07. |
| Acceptance | TA/RC/AC cases are unexecuted specifications; no gate closes on document approval alone. |

All 24 original gates remain **OPEN**. Refinement can continue from the R01 validity matrix to an explicit transition/publication contract and then the dependent R02–R07 specifications. Any further approval must retain its scope: direction, specification review, capability acceptance and implementation authority are separate decisions.
