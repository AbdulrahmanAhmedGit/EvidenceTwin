# EvidenceTwin V1 — R02 numerical contracts and precision

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R02 after approval to continue from the [lifecycle/publication draft](CHECK_LIFECYCLE_PUBLICATION_DRAFT.md). All **24 gates remain OPEN**. Decimal is the subsequently selected recommended primary refinement direction; exact numeric types/encoding, context policies, algorithm/convention revisions, field names, public schemas and implementations are not selected. No statistical method or library is selected; no production work, deployment or capability enablement is authorized. All numerical examples below are **hypothetical, unexecuted acceptance specifications**, not scientific findings or passing tests.

Partially Supported remains a proposed/unresolved claim verdict. Numerical match/mismatch and numerical undefined/blocked outputs do not automatically select a claim verdict, source status or report-verification status.

**Subsequent owner direction:** A — Decimal is the recommended primary arithmetic direction for refinement only. The [Decimal contract](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md) develops original representations, explicit context/rounding, separate tolerances, units, invalid/undefined inputs and approved statistical conversion boundaries. Exact policies/methods/libraries/acceptance remain OPEN. Rational arithmetic is a specialized future option, not a fallback; no silent binary conversion is allowed.

## 1. Contract layers

Keep these layers separate:

1. Original evidence and its claimed/established provenance.
2. Parsed numerical observations, units and explicit selection/transformation.
3. Reproducible computation and its numerical validity.
4. Comparison with a defined numerical assertion and precision/tolerance.
5. Claim eligibility under source/methodology/comparability requirements.
6. Material-claim coverage, report gates and overall conclusion.

A valid arithmetic result at layer 3 does not complete layers 1, 5 or 6. A successful parser at layer 2 does not establish scientific measurement correctness. The canonical record still uses independent typed applicability/execution/requirement dimensions, with separate observations and provenance.

## 2. Logical input types

These are required logical components, not selected Python/TypeScript classes, JSON keys or database layouts.

| Type | Required content and constraints |
| --- | --- |
| Original numerical token | Exact original text/cell value, source artifact/version, locator and evidence whether it is a supplied value, formula/cached value, derived value or original observation. Do not discard original formatting on parse. |
| Parsed numerical atom | Validated interpretation, unit/scale, parser/configuration version and any ambiguity/confirmation. A missing token is not the number zero. |
| Unit/quantity descriptor | Variable definition, physical/count/percentage meaning, measurement/aggregation basis and any approved conversion. Matching labels alone do not prove comparable quantities. |
| Observation selection | Dataset/table/sheet/range version, explicit filters, observation unit, original/effective counts and exclusion reasons/approval. Row selection is part of the evidence, not a UI convenience. |
| Parameter binding | Named input roles such as numerator/denominator, base/new, values/weights or group membership. Do not infer roles from position alone. |
| Missing/invalid-value policy | Applicable supported method, explicit selection treatment and authorization for transformations. No automatic deletion, imputation or deduplication. |
| Precision contract | Source-declared precision/claim tolerance, numerical computation configuration and display formatting as independent items; applicable confirmations and units/base. |
| Method request | Procedure/version, exact parameters/selection/transformation and required source/comparability/assumption checks. |

Count quantities need their own observation-unit semantics. A file row, unique record, participant and event are not interchangeable merely because their counts match.

### Data-value categories

Distinguish eligible finite values, missing observations, invalid/ambiguous tokens, supported derived values and inspection-only formula caches. The exact tagged/field representation remains OPEN. A token cannot become eligible merely because a general-purpose parser can coerce it.

Formula-derived XLSX values follow the recommended Q13 restriction: retain formula/cache metadata for inspection but do not treat a cache as verified formula reproduction. Any numerical verification depending on it requires traceable inputs/sufficient provenance under the approved capability policy.

## 3. Logical numerical output types

| Output class | Required record | What it does not mean |
| --- | --- | --- |
| Defined numerical result | Typed finite value, unit/scale, exact input/selection/method references, reproducible intermediates/counts, numerical precision and limitations. | Not automatically source-verified or evidence that the submitted assertion is supported. |
| Mathematically undefined result | Performed evaluation scope, undefined condition and input proof, e.g. division by established zero. No fabricated numerical value. | Not the number zero, not an infrastructure exception, and not an automatic scientific contradiction. |
| Scientifically/input blocked | Missing/ambiguous prerequisite, affected check/selection and required evidence/correction; performed scope recorded accurately. | Not a completed computation merely because the blocker was diagnosed. |
| Execution error | Safe technical cause, actual performed scope and recovery prerequisites. Preserve partial diagnostics separately. | Not an observation that the claim is false. |
| Provisional observation | Explicitly nonfinal observation linked to the running attempt and bounded scope. | Not eligible for final satisfaction or aggregation. |

