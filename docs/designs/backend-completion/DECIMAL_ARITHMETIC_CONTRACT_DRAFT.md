# EvidenceTwin V1 — Decimal arithmetic and explicit conversion boundaries

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** The owner selected **Decimal as the primary arithmetic direction for V1 refinement only**. This document refines [R02](NUMERICAL_CONTRACTS_DRAFT.md); it does not approve precision values, rounding modes, numerical/statistical implementations, libraries, final schemas or acceptance criteria. All **24 gates remain OPEN**. No production implementation, deployment or capability enablement is authorized. All acceptance obligations are unexecuted specifications.

Partially Supported remains a proposed/unresolved claim verdict. Rational arithmetic is a specialized future option requiring demonstrable benefit and separate review, not an automatically selected fallback. Binary conversion is permitted only at an explicitly defined, reviewed boundary for an approved statistical procedure that requires it; no silent Decimal-to-float conversion.

## 1. Original representation and parsed value

Retain original source bytes/artifact identity and the original numerical token/cell representation independently from the interpreted Decimal value. Record encoding/locale, locator, parser/version, unit/scale, source/derived/formula-cache category and any researcher-confirmed ambiguity resolution.

Examples of representations that must remain distinguishable include trailing zeros, exponent notation, explicit sign, decimal/thousands separators, percent notation and blank/missing markers. Equal interpreted values do not erase those original representations. Token formatting alone does not establish measurement uncertainty or source-declared rounding precision.

Parsing may not first coerce a source decimal through a binary float and then claim to have preserved its original decimal value. If an upstream source already provides a binary numerical representation, preserve that origin and its conversion limitations explicitly; do not invent an exact original decimal token.

Original evidence remains immutable. Normalization, scale conversion and confirmed parsing create attributable derived interpretation records; they do not overwrite the source token or change its provenance.

## 2. Value classification before arithmetic

| Logical category | Required treatment |
| --- | --- |
| Eligible finite Decimal | Declared parse/unit/scale and admissible method inputs; eligible only under the procedure's scientific prerequisites. |
| Missing | Explicit marker/absence and its declared meaning; not numeric zero. Treatment follows an approved method/transformation policy. |
| Non-finite | Retain original NaN/infinity or equivalent source representation as a diagnostic/category; never an eligible finite scientific result. Any interpretation as a missing sentinel requires an explicit parsing policy. |
| Ambiguous | Preserve the raw value and possible interpretations; block affected arithmetic until required confirmation/resolution. No convenient coercion. |
| Invalid or outside configured bounds | Safe parse/resource reason, affected locator and next action; no fabricated substitute value. |
| Formula/cache/unsupported derived input | Preserve metadata and follow the approved provenance/formula eligibility policy. A cached number is not proof of correct/current formula execution. |

An affected observation does not automatically invalidate unrelated evidence. Record exact exclusions/blocked ranges and prevent claims depending on them from being reported fully checked. Never drop observations silently or describe the inspected subset as the whole dataset.

## 3. Explicit, versioned arithmetic context

Every deterministic arithmetic request/result must bind a complete approved context. No ambient thread/process setting or library default is an EvidenceTwin policy. Exact names/types and numeric values remain OPEN.

| Context element | Required contract |
| --- | --- |
| Precision budget | Declared supported precision and any intermediate/guard-digit policy; bounded by resource limits. No promise of arbitrary or infinite precision. |
| Rounding rule | Explicit operation/intermediate/output rounding behavior; tie and signed-value treatment where relevant. Source-report rounding and display formatting remain separate. |
| Range bounds | Supported coefficient/input size, exponent/range and output limits, including oversized exponent/token handling before expensive computation. |
| Exceptional-condition policy | Which undefined/inexact/range/invalid situations block, produce diagnostics or are admissible with documented limitations. Exact classifications need review. |
| Evaluation order | Deterministic ordering/grouping of aggregate operations and permitted transforms; no unexplained reordering across workers. |
| Quantization/output scale | Explicit unit-dependent reporting/scale rules, if required, without altering the retained pre-display result or scientific tolerance. |
| Context identity | Procedure/context version and reproducible configuration; pinned to the attempt and output manifest. |

