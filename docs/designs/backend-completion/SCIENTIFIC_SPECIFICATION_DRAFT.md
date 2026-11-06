# EvidenceTwin V1 — Scientific applicability and verification specification

Author: Abdulrahman Ahmed. Draft refinement: 2026-11-06.

**Status: Recommended for owner approval.** This is design-only refinement of the incorporated [Q01–Q60 baseline](RECOMMENDED_DECISIONS.md). The owner approved further Technical Design Refinement, not final approval of the individual specifications below. All [Decision, Enablement and Pilot gates](TECHNICAL_PLAN_GATES.md) remain **OPEN**. No capability is enabled, no numerical method/library is selected for production, and no acceptance result is claimed.

This draft develops D01/D07/D09 and defines required evidence for E01–E05. It does not select PostgreSQL, an identity provider, hosting or object-storage products. Those remain separate open decisions.

**Owner clarification (2026-11-06): Partially Supported is a proposed, unresolved claim verdict.** Its exact meaning, eligibility and aggregation behavior require explicit review before formal specification approval. Earlier mentions must not be read as an approved outcome. It is distinct from the already approved Partial claim-coverage/report-completeness concepts and Partially Verified source status. Do not include it in an approved verdict set, silently map it to another verdict or use it to authorize final aggregation. Preserve the clarification throughout R01–R07, which the owner authorized refining in that order; no final method/representation decision or gate closure is implied.

## 1. Unit of evaluation and immutable scope

Evaluate a defined assertion against one evidence revision and one declared temporal layer. A report may contain many such evaluations; it cannot silently mix historical numerators with current denominators, different populations, or incompatible measurement definitions.

The conceptual evaluation input must identify:

| Input | Required meaning |
| --- | --- |
| Claim reference | Original wording plus a normalized measurable assertion; preserve original and extracted values separately. |
| Classification reference | Confirmed Primary/Supporting/Contextual role, separate materiality, confirming actor/time and immutable classification revision. Preparatory individual assessments may reference an explicitly unconfirmed proposal; final aggregation may not. |
| Scope | Population, geography, time, variables, units, denominator/aggregation and relevant study design. Unknown fields are explicit, not empty values treated as established metadata. |
| Evidence bindings | Exact source snapshot/document passage, dataset version, worksheet/table/row/column/range and original artifact identifiers/hashes. |
| Method request | Procedure identifier/version, input roles, parameters, precision/tolerance basis, transformations and applicable prerequisites. |
| Policy reference | Versioned source/scientific applicability rules, review mode, declared mandatory checks and justified Not Applicable conditions. |
| Temporal reference | Historical or current layer, exact dataset/methodology identity, reported publication date, retrieved snapshot time and evidence for any historical attribution. |

The schema remains conceptual until D01 approval. Internal IDs must not become unscoped public access paths. Confirmation of a binding records research intent; it does not verify that the source is authentic or the dataset correct.

Every amended classification, source/data snapshot, transformation or claim scope creates attributable revision history. A same-input retry creates a new attempt. Store which input/policy versions each result actually used. Reusing a completed computation requires an explicit input/version equivalence rule; no reuse merely because titles or rounded values match.

## 2. Check result semantics

A check needs to answer three separate questions: was it required, did it run, and what did it establish? Do not encode all three in a success boolean.

| Dimension | Conceptual states | Interpretation |
| --- | --- | --- |
| Applicability | Mandatory, Optional, Not Applicable | Selected by an approved policy against declared inputs. Not Applicable carries the rule and evidence justifying it. An unavailable check is not automatically Not Applicable. |
| Execution | Not started, running, performed, not performed, execution error | Distinguish a check that ran from missing inputs, unimplemented methods, inaccessible sources and tool/provider errors. Retain safe structured reasons. |
| Requirement result | Satisfied, not satisfied, not established | A source identity mismatch can be performed/not satisfied. A source that could not be retrieved is not performed/not established. |
| Scientific observation | Structured output, claim-relevant evidence relation, limits | A calculation that contradicts a submitted number can be successfully performed and valid. Contradiction is not a calculation execution failure. |

