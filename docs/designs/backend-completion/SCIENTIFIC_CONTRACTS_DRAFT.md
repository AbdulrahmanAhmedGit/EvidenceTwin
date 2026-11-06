# EvidenceTwin V1 — R01–R07 scientific contract refinement

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** Formal specification approval is pending. This artifact develops R01–R07 in the order authorized by the owner, from the [scientific specification draft](SCIENTIFIC_SPECIFICATION_DRAFT.md). All **24 Decision, Enablement and Pilot gates remain OPEN**. No statistical method, implementation library, database product or production representation is selected. All acceptance cases below are **unexecuted specifications**. No production implementation, deployment or capability enablement is authorized.

**Verdict boundary:** Partially Supported is a **proposed, unresolved claim verdict**. Its definition, eligibility and aggregation behavior need explicit review. It is not an approved branch in these contracts and cannot be silently mapped to Supported, Contradicted, Insufficient Evidence, Unresolved or a coverage state. Preserve an incoming proposal as an unapproved candidate with a blocker rather than publishing it as a final assessment. This does not change Partial claim coverage, report completeness or Partially Verified source status.

These are logical contracts and predicates, not public JSON schemas, Python models, table definitions or library calls. Field names are conceptual pending D01. Known facts, missing facts and unestablished facts must remain distinguishable; their final serialized representation is unresolved.

**Continued-refinement approval (2026-11-06):** the owner approved this working contract draft for further design refinement, retaining all stated boundaries. The [R01 representation comparison](CANONICAL_CHECK_CONTRACT_OPTIONS.md) developed both alternatives against common semantic cases and RC01–RC12 obligations; the subsequent direction decision is recorded below. This is not a final schema choice or formal specification approval.

**Subsequent direction decision:** the owner selected A — Separate Typed Axes as the recommended refinement direction. The [typed dimensions/validity matrix](TYPED_CHECK_AXES_DRAFT.md) makes its three logical types, centralized whole-record validation, trust boundaries and stale/unauthorized publication guards explicit. Exact names/enums/transitions/persistence/API projections remain OPEN; this does not close D01 or any of the 24 gates.

**Subsequent Not Applicable direction:** the owner selected B — Explicit Typed Absence within the independent determination slot. The [absence contract](EXPLICIT_ABSENCE_CONTRACT_DRAFT.md) distinguishes justified absence, Present Not Established, Undetermined applicability and malformed missing/null data. Rationale/policy/evidence remain explicit; exact fields/cross-field rules and all 24 gates remain OPEN.

## R01 — Canonical check and assessment records

### R01.1 Scope envelope

Every check/assessment must resolve this logical envelope before it can contribute to a report:

| Field group | Contract |
| --- | --- |
| Scope identity | Internal owner/case, claim revision, evidence revision, execution attempt and temporal layer. A public ID alone is not an authorization grant. |
| Procedure identity | Procedure/version, policy/version and specification revision. Separate these from API, prompt, model and source-snapshot versions. |
| Bindings | Exact input artifacts/dataset/table/range/variables/source locators and transformation references. Bindings point to immutable revisions. |
| Confirmation | Required confirmed role/materiality/binding/scope references and confirming actor/time. An independently assessable preliminary record may be explicitly unconfirmed but cannot enter final aggregation. |
| Configuration | Approved method parameters and exact parsing/selection/precision settings; no implicit runtime/library defaults. |
| Assurance dependencies | Source verification, methodology, comparability and prerequisite check references. Do not duplicate them as disconnected booleans. |

**Scope consistency predicate:** every referenced object must be authorized for the actor/case, resolve to the recorded revision and belong to the declared evaluation scope. A mismatch blocks the result's use; it does not silently trigger a lookup of another record or rewrite input identity. Historical/current evidence cannot be substituted on missing-reference recovery.

### R01.2 Check lifecycle and result

| Logical field | Required content |
| --- | --- |
| Applicability decision | Mandatory/Optional/Not Applicable, approved rule reference and justification inputs. |
| Execution fact | Whether it started/finished, timestamps, component, attempt/lease identity and whether execution errored or could not be performed. |
| Requirement determination | Satisfied/not satisfied/not established, with the evidence and rule supporting that determination. |
| Scientific output | Typed result, unit, selection/counts, diagnostics and claim-relevant supporting/conflicting/missing evidence. No model text masquerading as a calculation. |
| Failure/blocker | Stable conceptual reason, safe explanation, affected claim/check, missing inputs, retry/correction prerequisites and related evidence. Exact public error codes remain open. |
| Audit | Input/output references, method/software versions, observation time and any superseding revision. Original attempt history is preserved under retention policy. |