Use a calculation-scoped context so unrelated calls cannot contaminate its precision settings or diagnostics. Retain the diagnostic facts associated with that calculation, not flags left by an earlier operation. How contexts are isolated/implemented remains a library/runtime design choice, not selected here.

Finite decimal input representation does not imply that every derived result terminates or is exact at the chosen context. Division and other operations may need approved rounding and recorded limitations. A recurring result cannot silently become an exact finite number. Do not round repeatedly for display and then feed those formatted values back into the scientific calculation.

## 4. Defined, undefined and blocked results

A defined output records its finite Decimal value, unit/scale, source and selection references, exact input roles, context/method version, reproducible intermediates/counts and precision/rounding diagnostics. Separate an exact result under the approved operation from an accepted rounded result and from an unresolved numerical condition. Exact wire spelling and output encoding remain OPEN.

An established zero denominator produces a mathematically undefined ratio with input proof, not infinity or a successful zero. An unknown denominator produces a missing-prerequisite blocker. The two must remain distinguishable in the canonical execution/requirement/observation fields.

Overflow, underflow, invalid operation, lost significance or an inexact result requires the approved context policy; it cannot be ignored merely because a runtime returned a value. Undefined/block/error handling follows R01 whole-record validity and guarded publication. Detecting undefinedness can complete a diagnostic check without establishing the requested finite ratio.

## 5. Separate tolerance contracts

| Tolerance | Required meaning |
| --- | --- |
| Absolute | Quantity difference allowed in an explicit compatible unit. A tolerance in percentage points is not a relative-percent tolerance. |
| Relative | Allowed scaled difference with an explicit comparison base and interpretation. The base is not silently chosen from whichever value is convenient. |
| Numerical computation allowance | A separately justified implementation/conversion error policy. It does not widen the scientific tolerance or prove measurement precision. |

Each tolerance records its authority (source, approved method or researcher-confirmed ambiguity), value, unit/base, inclusivity rule and applicable assertion/evidence revision. Neither an unspecified “approximately” nor the existence of a Decimal context supplies a scientific tolerance.

Absolute/relative composition remains OPEN: requiring both versus accepting either versus another explicitly reviewed predicate have different boundary behavior. Zero/negative relative bases and tie/endpoint handling also remain OPEN. No default is selected. If a required tolerance is unresolved, the numerical assertion remains unresolved rather than receiving a favorable match/mismatch.

Scientific tolerance is applied to the eligible retained computation result under its approved precision contract. If the computation/conversion limitations make a decision at the tolerance boundary unestablished, record that limitation instead of resolving it through UI rounding or an arbitrary epsilon.

## 6. Unit-aware comparison and percentages

Before comparison, establish variable definitions, units/scales, population, denominator/aggregation, period and permitted transformations. Matching decimal values alone cannot establish comparability.

Percentage inputs preserve whether the source expresses a percent value or a fraction; any conversion is explicit and traceable. Percentage-point change subtracts compatible percentage values. Relative percentage change additionally uses a declared base and direction. Neither output is a substitute for the other, and neither establishes statistical significance.

Unit conversions use approved definitions and transformations, preserving original and converted values/units. Unknown units, unsupported measurement scales or incompatible populations/denominators block dependent comparisons. Rounding intervals from source reporting remain distinct from confidence intervals and physical measurement uncertainty.

## 7. Explicit Decimal-to-binary statistical boundary

This section permits a boundary design **only for separately approved statistical procedures/libraries where required**, not an automatic conversion in the numerical core. No statistical method, library or binary representation is selected by this draft.

| Boundary record | Required content |
| --- | --- |
| Approval/purpose | Approved statistical procedure and library/configuration version, why conversion is necessary and which outputs it may affect. |
| Input identity | Exact Decimal values and source/selection/context references retained independently of the converted inputs. |
| Conversion rule | Specified target representation, range/rounding behavior, handling of nonrepresentable values and any deterministic order. |
| Precision limitations | Documented conversion effects, admissible numerical-error expectations and diagnostics for that method. No assertion of exactness merely because conversion succeeded. |
| Procedure output | Actual statistic/inference output, method and conversion configuration, error/assumption limits and lineage back to original Decimal input. |
| Return/projection | Explicit representation of the approximate procedure result; conversion back to Decimal must not imply that the binary calculation became exact decimal arithmetic. |

