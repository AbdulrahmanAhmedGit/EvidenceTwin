# EvidenceTwin V1 — FD01–FD02 canonical schema and publication proposal

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner approved proceeding from the [cross-contract review](CROSS_CONTRACT_REVIEW.md) to FD01–FD02. This document proposes concrete logical field names, enum spellings, invariants and publication predicates for review. They are **not selected final schemas or executable implementation**. Separate Typed Axes and Decimal remain the recommended refinement directions; all **24 gates remain OPEN**. No method/library/product selection, production code, deployment, acceptance execution or capability enablement is authorized.

Partially Supported remains a proposed/unresolved claim verdict. It is not admitted by any proposed final-verdict schema or publication path here. Source Partially Verified and Partial coverage remain distinct.

**Subsequent owner direction:** B — Explicit Typed Absence is the recommended determination-slot refinement for justified Not Applicable, with rationale/policy/evidence, separate unresolved applicability and no ambiguous null. The [absence contract](EXPLICIT_ABSENCE_CONTRACT_DRAFT.md) refines this direction. Exact names/fields/cross-field rules and all gates remain OPEN; this is not a switch from Separate Typed Axes to a combined whole-record union.

## 1. Scope and representation boundaries

The candidate canonical shape below is internal to the scientific contract. It is not a Python model, database schema or `/api/v1/` DTO. Snake-case labels are proposed working names; public spelling/serialization remains an explicit projection decision. No raw internal object is automatically a public response.

`Ref<T>` denotes an authorized immutable/versioned reference of logical type T. `Instant` denotes an attributable timezone-aware observed instant under a time-source policy still to be specified. Neither chooses ID syntax, token/signature format, database type or clock mechanism. Collections are bounded by approved resource limits, whose values remain OPEN.

## 2. Candidate canonical check envelope

| Proposed field | Logical type / cardinality | Meaning and required invariant |
| --- | --- | --- |
| `contract_revision` | Ref to the approved canonical schema | A caller cannot select an unknown contract and receive successful validation. |
| `check_id` | Stable logical check ID | Identifies the requirement being evaluated, not a capability or authorization token. |
| `record_revision` | Record/predecessor version reference | Technical candidate/final-record revision, separate from scientific evidence revision and execution attempt. Exact update/history mechanics remain open. |
| `case_ref` | Ref to authorized research case | Must match all referenced claims/evidence/results; do not trust caller-supplied ownership. |
| `claim_ref` | Ref to exact claim revision | No implicit lookup of the newest claim. |
| `evidence_revision_ref` | Ref to exact evidence revision | Binds data/source/selection lineage; matching values or titles do not establish identity. |
| `classification_ref` | Optional Ref to classification revision | May be explicitly absent for a permitted preliminary independent assessment; required for final aggregation scope. Absence never means confirmed. |
| `temporal_context_ref` | Ref to historical/current evaluation context | Retains exact source/methodology bindings; historical/current cannot be silently interchanged. |
| `attempt_ref` | Ref to execution attempt | Defines execution/configuration/ownership context; not an authorization receipt. |
| `procedure_ref` | Ref to procedure specification/version | Specifies the exact requirement, inputs/outputs and scientific admissibility, not merely a method-family name. |
| `policy_ref` | Ref to applicability/assurance policy/version | Determines Mandatory/Optional/Not Applicable and eligibility dependencies. |
| `applicability` | ApplicabilityDimension | Independent typed applicability and its proof. |
| `execution` | ExecutionDimension | Independent actual lifecycle/performed/error/cancellation facts. |
| `determination` | Explicit discriminated RequirementSlot | Present typed requirement result or justified typed absence under the subsequently selected B direction; exact tag/schema remains OPEN. |
| `observation_refs` | Ref collection to typed observations | Scientific outputs separate from all three dimensions; payload schema is procedure-specific. |
| `provenance_refs` | Ref collection to evidence/transform lineage | Must resolve and correspond to the actual operation/scope. No credentials. |
| `diagnostic_refs` | Ref collection to safe blockers/diagnostics | Unknown/missing/conflict/error detail, not scientific proof by itself. |