The comparison below is direction-decision history: A is the selected recommended refinement direction; B is not selected. Neither concrete production schema is approved:

| Profile | Mechanism | Tradeoff / failure condition |
| --- | --- | --- |
| A — Separate typed axes | Store applicability, execution and determination separately; validate cross-field predicates. | Easy independent inspection but invalid combinations are possible without whole-record validation. Fails if a satisfied determination can coexist with no required execution/proof. |
| B — Tagged variants | Model permitted combinations as explicit variants carrying only allowed fields. | Structural rejection of many invalid states, but more variants/DTO projections. Fails if an omitted variant is collapsed into generic success/unknown. |

A is selected for refinement only. The common validity requirements still apply:

1. A required performed check has the execution and evidence needed by its procedure; successful HTTP, a started stage or model agreement is insufficient.
2. Not Applicable needs an approved justification. It cannot erase an unavailable Mandatory check.
3. Execution error and unavailable input remain distinct from a performed check finding conflicting evidence.
4. Missing outputs are missing, not zero; nonfinite/undefined results carry a diagnostic, not successful finite values.
5. A cancelled/stale attempt cannot publish into an active/newer attempt. Retained late outputs remain historical/settlement records only under approved policy.
6. A source/authentication check failing does not by itself contradict a scientific claim; eligibility dependencies determine what can still be assessed.

### R01.3 Assessment and coverage contract

A claim assessment identifies its assertion, temporal scope, check results, supporting/conflicting/missing evidence, concise evidence-based rationale, limitations and next steps. Verdict eligibility is evaluated against the applicable scientific rules; it is not copied directly from an LLM response.

Existing distinctions Supported, Contradicted, Insufficient Evidence and Unresolved must be preserved. Their exact scientific predicates require policy approval; naming them here does not finish that work. No final Partially Supported outcome is accepted while its contract is unresolved. A proposed unsupported label must generate an explicit assessment-eligibility blocker rather than fabricated certainty.

Claim completion depends on satisfaction of its mandatory requirements, not verdict sentiment or count of passed technical checks. Report projection retains `claim_coverage_status`, `report_verification_status`, `overall_conclusion`, and historical/current dimensions separately. Any unmet mandatory report gate prevents complete report verification. An unresolved proposed verdict cannot be consumed by a supposedly finalized aggregation rule.

**R01 review output needed:** representation profile, allowed combinations, exact schema/types, verdict predicates and public mappings. D01/E05/E07 remain OPEN.

## R02 — Numerical request and output contracts

### R02.1 Common request/result

| Request item | Required rule |
| --- | --- |
| Observation selection | Immutable dataset/range/filter reference with declared observation unit, original/effective counts and recorded exclusions. Selection is not an implicit first-N-row preview. |
| Numerical interpretation | Validated parse/locale/unit/scale and explicit missing/invalid-value policy; retain original tokens. No automatic dropping/imputation. |
| Inputs and roles | Named numerator/denominator, base/new, values/weights or group keys as required. Positional guesses cannot establish these roles. |
| Precision parameters | Source precision, rounding/tolerance rule, implementation precision and output unit; scientific versus numerical-computation tolerances are distinct. |
| Assumptions | Evidence-bound admissibility, comparability and methodology prerequisites. Researcher intent and established evidence are separate. |

The result retains exact input/selection references; procedure/configuration version; typed numerical output/unit; intermediate components needed to reproduce it; counts/exclusions; precision/format information; and diagnostics/limitations. Validity of arithmetic and authenticity of inputs are separate fields/dependencies. No result is labeled source-verified solely because it can be recalculated.

### R02.2 Candidate procedure predicates