Implicit conversions in adapters, serialization, array construction or convenience helpers violate this contract. If range/precision prerequisites cannot be established, block the affected procedure rather than silently changing representation, clipping values or substituting a different test.

Round-trip difference alone is not a sufficient bound on error of a complete statistical procedure. Numerical-error expectations must be justified for that procedure and its conditioning/input scope. Source/measurement uncertainty, statistical uncertainty and representation error remain separately recorded.

Any future use of rational arithmetic requires its own approved scope, bounds, conversion and reproducibility contract. It must not silently take over when a decimal operation is difficult or its precision policy is unresolved.

## 8. Output, wire and reproducibility metadata

The retained result/manifest must resolve original tokens/artifacts, parsed Decimal values and interpretation, observation selection/exclusions, procedure/context revision, precision/range/rounding settings, operation order, intermediate components needed for replay, unit/scale, diagnostic conditions, source/assertion precision/tolerances and any approved conversion record.

Serialization must preserve that meaning without automatically reducing Decimal values to JSON numbers interpreted as binary floats by a consumer. Decimal strings versus structured coefficient/exponent/value metadata and exact API types remain unresolved D01 choices. Display-only formatting must not become the source of backend scientific comparisons.

Reproduction claims must name the approved context/version and retained inputs. Changing precision or rounding creates a different configured computation that needs an attributable result/attempt revision under the approved policy, not an invisible update to a historical verdict.

## 9. Acceptance obligations — unexecuted specifications

| ID | Required future observable behavior |
| --- | --- |
| DC01 | Original tokens, trailing zeros, notation/locale and source locators survive parsing without silent binary intermediates. |
| DC02 | Missing, ambiguous, invalid and non-finite input categories remain distinct from finite zero. |
| DC03 | Each calculation binds an explicit isolated context; previous operations cannot contaminate settings/diagnostics. |
| DC04 | Recurring/rounded results disclose context and limitations; no arbitrary-precision or exactness claim. |
| DC05 | Zero versus unknown denominator yields distinct undefined versus missing-prerequisite results. |
| DC06 | Range/invalid/inexact conditions follow approved policy and cannot silently become a successful finite result. |
| DC07 | Absolute and relative tolerances retain separate units/base/authority; unresolved composition cannot default to a pass. |
| DC08 | Percentage-point versus relative change and fraction-versus-percent scale remain explicit. |
| DC09 | UI formatting cannot change stored scientific comparison or widen tolerance. |
| DC10 | Decimal-to-binary conversion occurs only under the approved boundary manifest; implicit conversions are rejected. |
| DC11 | Converted statistical outputs disclose approximation/lineage; converting back does not fabricate exactness. |
| DC12 | Oversized coefficient/exponent or unsupported precision is bounded, not a resource-exhausting arbitrary-precision promise. |
| DC13 | Revised precision/context produces attributable history rather than silently replacing an earlier result. |
| DC14 | Partially Supported remains an unresolved proposed verdict; numerical comparison does not approve it. |

No DC case has executed, passed or established a measured error bound. Reviewed fixtures, exact context policy, library/procedure approval and actual acceptance evidence remain required.

## 10. Open decisions and references

Still OPEN: context precision/range values; operation/output rounding and tie rules; accepted exception/inexact policies; summation/operation ordering; scientific tolerance composition/bases; output/wire types; per-procedure binary conversions/error expectations; statistical methods/libraries; exact fixtures/acceptance criteria. Decimal is the recommended primary direction only. All 24 existing gates remain OPEN.

Reference check on 2026-11-06: the [General Decimal Arithmetic specification](https://speleotrove.com/decimal/decarith.html) provides the decimal model; [official Python Decimal documentation](https://docs.python.org/3/library/decimal.html) illustrates context/diagnostic and binary-conversion hazards. They are reference material, not a selected implementation or endorsement of runtime defaults. No package was installed and no scientific/runtime tests were executed.
