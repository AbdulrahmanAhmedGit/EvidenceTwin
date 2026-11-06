# EvidenceTwin V1 — R03 statistical request, prerequisite and result contracts

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R03 after approval to continue from the [Decimal contract](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md). **All 24 gates remain OPEN. No statistical method, variant, library, confidence level, significance threshold, sample-size threshold or acceptance criterion is selected.** No production implementation, deployment or capability enablement is authorized. Candidate cases are unexecuted specifications, not measured scientific results.

Partially Supported remains a proposed/unresolved claim verdict. Descriptive arithmetic, source reporting, statistical inference, scientific interpretation and report completeness are separate. Decimal remains the primary deterministic arithmetic refinement direction; a statistical binary-conversion boundary requires its own approved contract.

## 1. Separate the assertions being checked

| Assertion type | Contract meaning |
| --- | --- |
| Source-reporting assertion | Whether the original source actually reports the quoted statistic, p-value or interval in context. Content correspondence does not independently reproduce the statistic or validate its method. |
| Descriptive computation | A defined summary/coefficient calculated for the selected observations under an approved numerical/procedure contract. It does not automatically carry an inferential p-value or population interpretation. |
| Inferential computation | A declared statistical procedure, estimand/hypothesis and admissible study/sampling assumptions with enough data/metadata to reproduce the requested output. |
| Scientific interpretation | What the statistic demonstrates, suggests or cannot establish for the stated population/design; causation/generalization must not be inferred merely from a numerical result. |

A sentence can contain several assertions, such as a numerical change and a significance claim. Preserve their distinct checks and evidence dependencies. Any normalized claim/classification/binding that affects aggregation still needs the confirmed-scope contract; this does not authorize silently splitting or relabeling the research question after observing results.

Source-authenticated quoted output may establish what a publication reported while leaving independent reproduction or methodological validity unresolved. A failed independent reproduction also needs its own evidence before concluding that the source's claim is contradicted.

## 2. Logical request contract

Names are conceptual; exact DTO keys/types remain OPEN. This is not a runtime API or selected internal model.

| Logical component | Required content |
| --- | --- |
| Scope identity | Authorized case, exact claim/classification/evidence/data revisions, attempt and historical/current layer. |
| Purpose | Source-reporting, descriptive output, inference or an explicitly defined combination. Each requested output has its own prerequisites. |
| Method specification | Approved method/policy/version reference, input/output contracts and selection authority. A caller-provided “approved” flag or method-family name is insufficient. |
| Estimand/hypothesis | Target quantity or population relation, null/alternative where applicable, direction/group contrast and original claimed statistic. |
| Input role binding | Exact variables, paired observation identity, independent groups or contingency counts; selected ranges, units and transformation lineage. |
| Design/sampling evidence | Study design, observation unit, sample size basis, collection/sampling, dependence/cluster/repetition/weight information and scope limitations; record unknown facts explicitly. |
| Missing-data policy | Original/effective sample counts, invalid/missing values, paired exclusions and explicitly approved transformations. No hidden deletion or NaN omission. |
| Inferential parameters | Applicable confidence coefficient, alternative, significance interpretation, variance/correction/interval method and any multiplicity policy. None has an implicit default. |
| Numerical boundary | Decimal input identity/context; any approved target representation/conversion manifest, method-specific numerical-error expectations and resource bounds. |
| Reproducibility | Procedure/configuration/software references, input selection and permitted stochastic parameters if a separately approved method requires them. |

Raw observations versus summary inputs are an explicit per-method decision. A summary's count, mean or variance must have definitions/provenance adequate to the procedure; matching column labels cannot establish compatibility. Do not infer independent subjects from file-row counts or statistical design from a researcher's selected dropdown alone.

## 3. Prerequisite evidence contract

For each requested output, a versioned applicability policy states required prerequisites and acceptable evidence. Each prerequisite record identifies the rule, exact input/design evidence, performed check, determination and limitations using the independent canonical dimensions.