| Candidate procedure | Preconditions and mathematical result | Required rejection/blocking behavior |
| --- | --- | --- |
| Count | Explicit mode: observation rows, eligible numerical observations or another declared unit. Return exact count and coverage components. | Reject unspecified count unit/mode and unsupported duplicate interpretation. A row is not automatically a subject. |
| Sum | Compatible selected values under a stated missing/empty policy; output sum in the declared unit. | Incompatible units, ambiguous values or unresolved empty-selection semantics block the result. No default empty sum silently enters a claim. |
| Arithmetic mean | Eligible nonempty selection; output sum divided by effective observation count, with both retained. | Empty selection/implicit weighting blocks. Do not average subgroup means without an approved weighting basis. |
| Median | Eligible nonempty ordered numerical selection; proposed central-order convention must be specified in the method revision. | Even-count interpolation/ordinal suitability must not come from an unreviewed default. |
| Min/max | Eligible nonempty observations; retain all referenced extremal observations under a specified tie policy. | No claim about population extrema or unobserved tails. Missing/empty semantics require approval. |
| Ratio and percentage | Declared compatible numerator/base; denominator nonzero. Percentage is 100 times the ratio under a declared scale. | Zero/unknown denominator blocks. Proportion constraints are not applied to arbitrary ratios or aggregate generation shares by assumption. |
| Percentage-point difference | Two explicitly percent-scaled values with direction and comparability established. | Fraction/percent scale mismatch needs recorded conversion, not silent subtraction. |
| Relative percentage change | 100 times new-minus-base divided by base; retain declared base and direction. | Zero base is undefined. Negative-base interpretation remains an explicit unresolved policy, not “improvement” by sign alone. |
| Weighted mean | Paired values/weights, supplied interpretation, approved weight class and nonzero total weight. | Unknown weight meaning/sign admissibility, missing pairs or zero sum blocks. Weight classes are not interchangeable. |
| Grouped aggregation | Explicit keys/membership and an already specified operation per group. | Unsupported joins, unknown groups or unapproved many-to-many expansion blocks dependent results. |
| Distribution components | Each component has its own method definition, e.g. an approved quantile or variance convention. | Defer unspecified components. No automatic binning/quantile/variance default. |

These are candidate contracts only; owner approval of algorithm/conventions is still required. Proposed pure arithmetic definitions do not select statistical methods or implementation libraries.

### R02.3 Comparison against a reported value

The comparison request identifies the reproduced output, exact assertion value/unit, source-declared precision or confirmed tolerance, direction and compatible scope. A comparison is eligible only when both numerical and assurance prerequisites for the assertion are met.

Do not choose one of these unresolved precision mechanisms without approval: exact decimal representation versus a bounded binary representation; rounding tie/endpoint rules; significant-figure versus fixed-decimal claims; absolute/relative tolerance composition; and behavior for negative bases. The output must distinguish an arithmetic mismatch, unresolved precision and incompatible quantities. Unresolved precision never becomes a convenient pass/fail.

**R02 review output needed:** method revision per operation, numerical types/serialization, every edge policy and expected reference outputs. D07/E01 remain OPEN; this is not an executed calculation engine.

**R02 refinement available:** the owner approved continuing from the lifecycle draft. The [numerical contracts draft](NUMERICAL_CONTRACTS_DRAFT.md) developed logical input/output types, procedure boundaries, precision/comparison contracts, three representation alternatives and NC01–NC16 as unexecuted specifications. The subsequent Decimal direction is recorded below; no statistical method/library or final numerical schema is selected, and all gates remain OPEN.

**Subsequent R02 direction:** the owner selected Decimal as the recommended primary refinement direction, not a final context/precision policy. The [Decimal contract](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md) records explicit contexts/tolerances and statistical conversion boundaries. Exact values, rounding/exception rules, method/library choice, wire types and acceptance remain OPEN; all 24 gates remain OPEN.

## R03 — Parameterized statistical contracts

### R03.1 Required request contract

A request must name a scientifically reviewed method specification, versioned data/selection and estimand, study design, sampling/independence evidence, group/pair roles, missing-value treatment, alternative/confidence parameters where applicable, and the requested descriptive versus inferential output. No universal alpha, confidence level, sample-size cutoff or method default is supplied here.

If the method specification or any mandatory prerequisite is unresolved, return a documented unavailable/blocked assessment rather than executing another method. The statistical library, method variant and test parameters are not selected by this contract.

| Candidate family from the baseline | Explicit method configuration still needed |
| --- | --- |
| Pearson | Pair alignment, degenerate/near-degenerate behavior, descriptive coefficient definition, inferential method/assumptions and any interval construction. |
| Spearman | Rank/tie rules, pair handling and whether inference is permitted for the observed design/sample under an approved method. |
| Mean interval | Estimand/estimator, variance/design handling, confidence coefficient and an explicitly approved interval construction. |
| Proportion interval | Defined count/base and observation model, confidence coefficient and interval construction; arbitrary aggregate ratios do not become binomial proportions. |
| Welch comparison | Independent group definition, permitted input forms, variance/degeneracy handling, alternative, uncertainty outputs and design applicability. |
| Chi-square independence | Valid contingency count input, expected-count/design rules, correction and asymptotic or other separately approved calculation. |