These names describe required distinctions, not finalized public enum strings. The owner subsequently selected **separate typed axes as the recommended refinement direction**; the tagged-union alternative remains decision history. The [typed dimensions/matrix draft](TYPED_CHECK_AXES_DRAFT.md) develops cross-field validity and centralized validation. Exact names/enums/transitions/persistence/API projections remain OPEN, as do D01 and all other gates. An impossible state must never authorize verification.

The owner later selected [explicit typed absence](EXPLICIT_ABSENCE_CONTRACT_DRAFT.md) for justified Not Applicable within the determination slot, not as a requirement-determination value. Satisfied/Not satisfied/Not Established above describe the Present branch. Undetermined applicability is separately unresolved; missing/null data cannot imply absence. Exact names/fields/cross-field rules remain OPEN.

Each retained check result needs its check/procedure/policy IDs and versions; input references and exact selection; parameter/assumption evidence; execution timestamps; structured outputs; requirement result and reason; supporting/conflicting references; missing items; limitations; and links to the producing attempt. References to facts derived by a model must identify them as interpretations until independently established.

Proposed validation invariants for review:

- No Satisfied result from a check that was not performed, except a separately justified Not Applicable rule which does not masquerade as execution.
- No numerical output of NaN/infinity as a successful finite finding. Preserve a typed undefined/degenerate reason instead of zero.
- No successful check if its required input or procedure specification is unresolved.
- No publication of citations to nonexistent or unauthorized evidence. Existence validates a reference, not that it supports the finding; correspondence is a further check.
- Original findings survive retry/cancellation as historical attempt records where retention permits; stale work cannot publish into the active report.
- A scientific conflict is evidence-linked, not inferred from an execution error, missing field or provider refusal.

## 3. Proposed Scientific Applicability Matrix

**Status: Recommended for owner approval.** This matrix describes applicability, not implemented support. All candidate procedures remain unavailable until their required Decision and Enablement gates close for that scope.

Shared prerequisites: confirmed aggregation scope where needed; exact claim/evidence identity; adequate provenance for the claim's assurance level; reproducible data selection; explicit policy/method versions; appropriate units/definitions; and traceable limitations. Missing shared prerequisites block dependent conclusions without discarding independent computations already possible.

| Claim/check family | Mandatory inputs and checks | Conditional requirements and justified Not Applicable | Required retained output |
| --- | --- | --- | --- |
| Reported numerical/descriptive value | Exact variable/range, unit, aggregation, missing-value/selection rules; source/data match and deterministic reproduction. | Inferential statistical testing is Not Applicable to a purely descriptive arithmetic assertion that makes no inferential claim; record that scope. | Observed calculation, reported value, precision/rounding comparison, evidence references and unmet prerequisites. |
| Percentage/ratio/change | Numerator/denominator and their definitions, base/time ordering, units, comparability, exact transformation and rounding basis. | A population proportion/count relation is distinct from an unconstrained mathematical ratio; choose the declared method, not an implicit clamp to 0–100. | Reproduced ratio/change and units; signed/absolute/relative interpretation; undefined-denominator and scope blockers. |
| Group/time comparison | Compatible definitions, population, units, measurement/aggregation, denominators and periods; deterministic group results and contrast. | Different populations may be the comparison's intent, but generalization/causal inference needs separate justification. Missing time compatibility cannot be waived by equal headers. | Per-group inputs/results, contrast, explicit comparability limits and claim assessment boundaries. |
| Visualization fidelity/framing | Actual inspected image, matching source/data binding where claimed, chart family, axes/scales/labels/encoding and visible uncertainty. | Image-only audits may inspect framing; exact numerical/statistical verification remains unavailable without sufficient data. Neutral Twin applies only to a supported, reproducible rendering protocol. | Observed chart properties, data correspondence, recorded presentation changes, precise limits and no guessed missing values. |
| Basic statistical assertion | Approved test/interval specification, suitable study/design data, sample size, sampling/independence evidence, alternative/confidence level, missing-data treatment and numerical reproduction. | Descriptive coefficients do not automatically require/authorize a p-value. Unsupported methods cannot be Not Applicable merely to complete a significance claim. | Statistic, method/version, inferential output only when eligible, assumption evidence, diagnostics and unresolved conditions. |
| Methodological/interpretative assertion | Claim scope, study design, relevant source/methodology, identified confounding/sampling/generalization limits and evidence-linked review. | Complex causal identification, specialized clinical validation and predictions remain outside verified V1. Audit unsupported language without inventing a causal effect estimate. | Supported methodological observations, unsupported inferential leap, missing studies/details and limitations; no blanket proof of causation. |

