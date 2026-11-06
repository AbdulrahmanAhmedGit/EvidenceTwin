# EvidenceTwin V1 — R07 versioned acceptance-corpus contract

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R07 after approval to continue from the [Council contract](COUNCIL_REVIEW_CONTRACTS_DRAFT.md). **All 24 gates remain OPEN.** Corpus schema, exact fixture artifacts/expected outputs, review authority and acceptance criteria remain proposals. No statistical method, library, production code, deployment, test execution or capability enablement is selected or authorized. All referenced acceptance cases remain **unexecuted specifications**.

Partially Supported remains a proposed/unresolved claim verdict. A case must not make it an approved expected outcome or silently map it to another verdict. A test of its rejection/blocked eligibility is distinct from approval of its scientific meaning.

## 1. Three artifacts, three meanings

| Artifact | Required meaning |
| --- | --- |
| Acceptance specification | Proposed behavior/invariant, declared scope, required evidence and why it matters. It can exist before an implementation or approved method. |
| Reviewed executable case definition | Exact permitted fixtures, method/policy/configuration, expected outputs/predicates and recorded approval sufficient for a separately authorized test execution. It does not imply execution occurred. |
| Execution/evaluation record | Actual environment/configuration, inputs/outputs/events, observations and evaluator decision from a real authorized run. It cannot be populated from a proposal or intended result. |

All current obligation rows are specifications. Existing manually investigated evidence can be a reference input without becoming a passed executable case. No blank result field, empty failure list or missing execution record may be interpreted as a pass.

## 2. Corpus and case identity contracts

Exact field names, JSON schemas, file layout and storage/API representations remain OPEN. The logical record needs these components:

| Component | Required content |
| --- | --- |
| Corpus identity | Stable corpus ID/version, declared purpose/scope, policy/specification versions and attributable revision history. |
| Case identity | Stable case/version, originating specification IDs, related/duplicate obligations and intended capability scope. |
| Evidence class | Real-source reference, explicitly synthetic/hypothetical input, controlled invalid/malicious input or another approved declared class. Never represent synthetic content as observed science. |
| Scientific scope | Exact claims, primary/supporting/contextual roles, separate materiality, confirmed/expected-confirmation state and historical/current layer. |
| Fixture manifest | Permitted artifact references/hashes/versions, provenance, source rights/retention/access, original versus derived content and exact missing inputs. |
| Procedure/policy | Approved method/context/source/applicability/protocol/schema references and required prerequisites; no runtime defaults fill missing specifications. |
| Expected results | Typed computations/units/precision, evidence/check/claim/report predicates, expected blockers/errors and justified unavailable outputs. |
| Review record | Who reviewed what exact version, approval scope/time, scientific basis, unresolved issues and independent-review availability/status. |
| Execution plan | Required environment/data/configuration, adapters/mocks versus live boundaries, resource/privacy/spend authorization and observables. |
| Gate traceability | Which specific Decision/Enablement/Pilot requirement the case can inform, and which it cannot establish. |

Changing fixtures, expected outputs, policies or scientific scope creates an attributable case/corpus revision. Previous execution records remain tied to their original versions. Do not improve a historical pass by editing its expected output afterward.

## 3. Fixture manifest and admissibility

Retain original bytes and exact source/dataset/image identities where permitted. Derived fixture tables, extracted text, synthetic defects and transformations need explicit lineage and labels. A source excerpt, metadata-only reference and complete dataset are different evidence scopes.

For every artifact identify original/canonical reference, version/retrieval provenance, stored object/hash, relevant locator/range, actual coverage, known limitations and ownership/access/retention permissions. A hash does not establish official authenticity or publication-time identity. A public source does not make private research annotations available to unrelated cases.

Synthetic arithmetic and controlled provider/error fixtures are permitted only as clearly labeled acceptance inputs. They may test validation or application behavior; they do not prove source authenticity, statistical procedure adequacy or real provider operation. No live confidential/provider credentials belong in fixtures or corpus manifests.