| Prerequisite | Required evidence or unresolved question |
| --- | --- |
| Measurement/variable meaning | Units/scales and definitions actually fit the requested estimand, ranking or categorical count interpretation. |
| Observation alignment | Paired values refer to the same declared observations; group membership/counts and exclusions are traceable. |
| Sampling/design | Available study/methodology evidence supports the procedure's inference scope. Unknown sampling is not established by a plausible numerical distribution. |
| Independence/dependence | Design evidence identifies repeated/paired/clustered observations and relevant assumptions; numerical arrays alone do not prove independence. |
| Sample adequacy | Approved method-specific count/design/degeneracy rules, effective sample definition and diagnostics. No universal minimum is supplied here. |
| Missing data | Explicit treatment and potential bias/selection limits; missingness does not automatically justify complete-case analysis or imputation. |
| Method selection | Versioned approved procedure and relevant alternative/interval/correction rules fixed under the declared selection policy, not chosen for a favorable result. |
| Numerical suitability | Finite admissible inputs, validated conversion and method-specific error/conditioning rules where required. Successful conversion alone is insufficient. |

An assumption may be supported by documented methodology, contradicted by known design or unestablished. Do not turn “not detected as wrong” into “verified true.” Record the scope of any diagnostic; it does not prove every scientific assumption.

If a mandatory prerequisite is missing, block the dependent inferential output with explicit missing evidence/next steps. Preserve any separately eligible descriptive/source-reporting result. If an approved method is not yet specified, it remains unavailable even if the data would otherwise look suitable.

## 4. Candidate-family contract sheets

Every family below comes from the recommended baseline. None is an approved implemented method. Each needs an exact specification, scientific review and E01 acceptance before enablement.

### Pearson candidate

- **Input binding:** two numerical variables with exact paired observation alignment, units/transformations and missing-pair policy.
- **Descriptive request:** explicit coefficient specification and constant/near-degenerate handling with retained eligible counts and diagnostics.
- **Inferential request:** separately approved hypothesis-test/interval construction and its sampling/distribution/design requirements.
- **Blocking conditions:** undefined/invalid coefficient under the eventual method, incompatible pairs, unresolved inference assumptions or unsupported conversion/error policy.
- **Output separation:** an eligible coefficient cannot silently acquire an unapproved p-value or CI. Correlation does not establish causation.

### Spearman candidate

- **Input binding:** paired ordered observations, declared measurement meaning and traceable exclusions.
- **Required method choices:** ranking and tie conventions, degenerate behavior, then a separately approved inference/small-sample procedure if requested.
- **Blocking conditions:** ambiguous ordering/alignment, unapproved ties/missing policy or unestablished inference prerequisites.
- **Output separation:** preserve coefficient/pair count and diagnostics independently of p-value eligibility; no automatic asymptotic or resampling fallback.

### Mean-interval candidate

- **Input binding:** the target mean/estimand, observation population/design, units, eligible count and raw/summary inputs permitted by a specific method.
- **Required choices:** interval construction, confidence coefficient, estimator/variance definition, design applicability and numerical policy.
- **Blocking conditions:** unknown sample/design/variance meaning, unsupported weighted/clustered/dependent interpretation or unresolved method.
- **Output:** explicitly constructed interval with method/confidence/design, not a probability claim generated from the endpoints. No interval inferred from decimal rounding.

### Proportion-interval candidate

- **Input binding:** defined success/event count, relevant denominator and their observation/sampling model.
- **Required choices:** interval construction, confidence coefficient, valid count/design conditions and boundary behavior.
- **Blocking conditions:** unknown denominator, incompatible aggregation or an arbitrary continuous/aggregate ratio misidentified as a sampled binomial proportion.
- **Output:** bounds, unit/scale and count/design/method references. The Ember generation-share ratio is not automatically eligible for a binomial interval merely because it is expressed as a percentage.

### Welch-comparison candidate

- **Input binding:** two declared independent groups, mean contrast/direction, permitted raw/summary data, sample/design and variance definitions.
- **Required choices:** exact method, alternative/interval outputs, small-sample/degeneracy/missing-data policy and numerical conversion specification.
- **Blocking conditions:** paired/repeated groups misrepresented as independent, undefined variances/counts, unresolved design or unsupported summary contract.
- **Output:** defined estimate/contrast, statistic, effective counts and only eligible inferential outputs. No silent switch to a pooled-variance test or another test.

### Chi-square-independence candidate

- **Input binding:** a traceable contingency table of observed counts, category definitions and sampling/design evidence.
- **Required choices:** expected/observed count adequacy, degrees-of-freedom handling, correction, calculation variant and missing/structural-zero policy.
- **Blocking conditions:** ineligible/ambiguous counts, invalid category/table design or unapproved sparse-table handling.
- **Output:** method-specific statistic, count/expected-value diagnostics and eligible inferential result. No silent alternative test or correction chosen after seeing the p-value.