The case authorization relationship is resolved from trusted application state, not a mutable `owner_id` or client role. Checkpoints/result revisions cannot change the bound scientific input behind an existing reference. Amendments create attributable evidence/classification changes and affected-result reevaluation.

Procedure-specific observation payloads need reviewed schemas/units/precision before they can be eligible outputs. An arbitrary JSON blob cannot become verified evidence merely because the envelope validates.

## 3. Candidate dimension types and values

### ApplicabilityDimension — proposed fields

| Field | Candidate type/value | Whole-record constraint |
| --- | --- | --- |
| `kind` | `mandatory`, `optional`, `not_applicable`, `undetermined` | Proposed values distinguish unresolved applicability from justified exemption. Unknown values are malformed, not automatically Undetermined or Optional. |
| `rule_ref` | Ref to policy rule where established | Resolved Not Applicable requires an approved scope-specific rule/proof. Undetermined applicability retains requested context/blockers without pretending a resolved rule exists. Exact conditional schema remains OPEN. |
| `basis_refs` | Collection of evidence/scope references | Must provide the proof required by the rule; Not Applicable cannot be justified merely by unavailable implementation. |
| `decided_by_ref` | Attributable actor/component reference | Scientific-policy applicability is distinct from researcher confirmation. |
| `decided_at` | Instant | Actual attributed decision time; no invented timestamp. |

### ExecutionDimension — proposed fields

| Field | Candidate type/value | Whole-record constraint |
| --- | --- | --- |
| `state` | `pending`, `running`, `blocked`, `performed`, `errored`, `cancelled`, `not_required` | Proposed closed enum, not final transition approval. Performed-but-unresolved is represented by `performed` plus `not_established` determination. |
| `step_ref` | Optional Ref to execution step | Required where an actual step exists under the lifecycle policy; absence cannot imply execution. |
| `execution_owner_ref` | Optional trusted ownership/fence reference | Required for guarded worker mutation/publication, not exposed as a public credential. |
| `started_at` / `finished_at` | Optional Instants | Required/forbidden combinations follow actual performed facts and approved lifecycle policy. No duration from a fake timer. |
| `performed_scope_refs` | Collection of actual operation/input references | Exact inspected or computed scope, including partial work; not intended-but-unexecuted scope. |
| `reason_ref` | Optional typed diagnostic | Required for Blocked/Error/Cancellation and unresolved context where the specification requires it. |

Remote-call settlement is a separate record. `cancelled` or expired ownership does not prove remote termination or justify permit release. A performed final result predating cancellation remains historical performed work; attempt cancellation does not rewrite it.

### RequirementDimension — proposed fields

| Field | Candidate type/value | Whole-record constraint |
| --- | --- | --- |
| `state` | `satisfied`, `not_satisfied`, `not_established` | Proposed closed enum; neither a source/claim verdict nor a report-completion field. |
| `predicate_ref` | Ref to exact procedure/policy requirement | Reproducing a value differs from matching a supplied assertion. |
| `proof_refs` | Collection of establishing evidence/results | Satisfied/Not satisfied needs the proof required by the predicate. Presence without correspondence is insufficient. |
| `unresolved_reason_ref` | Optional typed diagnostic | Required where the prerequisite/evidence remains unestablished; distinguish not performed from performed-but-unresolved. |

The fields in the table above belong to the **PresentDetermination** branch. Under the subsequently selected B direction, Not Applicable uses a separate **AbsentDetermination** branch with explicit rationale, applicability decision/policy and required evidence. It does not carry `not_established` as a scientific requirement value, and cannot be inferred from missing/null data. Exact tags and payload/reference shape remain OPEN.

### Not Applicable determination encoding — B direction selected; exact schema OPEN

| Option | Mechanism | Tradeoff and failure condition |
| --- | --- | --- |
| A — Common unestablished determination | Use the typed `not_established` candidate state with justified Not Applicable and `not_required` execution. Applicability determines that no mandatory scientific requirement is outstanding. | Keeps a uniform three-state determination model; fails if a reader counts every `not_established` as missing required work without checking applicability. |
| B — Explicit typed absence | Represent no scientific determination as an explicit typed absence for the justified Not Applicable case, with the policy proof still in Applicability. Exact tag/encoding stays open. | Distinguishes “not required to determine” from unresolved evidence; adds an absence branch and fails if missing/malformed data is treated as this deliberate justified absence. |