Expected unavailable/missing-evidence states must be deliberate inputs, not accidentally missing files. A case with an unresolved required method or unreviewed expected output is not ready for execution as scientific acceptance; retain its specific readiness blockers. A test that correctly rejects an unapproved method does not enable that method.

## 4. Expected-output contract

An expected-output record must state the exact quantity/claim/condition it tests and the approved comparison predicate. Separate:

- Deterministic output and context/units/selection/precision, including undefined versus missing/blocked results.
- Source identity/content/provenance/notice findings and their applicable proof.
- Per-check applicability, execution and requirement determination; negative evidence is not technical error.
- Claim verdict eligibility with supporting/conflicting/missing references and unresolved disputes.
- Claim coverage, report verification, overall conclusion and historical/current layers.
- Unauthorized/stale/invalid/publication blockers and safe API/UI behavior.

An expected number without denominator, units, precision and input scope is not an adequate numerical oracle. No unapproved statistical default, tolerance, p-value threshold or rounding rule may become normative merely because it appears in a fixture.

For AI contributions, exact prose matching alone is insufficient. Define policy-based observables such as valid identities/citations, supported evidence correspondence, required missing-evidence disclosure and preservation of disagreements. The final predicate/evaluation method still needs approval; an LLM cannot be the sole authority certifying its own scientific correctness.

Review factual claim interpretations against the traceable evidence and deterministic outputs where applicable. Qualitative reference judgments need attributable owner/domain review; disagreements in the reference itself are recorded, not averaged away. No accuracy percentage or benchmark score is supplied by this contract.

## 5. Review and readiness records

Keep owner scientific-policy approval, independent domain review, technical contract review and actual execution evaluation distinct. Record the exact artifact/version and scope of each approval. Earlier brainstorming/design reviews are not scientific ground-truth validation or executed acceptance evidence.

The owner approves reference judgments and calculations. Independent domain review is recorded where available; if it is unavailable, say so and preserve the required acceptance restriction rather than claiming independence. Named reviewer assignments, exact review requirements and material-change rereview policy remain OPEN.

A reviewable readiness record must identify unresolved method/precision/source/fixture/permission/configuration dependencies. “Ready to review,” “approved expected case” and “executed pass” cannot be synonyms. Exact readiness enums/transitions remain OPEN; none is silently assigned by this document.

If an expected outcome depends on proposed Partially Supported semantics, that outcome remains unresolved and cannot be approved by inference from an old prompt or frontend enum. Negative cases may require rejection of that proposal without defining the verdict itself.

## 6. Existing specification-family inventory

These families contain **150 specification rows in total**, including overlaps and refinements. This is a document inventory, **not 150 independent cases/tests**, measured coverage or executed results. Case deduplication/composition and actual fixture counts remain OPEN.

| Family | Rows | Definition | Primary concern |
| --- | --- | --- | --- |
| AC01–AC20 | 20 | [R01–R07 overview](SCIENTIFIC_CONTRACTS_DRAFT.md) | Cross-cutting scientific, scope and report acceptance. |
| RC01–RC12 | 12 | [R01 representation comparison](CANONICAL_CHECK_CONTRACT_OPTIONS.md) | Canonical meaning and invalid combinations; A is the subsequent recommended direction. |
| TA01–TA12 | 12 | [Typed axes](TYPED_CHECK_AXES_DRAFT.md) | Three dimensions, whole-record validation and trust boundaries. |
| LP01–LP12 | 12 | [Lifecycle/publication](CHECK_LIFECYCLE_PUBLICATION_DRAFT.md) | Mutations, authorization/fencing, races and truthful incomplete views. |
| NC01–NC16 | 16 | [Numerical contracts](NUMERICAL_CONTRACTS_DRAFT.md) | Units, inputs, arithmetic scope, undefined results and comparisons. |
| DC01–DC14 | 14 | [Decimal refinement](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md) | Original representations, context/tolerances and approved conversion boundaries. |
| ST01–ST16 | 16 | [Statistical contracts](STATISTICAL_CONTRACTS_DRAFT.md) | Descriptive versus inference, design evidence and candidate-method blockers. |
| SP01–SP16 | 16 | [Source procedures](SOURCE_PROCEDURES_DRAFT.md) | Retrieval/authenticity/content/notices and temporal binding. |
| CF01–CF16 | 16 | [Confirmation/revisions](CONFIRMATION_REVISION_CONTRACTS_DRAFT.md) | Researcher authority, stale confirmation, amendments and exact snapshots. |
| CR01–CR16 | 16 | [Council protocol](COUNCIL_REVIEW_CONTRACTS_DRAFT.md) | Role packets, phase eligibility, evidence judging and legacy gaps. |