S01–S05 in the parent specification remain unselected. A method family appearing here is a requested contract to develop, not an approved statistical method or dependency.

### R03.2 Required output and failure contract

Preserve method/configuration, estimand/group contrast, eligible sample counts, diagnostic/assumption evidence, statistic and any independently eligible p-value/interval, input lineage and limitations. Unavailable inferential output remains explicitly unavailable even when a descriptive coefficient is computable. A p-value is not evidence of causation or a measure of effect magnitude.

Invalid design, unsupported method, missing prerequisite and execution error must remain separate. Failed prerequisite checks cannot be fixed by silently changing the alternative, test, sample selection or confidence construction. Any approved resampling method would additionally require its iteration/randomness/error contract and record; this document does not select one.

**R03 review output needed:** resolve scientific variants and exact assumption/adequacy predicates with reference review; only then specify implementation comparison. D07/E01 remain OPEN. Primary methodological references and their limitations remain linked in the parent specification; no additional method claims or package selection are made here.

**R03 refinement available:** after approval to continue from the Decimal draft, the [statistical contract](STATISTICAL_CONTRACTS_DRAFT.md) develops source-reporting versus descriptive/inferential purposes, prerequisite evidence, candidate-family inputs/outputs, numerical boundaries and publication blockers. S01–S05 remain unselected; ST01–ST16 are unexecuted specifications. No method/library/level/threshold or gate is selected/closed.

## R04 — Source procedures and proof records

### R04.1 Retrieval versus source-verification contracts

The retrieval task identifies an authorized case/source request, bounded public URL/content policy and snapshot revision purpose. Its outcome retains original/final locations, actual retrieval time, safe transport facts, content type/size, retained artifact/hash and any unavailable/error reason. Destination/redirect/network isolation are separately required; a successfully downloaded file is not an authenticated scientific source.

The source-verification request binds the artifact to a claimed official record and the approved source-family policy. Record claimed versus established metadata separately. Concrete connectors, permitted identity evidence and matching algorithms remain unselected.

| Proof class | Required proof record |
| --- | --- |
| Identity | Official publisher/repository attribution and canonical record; original versus secondary relation and the procedure establishing it. |
| Version/integrity | Identifiers, publication/version/revision claims, exact content/hash and evidence tying the official record to that artifact. Hash alone is not authenticity. |
| Content correspondence | Exact page/section/table/cell/chart locators, the observed relevant content and comparison against supplied evidence with context/units intact. |
| Data provenance | Original provider/documentation, variable/collection/transform lineage and selected data records where the claim depends on them. |
| Notices | Official correction/retraction/revision search scope, observation time, discovered notices and affected versions/claims; distinguish unknown status from established absence under the limited procedure. |

Each proof record needs applicability, executed/unperformed distinction, requirement result, evidence locator, procedure version and limitations. No DOI/title/domain/HTTPS shortcut satisfies the entire record.

### R04.2 Status and temporal constraints

Source Verified requires every applicable mandatory source requirement established under an approved policy. Partially Verified, Unverified and Inaccessible retain their agreed distinctions, but exact intermediate predicates and reachable-content/identity failure precedence remain open for D07 review. No source status alone determines claim truth.

A historical binding references the publisher's asserted publication-time dataset/methodology and attributable version proof. A current binding references a separately retrieved identified snapshot. If historical proof is absent, retain Historical Verification Incomplete even if later numbers match. New refreshes create immutable snapshots and linked comparisons; unknown revision reason/date stays unknown.

**R04 review output needed:** concrete procedures per source family, proof acceptance/status predicates, historical archive criteria and retrieval isolation validation. D03/D07/E02 remain OPEN. Ember historical identity and original-chart access remain unresolved evidence tasks, not successful acceptance outputs.

**R04 refinement available:** after approval to continue from R03, the [source procedure draft](SOURCE_PROCEDURES_DRAFT.md) develops separate retrieval/snapshot/proof contracts, family procedures, notice impact, current availability versus retained assessments and historical/current binding. Source connectors/status precedence/archive rules remain OPEN; SP01–SP16 are unexecuted specifications. No library/implementation or gate is selected/closed.