The proposed allowlist does not authorize advanced regression, survival/time-series inference or complex causal identification. An output requiring an unapproved effect-size construction or variance/interval method remains unavailable; no new method is implicitly added by a report field.

## 5. Result contract and independent output eligibility

| Result component | Required content |
| --- | --- |
| Identity/configuration | Exact claim/data/method/policy/context/conversion/software versions and producing attempt. |
| Procedure purpose | What was reproduced versus merely quoted or descriptively calculated. |
| Estimate/statistic | Typed value/unit or explicit undefined/block/error reason; admissible scope and numerical diagnostics. |
| Eligible inference | P-value and alternative, or interval/confidence construction, only when their independent required specifications/checks are satisfied. Absent output is not zero. |
| Counts/design | Original/effective/group/paired counts, denominator definitions and relevant study/selection limits. |
| Prerequisite record | Which assumptions/checks are supported, not satisfied or unestablished with their evidence; no generic “assumptions passed” claim. |
| Interpretation | Effect/association/uncertainty limits, source correspondence and next evidence needed. A p-value is neither effect magnitude nor causal proof. |
| Audit/provenance | Input/selection/transformation locators, actual calculations/output references and model interpretations clearly distinguished. |

No output is accepted solely because a library returned a finite statistic. The whole-record validator and method predicate must establish its requested meaning. Descriptive eligibility does not authorize inference, and inference does not automatically establish source authenticity or complete the report.

## 6. Hypotheses, selection and uncertainty interpretation

Record the original source's reported method/alternative/threshold separately from the procedure EvidenceTwin is authorized to reproduce. A disagreement in method or input version is not resolved by quietly choosing whichever output matches the publication.

The procedure-selection policy must distinguish prespecified versus exploratory work, define the relevant comparison family where needed and address multiplicity rather than hiding it. Exact correction/interpretation policies remain OPEN; no new multiplicity method is selected. Unknown original analysis plans or undocumented test searches stay limitations.

Do not infer significance solely from a coefficient, chart appearance, overlap/nonoverlap of displayed uncertainty intervals or an AI statement. Record what the approved procedure can actually establish. Absence of sufficient statistical information is Insufficient Evidence for the affected assertion, not evidence it is false. An unresolved method comparison remains unresolved rather than being called Partially Supported.

## 7. Decimal/binary and stochastic boundaries

Deterministic numerical source values remain Decimal-oriented under R02. A separately approved statistical method may require a binary numerical implementation; it must use the explicit [conversion manifest](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md), not an implicit array or serialization conversion.

Preserve original Decimal inputs, converted representation/configuration, range/precision diagnostics, method-specific numerical-error expectations and approximate output identity. Converting the result back to Decimal does not make the statistical computation exact. Representation error, sampling/statistical uncertainty and source/measurement uncertainty remain separate.

No resampling/randomized statistical method is selected. If one is later approved, specify its algorithm, random-state/iteration policy, convergence/error handling, reproducibility limits and resource budgets rather than adding a seed field and claiming repeatability. Paired visual-order randomization is a separate review-protocol concern, not automatic approval of statistical resampling.

## 8. Failure and publication predicates

| Condition | Required behavior |
| --- | --- |
| Method/specification unapproved or unavailable | Block affected output; identify missing specification/enablement. Do not execute a substitute. |
| Required data/design missing | Retain specific missing items and any eligible independent output; no fabricated sample size/denominator. |
| Known design/prerequisite conflict | Record actual conflict and its scope. It may invalidate the test's applicability without disproving the substantive claim. |
| Mathematically undefined statistic | Retain input proof/diagnostic under the exact method policy; not a finite zero or technical-crash conclusion. |
| Numerical conversion/range failure | Block/error according to approved policy; no clipping, representation change or altered selection without recorded approval. |
| Technical execution failure | Record safe actual failure and recovery prerequisites; not scientific contradiction. |
| Statistic conflicts with claimed value | Evaluate exact evidence, scope and precision before an approved verdict; do not confuse a performed mismatch with failed execution. |
| Model proposes unsupported interpretation/verdict | Retain interpretation as such and reject ineligible synthesis. Partially Supported remains unresolved and cannot become an approved outcome. |

