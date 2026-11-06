# EvidenceTwin V1 — R05 researcher confirmation and revision contracts

Author: Abdulrahman Ahmed. Date: 2026-11-06.

**Status: Recommended for owner approval.** This refines R05 after approval to continue from [R04 source procedures](SOURCE_PROCEDURES_DRAFT.md). **All 24 gates remain OPEN.** Exact field names/enums, endpoint DTOs, version/precondition mechanisms, lifecycle transitions and result-reuse rules remain proposals. No production code, deployment, statistical method/library selection or capability enablement is authorized. All acceptance obligations below are unexecuted specifications.

Partially Supported remains a proposed/unresolved claim verdict. Researcher confirmation establishes attributable choices and scope, not scientific truth, source authenticity or a right to change evidence-based verdicts directly.

## 1. Distinct kinds of approval

| Researcher action | What it establishes | What it does not establish |
| --- | --- | --- |
| Confirm claim wording/role/materiality | Research intent and classification for an exact claim revision. | That the claim is scientifically correct or every proposed assumption is a fact. |
| Confirm evidence binding | Which exact passage/dataset/range the assertion concerns; explicit ambiguity resolution. | That the source is authentic or the binding corresponds correctly without independent checks. |
| Select/exclude data scope | The requested worksheets/ranges/observations and attributable exclusion rationale. | That the excluded evidence is irrelevant to every conclusion or that a subset equals the entire dataset. |
| Approve transformation | Requested recorded parsing/filter/join/unit/aggregation specification. | Methodological validity, appropriate denominators or admissibility of unapproved procedures. |
| Authorize external processing | Permission for the disclosed provider/data/stage scope under actual configured terms. | Permission for silent rerouting or unrelated future transmission. |
| Acknowledge limitations | Awareness of specific gaps/limits. | Satisfaction or waiver of mandatory scientific checks. |

Scientific-policy approval, deployment/operator permissions and researcher confirmation are separate authorities. A user cannot convert an unavailable Mandatory check into Optional by clicking a confirmation control.

## 2. Logical record contracts

Names describe conceptual components, not selected public fields, Python classes or persistence layout. Proposed and confirmed values must remain structurally distinguishable; a single mutable role/materiality field cannot erase the proposal/confirmation history.

### Proposal record

- Authorized case and exact claim/evidence/source/parser/selection revisions being considered.
- Original claim text and proposed normalized assertion, role and materiality as separate values.
- Proposed rationale, explicit assumptions, evidence bindings and relevant ambiguity/limit records.
- Proposing component/model configuration where applicable, observation time and policy/specification references.
- Stable proposal/revision identity and predecessor relationship, with enough content identity to reject stale confirmation.

A proposal may come from AI, deterministic discovery or a researcher edit. Its origin is explicit; an AI proposal cannot be labeled researcher-confirmed because the researcher initiated extraction.

### Confirmation record

- Exact proposal/content/scope revision confirmed, not an instruction to confirm whichever record is latest.
- Researcher-confirmed wording/role/materiality, bindings, selected data scope and required ambiguity decisions, including explicit overrides.
- Internal authorized actor identity and trusted audit time; client-supplied actor/time fields are not authoritative proof.
- Required explanation/approval evidence under the applicable policy, including combination/transform justification.
- Immutable confirmation revision and predecessor/superseding relationship where appropriate.
- Separately referenced processing-authorization record if execution transmits evidence externally.

The confirmation identity/content equivalence mechanism remains OPEN: version IDs, content fingerprints and guarded update tokens need a concrete D01/D09 contract. No cryptographic signature, hash algorithm or API precondition syntax is selected here.

### Analysis scope snapshot

An accepted analysis/attempt binds exact confirmed claim/classification/evidence/binding/selection/transformation references, requested mode, pinned configuration and applicable policy versions. Store the snapshot used for each assessment/report, not a live pointer to mutable settings. Required processing authorization must match that execution scope.

External-source snapshots, classification revisions, attempts and report versions keep distinct identities. A new evidence revision is not a retry of unchanged evidence; an updated provider/model configuration cannot silently rewrite a pinned attempt.

## 3. Classification and materiality predicates

Approved role meanings remain Primary, Supporting and Contextual. Materiality is a separate decision; do not automatically set it from role or infer role from a materiality flag. Multiple Primary claims are permitted under the incorporated direction. Exact invalid-combination rules still require a reviewed policy rather than arbitrary UI defaults.

Before final aggregation, require:

1. An authorized confirmation for every required role/materiality assignment in the target scope.
2. At least one material in-scope claim; no empty-set Complete result.
3. No unresolved conflict/ambiguity that prevents a defensible classification or essential binding.
4. The analysis uses exactly the confirmed classification revision, not a later edited value.
5. Evidence/methodology checks remain independent of the confirmation decision.