## R05 — Confirmation, revision and scope contracts

### R05.1 Confirmation record

| Content | Required semantics |
| --- | --- |
| Proposal | Proposed claim roles, materiality, rationale, evidence bindings and parser/transform selections; identify proposing component and input revision. |
| Confirmation | Independently recorded researcher choice/override, internal actor ID/time and exact proposal/evidence/classification revision being confirmed. |
| Scope selection | Included/excluded sheets/ranges, reason, methodological basis of any combination and links to approved transformations. |
| Revision | Parent/superseded reference, changed fields and attribution; immutable historical confirmation remains addressable under retention rules. |
| Authorization | Confirmation is valid only for an actor with permission for the case and operation. An AI actor cannot impersonate the researcher. |

Confirmation must reject stale proposal/evidence revisions rather than confirming whatever is currently latest. The current revision's confirmed roles/materiality/bindings determine its aggregation, not whichever settings were last edited in the UI. A changed classification creates a recorded revision and requires evaluation of affected results before any new report; it does not alter the old one.

### R05.2 Preconditions and postconditions

- **Discover/propose:** may produce a clearly marked unconfirmed record; no final aggregation authorization.
- **Confirm:** requires authorized actor, exact immutable revision and resolution of mandatory ambiguities. Preserve explicit overrides and rationale where policy requires it.
- **Amend:** creates a new revision; retain the old report/assessments and invalidate no historical artifact silently. The new revision must not reuse old approval for changed external-processing scope.
- **Independent assessment:** may be inspectable without confirmed aggregation scope; it remains linked to its exact proposal/evidence and cannot stand in for final confirmation.
- **Aggregate:** requires material claims and confirmed role/materiality plus mandatory binding/processing approvals for the exact analysis snapshot. Zero/ambiguous/unconfirmed material scope yields a blocker, not an empty-set complete result.

Materiality is not inferred merely from Primary/Supporting/Contextual role. Confirming a transformation does not prove it methodologically valid. Missing evidence requests name the affected assertion/check and acceptable evidence category; a researcher response creates an attributable amendment instead of retrying stale evidence.

**R05 review output needed:** concrete revision/confirmation DTOs, concurrency/precondition mechanism, invalid-scope handling and user journey. D01/D09/E03/E05 remain OPEN; no new endpoints or UI code are implemented.

**R05 refinement available:** after approval to continue from R04, the [confirmation/revision contract](CONFIRMATION_REVISION_CONTRACTS_DRAFT.md) develops separate proposal/confirmation/snapshot records, operation preconditions, stale/concurrent confirmation, change dependencies and researcher-facing blockers. Exact schemas/reuse/transitions remain OPEN; CF01–CF16 are unexecuted specifications, and no gate closes.

## R06 — Review packets, phase dependencies and judge validation

### R06.1 Packet manifest

Each phase's immutable packet identifies the attempt/claim/evidence/policy versions, relevant confirmed definitions, role-specific source locators and deterministic results, exact excerpts/images, known limitations, omitted ranges, input order and model/provider/prompt/schema configuration. It declares which other outputs it may see. Pinned configuration missing or revoked is a blocker, never a silent substitution.

The packet is bounded by approved resource/privacy rules; no unrestricted full-dataset transmission is inferred. Record what was actually sent, not only the intended template. Source/model content is untrusted; embedded instructions cannot change permissions or the scientific policy. Actual prompt text changes remain subject to owner review.

### R06.2 Phase dependency table

| Phase | Required inputs | Must not receive / gate |
| --- | --- | --- |
| Initial specialized review | Its declared packet, role responsibility and appropriate visual/evidence condition under the approved protocol. | No other reviewers' conclusions. Conversation isolation is recorded without claiming scientific/model independence. |
| Paired visual condition | Same relevant claim/necessary metadata and independently prepared permitted visuals; exact concealed condition/order manifest. | Avoid original/neutral labels and uncontrolled interpretive context as specified by the proposed protocol. Randomization/pairing mechanism remains to be approved, not selected here. |
| Full Council cross-review | All four valid initial reviewer outputs plus traceable evidence and both visual conditions where applicable. | Missing/invalid initial output blocks the phase; no fabricated substitute or reduced-quorum Full Council. |
| Evidence Judge | Valid required cross-review and traceable evidence/check/claim records under approved report eligibility rules. | No new unsupported evidence, majority vote or confidence-as-proof. Phase completion cannot override unmet source/data/report gates. |
| Focused Review | Explicit policy-defined subset and clearly declared limited scope. | Permitted subsets and cross-review/judge applicability remain open; cannot be presented as a full Council. |

