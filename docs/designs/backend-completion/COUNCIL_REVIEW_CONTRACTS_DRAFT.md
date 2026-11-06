# EvidenceTwin V1 — R06 Council packets, phases and evidence judging

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R06 after approval to continue from [R05 confirmation/revision contracts](CONFIRMATION_REVISION_CONTRACTS_DRAFT.md). **All 24 gates remain OPEN.** Exact packet/output schemas, Focused subsets, prompts, visual templates, paired-condition protocol and validation implementations remain proposals. No scientific/statistical method, library, production code, deployment or capability enablement is selected or authorized. All acceptance obligations below are unexecuted specifications.

Partially Supported remains a proposed/unresolved claim verdict. Model output is an analytical contribution, not a primary source, deterministic calculation or automatic final assessment. Agreement, model diversity and successful phase execution do not establish scientific truth.

## 1. Existing integration boundary — inspected, not changed

Relevant sections of the existing prompt files and `services/provider.py` / `services/workflow.py` were inspected during this refinement. This was a read-only integration check, not a full prompt/domain audit or runtime test.

| Existing asset | Relevant boundary for the V1 contract |
| --- | --- |
| `prompts/shared.md` | Shared role/evidence discipline and reviewer JSON shape; initial reviews must not consume other reviewers' conclusions. Existing `partially_supports` is a model position, not approval of a canonical verdict. |
| `prompts/VISUAL ANALYST.md` | Original/neutral inspection and framing scope; a neutral label is not scientific proof. The actual controlled-disclosure protocol needs separate review. |
| `prompts/STATISTICAL AUDITOR.md` | Quantitative interpretation and referenced calculations; model arithmetic is not a deterministic verification result. |
| `prompts/SCIENTIFIC SKEPTIC.md` | Study/design/inference/generalization review; suggested alternatives require evidence rather than model authority. |
| `prompts/COUNTERFACTUAL ANALYST.md` | Presentation-sensitivity comparison; missing Neutral Twin/transformation history prevents reliable comparison. |
| `prompts/Cross-Reviewer.md` | Critique existing findings without erasing originals or resolving by majority. |
| `prompts/EVIDENCE JUDGE.md` | Legacy model verdict vocabulary/definitions need explicit reconciliation with canonical V1 eligibility and separate report fields. |
| `services/provider.py` | Existing strict JSON/identity/reference checks provide structural boundaries; ID existence alone is not evidence correspondence. |
| `services/workflow.py` | Existing exploratory output remains model interpretation and overview assessment remains `not_evaluated`; do not reinterpret that as V1 scientific verification. |

**Confirmed contract migration gaps:**

- Existing Judge prompt/schema permits `partially_supported`. The new canonical contract explicitly leaves Partially Supported unresolved. Preserve legacy/model proposals as interpretations; do not promote, silently rewrite or map them to a new approved verdict.
- Existing `unsupported` vocabulary does not directly supply the new Contradicted-versus-Insufficient-Evidence semantics. No automatic `unsupported → contradicted` mapping is approved.
- Existing combined Judge `overall_verdict` is not the new independent claim coverage, report verification, overall conclusion and temporal layers.
- Current reference validation explicitly checks referential integrity, not scientific support. An existing ID can be irrelevant, mismatched or misinterpreted.
- Existing exploratory shared-provider execution is not a completed per-role provider/configuration management contract. Pinning, secret access and unavailable configuration behavior need the new approved adapter design.
- Schema-valid `insufficient_input` is not proof that a role's mandatory review obligations were completed. Protocol eligibility must examine substantive required scope as well as JSON validity.
- Prompt filenames, labels and metadata can reveal visual conditions. A future blinded protocol needs explicit packet/identifier/disclosure review; existing prompts alone do not demonstrate that blinding occurred.

No prompt text, provider schema, workflow code or configuration is modified by this document. Any eventual change needs reviewed/versioned prompts, compatibility treatment and separate implementation authority.

## 2. Independent review packet contract

Each dispatched packet must identify the authorized case/claim/evidence/classification/attempt/temporal revisions, approved role/protocol, actual supplied evidence and pinned non-secret model/prompt/schema configuration. A packet cannot reference “latest data” or mutable UI settings as its scientific basis.