Source authenticity, deterministic arithmetic and statistical suitability are separate outputs. A correctly reproduced ratio from supplied bytes does not by itself verify the publisher or publication-time dataset. Conversely, authenticity does not establish a correct scientific conclusion.

## 4. Deterministic numerical procedure contracts

Every candidate below inherits exact scope/lineage, finite-value handling, explicitly declared missing-data rules, output precision and source/binding requirements. These are proposed mathematical contracts, not deployed calculations. No automatic exclusions or imputation are authorized.

| Candidate | Proposed input/output definition | Blocking conditions and remaining choice |
| --- | --- | --- |
| Count | Count declared observation units after the explicit selection; distinguish total rows, valid observations and missing observations. Return count with unit and inclusion/exclusion counts. | Unspecified observation unit/count mode or duplicate/exclusion policy. Do not silently count rows as independent subjects. |
| Sum | Sum selected compatible numerical observations; preserve unit and selected count. | Incompatible units, ambiguous numeric parsing or unapproved missing-value handling. Empty-selection result policy remains to be specified rather than inferred from a library's identity value. |
| Arithmetic mean | `sum(x) / n` for the declared valid selection; retain sum/count and unit. | No eligible observations or ambiguous weighting. A mean of subgroup means is not an overall mean without justified group weights. |
| Median | Sort the declared selected values; middle value for odd count, arithmetic mean of the two central values for even count under the proposed conventional definition. | Empty/ambiguous selection. This proposed convention requires method approval; no unsupported ordinal interpolation. |
| Minimum/maximum | Extremal observed value(s), with original row/cell references and unit. | Empty/invalid selection; do not infer an unobserved population extreme or distribution tail. |
| Ratio/percentage | Declared numerator divided by declared nonzero denominator; multiply by 100 for percent. Retain both components, units and observation/aggregation basis. | Unknown/zero denominator, incompatible numerator/base definitions or unresolved proportion-versus-ratio meaning. No numerical result makes the source verified. |
| Percentage-point difference | Difference between two percentages expressed on the same scale, with declared direction and compatible definitions. | One input encoded as a fraction and the other as a percentage without a recorded conversion; incompatible populations/time/units. |
| Relative percentage change | `100 × (new − base) / base` with explicit direction, nonzero base and compatible units/definitions. | Zero base is undefined. Negative-base interpretability requires an approved policy/clarification rather than a silently misleading “improvement” claim. |
| Weighted arithmetic mean | `sum(w × x) / sum(w)` with paired observations, supplied weights and documented weight interpretation/aggregation. | Missing/ambiguous weights, zero weight sum, incompatible scope. Which weight classes/sign restrictions are admissible remains open; do not silently treat survey/precision/frequency weights as interchangeable. |
| Grouped aggregation | Apply an approved operation separately to explicit groups, preserving missing-key handling, group membership, units and lineage. | Implicit joins, duplicate expansion, unknown grouping keys or unsupported cross-group comparisons. |
| Distribution summaries | Return only explicitly specified count/range/frequency/quantile/dispersion components with their definitions. | Quantile convention, bins, sample-versus-population variance and admissible components remain open; “basic distribution” is not an executable algorithm. |

### Precision and rounding

Keep parsed numerical precision separate from display formatting. A reported decimal value defines a rounding claim only when its representation and rounding rule are established. For nearest rounding at a declared decimal step, compare against the corresponding rounding interval; tie-boundary inclusion depends on the approved rounding mode. Truncation, significant figures and an explicit tolerance are different policies and cannot be substituted silently.

Record absolute and relative tolerances independently, including their units/base and authority. “Approximately” without usable precision remains unresolved until researcher confirmation. A numerical implementation tolerance for floating-point reproducibility is not the scientific tolerance of the claim. No confidence interval is inferred from decimal rounding.