Whether a particular role/materiality combination is scientifically inappropriate, or a scope needs a specific Primary assignment, must be handled under an explicit policy and researcher correction process. Do not silently supply a Primary role, mark every claim material or hide contextual evidence to obtain an aggregate result.

## 4. Operations and pre/postconditions

These are proposed semantic operations; exact endpoints, states and transition graph remain OPEN.

| Operation | Preconditions | Required result |
| --- | --- | --- |
| Discover/propose | Authorized exact input revision; configured bounded discovery/extraction and actual provenance. | Clearly unconfirmed proposals, worksheet/source inventory and explicit limitations. No final-aggregation permission. |
| Review/override | Current proposal and authorized actor; show proposed values/rationale and evidence scope. | Candidate researcher choices retained separately from the original proposal. No scientific verdict editing. |
| Confirm | Exact reviewed proposal/content/evidence revision still current for the requested confirmation; required ambiguities resolved and actor authorized. | Attributable immutable confirmation; no automatic confirmation of unseen newer proposals. |
| Accept confirmed execution | Required confirmation/processing authorization matches the exact analysis snapshot; resource/configuration/policy prerequisites hold. | Accepted pinned snapshot/job/attempt under the transactional queue contract, or explicit preserved-input blockers. |
| Assess independently | Explicitly authorized preliminary individual-assessment scope and its own resource/processing eligibility. | Inspectable results labeled with exact unconfirmed/confirmed input status; not final report-level aggregation. |
| Request more evidence | Affected claim/check and missing evidence are explicit. | Actionable requested evidence category/metadata and relationship to prior result; no invented missing data. |
| Amend | Authorized changed content/scope with exact parent revision and reason. | New attributable evidence/classification/binding/transform revision; earlier results remain historical. |
| Confirm amended scope | Review exact amended values/evidence and required processing changes. | New confirmation with dependency reevaluation; no implicit inheritance of approval for changed content. |
| Aggregate/publish | Confirmed nonempty material scope, valid evidence/checks and current publication guards. | Honest coverage/conclusion/report status; unconfirmed inputs remain blockers. |

Preliminary discovery, AI classification and independent assessments do not imply permission to run the confirmed full analysis. Their own external processing and shared provider controls still apply. Confirmed execution and final aggregation remain distinct gates; neither can be bypassed by reusing an unconfirmed preliminary result.

## 5. Stale confirmation and concurrency

A confirmation request identifies the exact content it reviewed. If the proposal, evidence, parse, selection or required policy context has changed, reject the stale confirmation for the changed scope and return a safe conflict with the reviewable differences. Do not automatically apply the earlier click to a new value or redirect it to the newest revision.

Form and validate the complete candidate confirmation/snapshot through the canonical contract. Guard its acceptance against concurrent authorization and revision changes. The implementation must prevent two racing requests from silently mixing role from one revision, materiality from another and evidence from a third. Exact comparison/locking/transaction mechanisms remain OPEN.

Equivalent duplicate confirmations need an explicit scoped idempotency policy; conflicting content under one operation identity cannot overwrite an accepted confirmation. Validate authorization before exposing earlier acknowledgements. A retry of transport is not approval of a different proposal.

Persist audit facts sufficient to explain what the researcher saw/confirmed, what changed and which snapshot used the choice. UI presentation/audit metadata alone is not proof that the underlying scientific source was verified.

## 6. Change impact and result reuse

| Change | Dependency effect to specify and validate |
| --- | --- |
| Claim wording/normalized assertion | Determine whether scientific scope/requirements change; require a recorded revision, not an undocumented text replacement. |
| Role/materiality | Reevaluates aggregation/coverage scope and determining findings; does not edit an already published conclusion. Numerical result reuse still needs explicit unchanged-input proof. |
| Source/dataset/version refresh | Reevaluate affected provenance, content, data and temporal bindings. Same URL or rounded value cannot prove unchanged evidence. |
| Parser/locale/units | Reevaluate derived values, conversions and dependent calculations/bindings; preserve original token/artifact. |
| Selected sheets/ranges/filter | Reevaluate counts/denominators, observations, joins and dependent method applicability. Show excluded scope. |
| Transformation/join/weights | Reevaluate output lineage, comparability and every affected calculation/assumption. Researcher approval cannot cure an invalid join or unknown unit. |
| Provider/model/prompt/protocol | Preserve old pinned configuration; use an attributable new attempt/configuration when required. No silent substitution or reused independent-review claim. |
| External-processing provider/data/stage scope | Reevaluate authorization; no blanket reuse of consent for a different provider or newly included sensitive evidence. |
| Display-only presentation | Must not change source values, confirmed scope, backend comparisons or stored verdicts. Define any equivalence policy explicitly. |