An incomplete report can present eligible statistical/descriptive results with explicit blockers. It cannot claim complete report verification while mandatory statistical requirements are unresolved. Unconfirmed primary/material classification still blocks final overall aggregation. Publication revalidates authorization, attempt/revision/fencing, full check state and actual proof under the R01 lifecycle contract.

## 9. Statistical decision bundle — still OPEN

| Decision | Alternatives requiring scientific review; none selected |
| --- | --- |
| S01 — Proportion construction | Wilson candidate versus exact binomial candidate versus another explicitly reviewed construction. Different bounds/coverage behavior; none applies automatically to arbitrary aggregate ratios. |
| S02 — Mean construction | Reviewed classical construction for its eligible design versus separately reviewed resampling construction; declining unsupported inference is always required when neither is admissible. Design/resource assumptions and limits differ. |
| S03 — Correlation inference | Descriptive coefficients only until inference is approved versus a separately specified eligible inferential method. Broader inference needs more assumptions/reference cases; no default small-sample p-value. |
| S04 — Contingency test variant | Explicit asymptotic adequacy/correction policy versus a separately reviewed alternative for eligible tables. No favorable-result fallback. |
| S05 — Distribution/dispersion components | Explicit per-component definitions versus deferral of unspecified components. Extra summaries require approved conventions/reference cases. |

Cross-cutting unresolved fields include levels/tails, design/sample/degeneracy predicates, missing-data and multiplicity policy, permitted raw/summary inputs, numeric error policy and library/runtime comparison. This is a review bundle, not an implementation configuration.

## 10. Acceptance obligations — all unexecuted specifications

| ID | Required future observable behavior |
| --- | --- |
| ST01 | A quoted source p-value is distinguished from independently reproduced inference and method validation. |
| ST02 | A descriptive coefficient does not acquire an unapproved p-value/interval through defaults. |
| ST03 | Paired observations and independent groups are not silently interchanged. |
| ST04 | Row counts cannot establish sample size/independence without the declared observation/design contract. |
| ST05 | Missing sample/design/denominator evidence blocks dependent inference without falsifying the claim. |
| ST06 | Constant/degenerate/invalid inputs produce the exact reviewed undefined/block diagnostics, not a fabricated statistic. |
| ST07 | A generation-share ratio is not treated as a binomial observation proportion merely because it is a percentage. |
| ST08 | Sparse/invalid contingency input cannot trigger an unapproved alternative or correction. |
| ST09 | Wrong/undefined variance or unsupported summary input cannot enter a valid independent-group test. |
| ST10 | An unspecified confidence level, alternative or required method parameter cannot come from a hidden library default. |
| ST11 | Test/selection/threshold changes are attributable; no favorable p-value search is hidden. |
| ST12 | Decimal/binary conversion retains input identity and documented approximation/error limits. |
| ST13 | Missing-data exclusions preserve effective counts and confirmation/lineage; no implicit omission or imputation. |
| ST14 | An interval or p-value does not imply causality, effect size, source authenticity or report completeness. |
| ST15 | Partially Supported proposals remain blocked as final verdicts pending their specification. |
| ST16 | Final publication rejects stale/unauthorized or wrong-revision results and preserves valid incomplete work with blockers. |

These require reviewed fixtures, exact expected outputs/method/policy configuration, source/design provenance and later separately authorized execution. No ST case has run or passed; no accuracy or numerical-error bound has been measured by this drafting work.

## 11. References, open gates and next refinement

Methodological reference points remain the official [SciPy Pearson](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.pearsonr.html), [Spearman](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html), [independent t-test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html), [chi-square independence](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chi2_contingency.html), [NIST mean interval](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm) and [statsmodels proportion interval](https://www.statsmodels.org/stable/generated/statsmodels.stats.proportion.proportion_confint.html) documentation inspected during the parent specification. These references identify methodological choices; they are not a dependency selection or scientific acceptance of EvidenceTwin.

R03 now has explicit request/prerequisite/output/publication contracts to review, while method variants, exact parameters and predicates remain OPEN. D01/D07/E01/E05 and every other original gate remain OPEN. R04 source procedures are the next ordered refinement; their source-proof results must remain independent of statistical computation. **Status remains Recommended for owner approval.**