No family has executed scientific acceptance under this design. Structural Markdown/ID/link checks performed while drafting do not execute any of these acceptance obligations.

## 7. Proposed capability traceability

| Enablement scope | Relevant proposed families | What still requires actual evidence |
| --- | --- | --- |
| E01 numerical/statistical | AC04–AC08, NC/DC/ST | Approved algorithms/variants/contexts/prerequisites and independently reproducible expected results; numerical correctness alone does not validate sources. |
| E02 source/temporal | AC09–AC11, SP | Approved connectors/source predicates, exact official/historical proof, notices and isolation. Manual retrieval/arithmetic is insufficient. |
| E03 ingestion/transforms | AC06/AC12, NC/DC/CF/SP | Exact bounded parser, worksheet/formula/locale/lineage/exclusion behavior and approved transformation rules. |
| E04 visuals/Council | AC15/AC16, CR/SP | Real visual evidence, reviewed rendering/disclosure/prompt protocol and full role/phase eligibility. |
| E05 assessment/report | AC01–AC03/AC13–AC17, RC/TA/LP/CF/CR | Canonical schema/predicates and preserved source/coverage/conclusion/temporal meanings; no majority or unapproved verdict. |
| E06 provider execution | AC18, LP/DC/CR | Actual configured controls, consent/minimized packets, numeric boundaries, pinned roles, limits, cancellation/settlement. Mocks do not prove real provider availability. |
| E07 API/browser integration | AC19, RC/TA/LP/CF/CR | Implemented v1/compatibility projections, authorization/errors and English/Arabic keyboard/responsive journeys. |

Pilot gates additionally need the actual hosted identity/isolation, workload/cost, privacy/retention, recovery, observability and migration evidence in the existing gate register. These families do not automatically cover every P01–P08 requirement or close a gate by association.

## 8. Ember case: readiness example, not a pass

The [Ember reference investigation](ember-2025-acceptance/acceptance_case.md) already preserves report-associated/current downloads, retrieval metadata/hashes and reference calculations. Those are existing research artifacts, not a new scientific run or approved executable-case oracle.

| Aspect | Corpus treatment |
| --- | --- |
| Research scope | Descriptive global electricity-generation share for the stated period, not total energy, significance or causal inference. |
| Existing reference arithmetic | Preserve its exact dataset/schema/filter/unit/context references; do not turn a research extraction/rounding example into the approved V1 parser/rounding policy. |
| Historical input identity | Still incomplete until publication-time dataset and applicable methodology binding is established. Later matching arithmetic is not proof. |
| Current snapshot | Separate existing identified reference snapshot; a new refresh would create a new case/evidence revision, not silently update an oracle. |
| Original chart | Original-chart inspection/retained accessible evidence remains a gap; no Neutral Twin or visual audit pass is claimed. |
| Scientific/technical execution | No completed backend source/Council/statistical/hosted acceptance run is inferred from manual investigation. |
| Expected status | Review exact missing-proof/report/claim predicates under the approved policy before turning them into a normative executable expected output. |

No source URLs were re-fetched, CSV calculations rerun or historical facts newly verified during this R07 drafting task. No claim that 43% must pass is permitted. Estimates/methodology/version limits and unknown revision reasons must remain explicit.