| Packet component | Required meaning |
| --- | --- |
| Claim definition | Relevant exact assertion, units/population/period/denominator and confirmed scope where required. Preserve unresolved assumptions. |
| Evidence manifest | Exact source/data/image/check IDs and versions; source assurance, inspected scope, data limitations and provenance. |
| Deterministic results | Approved computation/check records and actual outputs/precision metadata; never substituted model arithmetic. |
| Selected content | Exact passages/ranges/images/excerpts with selection rationale, omitted scope and traceable original references. |
| Disclosure profile | What this role/condition may see, what must remain withheld and why. Initial isolation excludes other reviewer conclusions. |
| Model execution config | Pinned provider/model and available version, parameters, prompt/schema revisions, required image support and authorization context; no secrets in the packet. |
| Limits/authorization | Per-role context/image/resource and external-processing scope under approved limits/terms; no unbounded transmission. |

Retain what was actually sent, including ordering and any truncation/exclusion, not only an intended template. An evidence excerpt cannot appear as complete dataset coverage. New content changes the packet revision and may affect processing authorization and result equivalence.

Evidence and prior model text are untrusted content. They cannot change policy, permissions, output predicates, tools or secret access. Any tool-assisted evidence acquisition or calculation belongs to the approved scoped Core/adapter contract, not arbitrary instructions found in a chart or document.

## 3. Role-specific obligations

| Role | Relevant supplied basis | Permitted contribution and explicit limit |
| --- | --- | --- |
| Visual Analyst | Actual visual inputs, chart/data binding, labels/scales/units, relevant uncertainty and recorded rendering assumptions. | Evidence-linked visual framing observations. No invented pixel-derived exact dataset or significance/causality conclusion. |
| Statistical Auditor | Exact data scope, deterministic outputs, denominators/comparability, method/prerequisite records and uncertainty limits. | Inspect numerical/statistical consistency and unsupported interpretation. Any model calculation remains a proposal until deterministic reproduction. |
| Scientific Skeptic | Claim definition, source/methodology/study design and relevant population/sampling/alternative-explanation evidence. | Identify evidenced methodological limits without declaring speculative confounders true or rejecting evidence merely because it is observational. |
| Counterfactual Analyst | Actual compared visual conditions, same relevant evidence, controlled-transform/provenance record and eligible interpretation observations. | Inspect framing sensitivity. Missing/unsupported twin or transformation history must remain a reliable-comparison blocker, not a guessed chart. |

Role names do not prove roles executed correctly. Record actual inputs, configuration, output status and coverage. Shared source/model errors remain possible even with isolated conversations or different model families.

## 4. Visual-condition and disclosure contract

The recommended Blind Optics direction uses the same relevant claim and necessary metadata across compared conditions, independently prepared visual inputs, controlled disclosure, randomized order where paired review applies and no unnecessary original interpretation. Cross-review may later access the relevant conditions and evidence records.

The implementation must record the real condition/ordering/disclosure assignment and the mapping to original artifacts for audit without leaking withheld labels into the initial packet. Exact aliasing, filename/identifier treatment, pairing/randomization method, role applicability and number of condition-specific calls remain OPEN. No owner prompt is silently edited to achieve this.

Four reviewer **roles** do not necessarily mean four total LLM **requests** if an approved paired protocol uses condition-specific reviews. Requests, cost, context and shared permits must reflect actual calls. A combined role output must retain its component condition records rather than claiming one conversation was isolated from content it already saw.

Neutral Twin construction is a separate approved rendering contract; this protocol cannot label a guessed/unsupported chart as a standardized comparison. If source conditions or transformations are missing, retain the resulting limit and block any mandatory comparison-dependent completion.

## 5. Reviewer output and validation layers

| Layer | Validation obligation |
| --- | --- |
| Transport/execution | Actual call/response/error/uncertainty and pinned configuration; HTTP success is not review success. |
| Structure | Correct declared role/phase identity, supported schema, required fields and no unknown/coerced values. Exact v1 shapes remain OPEN. |
| Scope | Exact case/claim/evidence/packet/condition/attempt references and required claim coverage; no fabricated identifiers. |
| Evidence correspondence | Cited source/data/check actually supports the observation in context, not merely exists in the manifest. |
| Role coverage | Actual obligations and inputs were examined; a valid insufficient-input message does not establish completed scientific review. |
| Policy eligibility | Permitted interpretations/verdict predicates and mandatory check rules; no unsupported source verification or canonical verdict promotion. |
| Publication | Whole-record validity and current authorized scope/attempt/fencing under the R01 contract. |

Required logical output components include role/configuration/phase, examined claims and packet revision, findings with evidence IDs and concise reasoning, uncertainty/missing inputs, exact inspected scope and safe error details. Raw/generated text may be retained under policy separately from accepted canonical contributions.