The canonical validity matrix and the method's exact requirement determine whether detecting an undefined condition completes a diagnostic check. It never creates a finite ratio result. Preserve this distinction instead of treating every undefined result as either a crash or contradiction.

Every defined result must expose enough intermediates to reproduce the operation under the approved policy: counts/sums for a mean, numerator/base for a ratio, group membership/weights for aggregation and exact transformation references. Large record collections stay behind bounded evidence references rather than duplicated into every result.

## 4. Procedure contract detail

These proposed definitions are for review. Each becomes a capability only after its exact convention, prerequisites and acceptance evidence are approved.

| Procedure | Input contract | Proposed output contract | Unresolved or blocking boundary |
| --- | --- | --- | --- |
| Count | Declared observation/count mode and exact selection. | Count, observation unit, included/missing/invalid/excluded counts as applicable. | Unknown count mode, unsupported duplicate policy and ambiguous subject/row interpretation block. Whether an empty declared selection yields a meaningful zero depends on count semantics, not an unrelated mean policy. |
| Sum | Compatible additive quantities and approved selection/missing policy. | Sum, unit, effective count and lineage. | Empty-selection semantics and admissibility of nonadditive/offset-scale quantities need explicit method policy; same unit string alone is insufficient. |
| Arithmetic mean | Nonempty eligible values with a common declared meaning and no implicit weights. | Sum divided by effective count, both retained, with unit. | Empty/ambiguous selection and hidden weighting block. A mean of subgroup means requires a justified weighting basis. |
| Median | Nonempty eligible ordered quantitative values and approved convention. | Central-order value/interpolation and location/selection references. | Even-count convention and applicability to ordinal input remain open; no library default. |
| Minimum/maximum | Nonempty eligible comparable values. | Observed extremum plus input locator(s) and explicit tie handling. | Empty/invalid selection; cannot infer unobserved population extrema. |
| Ratio | Declared numerator/base quantity and nonzero base, with compatible scientific definition. | Numerator divided by base; retain both components and result unit. | Unknown/zero base, incompatible definitions, unsupported sign/scale meaning. An arbitrary ratio is not automatically a proportion. |
| Percentage | Eligible ratio and an explicit percent-scale interpretation. | 100 times ratio with numerator/base and percent unit retained. | Do not clamp a nonproportion ratio to 0–100 or silently substitute a fraction. |
| Percentage-point difference | Two comparable percentage values on declared matching scales and a direction. | New-minus-base in percentage points, retaining both original values. | Fraction-versus-percentage ambiguity and incompatible definitions block until explicit approved conversion/binding. |
| Relative percentage change | Comparable base/new values and explicit temporal/directional ordering; nonzero base. | 100 times new-minus-base divided by base, with base/new/difference retained. | Zero is undefined; negative-base interpretation remains an explicit policy choice, not an automatic “improvement.” |
| Weighted mean | Paired values/weights, documented weight interpretation, admissible class/sign and nonzero total weight. | Weighted sum divided by weight sum; record paired counts, components and unit. | Unknown weight interpretation, missing pairs, zero total and unsupported weights block. Statistical survey/precision inference is not implied by a descriptive weighted calculation. |
| Grouped aggregate | Declared keys, membership, missing-key rules and approved operation. | Per-group operation/output, membership/selection references and group-specific limits. | Implicit joins or arbitrary many-to-many expansion block. Cross-group comparability needs a separate check. |
| Distribution component | Named quantile/bin/variance/frequency method and approved conventions. | Only requested, explicitly defined components and units/counts. | Quantile interpolation, bins and sample/population variance stay unresolved; no generic “distribution verified” output. |

Each operation must distinguish invalid inputs from valid inputs yielding a result that conflicts with an assertion. No numerical procedure can silently change filters, units, weights or method to make the comparison pass.

## 5. Unit and selection invariants

