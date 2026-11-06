# EvidenceTwin V1 — R01 canonical check representation options

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner selected **A — Separate Typed Axes as the recommended V1 refinement direction**, not a final schema or formal scientific specification. The [typed-dimensions/matrix draft](TYPED_CHECK_AXES_DRAFT.md) develops that direction. This comparison remains decision history for A and B; B is not selected. **All 24 gates remain OPEN.** No statistical method, library, production schema/code, deployment or capability is selected or enabled. Acceptance rows below remain unexecuted specifications.

Partially Supported remains a **proposed, unresolved claim verdict**. It is not a check state, an approved outcome or a synonym for partial coverage. Neither option introduces an aggregation rule for it.

## 1. The decision and its scope

Choose the canonical scientific check representation, not the database engine or public `/api/v1/` schema:

- **A — Separate typed axes:** represent applicability, execution and requirement determination independently; enforce their valid combinations through explicit whole-record predicates.
- **B — Tagged variants:** represent each permitted combination as a named variant with required/forbidden payload fields; derive the independent dimensions for inspection.

Both must preserve independent meaning. A tag such as Satisfied means a check requirement was established, not that the submitted scientific claim is true. A valid calculation may contradict a claim. An unavailable source cannot establish a contradiction solely through its absence.

The owner selection approves a recommended representation direction only. Exact field names, enum values, schema versions, state transitions, payload types, persistence/API projections and scientific predicates still require specification/review. It closes neither D01 nor any other gate.

## 2. Common contract both options must express

| Logical component | Required content / invariant |
| --- | --- |
| Identity | Check record/version, authorized case scope, claim/evidence revisions, attempt and producing component. No identity substitution on recovery. |
| Applicability | Mandatory/Optional or justified Not Applicable under an approved policy rule and its evidence. Missing implementation/input is not Not Applicable. |
| Execution facts | Not started, running, finished, execution error or cancellation facts as applicable; actual timestamps and attempt/fencing references. No finished execution inferred from a queue status. |
| Requirement determination | Satisfied, not satisfied or not established with the procedure/policy/evidence establishing that result. |
| Scientific observations | Procedure-specific output/unit/selection/counts, supporting/conflicting/missing evidence and limits. Not interchangeable with requirement determination. |
| Provenance | Input/output references, exact method/policy/configuration versions, original data/source locators and retained audit history. |
| Blockers/diagnostics | Safe structured cause, performed versus unperformed distinction, missing prerequisites, affected scope and next action. Public error codes remain a separate contract. |
| Finality | Once finalized, a result does not silently change. Re-execution/correction produces a linked result revision; active projection cannot accept stale/cancelled writes. |

An implementation may project a mutable current execution view from append-only events or use another approved storage design. This document selects neither storage strategy. Retained results still obey authorized deletion/retention policy; finality is not a promise of perpetual storage.

## 3. Proposed semantic cases and payload requirements

These are candidate semantic cases for reviewing both profiles, not a selected enum or approved state machine. Exact completeness of the cases remains a D01 review task.

| Case | Execution/requirement meaning | Required payload | Forbidden implication |
| --- | --- | --- | --- |
| Pending | Applicable check accepted but not started; requirement not established. | Scope, applicability, requested procedure and pending cause. | No satisfied requirement or published scientific output. |
| Running | Work started; no final requirement determination. | Start/event references and any explicitly provisional diagnostics. | A partial observation is not a final result. |
| Satisfied | Procedure performed and its check requirement established. | Required execution proof, procedure output and evidence establishing satisfaction. | Does not imply Supported claim or overall Verified report. |
| Not satisfied | Procedure performed and evidence establishes failure of the specific check requirement. | Negative finding, proof/locator, policy predicate and limits. | Does not automatically contradict every claim using the source. |
| Not established after inspection | Procedure performed but cannot establish the requirement from inspected evidence. | What was inspected, unresolved evidence/ambiguity and next steps. | Not interchangeable with no execution or established negative evidence. |
| Blocked before performance | Required inputs/procedure/authorization unavailable; check not performed. | Specific unavailable prerequisite and performed/unperformed indication. | No manufactured output or Not Applicable waiver. |
| Execution error | Work failed technically; no eligible final scientific determination. | Safe cause, execution scope, actual event/attempt references and recovery prerequisites. | Tool/provider failure is not a scientific contradiction. |
| Cancelled | Logical execution cancelled; any external settlement tracked separately. | Cancellation/attempt event, performed scope and separate retained response/settlement references where permitted. | Cancellation alone does not establish remote termination or permit release. |
| Not Applicable | Approved policy establishes this check is outside the assertion's requirements. | Rule/version, applicability evidence and authorizing policy context. | Do not report scientific procedure execution or silently turn an unavailable Mandatory check into this case. |

