# EvidenceTwin V1 — Explicit typed absence and unresolved applicability

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner selected **B — Explicit Typed Absence as the recommended V1 refinement direction only**. This refines the [FD01–FD02 proposal](CANONICAL_SCHEMA_PUBLICATION_PROPOSAL.md). Exact type/field names, discriminator values, detailed cross-field rules, transitions and API/persistence projections remain OPEN. **All 24 gates remain OPEN.** No implementation, statistical method/library selection, deployment or capability enablement is authorized. Examples and acceptance obligations are unexecuted specifications.

Partially Supported remains a proposed/unresolved claim verdict. This document concerns absence of a required scientific determination, not claim support or incomplete coverage labels.

## 1. Four distinct meanings

| Meaning | Required representation and implication |
| --- | --- |
| Justified Not Applicable | A resolved applicability-policy decision establishes that this scientific check is not required for the exact scope. Represent the scientific determination slot through an explicit typed absence branch carrying its rationale/proof. |
| Undetermined applicability | Whether the check is required cannot yet be established. Preserve a separate unresolved applicability state and its reason; it is not an exemption or a valid absence decision. |
| Not Established requirement | A determination exists as an explicit typed state saying the requirement is unestablished, possibly because work is pending, blocked or performed-but-unresolved. Execution remains a separate fact. |
| Missing/malformed determination data | Required slot/discriminator/payload is missing, invalid, unknown or an ambiguous null. This is a schema/validation issue, not Not Applicable or an automatic Not Established assignment. |

Both unknown applicability and a missing required input can block verification, but for different reasons. Do not infer that applicability is unknown merely because a known Mandatory procedure lacks its dataset. Conversely, do not guess Mandatory/Optional/Not Applicable when the applicability policy cannot yet resolve scope.

## 2. Independent axes with a discriminated requirement slot

The canonical record still has independent Applicability, Execution and Requirement Determination components, plus scientific observations/provenance. B introduces a discriminated type **inside the determination slot**; it does not switch the entire check record back to the rejected combined-variant representation.

Illustrative logical type, **not selected field names, a production schema or executable code**:

```text
RequirementSlot =
    PresentDetermination {
        explicit discriminator identifying presence;
        typed RequirementDetermination;
    }
  OR
    AbsentDetermination {
        explicit discriminator identifying justified absence;
        typed NotApplicableBasis;
    }
```

The presence branch carries the applicable Satisfied, Not satisfied or Not Established determination contract. The absence branch carries no scientific requirement-determination value. It cannot contain Satisfied or a hidden secondary determination alongside its absence basis.

The slot itself is explicitly required by this candidate direction. An omitted field, empty object, unknown discriminator or bare null cannot satisfy either branch. Exact serialized tags and whether any transport-level null exists elsewhere are separate open DTO questions; none may create an implicit exemption here.

## 3. Typed absence basis

| Logical member | Required content |
| --- | --- |
| Rationale | Explicit scientific/scope reason why the check is not applicable, not “input missing,” “backend unavailable” or a researcher desire to finish. |
| Applicability decision reference | Exact resolved Not Applicable decision with its revision and actor/component attribution. |
| Policy/rule reference | Approved scope-specific applicability policy and rule/version authorizing the exemption. A caller-supplied string naming a rule is not proof of approval. |
| Required applicability evidence | Actual claim/scope/design/source facts required by that rule, with exact versioned locators. Preserve unavailable evidence rather than inventing it. |
| Scope binding | Exact claim, classification, evidence and temporal revision to which the decision applies. No blanket exemption for future revisions. |
| Decision provenance | Actual decision attribution/time and relevant validation/revision history, without impersonating researcher confirmation or exposing secrets. |

The absence payload must make the rationale and policy association explicit. It may refer to a single authoritative immutable applicability-proof record rather than duplicate mutable facts, but the exact reference-versus-inline projection remains OPEN. Whole-record validation must detect contradictory scope/policy/rationale copies either way.

This proof does not mean a scientific procedure ran. Applicability evaluation can have its own auditable execution, separate from the waived procedure. No successful scientific output is manufactured from the exemption.

## 4. Undetermined applicability payload

Preserve the requested policy/scope context where known, the question that cannot be resolved, missing/ambiguous applicability evidence, attributable evaluation facts and next input/review required. Exact fields/enums remain OPEN.

An unresolved applicability decision cannot carry an AbsentDetermination branch justified as Not Applicable. It also cannot assert a satisfied mandatory requirement or final scientific eligibility. Pending/blocked/preliminary work can remain visible under the declared scope while final aggregation obeys its confirmation and applicability gates.

Unknown enum values or malformed records are not automatically converted to the recognized Undetermined state. The latter is an explicit truthful record of unresolved applicability, not a catch-all parser fallback.

## 5. Proposed cross-field relation for review

The following refines the current candidate matrix; it is not final cross-field-rule or transition approval. Exact lifecycle names, admissible preliminary operations and policy predicates remain OPEN.