All LLM requests obey the approved configurable caps: 1 in flight per analysis, 2 globally, with at most 2 executing analyses and persistent waiting work. Preparatory requests need scoped identity/accounting and shared provider controls as well. Details of shared permits/rates/budgets/uncertain calls remain separate OPEN gates, not filled by a process-local semaphore.

### R06.3 Output and judge eligibility

Review output identifies the actual role/configuration/status, examined claim IDs, findings, evidence citations, uncertainty and safe error details when invalid. An output that cites a real ID still needs correspondence validation; an existing citation can be irrelevant or misrepresented.

Judge proposals are validated for permitted verdict predicates, exact claim scope, supported/contradictory/missing evidence, unresolved disputes, duplicate findings and mandatory check coverage. Proposed Partially Supported remains ineligible until explicitly specified/approved; preserve its proposal without silently translating it. Invalid judgment creates a blocker/correction record, not a fabricated final verdict.

The final synthesis explains determining material/primary findings and preserves each individual assessment. A contradiction can be fully evaluated; an absence cannot become falsehood. Material disputes that policy cannot resolve remain visible for researcher review. Any proposed resolution must cite why evidence resolves the dispute, not how many agents agree.

**R06 review output needed:** exact packets/prompts/templates/schema revisions, paired-condition protocol, Focused subset rules and all phase failure predicates. D07/E04–E06 remain OPEN; no AI execution or prompt modifications performed.

**R06 refinement available:** after approval to continue from R05, the [Council contract](COUNCIL_REVIEW_CONTRACTS_DRAFT.md) develops role packets/outputs, phase eligibility, critiques/disputes, Judge validation and actual legacy prompt/schema migration gaps. Relevant existing sections were inspected read-only; no prompt/runtime changes. Exact schemas/protocol/mappings remain OPEN; CR01–CR16 are unexecuted specifications and no gate closes.

## R07 — Acceptance corpus contracts

### R07.1 Required case record

An acceptance case needs a stable ID/version, policy/method revisions tested, provenance and permitted fixture artifacts, original byte hashes, exact assertions/classifications/bindings, methodology/prerequisites, approved expected check outputs/coverage/verdict predicates, known uncertainties, reference calculations and review authority. Synthetic/hypothetical inputs must be labeled as such; they are not real scientific observations.

Record expected behavior separately from observed execution. At this stage **all execution/result/review-pass fields are absent or explicitly unexecuted**, not populated with assumed passes. Reference expectations themselves require owner/scientific review before they can be normative acceptance criteria.

### R07.2 Candidate cases — all unexecuted specifications