For example, comparing a reproduced value with an asserted value can be successfully performed while observing a numerical conflict. The check's actual requirement must be explicit: “reproduce the quantity” differs from “the supplied quantity matches the source.” Do not mark an incorrect assertion as a satisfied match or mark successful reproduction as a tool failure. The policy defines the requirement being evaluated; observations retain the numerical relationship separately.

## 4. Option A — Separate typed axes

### Mechanism

One check record contains typed applicability, execution and requirement fields plus their evidence/diagnostic payloads. A whole-record validator checks their combinations and all referenced proof. The UI can render dimensions directly without interpreting a combined result tag.

Illustrative logical record, **not a production schema or actual scientific result**:

```text
check: an authorized, version-bound calculation check
applicability: Mandatory under a referenced rule
execution: finished under a recorded attempt
requirement: Satisfied — quantity was reproducibly computed
scientific observation: conflicts with the asserted numerical value
evidence: exact input/output references and claim binding
```

The record can be valid without suggesting the submitted claim is supported. Another check for source authenticity can independently be blocked.

### Required cross-field predicates

- Satisfied or Not satisfied requires performed work and the exact proof demanded by the procedure. No API caller may set these independently to bypass validation.
- Not Applicable requires justified applicability and no fabricated scientific execution; applicability review itself may have an audit event.
- Pending/running/blocked/error records cannot carry an eligible final scientific determination. Preserve useful partial diagnostics explicitly as provisional.
- A performed but unresolved inspection differs from blocked-before-performance even if both lack a final established requirement result.
- All result/input/proof identities must match the scope envelope; safe enums do not validate evidence correspondence.
- Validate complete records at every trust boundary and before publication; validation of an individual patched field is insufficient.

### Tradeoffs and failure conditions

Independent inspection/filtering is direct, and new execution facts need not create a combined variant for every requirement state. The cost is an explicit cross-field validity table and validation on every write/projection path. It fails if partial updates, adapters or database writes can bypass those predicates, or if the application equates a valid enum combination with proof of scientific satisfaction.

## 5. Option B — Tagged variants

### Mechanism

Represent the permitted semantic cases as explicit variants with common scope/provenance. Each variant carries only its permitted required payload. Independent applicability/execution/determination views are derived through an exhaustive documented mapping; a single Success/Failure tag is insufficient.

Illustrative logical variant, **not a production schema or actual scientific result**:

```text
variant: performed check with requirement satisfied
scope: exact authorized claim/evidence/attempt references
completion proof: procedure output and policy-required references
scientific observation: conflicts with the asserted numerical value
```

“Requirement satisfied” still means the declared check requirement, not claim support. A separate source-check variant can remain blocked or unresolved.

### Required structural and semantic predicates

- Reject an unknown variant rather than defaulting it to success, unknown or an empty record.
- Required proof is structurally present, but its authorization, identity, correspondence and procedure eligibility still require semantic validation.
- Distinct variants preserve inspected-unresolved versus unperformed, negative evidence versus execution error, and Not Applicable versus unavailable.
- No variant implies complete report verification. Exhaustive mapping must expose the independent dimensions without losing negative/uncertain observations.
- Version adding/changing variants requires explicit compatibility behavior; old readers cannot silently coerce a new variant.
- No forced fit into an existing variant if a scientifically distinct case is missing; report the schema/policy gap and retain the raw authorized observation separately.

### Tradeoffs and failure conditions