| Applicability fact | Execution fact | Determination slot | Candidate constraint |
| --- | --- | --- | --- |
| Resolved Mandatory/Optional | Pending/Running/Blocked | Present Not Established | Actual execution/reason retained; no implied final satisfaction. |
| Resolved Mandatory/Optional | Performed | Present Satisfied/Not satisfied/Not Established | Exact performed proof and requirement semantics determine the value. |
| Resolved Mandatory/Optional | Error/Cancelled-before-finalization | Present Not Established | No final scientific determination inferred from failure/cancellation; history/settlement remains separate. |
| Resolved Not Applicable | No scientific execution required | Explicit AbsentDetermination with NotApplicableBasis | Policy/rationale/evidence/scope must establish the exemption. No scientific result implied. |
| Explicit Undetermined applicability | Pending/Blocked applicability resolution | Present Not Established with applicability blocker | Cannot become justified absence or complete scientific eligibility. Any separately authorized preliminary work needs its own exact contract. |
| Mandatory/Optional/Undetermined | Any | AbsentDetermination justified only by unavailable inputs | Invalid exemption; do not bypass known or unresolved requirements. |
| Not Applicable | Any | Missing/null/unknown determination slot | Malformed; no automatic absence inference even if the applicability field says Not Applicable. |

An earlier performed result later considered outside a revised scope is not retroactively rewritten into never-performed absence. Create the new applicability/scope revision and preserve its relation to historical results. A legitimate revised applicability decision needs actual approved rule/evidence, not a partial patch over an unavailable Mandatory check.

## 6. Central validation and guarded publication

At every trust boundary and before publication, validate the complete record:

1. The explicit discriminator chooses exactly one admissible branch; required payload exists and forbidden extra determination/absence payload does not.
2. A present determination satisfies its state/procedure/proof contract and matches actual execution.
3. An absent determination resolves to a genuine Not Applicable decision, policy/version, rationale and required evidence for the exact scope.
4. Undetermined applicability remains unresolved and cannot be treated as absence or policy satisfaction.
5. Missing/malformed/unknown data produces explicit invalid/incompatible handling, not exemption, zero or automatic Optional/Not Established conversion.
6. Known Mandatory checks cannot be waived by missing inputs, runtime limitations or user confirmation alone.
7. Current authorization, attempt/fencing, cancellation and evidence/classification revision guards still govern any authoritative write/publication.

Individual discriminator, applicability or proof-field patches cannot bypass whole-record validation. Adapters/operator tools/imports and model outputs obey the same rule. A valid absent branch does not authorize report Complete if other mandatory requirements or report gates remain unmet.

## 7. Coverage, report and API projections

Justified absence is not a failed Mandatory check, nor a successful performed check. Coverage derivation considers the resolved approved applicability set and its required checks. Exact completeness predicates still need formal approval; do not calculate a pass percentage by counting absence as successful execution.

Not Established and Undetermined applicability keep their own blockers/next steps; absence cannot hide missing evidence. Report claim coverage, verification, overall conclusion and source/temporal dimensions remain separate. A valid Incomplete report can expose the distinctions without implying Verified.

Public/legacy/export projections must preserve absence versus unresolved versus malformed meaning. A legacy client unable to represent the branch needs explicit incompatibility or an approved truthful adapter; an ambiguous null or silent `not_established` mapping is not automatically acceptable. Exact mappings remain OPEN.

## 8. Boundary examples and existing acceptance obligations

All examples are hypothetical/unexecuted, refining existing RC/TA/LP/AC obligations rather than adding executed tests or a new counted case family.

| Example | Required proposed behavior / related obligations |
| --- | --- |
| An approved policy genuinely excludes an inference check for the confirmed assertion scope. | Absent branch requires actual rule/rationale/evidence; no scientific execution is claimed. TA04/RC02. |
| A required dataset is missing for a known Mandatory check. | Blocked Present Not Established, not absence or an applicability exemption. TA01/TA04. |
| Applicability depends on unresolved claim/design context. | Explicit Undetermined applicability with blocker; no default Not Applicable. TA09. |
| Determination field is absent/null despite an outer Not Applicable label. | Invalid/incompatible record, not automatic proof of exemption. TA05/TA09. |
| An existing Mandatory result is patched to an absent branch. | Revalidate whole scope/policy/history and reject unjustified bypass; legitimate change needs attributable revision/proof. LP01/LP05. |
| Model/legacy output proposes Partially Supported or an unsupported absence tag. | Preserve unapproved proposal and reject final eligibility; no favorable mapping. TA10/AC03. |
| A report has one justified absence but another mandatory report blocker. | Preserve truthful coverage; report remains Incomplete as required. TA11/AC17. |

## 9. Remaining formal decisions

Still OPEN: exact discriminator/type/field names; branch payload/reference schemas; precise applicability/validity/transition predicates; treatment of preliminary operations under unresolved applicability; confirmed-scope dependencies; scientific policy proof requirements; serialization/legacy mappings and reviewed acceptance fixtures.

The owner selected the **direction**, not those exact rules or final schemas. **Status remains Recommended for owner approval; all 24 gates remain OPEN.** No implementation, deployment, statistical method/library selection or capability enablement is authorized.

**Continued refinement:** the owner approved proceeding with further schema design. The [FD02 publication/idempotency comparison](PUBLICATION_IDEMPOTENCY_OPTIONS.md) now develops the remaining guarded-commit mechanism directions without selecting either or weakening typed absence and whole-record validity.