The owner subsequently selected Decimal as the recommended primary arithmetic refinement direction. Remaining precision choices are explicit context/bounds/rounding, serialization, approved statistical binary-conversion boundaries, tie/endpoint handling, negative/zero base interpretation, measurement precision and whether a source's rounded assertion or underlying record is being evaluated. See the [Decimal contract](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md). These details still need D01/D07 approval and boundary tests; the direction choice is not reopened.

## 5. Statistical candidates: descriptive output versus inference

**Status: Recommended for owner approval.** References below identify methods and hazards; they do not choose SciPy/statsmodels versions or dependencies. Correct library execution cannot establish sampling independence or study suitability from numerical values alone.

| Candidate | Required procedure contract | Must remain explicit/unresolved until approved |
| --- | --- | --- |
| Pearson coefficient | Paired variables and row alignment, numerical selection and nondegenerate variation; retain coefficient, eligible pair count, units/transformations and limitations. | Coefficient computation and inference are separate. Specify missing-pair handling, constant/near-constant diagnostics, valid inference assumptions and any CI method. [SciPy Pearson documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html) distinguishes the coefficient, hypothesis-test method and degenerate inputs. |
| Spearman coefficient | Paired ordered observations and an explicit ranking/tie policy; retain coefficient, pair count and transformations. | P-value method, sample-size/assumption policy and resampling specification remain open. The [SciPy Spearman documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html) warns about small-sample p-value accuracy; a coefficient alone does not justify an asymptotic inference result. |
| Mean confidence interval | Target population/estimand, sampling/design evidence, confidence level, unit, sample size and the specified estimator/variance method. | Choose the interval construction and admissible design. A classical t interval is one candidate, not a default for arbitrary skewed, clustered, weighted or dependent data. [NIST mean interval guidance](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm) describes confidence as coverage of a procedure, not probability that a fixed interval contains the parameter. |
| Proportion confidence interval | Defined success/failure observations, count/denominator, sampling assumptions and confidence level; explicitly distinguish a binomial proportion from a ratio of aggregate quantities. | Wilson versus an exact binomial construction versus another reviewed interval are separate choices. [statsmodels proportion intervals](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html) exposes multiple methods; its default is not an EvidenceTwin policy. |
| Welch independent two-sample comparison | Two defined independent groups, observed data/adequate summary contract, sampling evidence, mean contrast, alternative hypothesis and variance/degeneracy checks. | Define accepted raw/summary inputs, design/small-sample policy, confidence interval, tails and failure cases. The [SciPy t-test documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html) requires explicit unequal-variance selection for Welch; do not accidentally inherit the equal-variance default. |
| Chi-square independence | Observed frequency contingency table with declared categories/count provenance, valid sampling/design, expected-count and degrees-of-freedom checks. | Approve expected/observed count adequacy rules, correction and asymptotic-versus-reviewed alternative. [SciPy chi-square documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html) distinguishes continuity correction and resampling choices; sparse/invalid tables cannot silently pass. |

An observed p-value alone does not measure effect magnitude or prove scientific importance. Record the alternative and any significance threshold before interpretation; do not try multiple methods and report only a favorable one. Multiple comparisons, method selection, exploratory versus prespecified tests and missing assumptions need explicit policy. No universal threshold or minimal sample size is selected by this document.

### Statistical method decision bundle — all OPEN

| Choice | Options to approve, with tradeoffs/failure conditions |
| --- | --- |
| S01 — Proportion interval | Wilson candidate offers a score-based interval; an exact binomial candidate uses a different construction and can be conservative. Both need appropriate binomial/design assumptions; neither applies automatically to a generation-share ratio. No option selected. |
| S02 — Mean interval | A reviewed classical t-based interval has a compact specification but depends on admissible sampling/design/distribution conditions. A separately reviewed resampling approach handles different conditions but adds resampling/seed/degeneracy policy. Declining inference outside the approved construction remains valid. No option selected. |
| S03 — Correlation inference | Expose descriptive coefficients only until inference rules pass, or enable a separately specified inferential procedure for eligible designs. The first limits coverage; the second needs additional assumption/small-sample tests. An unavailable p-value is not a zero p-value. No option selected. |
| S04 — Chi-square variant | Explicit asymptotic correction/count policy, or an approved alternative for eligible tables after separate scientific review. These change the numerical test; no fallback may be selected because it produces a favorable p-value. No variant selected. |
| S05 — Numerical summaries | Approve each quantile/bin/variance convention as a method identifier, or defer those components while exposing already-specified summaries. Extra components improve coverage but require more reference cases; silently inheriting library defaults is unacceptable. No convention selected. |