The owner selected B as the recommended refinement direction only. A remains decision history and is not the current candidate encoding. Independent axes and whole-record validation remain required; Not Applicable cannot count as scientific execution or waive unavailable Mandatory work. The candidate matrix below is updated for typed absence and explicit unresolved applicability.

## 4. Candidate whole-record validity relation

This refines the typed-axes matrix using proposed spellings and the subsequent explicit-absence direction. Ordinary determination values below are in the Present branch. Each row still requires valid scope, policy, proof and authorization. Undefined/unknown combinations are rejected; no coercion/fallback.

| Applicability | Execution | Allowed determination | Additional condition |
| --- | --- | --- | --- |
| mandatory/optional | pending | not_established | No eligible final output or fabricated execution facts. |
| mandatory/optional | running | not_established | Only explicitly provisional observations; actual start/performed scope as appropriate. |
| mandatory/optional | blocked | not_established | Specific unperformed prerequisite; no fabricated scientific output. |
| mandatory/optional | performed | satisfied | Complete actual procedure and establishing proof for that requirement. Claim may still be Contradicted. |
| mandatory/optional | performed | not_satisfied | Actual negative requirement proof; not automatic scientific falsehood. |
| mandatory/optional | performed | not_established | Actual inspection/computation scope plus precise unresolved reason. |
| mandatory/optional | errored | not_established | Technical failure details and any partial diagnostics; no eligible final determination from failed work. |
| mandatory/optional | cancelled | not_established | Cancelled-before-finalization facts; retained remote outputs remain settlement/history, not active scientific publication. |
| not_applicable | not_required | Explicit AbsentDetermination | Approved rationale/policy/applicability evidence; no scientific determination value or fabricated execution. |
| undetermined | pending/blocked applicability resolution | Present not_established | Explicit unresolved applicability blocker, not exemption; detailed preliminary-operation rules remain OPEN. |

Raw diagnostic/history preservation remains possible outside eligible final output. Optional checks still obey validity. A valid Blocked/Error/Unresolved record can be visible without being a satisfied scientific requirement.

### Proposed transition obligations, not a finalized transition graph

- Starting work requires a current Pending candidate, valid dispatch/ownership/prerequisites and full candidate validation.
- Running work can propose performed, blocked/uncertain, error or cancellation facts only if their actual performed scope and matrix combination are valid.
- A blocked-before-performance candidate may resume only under an explicitly approved same-step-versus-new-step/attempt policy. That policy remains OPEN.
- A finalized performed result cannot be patched from negative/unresolved to satisfied; correction/re-evaluation creates attributable new result identity/history.
- Not Applicable cannot be reached as a workaround for unavailable Mandatory work. Changed policy/scope requires a recorded applicability/revision decision.
- Every operation reconstructs the complete candidate and validates predecessor/current context. Changing one field at a time cannot traverse an otherwise forbidden combination.

## 5. Validation inputs and outcome proposal

Logical input to one centralized validator:

```text
complete candidate record
+ expected predecessor / mutation identity
+ trusted current actor and case permissions
+ authoritative active attempt, cancellation, ownership/fence and revision facts
+ approved schema / applicability / procedure / configuration references
+ resolved evidence, observation and provenance records
+ intended operation and publication scope
```

This is specification notation, not executable code or a chosen function signature. No client/model-provided validity flag substitutes for trusted context.

The candidate validation outcome distinguishes:

1. **Invalid:** shape/type/matrix/scope/reference/operation violations. Not authoritative eligible evidence; safe rejected-operation diagnostics may be retained.
2. **Valid but blocked/incomplete:** record is truthful but a scientific/aggregation/publication prerequisite is not established. Preserve it with blockers and permitted incomplete views.
3. **Eligible for the declared operation/scope:** every requirement of that specific operation is established. Not a transferable permission receipt or proof of all scientific claims.

Exact output enum/error DTO and receipt/integrity format remain OPEN. Reusing a validation result at another trust boundary needs its own approved policy; no optimization is selected. Publication requires current guards even if immutable payload validation happened earlier.