- Keep numerical scale separate from displayed text: `42%`, a fraction representing that percentage and a plain quantity of 42 are not interchangeable without declared interpretation/conversion.
- Unit conversions require a known approved conversion and recorded input/output evidence. Unknown units or unsupported measurement transformations block dependent comparisons.
- Population, denominator, aggregation and timeframe comparability are explicit scientific predicates. Matching column names/units alone cannot establish them.
- Missing data cannot become zero unless the evidence itself establishes zero under the variable definition; a researcher confirmation alone does not prove the missing observation was zero.
- Filters/exclusions/joins are versioned transformations, not invisible cleanup. Record original/effective observations and why denominator changes.
- Duplicates/outliers remain reported until an explicitly approved transformation is applied. Row multiplicity can represent real repeated observations, not automatically an error.
- Numeric inputs from previews are bounded selected evidence. A preview result cannot claim full-dataset coverage without the complete relevant computation.

## 6. Three precision contracts

| Precision layer | Required definition |
| --- | --- |
| Evidence/assertion precision | What the source/claim actually states, its measurement/rounding meaning, reported decimal/significant-figure basis or researcher-confirmed tolerance. |
| Computation precision | Representation, arithmetic context, intermediate rounding and error bounds; exact software/configuration references when eventually implemented. |
| Presentation precision | Formatting of values already computed; does not change stored comparison predicates or retrospectively widen tolerances. |

Original token formatting is preserved but is not automatically a statement of measurement uncertainty. A rounding interval is not a confidence interval. Any measurement uncertainty must have its own evidence/model rather than be invented from the last displayed digit.

### Rounding and tolerance comparison

The request must identify one approved comparison interpretation: exact asserted value, source-rounded interval, or explicitly confirmed tolerance. Do not silently switch among them. For a nearest-rounded assertion with declared rounding step, the candidate interval lies around the reported value by half that step; endpoint inclusion depends on the approved tie rule. Truncation and significant-figure reporting require their own rules.

Keep absolute tolerance in the result's unit and relative tolerance with an explicit base. Their combination policy (e.g. which must be satisfied), zero/negative-base behavior and exact boundary inclusion remain OPEN. A floating-point implementation tolerance is not the scientific tolerance of the claim. “Approximately” without usable precision remains unresolved until confirmation.

Compare using the recorded computation result and approved precision policy, not UI-rounded values. If numerical uncertainty straddles the decision boundary under the eventual arithmetic contract, do not force match/mismatch by formatting or implicit epsilon; the approved precision policy must define the response.

## 7. Numerical comparison contract

| Logical item | Meaning |
| --- | --- |
| Assertion | Reported value, unit, direction/time and exact claim/evidence version. |
| Computed result | Eligible defined numerical output with method/selection/provenance. Undefined or blocked outputs cannot become comparison numbers. |
| Comparison basis | Matching scientific definitions/populations/periods/base, conversions and precision/tolerance authority. |
| Numerical relation | Matches the approved precision criterion, conflicts with it, or cannot be established because scope/precision/prerequisites remain unresolved. Exact labels remain OPEN. |
| Claim eligibility | Separate assurance/source/methodology checks establish whether the numerical relation can support an approved claim verdict. |

A numerical mismatch is not automatically Contradicted if source identity, comparability or assertion interpretation is inadequate. Conversely, a demonstrably wrong value need not be treated as an execution failure. Keep the arithmetic observation, check requirement determination and final claim assessment independent.

Partially Supported cannot be used to bridge a numerical mismatch into a conveniently acceptable result; its meaning/eligibility/aggregation remain unresolved. No new verdict is approved by this contract.

## 8. Representation direction options — A recommended for refinement

This is a numerical-design choice within R02/D01/D07, not a statistical-method or library selection. All options preserve original tokens and provenance. No option guarantees scientific correctness merely through numerical precision.

| Option | Mechanism | Tradeoffs and failure conditions |
| --- | --- | --- |
| A — Decimal-oriented arithmetic | Preserve supported decimal evidence as exact parsed decimals; specify arithmetic precision/rounding for operations with nonterminating results. | Fits decimal-reported evidence and keeps formatting/quantization explicit. Requires bounded arithmetic context, exponent/input limits and explicit conversion boundaries for later statistical procedures. Fails if rounding/context is implicit or recurring divisions are treated as exact finite decimals. |
| B — Rational-oriented arithmetic | Represent eligible finite decimal/integer evidence and basic arithmetic as exact integer ratios where supported; convert only under declared output/interop rules. | Retains exact fractions for supported operations; needs numerator/denominator size limits, serialization and nonrational procedure boundaries. Fails if growth is unbounded or exact ratios are mistaken for uncertainty-free measurements. |
| C — Bounded binary arithmetic | Use a specified bounded binary representation with explicit parse/conversion, error/rounding and comparison rules. | Can simplify numerical-library interchange, but decimal-report boundaries and cancellation/overflow require careful error policy. Fails if a generic epsilon or display-rounded value decides the scientific assertion. |