This matrix identifies dependencies, not an approved cache/reuse algorithm. Exact equivalence predicates, invalidation and selective rerun policies remain OPEN. Until established, do not silently reuse earlier proof or confirmation for changed inputs. A cryptographic hash alone does not establish all source/policy/authorization equivalences.

Creating a new revision does not automatically delete/cancel historical attempts. Which attempt remains an active publication target and whether earlier running work is cancelled needs the approved lifecycle policy. No result may be published under the wrong revision or overwrite the new active scope. Authorized historical inspection remains separate from current active publication.

## 7. Researcher review journey and integration boundary

Within the existing frontend architecture, the proposed confirmation interaction must expose original and proposed claims, distinct role/materiality, proposed rationale, relevant bindings/locators, included/excluded worksheets/ranges, ambiguous parses/transforms and required processing disclosure. Researcher overrides and corrections must be possible without losing the original proposal.

Use explicit confirmation actions and preserve inputs on API/network errors. Do not show success before authoritative acceptance. Return stale-conflict/blocker information tied to specific fields/claims so the researcher can review changed content. Loading and pending states cannot silently complete confirmation.

Keyboard access, visible focus, error associations, screen-reader status, English/Arabic and RTL behavior apply to these interactions. This is an integration requirement, not a frontend redesign or implemented new route. Exact DTOs and UI placement remain D01/D09/E07 decisions.

A review control must not imply “agreeing with the AI” or verifying the truth of a claim. Show separately what was confirmed, what evidence remains unverified and why aggregation/execution is blocked. Confirmation of exclusions must not hide the fact that dependent scientific content remains unchecked.

## 8. Audit, privacy and deletion

The classification history preserves proposed values/rationale, confirmed values/overrides, actor/time, linked revisions and the reports/attempts that used them. Confirmation audit is attributable without copying unnecessary personal data, secret credentials or unrestricted evidence content into ordinary logs.

Access to history follows current authorized case permissions. Identity deletion/suspension and retained audit attribution follow approved lifecycle/retention rules; exact retained identity fields/durations remain OPEN. Immutability prevents silent rewrite, not authorized deletion. Restoring a backup must not resurrect deleted access or treat a revoked identity as freshly authorized.

## 9. Acceptance obligations — unexecuted specifications

| ID | Required future observable behavior |
| --- | --- |
| CF01 | AI-generated/proposed values never become researcher-approved solely because extraction was requested. |
| CF02 | Proposed and confirmed roles/materiality/rationale remain separate with actor/time and revision history. |
| CF03 | Roles do not automatically determine materiality; multiple Primary claims do not collapse into an arbitrary single primary. |
| CF04 | Zero/unconfirmed/ambiguous material scope blocks final aggregation without hiding independent assessments. |
| CF05 | A stale proposal/evidence/selection confirmation cannot silently apply to a newer revision. |
| CF06 | Concurrent role/materiality/binding updates cannot produce an unreviewed mixed snapshot. |
| CF07 | Researcher overrides preserve original proposals and do not directly edit an evidence-based verdict. |
| CF08 | Changed classifications/evidence produce new revisions while prior reports retain their exact confirmed basis. |
| CF09 | Source refresh or changed parsing/ranges/joins reevaluates affected dependencies; same URL/value is not automatic reuse proof. |
| CF10 | Changed provider/data/stage processing scope cannot silently inherit earlier authorization. |
| CF11 | Preliminary individual assessments are labeled and cannot substitute for final aggregation confirmation. |
| CF12 | Missing-evidence response creates an attributable amendment rather than retrying stale inputs. |
| CF13 | Cross-account/unauthorized confirmation and duplicate-acknowledgement lookup are rejected without leaking private state. |
| CF14 | Network/conflict errors preserve researcher input and do not display false confirmation success. |
| CF15 | Partially Supported remains unresolved; confirmation or scope edits cannot approve it as a final verdict. |
| CF16 | English/Arabic keyboard/readout behavior accurately exposes confirmation, blockers and changed revision scope. |

No CF case has run or passed. Reviewed request/response fixtures, exact conflict/revision/idempotency predicates, user journey acceptance and later separately authorized execution remain required.

## 10. Open contract items and next refinement

Still OPEN: exact proposal/confirmation/snapshot schemas; role/materiality conflict rules; confirmation identity/content and preconditions; allowed operations/transitions; active versus historical attempt handling; dependency-equivalence/reuse policy; processing reauthorization details; lifecycle retention; precise UI/API conflicts and reviewed case expectations.

This draft develops D01/D09 and evidence for E03/E05/E07 without closing them. R06 review-packet/phase/judge contracts are the next ordered refinement. **Status remains Recommended for owner approval; all 24 gates remain OPEN.** No statistical method/library, production implementation, deployment or capability enablement is selected or authorized.