## 6. Formal publication predicates — proposed for review

Define these logical predicates against authoritative state; unknown required facts fail the affected operation with an explicit reason rather than defaulting true:

| Predicate | Required truth condition |
| --- | --- |
| `Authorized` | Current internal actor/service permission for exact case/resource/action; no stale role/client flag or cross-account lookup leak. |
| `ExactScope` | Candidate, evidence/classification/temporal references and target agree; any permitted preliminary absence is explicit. |
| `CurrentWriteContext` | Expected predecessor, active publication target, attempt ownership/fence and cancellation/supersession state permit this write. |
| `CanonicalValid` | Complete candidate conforms to the approved types, validity matrix, mutation operation and substantive reference correspondence. |
| `VersionAdmissible` | Pinned procedure/policy/configuration is approved for this attempt under the version-use policy; “latest” alone is not required or equivalent. |
| `ArtifactsAccepted` | Required artifact identities/versions/permissions and accepted-availability state resolve under an approved object/DB coordination contract. |
| `ConfirmedScope` | Required researcher-confirmed materiality/roles/bindings and processing authorization match the exact aggregation/execution snapshot. |
| `FindingEligible` | The requested scientific finding meets its own method/assurance/precision prerequisites; a merely valid observation is not automatically a verified claim. |
| `AggregateEligible` | Nonempty material scope, approved verdict predicates, confirmed primary/materiality rules and determining evidence support the requested conclusion. |
| `CompleteReportEligible` | All material-claim mandatory requirements and report-level mandatory gates are satisfied under the approved matrix. |

Candidate operation conjunctions:

```text
AdmitCheckRecord := Authorized AND ExactScope AND CurrentWriteContext
                   AND CanonicalValid AND VersionAdmissible
                   AND required-artifact conditions for that truthful record

PublishFinding := AdmitCheckRecord AND FindingEligible

PublishFinalAggregate := AdmitCheckRecord AND ArtifactsAccepted
                         AND ConfirmedScope AND AggregateEligible

PublishReportAsComplete := PublishFinalAggregate AND CompleteReportEligible
```

The expressions define intended logic, not selected runtime evaluation or transaction code. A Blocked record can truthfully identify a missing artifact without satisfying `ArtifactsAccepted`; it cannot publish a finding that requires that artifact. A valid Incomplete report may preserve findings/blockers without claiming `CompleteReportEligible`. Unconfirmed preliminary progress/individual assessments do not become a final aggregate.

`AggregateEligible` does not require every claim to be Supported: confirmed material evidence can justify Mixed, Contradicted or Inconclusive under the approved conclusion policy. Partially Supported is excluded while unresolved. Exact claim-verdict predicates and admissible uncertainty cases remain OPEN.

## 7. Guarded commit and race obligations

Payload validation before long-running work is not enough. The commit must re-establish the authoritative permission/predecessor/attempt/fence/revision/cancellation predicates so no intervening conflicting write can silently invalidate publication.

The comparison below is decision history: the owner subsequently selected conditional/version-guarded publication as the recommended direction. Concrete mechanisms remain unapproved:

| Mechanism | Tradeoff and failure condition |
| --- | --- |
| Conditional/version-guarded acceptance | Reject when required authoritative versions no longer match. Reduces long lock scope but fails if a relevant permission/fence/object-state change is not included or retry merges an unreviewed scope. |
| Transactional guarded acceptance | Read/guard affected state within bounded locking/isolation and commit the accepted result/audit relation. Requires explicit contention/deadlock handling and fails if external state is assumed covered by the database transaction. |

Conditional/version-guarded publication is the selected recommended direction, with short atomic transactions rather than long-lived pessimistic locking as the primary strategy. Concrete database engine/isolation, guard/fencing schema, authorization/revocation consistency, object acceptance, audit atomicity, idempotency and recovery mechanisms remain D01–D06 decisions. No database transaction alone proves atomicity with an external object store, identity provider or LLM request.