Finding identifiers must be unique in their declared scope and target exact source/claim/condition references. A finding marked severe is not automatically material or scientifically established; confirmed materiality and policy evidence still govern aggregation. A reviewer position remains an interpretation rather than a final canonical claim verdict.

## 6. Full Council and Focused phase contracts

| Phase | Prerequisite and required behavior |
| --- | --- |
| Initial specialized review | No access to other initial reviewers' conclusions; use the approved role/condition packet and pinned configuration. Sequential scheduling under the per-analysis cap does not authorize conversation sharing. |
| Full Council cross-review | All four required initial role outputs are valid and protocol-eligible. Retain exact versions and any condition-specific components; do not fabricate missing reports or quietly reduce quorum. |
| Evidence Judge | Valid required cross-review plus original evidence/checks and actual initial contributions; proposed synthesis remains bounded by canonical policy validation. |
| Full Council completion | Required role/phase obligations met under the approved protocol; failed/missing mandatory work blocks completion. Completing AI phases does not satisfy unresolved source/data/statistical/report gates. |
| Focused Review | Explicitly declared smaller subset and scope. Exact permitted roles and cross-review/Judge applicability remain OPEN; never represent it as completed Full Council. |

Eligibility of insufficient-input outputs needs exact phase predicates: retain their valid diagnostics but do not count missing required work as completed solely because the response parses. If the protocol permits diagnostic cross-review of partial work, it must be separately declared and cannot be represented as the required completed Full Council phase. No such reduced protocol is selected here.

Model refusal, invalid schema, missing citations or incomplete mandatory role scope must remain inspectable. Bounded retries follow the approved failure/replacement policy; do not repeatedly re-prompt until a desirable answer appears or silently substitute another pinned provider/model.

## 7. Cross-review and disagreement records

Cross-review consumes exact accepted reviewer-output versions and evidence packets. A critique identifies target reviewer/finding, issue category, claim/evidence/condition scope, supporting references, explanation and proposed correction. It does not erase or rewrite the original report.

Record disagreements separately with the disputed assertion, each actual position, supporting/conflicting/missing evidence, competing assumptions and resolution requirements. Duplicate findings may be grouped with explicit original references, but repetition does not increase evidentiary weight or create independent confirmation.

Resolution requires traceable evidence and an approved scientific rule. If a dispute cannot be resolved, record that and its effect on the claim/conclusion. No agent-count/majority/confidence score resolves a conflict. Corrected contributions create attributable revisions linked to original findings; no silent convergence story.

## 8. Evidence Judge contract

The Judge may propose an evidence-linked synthesis from valid contributions, but it is not an unrestricted scientific authority. The canonical eligibility/aggregation layer retains final policy control.

The proposal must identify each claim, its exact scope, supporting/conflicting/missing evidence, source and deterministic checks, unresolved disputes, limitations and recommended interpretation. It must explain which confirmed material/primary findings determine any proposed overall conclusion.

Validate:

1. Exact case/claim/evidence/attempt/protocol versions and permitted output vocabulary.
2. Citation existence **and correspondence**, not counts of references or reviewer votes.
3. Each claim-verdict predicate against the approved scientific applicability/assurance requirements.
4. Separate claim coverage, report verification and supported/mixed/contradicted/inconclusive conclusion rules.
5. Primary-claim and materiality confirmation; unresolved primary disputes cannot be hidden by definite subsidiary findings.
6. Mandatory report/phase blockers, historical/current independence and reproducibility references.
7. Preservation of original review/critique/disagreement records and actual missing information.

Partially Supported remains unresolved and cannot pass final verdict eligibility. Legacy `unsupported` cannot silently become Contradicted. Existing model-output fields are retained only under an explicit reviewed compatibility/interpretation contract, not reused as the new report DTO.

Invalid/unsupported synthesis produces a structured blocker/correction requirement, not an invented final outcome. Eligible incomplete reports may preserve completed findings and uncertainty without claiming Verified. A corrected Judge response does not remove the requirement to revalidate its full output.

## 9. Scheduling, private processing and audit

All requests, including preparatory and condition-specific calls, use approved shared controls: initially 2 executing analyses, 1 in-flight LLM request per analysis, 2 globally. Provider/model rate/context/image/budget limits and actual processing authorization apply independently. Per-role pinned assignments need a real adapter/configuration contract; provider credentials never enter packet/API/log content.

Cancellation prevents undispatched work and active publication by the cancelled attempt; in-flight calls remain under explicit settlement/usage reconciliation. Late outputs cannot overwrite newer scope or prove a permit can be released. Dispatch uncertainty cannot trigger blind paid replay.