These are method decisions within D07/E01, not new enabled features or final specifications. Owner/reference review is required before selecting any path.

## 6. Source-family mandatory-check draft

Separate a source's identity/authenticity result from the scientific accuracy of its contents. The four agreed source labels remain Verified, Partially Verified, Unverified and Inaccessible. Final predicates for the intermediate labels still need source-policy approval; do not infer them from a single successful check.

Check families:

- **I — Identity:** attributable publisher/repository and official record, original versus secondary status, canonical location.
- **V — Version/integrity:** title/organization/authorship where applicable, date/identifier/version, exact bytes/hash and relevant publication-time attribution.
- **C — Content:** actually inspect the relevant passage/table/dataset/chart; preserve context, units and submitted-source correspondence.
- **P — Data provenance:** original provider, dataset documentation, variable definitions, collection/transformations and record lineage where applicable.
- **N — Notices:** applicable official corrections/retractions/version changes, search scope/results and unresolved availability.

| Source family | Proposed required evidence | Not Applicable versus unavailable |
| --- | --- | --- |
| Original publisher HTML | Official publication attribution/record plus retained relevant content, metadata and version/retrieval evidence. Match quoted values/claims to specific sections, then inspect official notices. | Dataset-specific P details can be Not Applicable only if no dataset inference depends on them. Failed rendering/extraction or absent metadata is unavailable, not a passed identity/content check. |
| Official CSV/XLSX download | Official release/reference record bound to the exact downloaded artifact, declared encoding/schema/version, documentation, original provider and numerical record lineage; inspect applicable revision notices. | Lack of a DOI is not automatically failure if the approved family policy uses another official identifier; unknown release identity still cannot pass. Hidden/cached worksheets need ingestion policy, not automatic source assurance. |
| Versioned repository record | Official repository identity and persistent release/version record linked to exact files/documentation, checksums/content inspection and revision history. | A repository landing page without matching artifact/version is not enough. A mirrored copy requires its own attribution proof; missing original identity stays unresolved. |
| Text-based research PDF | Official publication/repository record, matching title/date/author/version and retained bytes; bounded extraction with page/section/table references and correspondence checks; official notices. | An unreadable/scanned relevant passage cannot be treated as inspected. Text extraction alone does not prove chart fidelity, correct table structure or the original dataset. OCR remains outside the proposed validated scope. |

All applicable mandatory I/V/C/P/N checks need recorded proof and results before Source Verified. Optional checks and unavailable information remain documented. A hash preserves content identity after retrieval; it does not establish authenticity. An accessible file from an unknown publisher is not automatically authentic; a temporarily inaccessible authentic source is not automatically fake.

Each source snapshot record must retain claimed versus established metadata separately; original/canonical URLs; retrieved timestamp; artifact version/hash/size/type; official record references; content locators; notice search scope/time; check results; and limitations. No empty author/date field is silently replaced by generated metadata.

### Publication-time and current layer

Historical verification needs evidence establishing that dataset and methodology versions belong to the publication-time assertion. Later retrieval of a report-associated file is not sufficient merely because its arithmetic matches the printed result. Current refresh creates new evidence and result revisions, preserving the previous snapshot and any unknown cause of revision.

Retain original report value/precision, historical value only when its identity is established, separately computed current value, signed/absolute differences, relative base, documented revision date/cause and interpretation effect. A pending historical proof must remain Historical Verification Incomplete; current disagreement cannot silently become Historically Contradicted.

The [Ember case](ember-2025-acceptance/acceptance_case.md) remains a reference investigation, not a passed backend acceptance case. Do not fill its missing historical/chart evidence by interpreting a matching later number as proof.

Open source decisions: concrete supported connectors/official lookup procedures; intermediate status predicates; archival provenance acceptance; notice applicability/reachability; and exact artifact/content matching. This table does not close E02.

## 7. Review modes and report-level mandatory gates

The following gates refine the recommended process. Mandatory policy/phase definitions remain subject to D07 approval. They are not a new implementation or a way to weaken earlier approved report semantics.