This table is decision history: the owner selected A as the recommended primary refinement direction. B remains a specialized future possibility only; C is not the primary direction. Binary conversion is permitted only at explicitly reviewed boundaries for approved statistical procedures when required, with recorded precision/error limitations. No runtime/library or exact precision policy is selected. Exact wire encoding remains a separate open DTO decision.

## 9. Acceptance specifications — no cases executed

All values below are hypothetical arithmetic fixtures, not verified measurements or scientific outcomes. Expected arithmetic expressions are proposed reference expectations, not observed runtime results. Source validity/claim eligibility must be tested separately with approved evidence.

| ID | Hypothetical case | Proposed expected contract behavior |
| --- | --- | --- |
| NC01 | Arithmetic mean of the explicitly eligible values 1 and 2. | Retain sum 3/count 2 and expected mean 3/2 with unit/selection; no source-verification implication. |
| NC02 | Percentage change from base 20 to new 21. | Retain base/difference and expected relative change 5%; whether a claim is Contradicted requires its separate evidence/precision contract. |
| NC03 | Supplied examples 42% and 40%, ordered base to new. | Expected difference −2 percentage points; relative change is the distinct expression `100 × (40 − 42) / 42`. No significance inferred. |
| NC04 | Ratio with established denominator zero versus denominator unknown. | First records mathematical undefinedness; second records an unestablished prerequisite. Neither becomes zero or a fabricated finite percentage. |
| NC05 | Mean of an empty selection versus count of an explicit empty selection. | Require separate approved empty/count semantics; do not inherit mean/sum/count behavior from one generic library default. |
| NC06 | Values 2 and 4 with explicitly supplied admissible weights 1 and 3. | Expected weighted components 14/4, distinct from unweighted mean; actual eligibility still requires approved weight-class/selection policy. |
| NC07 | Ambiguous missing value, separator, duplicate or excluded row. | Block dependent interpretation until required mapping/transformation confirmation; no silent zero, imputation or drop. |
| NC08 | Formula cache used as the only numerical source. | Inspection metadata remains visible; do not treat it as independently recalculated formula evidence. |
| NC09 | Mean of subgroups with unequal sizes and no weighting basis. | Preserve subgroup results but do not assert an overall mean by unweighted averaging. |
| NC10 | Numerically equal values with incompatible units/populations/denominators. | Numerical equality alone cannot establish a scientifically comparable or Supported claim. |
| NC11 | Value exactly at a rounding/tolerance boundary or “approximately” without a tolerance. | Require explicit approved boundary/ambiguity policy; no pass-forcing epsilon. |
| NC12 | Negative relative-change base or weight sum zero. | Apply the explicitly approved interpretation/undefined rule, not a favorable verbal interpretation. |
| NC13 | UI rounds a value differently from the stored computation. | Compare under the recorded scientific precision policy; display formatting does not change the verdict predicate. |
| NC14 | Same numeric output references a different dataset/claim revision. | Reject active use/publication for scope mismatch, regardless of numerical equality. |
| NC15 | Model proposes Partially Supported after a numerical comparison. | Retain as unapproved proposal with eligibility blocker, not an approved aggregation outcome. |
| NC16 | Local arithmetic complete but mandatory source/report check unavailable. | Preserve completed calculation/claim work to the extent eligible; report completeness remains governed by its explicit mandatory gates. |

Later fixtures need approved original inputs/metadata, exact procedure/precision configuration, expected outputs/errors and independent reference review where applicable. No NC case has executed or passed. This document validates neither a calculation engine nor scientific sources.

## 10. Open specification record and next step

| Item | Current status |
| --- | --- |
| Numerical representation direction | **A — Decimal recommended for refinement only; exact policy/schema approval OPEN.** |
| Exact numerical types/serialization and bounds | **OPEN.** |
| Missing/empty/weight/median/distribution policies | **OPEN; proposed contracts require review.** |
| Rounding modes, tie boundaries and tolerance composition | **OPEN.** |
| Procedure/source/claim eligibility predicates | **OPEN; no new verdict approved.** |
| NC01–NC16 expected fixtures/review/execution | **OPEN — unexecuted specifications.** |
| D01/D07/E01 and all original gates | **OPEN — all 24 remain OPEN.** |

The direction is recorded as A; next refine its context, conversion and precision policies under the shared contract. This does not select statistical methods/dependencies, approve numerical conventions, close a gate or authorize implementation. R03–R07 retain their unresolved choices.