The manifest retains actual prompt content/version or recoverable reference, model/configuration, packets/ordering/disclosures, validated and invalid outputs, calls/usage/uncertainty, critiques/resolutions and policy/publication decisions subject to retention/access rules. Historical stochastic text inspection is not identical-regeneration proof.

## 10. Acceptance obligations — all unexecuted specifications

| ID | Required future observable behavior |
| --- | --- |
| CR01 | Initial roles cannot consume another initial review's conclusions through shared conversation or packet content. |
| CR02 | Role/claim/evidence/condition identity mismatches are rejected before canonical admission. |
| CR03 | An existing citation ID without supporting content cannot establish a factual finding. |
| CR04 | Model arithmetic/source assertions remain interpretations unless the corresponding deterministic/source checks establish them. |
| CR05 | Missing/unsupported Neutral Twin or transformation record blocks reliable comparison without fabricated visuals. |
| CR06 | Actual blinded-condition disclosures/order are auditable; filenames/labels cannot silently defeat the declared protocol. |
| CR07 | Four role identities do not imply four total calls, independent models or completed scientific obligations. |
| CR08 | Missing/invalid required initial work blocks completed Full Council cross-review/completion. |
| CR09 | Focused scope and any diagnostic partial review are not labeled completed Full Council. |
| CR10 | Critiques/corrections preserve original findings; duplicate observations do not become additional independent evidence. |
| CR11 | Material disagreements retain actual positions/evidence and cannot resolve by vote/confidence. |
| CR12 | Judge validation separates claim coverage/report verification/conclusion/temporal meaning and honors mandatory blockers. |
| CR13 | Partially Supported and legacy Unsupported cannot silently become approved new verdicts. |
| CR14 | Pinned unavailable configuration/refusal/schema failure produces explicit limits rather than silent provider substitution. |
| CR15 | Every initial/cross/Judge/condition call obeys shared limits and authorized disclosed processing scope. |
| CR16 | Cancellation/stale/revoked-scope results cannot actively publish; uncertain external calls remain reconciled. |

No CR case has executed or passed. The current prompt/schema inspection establishes integration facts only, not scientific correctness, successful role execution or a completed live Council.

## 11. Baseline fingerprint and open review items

SHA-256 fingerprints of the nine inspected public prompt/runtime assets were recorded for change checking during this design task. They identify local bytes, not owner approval or scientific validation:

| Asset relative to `backend/evidencetwin_backend/` | SHA-256 |
| --- | --- |
| `prompts/COUNTERFACTUAL ANALYST.md` | `0fa1ee0620c0c0ea7a5775ccea9c623e2953bf9af25ad1b1964837b2adaf426e` |
| `prompts/Cross-Reviewer.md` | `afa021c366c2d89dc0c27cf9d0776b7d601122b13342c02b091e4f4a375201c4` |
| `prompts/EVIDENCE JUDGE.md` | `eaf5bec2f9e9c9453d07c70fca8c23d00781848022435e9476932121e6f74c41` |
| `prompts/SCIENTIFIC SKEPTIC.md` | `e6819dcadfc409c6d6a3290856939c3388a45fbdff6825e3dadee65f9ca134b2` |
| `prompts/STATISTICAL AUDITOR.md` | `272031b6892902dfbba3b38fb72d898baa951b59c650df672809608e64c789c4` |
| `prompts/VISUAL ANALYST.md` | `0c1a9aa25dc555b1c9cf7021561d90878e42595f21536c53bbe5fd84b3ccde6c` |
| `prompts/shared.md` | `7c0e37cc05f51e7048a64a943c5ce95494649a4fdbce31b6ba320208a384da02` |
| `services/provider.py` | `5a3e3fde134c22da8d7f0b5d5c00db34b3d41145532b235742af4ab2fb29e1f9` |
| `services/workflow.py` | `c5675c3f3c54b8dc2e1d993deee18aad9a41be508ddc690c4a09db8080b887b3` |

Still OPEN: exact canonical/legacy output mappings; proposed verdict definition/eligibility; packets/omission limits; reviewed prompt revisions; visual disclosure/assignment; phase/insufficient-input predicates; Focused subsets; pinned provider adapter; substantive citation validation; actual reviewed fixtures and later execution evidence.

R07 acceptance-corpus refinement is next. **Status remains Recommended for owner approval; all 24 gates remain OPEN.** No prompt, backend/frontend source, method/library or capability is changed by this document.