| Gate | Proposed requirement for final aggregation/verification | Failure/absence effect |
| --- | --- | --- |
| Scope | Material claims exist; roles/materiality and essential bindings are confirmed for the analysis revision. | Block final aggregation; independent assessments remain inspectable. |
| Scientific applicability | Approved, supported policy/procedures identify mandatory/optional/Not Applicable checks with evidence. | Do not represent an unspecified/unsupported check as satisfied. A mandatory gap blocks report complete. |
| Required evidence/calculations | Each material claim's mandatory source/data/comparability/numerical/statistical checks meet the declared policy. | Preserve completed claims, list missing/failed requirements and derive coverage independently. |
| Visual conditions | Where required, inspect the actual original chart and validated comparison rendering/protocol. | No substituted chart. Missing required conditions block that mandatory requirement. |
| Focused review | Record the declared role subset and its supported scope; enforce the phase requirements selected by the Focused policy. | It cannot be labeled Full Council. Exact permitted subsets and whether cross-review/judging applies are still OPEN. |
| Full Council | Four valid isolated initial reviewer outputs, valid cross-review based on all four and a valid Evidence Judge phase, under pinned configuration/protocol. | Any missing required phase blocks Full Council completion. AI phases completing does not satisfy missing scientific checks. |
| Assessment eligibility | Valid claim/evidence IDs, actual citation correspondence, allowed verdict predicates and preserved unresolved material disagreement. | Reject unsupported synthesis; do not convert invalid references, refusal or confidence into scientific proof. |
| Audit/reproducibility | Required retained inputs/policies/procedures/prompts/model/output references resolve and the report links their exact versions. | An unmet mandatory report gate forces report Incomplete even if claim coverage is Complete. |

Prompts and packet protocols require explicit reviewed versions. The system must preserve what was actually hidden/disclosed and any paired-condition ordering. It cannot report blinding or independence that did not occur. Reviewer/model diversity does not make a finding true.

Report derivation preserves already approved semantics:

1. A complete material claim has satisfied its own mandatory verification requirements; Supported and Contradicted outcomes do not by themselves distinguish completion. **Partially Supported remains proposed and unresolved**, pending its exact definition, eligibility and aggregation review; this section does not approve it. Record each claim's completed/missing/failed checks separately and do not silently reinterpret a proposed verdict as an approved one.
2. No material claim complete means coverage Incomplete; some but not all complete means Partial; all complete means Complete. Zero material claims blocks aggregation rather than passing by empty-set logic.
3. Any unmet mandatory report-level gate forces `report_verification_status=incomplete`. Claim coverage and findings remain unchanged. Never infer report verification from job completion.
4. Derive `overall_conclusion` using confirmed materiality/primary roles and the approved supported/contradicted/mixed/inconclusive rules. An unresolved primary claim that prevents a defensible overall assessment requires Inconclusive; other definite findings remain visible.
5. Do not infer coverage solely from a claim verdict string. Some uncertainty can be a defensibly documented outcome; missing mandatory evidence or an unperformed check still cannot be labeled satisfied. Exact claim-verdict eligibility requires the approved applicability policy.
6. Preserve historical/current layers. A current revision never silently edits a historical verdict or evidence manifest.

## 8. Required acceptance cases — specifications only, not results

All examples here are hypothetical test specifications unless linked to the existing Ember reference investigation. None is an executed scientific result or production fixture.