| Case ID | Contract exercised | Proposed observable expectation | Evidence still required |
| --- | --- | --- | --- |
| AC01 | R01 identity/scope | Wrong owner/claim/evidence revision cannot contribute to an assessment or trigger related unauthorized reads. | Reviewed scoped records and mismatch fixtures. |
| AC02 | R01 check-state invariants | Not performed/unavailable cannot be satisfied; performed conflict is not execution failure. | Final representation profile and allowed-state table. |
| AC03 | Unresolved verdict boundary | Partially Supported proposal blocks final verdict eligibility without silent remapping; raw proposed label remains auditable. | Approved unresolved-verdict handling and candidate-response fixture. |
| AC04 | R02 count/sum/mean | Explicit selection/count/missing policy determines result and traceable intermediates. | Approved numerical conventions and independent expected outputs. |
| AC05 | R02 denominator/precision | Zero/unknown base or unresolved tolerance yields typed undefined/blocker, not a zero or convenient pass. | Numeric type, rounding/endpoint policy and boundary cases. |
| AC06 | R02 grouped/weighted | Unknown weights/units or unjustified join/mean-of-means cannot establish an overall numerical finding. | Valid/invalid group/weight examples and approved classes. |
| AC07 | R03 inference gating | Descriptive output does not fabricate p-values/intervals when method/design assumptions are unresolved. | Selected scientific method specifications, not a library default. |
| AC08 | R03 invalid design | Constant/degenerate data, incompatible groups or sparse counts are handled under explicit method rules without favorable-method fallback. | Reviewed prerequisite/degeneracy/adequacy predicates. |
| AC09 | R04 identity/notices | Reachability/hash/identifier alone cannot produce Source Verified; authentic corrections/retractions affect relevant claims separately. | Official source/notice fixtures, matching procedure and expected source predicates. |
| AC10 | R04 temporal layers | Missing publication-time identity leaves historical verification incomplete while current evidence remains separately inspectable. | Attributable original/current versions and known/unknown revision facts. |
| AC11 | R04 Ember reference | Preserve reference arithmetic without inventing historical identity or original-chart verification. | Resolve the documented historical/chart gaps before any full end-to-end pass. |
| AC12 | R05 workbook scope | Hidden sheets/formulas/ambiguous headers/locale exclusions remain visible; no arbitrary code/links or silent scope changes. | Reviewed workbook fixtures, parser/limit policy and cell lineage. |
| AC13 | R05 confirmation/revisions | AI proposal is not confirmation; stale confirmation fails; changed classifications create a new revision and preserve earlier reports. | Final confirmation protocol and authorized actor fixtures. |
| AC14 | R05 no material claim | Zero/unconfirmed material scope blocks final aggregation while independent assessments remain labeled. | Approved scope validators and expected blocker records. |
| AC15 | R06 phase dependency | Missing required reviewer blocks Full Council cross-review/completion; Focused scope is explicit. | Approved phase/Focused policy and valid/invalid role-output fixtures. |
| AC16 | R06 citation/judge | Irrelevant/nonexistent/mismatched citations and unresolved material dispute cannot become definite outcomes through voting. | Expected evidence correspondence, judge predicates and reviewed disputes. |
| AC17 | R01/R06 report gate | Complete claim work survives a failed/unavailable mandatory report gate; report remains Incomplete with explicit cause. | Approved gate matrix and separate coverage/report DTO expectations. |
| AC18 | R06 caps/cancellation | No extra dispatch through initial/cross/judge paths; cancellation/uncertainty does not falsely settle external requests. | Approved shared-control/settlement design and later operational race tests. |
| AC19 | R01–R06 public projection | Browser/JSON/export preserve independent source, coverage, report, conclusion and temporal meanings; no legacy certainty fabrication. | Exact v1/compatibility contracts and later bilingual/browser fixtures. |
| AC20 | Reproducibility/recovery | Retained manifest resolves exact inputs/outputs/versions; deletion/restore does not resurrect access or promise missing content is replayable. | Approved lifecycle, restore plan and later actual recovery evidence. |

These specifications define what must be observable, not proof that an implementation does it. Later executed results must retain environment/configuration, input/policy versions, actual output, evaluator and failure evidence. A mocked API pass cannot be reported as real scientific/provider validation. No benchmark scores, scientific accuracy percentages or test-pass counts are invented.

**R07 review output needed:** owner-reviewed expected outcomes/artifacts, independent review availability/results, and a separately authorized execution plan. E01–E07/P05/P07 remain OPEN. Scientific fixture rights and retention are prerequisites to using external source copies.

**R07 refinement available:** after approval to continue from R06, the [acceptance-corpus contract](ACCEPTANCE_CORPUS_CONTRACT_DRAFT.md) separates specifications, reviewed executable case definitions and actual execution/evaluation records; inventories all ten obligation families without claiming independent tests/coverage; and maps required source/reference/gate evidence. No fixtures/oracles/acceptance criteria are finalized, no cases executed and all 24 gates remain OPEN.

## Consolidated decisions still open after this refinement

1. R01 Separate Typed Axes is the selected recommended direction; exact canonical/public types, enum values, transitions and projections remain OPEN.
2. Meaning, eligibility and aggregation behavior of proposed Partially Supported; not an approved verdict.
3. R02 numerical conventions, precision types and boundary policies; proposed mathematical contracts require review.
4. R03 method variants/assumptions and S01–S05; no statistical method or library selected.
5. R04 concrete source connectors/proof/status/temporal predicates and retrieval-isolation implementation.
6. R05 exact confirmation/revision protocol and R06 packets/prompts/visual/Focused scope rules.
7. R07 actual reviewed case artifacts/expectations and later executed acceptance evidence.

All original 24 gates remain OPEN; these are refinements within them, not new gate completions or permission to implement. Product, numeric operating, budget, retention, recovery and migration decisions in the gate register remain unchanged. **Status remains Recommended for owner approval.**