**Further refinement:** the [comparison](PUBLICATION_IDEMPOTENCY_OPTIONS.md) retains alternative history; the [version-guarded publication contract](VERSION_GUARDED_PUBLICATION_DRAFT.md) develops the owner-selected direction with comprehensive guard/write-path coverage, monotonic fencing, rejected-write audit and staged-result visibility. Exact implementation remains OPEN and no gate closes.

Required race behavior remains: stale workers cannot publish after reclaim; cancelled/superseded attempts cannot overwrite the active target; revisions cannot mix; authorization revocation follows the explicitly approved ordering; missing required artifacts cannot appear as accepted; duplicate acceptance cannot create conflicting active results. External-call settlement/budget/permits remain separate obligations.

## 8. Candidate boundary examples and existing obligations

All examples are unexecuted contract illustrations, not production records or approved scientific outcomes.

| Illustration | Candidate combination / context | Required behavior and existing reference |
| --- | --- | --- |
| Pending marked Satisfied | applicability mandatory; execution pending; determination satisfied | Invalid whole record; no field-patch bypass. TA01/TA05, RC01. |
| Inspected but uncertain | applicability mandatory; execution performed; determination not_established with actual scope/reason | Valid incomplete record distinct from never performed. TA02, LP03. |
| Computation conflicts with claim | execution performed; declared computation requirement satisfied; separate conflicting numerical observation | No automatic Supported or execution failure. TA03, RC03. |
| Missing data waived | applicability not_applicable with only unavailable-method reason | Invalid applicability proof. TA04, RC02. |
| Late result after cancellation | Candidate matrix otherwise valid; `CurrentWriteContext` false | Reject active publication; preserve permitted history/settlement. TA08, LP04. |
| All claims done, report gate missing | Claim coverage complete; `CompleteReportEligible` false | Valid Incomplete report with blocker, no Verified label. TA11, LP09, AC17. |
| Proposed Partially Supported | Model/legacy candidate outside approved verdict eligibility | Retain unapproved proposal and blocker, no silent mapping. TA10, AC03. |
| Replayed operation from wrong account | Earlier acknowledgement exists; `Authorized` false | No exposure of protected result/acknowledgement. LP06, AC01. |

These examples refine existing AC/RC/TA/LP obligations and do not create an additional counted acceptance family or executed evidence. Exact request/response fixtures still need specification and review.

## 9. Explicit decisions still required

| Item | What is proposed here | What remains OPEN |
| --- | --- | --- |
| Canonical fields/types | Candidate envelope and independent dimension members. | Exact names, scalar/ref representation, required/nullable/absent semantics and schema version. |
| Enum spellings and absence | Candidate applicability/execution/determination values and owner-selected explicit typed absence direction. | Exact discriminators/fields, formal vocabulary, unresolved-applicability/cross-field rules and unsupported-state compatibility. |
| State validity/history | Candidate combination table and transition obligations. | Complete legal transition graph, resume/new-attempt/finality and predecessor mechanics. |
| Observation/proof payload | Separate typed procedure results and provenance references. | Exact per-procedure schemas, proof predicates and resource bounds; no free-form blob becomes evidence. |
| Publication | Named predicates and operation conjunctions. | Approved scientific/authorization/artifact/version-use predicates and incomplete/preliminary DTO scope. |
| Commit mechanism | Two alternatives with common invariants. | Guard strategy, engine/isolation, authorization ordering, object/audit/idempotency coordination and recovery. |
| Public projection | Separate `/api/v1/` DTO boundary. | Wire spelling/types, Decimal encoding, cursor/error/legacy mappings and access behavior. |

Formal FD01–FD02 approval requires resolving these candidates, not merely approving another drafting step. Such approval still would not close Enablement/Pilot gates, prove actual implementation or authorize production work. **Status remains Recommended for owner approval; all 24 gates remain OPEN.**

**Candidate schema refinement:** the [publication guard schema proposal](PUBLICATION_GUARD_SCHEMA_PROPOSAL.md) separates untrusted commands, authoritative guard facts, validation bindings, operation profiles, outcomes and artifact acceptance relationships. Exact schemas and transition/transaction mechanisms remain proposals. Status remains Recommended for owner approval; all 24 gates remain OPEN. No implementation or capability enablement is authorized.