| Case | Expected invariant to test |
| --- | --- |
| Supplied 20% increase claim versus reproducible 5% from adequate version-bound evidence | Traceable contradiction of the numerical assertion; a valid completed computation, not a tool failure. |
| Treatment-causation claim with no raw data/sample size/test details | Insufficient Evidence/missing prerequisites; absence does not establish falsehood or a p-value. |
| 42% to 40% comparison | Preserve −2 percentage points versus relative change with an explicit base; no significance inferred from the pair. These are supplied example values, not verified source data. |
| Empty selection, zero denominator or zero relative-change base | Typed undefined/blocked output, never NaN/infinity or silently substituted zero. |
| Mean of differently sized subgroups | Require valid aggregation/weights; do not use an unweighted mean of means as a population result without justification. |
| Mismatched units, denominators, years or populations | Explicit comparability result and transformation requirements; no silent comparison verdict. |
| Correlation with constant input or unestablished inferential assumptions | Retain diagnostic/blocked inference and source scope; no invented p-value or causal conclusion. |
| Sparse/invalid contingency table or paired observations requested as independent groups | Block the unsupported procedure; no favorable-test fallback. |
| Source reachable but official identity/content/version unknown | Accessibility recorded without Source Verified. |
| Authentic corrected/retracted source | Record authentic identity and notice impact separately; assess affected claims rather than declaring all content false. |
| Workbook formula cache, hidden sheet, ambiguous separator/header or malformed range | Preserve raw bytes/lineage/exclusions, request required confirmation and block dependent checks; no code/link execution or silent coercion. |
| Image-only visual framing and missing Neutral Twin | Retain bounded visual findings with exact/statistical verification unavailable; no guessed data/twin. |
| One valid material claim, another missing evidence | Preserve the complete claim and Partial coverage; report gates and primary-claim conclusion rules applied independently. |
| Every material claim complete, mandatory report gate unavailable | Claim coverage Complete; report verification Incomplete with explicit blocker and all findings retained. |
| Unconfirmed classification, new classification revision or no material claim | Block aggregation or evaluate only the newly confirmed revision; never overwrite an earlier report. |
| Missing required Full Council reviewer, invalid citation or unresolved material disagreement | No fabricated phase completion, no majority resolution and explicit missing/invalid output. |
| Publication-time Ember identity absent but current snapshot available | Historical verification remains incomplete; preserve current/reference arithmetic independently and do not fill unknown history. |

Each case needs owner-approved evidence/provenance, exact input fixtures, expected check outputs/verdict predicates, error/coverage semantics and independent reference review where available before E01–E05 acceptance. Arithmetic examples alone cannot validate sources, inference, multi-user authorization or live provider execution.

## 9. Refinement deliverables and open choices

| Work item | Reviewable output still needed | Gates remain OPEN |
| --- | --- | --- |
| R01 — Canonical check representation | Refine the owner-selected Separate Typed Axes direction into exact types, allowed combinations, transitions and safe JSON/DTO projections; do not reopen the direction choice. | D01, E05, E07. |
| R02 — Numerical contracts | Approve each formula/convention, input/output types, numeric precision and boundary semantics with reference cases. | D07, E01. |
| R03 — Statistical variants | Resolve S01–S05 and all design/prerequisite/threshold/missing-data rules; approve dependencies only after comparison if needed. | D07, E01. |
| R04 — Source procedures | Turn family I/V/C/P/N requirements into concrete official-record/connectors/content matching with intermediate status and historical-proof predicates. | D03, D07, E02. |
| R05 — Scope and confirmation records | Define exact classification/binding/transformation confirmation, correction, no-material-claim and independent-preliminary-assessment contracts. | D01, D09, E03, E05. |
| R06 — Review protocol | Approve actual packets/prompts/templates, paired-order recording, allowed Focused subsets and every Full Council phase result schema. | D07, E04–E06. |
| R07 — Acceptance corpus | Supply reviewed reference artifacts and expected outputs for the cases above, then implement/test only under separate authority. | E01–E05, P07. |

None of these rows is a completed gate or formally approved whole specification. Separate Typed Axes and Decimal are subsequently owner-selected recommended refinement directions, not unresolved alternatives or implementation selections. Remaining details can be reviewed as a batch rather than chosen silently during implementation. The [R01–R07 contract refinement](SCIENTIFIC_CONTRACTS_DRAFT.md) develops them in order. Partially Supported remains an explicit unresolved verdict-design item throughout.

## 10. Primary references and evidence boundary

Official methodological/implementation references were inspected on 2026-11-06: [SciPy Pearson](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), [SciPy Spearman](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html), [SciPy independent t-test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html), [SciPy chi-square independence](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html), [NIST confidence limits for a mean](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm), and [statsmodels proportion intervals](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html). Links are documentation references, not pinned runtime packages or scientific acceptance of the platform.

No independent domain review, application tests, provider calls, installation, deployment or scientific capability enablement occurred in producing this document. It preserves **Recommended for owner approval** until the relevant decisions are explicitly resolved and approved.