## 9. Execution record contract — future authorized runs only

When separately authorized, an execution record must identify the immutable case/fixture/specification versions, actual implementation/environment, selected approved configurations, time and executor, actual outputs/events/artifact references, evaluator decision and deviations. Retain safe failures and blocker evidence, not only successful observations.

Distinguish evidence classes explicitly:

- Mocked/synthetic component or transport execution.
- Real local deterministic procedure execution under a specified environment.
- Controlled live external-source/provider execution with actual configuration and authorization.
- Hosted account/worker/file/report/browser integration and recovery/load execution.

These are conceptual classifications, not selected enum strings. Evidence from one class cannot silently become proof of another. No live provider call without approved privacy/spend controls, and no actual execution record may be backfilled from expected output.

Record passed predicate, failed predicate, blocked/unavailable prerequisite and not-executed scope distinctly. Exact run/evaluation statuses remain OPEN. A missing artifact or evaluator is not a pass; partial runs cannot claim all-case or all-capability coverage.

## 10. Nondeterminism and reference stability

Deterministic methods bind exact input, method/context and numerical comparison policy; approved reproducibility/error tolerances must not be widened after observing a failing output. Stochastic/model results retain actual text, parameters/configuration and policy-based evaluation, without guaranteeing identical regeneration.

If a later method, library, prompt, model, source version, fixture or expectation changes, identify affected cases and create a new evaluation scope. Preserve older results and why the reference changed. No invented reference fixes that merely turn failures into passes.

Material reference disagreement triggers attributable review and an unresolved case expectation. It is not resolved by more model votes or by using the system's own final answer as ground truth. Changed source data must preserve the historical/current policy rather than erase scientific history.

## 11. Gate evidence and restrictions

| Evidence offered | Can inform | Cannot establish by itself |
| --- | --- | --- |
| Written contract or specification row | Decision review and proposed acceptance criteria. | Implementation, enabled capability or a passing test. |
| Reviewed expected artifact/calculation | Reference/oracle approval for its declared scope. | Actual implementation execution or unrelated scientific methods. |
| Mocked transport/UI result | Frontend/contract behavior under the fixture. | Real Flask/scientific/provider integration. |
| Local deterministic result | Actual implemented procedure under recorded inputs/context. | Source authenticity, clinical validity, model independence or hosted isolation. |
| Live role response | Actual provider execution under recorded conditions. | Scientific truth, adequate cross-review or all mandatory report gates. |
| Coordinated restore/run evidence | Specific verified recovery behavior under configuration. | Universal availability, every retained artifact or future migrations. |

Any eventual gate-closing record must identify its approved scope, actual evidence and explicit authority under the gate register. R07 approval for refinement cannot close D07/E01–E07/P07 or any other gate. No measured accuracy/reliability/latency or benchmark improvement is asserted here.

## 12. Remaining inputs and design handoff

Still required: approved corpus/case schemas and lifecycle; exact reviewed scientific specifications; permitted real/synthetic fixtures; expected outputs/predicates; named scientific/reference reviewers and unavailable-review handling; actual source/historical/chart proof; selected implementation/configurations under separate authority; and later execution/evaluation records.

R01–R07 now each have an ordered refinement document. This means the design areas have been drafted, **not** that their exact contracts are formally approved, implementations exist or gates are complete. The next design step is cross-contract consistency review and an explicit remaining-decision bundle before formal specification approval.

**Subsequent review:** the owner approved that next review. The [cross-contract self-review report](CROSS_CONTRACT_REVIEW.md) records editorial reconciliation and FD01–FD10 remaining tasks. This is document review, not scientific/reference approval or execution of any acceptance case; all boundaries above remain unchanged.

Keep the benchmark product disabled until a separate approved rubric exists; corpus obligations are not benchmark scores. Keep NYAS student evaluation distinct and MCP outside the initial release dependency. **Status remains Recommended for owner approval; all 24 gates remain OPEN.**