Many impossible payload combinations can be rejected structurally and terminal-case handling can be exhaustive. The cost is a larger variant/projection contract, especially for preliminary, partial and cancellation histories. It fails if variants are overly coarse, if adapters erase distinctions, or if structural payload presence is treated as scientific evidence validity.

## 6. Lifecycle, publication and compatibility invariants

Both profiles must support the same semantics; neither determines a database transition mechanism.

| Operation | Proposed common predicate |
| --- | --- |
| Create check | Scope/applicability/procedure identity are explicit; a pending/blocked record does not imply completion. |
| Start work | Current attempt/fencing ownership and prerequisites are valid; no long-running transaction is inferred. |
| Finalize result | Validate the complete output/proofs and scope, not merely the latest event; stale/cancelled work cannot publish. |
| Justify Not Applicable | Record the exact policy and scope evidence; it cannot rewrite a missing implementation into an exemption. |
| Retry or revise | Produce attributable new execution/result identity and preserve the prior record; do not mutate a historical negative finding into a later success. |
| Project claim/report | Only approved verdict predicates and satisfied mandatory requirements contribute. Partially Supported remains a blocked unapproved verdict proposal. |
| Project public DTO | Preserve independent coverage/source/conclusion/temporal meaning; handle incompatible versions explicitly. Legacy adapters do not fabricate certainty. |
| Cancel/expire lease | Reject stale publication; keep remote-call uncertainty/accounting independent. No automatic assumption that a request stopped. |

Exact transitions, timestamps, concurrent update predicates, final payload types and publication eligibility remain to be specified and approved after the profile choice. This is not a claim that the current frontend or backend already implements them.

## 7. Representation acceptance obligations — unexecuted specifications

| ID | Candidate invalid or boundary input | Required review/test expectation |
| --- | --- | --- |
| RC01 | Satisfied requirement without performed execution or mandatory proof. | Reject before result eligibility/publication. |
| RC02 | Missing raw data disguised as Not Applicable. | Reject applicability waiver without an approved justification. |
| RC03 | Valid reproduction contradicts the asserted number. | Preserve completed computation and conflicting observation; do not label it a tool failure or automatic Supported. |
| RC04 | Source content inspected but original attribution remains unknown. | Preserve performed/unresolved inspection, distinct from unperformed retrieval. |
| RC05 | Official-record mismatch from performed authenticity procedure. | Preserve negative source finding; do not infer claim contradiction solely from this mismatch. |
| RC06 | Source retrieval/provider parsing error. | Retain technical/unperformed reason and no fabricated scientific conclusion. |
| RC07 | Stale attempt or mismatched evidence revision tries to finalize. | Reject active publication, preserve authorized audit history. |
| RC08 | Unknown tag or impossible axis combination. | Explicit incompatibility/validation blocker; no fallback to success or zero. |
| RC09 | Cancelled job receives a late provider result. | Keep settlement/history separate; no active report overwrite or automatic permit-release proof. |
| RC10 | Model proposes Partially Supported. | Preserve unapproved proposal with verdict-contract blocker; no mapping to another approved outcome. |
| RC11 | All material claims complete but mandatory report requirement unavailable. | Claim coverage remains Complete; report verification remains Incomplete with blocker. |
| RC12 | Old API reader cannot represent a new state/variant. | Defined incompatibility/adapter behavior; no silent scientific simplification. |

These obligations refine AC01/AC02/AC03/AC17/AC19 in the R01–R07 draft. They contain no fixture results, observed runs or assertions of passing tests. Owner/reference review and later separately authorized implementation/execution remain required.

## 8. Decision record to complete

| Item | Current status |
| --- | --- |
| Profile A or B | **A selected as recommended refinement direction only; final schema approval OPEN.** |
| Exact fields/variants and scientific requirement definitions | **OPEN.** |
| State/transition validity and public mappings | **OPEN.** |
| RC01–RC12 reviewed expectations and later execution | **OPEN — unexecuted specifications.** |
| D01, E05, E07 and other original gates | **OPEN — all 24 remain OPEN.** |

The direction decision is recorded as A. The next review concerns the typed dimensions, whole-record matrix and centralized validation in the linked draft. It does not choose an implementation library, enable a statistical method, approve Partially Supported or authorize production work.
