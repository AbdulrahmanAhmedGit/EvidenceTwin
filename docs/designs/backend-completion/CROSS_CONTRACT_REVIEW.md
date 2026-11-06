# EvidenceTwin V1 — R01–R07 cross-contract consistency review

Date: 2026-11-06. **Design status: Recommended for owner approval.**

The owner approved R07 for cross-contract consistency review. This is the drafting agent's document self-review, **not an independent Goldfish review, scientific/domain certification, implementation audit or runtime test**. All **24 Decision, Enablement and Pilot gates remain OPEN**. No production implementation, deployment or capability enablement is authorized.

## 1. Review scope and evidence

Reviewed the linked R01–R07 contract meanings and refinements against the Technical Plan, incorporated recommendations, owner clarifications and gate register. Checks combined focused reads/searches for superseded direction/approval language with structural link/ID/family inventory checks. This is not proof that every possible specification ambiguity or security issue has been found.

| Design area | Current reference for refinement |
| --- | --- |
| Overall authority/boundaries | [Technical Plan](../../../design_draft.md), [recommendations](RECOMMENDED_DECISIONS.md), [24-gate register](TECHNICAL_PLAN_GATES.md). |
| R01 semantics and mutation/publication | [Typed axes](TYPED_CHECK_AXES_DRAFT.md), [lifecycle/publication](CHECK_LIFECYCLE_PUBLICATION_DRAFT.md). The [option comparison](CANONICAL_CHECK_CONTRACT_OPTIONS.md) is direction-decision history. |
| R02 arithmetic and precision | [Numerical contracts](NUMERICAL_CONTRACTS_DRAFT.md), [Decimal refinement](DECIMAL_ARITHMETIC_CONTRACT_DRAFT.md). Decimal is the recommended primary direction only. |
| R03 statistics | [Statistical contracts](STATISTICAL_CONTRACTS_DRAFT.md). No method/variant/library/level/threshold selected. |
| R04 source/temporal | [Source procedures](SOURCE_PROCEDURES_DRAFT.md). Connectors, intermediate predicates and historical proof remain open. |
| R05 researcher scope | [Confirmation/revisions](CONFIRMATION_REVISION_CONTRACTS_DRAFT.md). Confirmation does not establish scientific truth. |
| R06 Council | [Council contracts](COUNCIL_REVIEW_CONTRACTS_DRAFT.md). Legacy prompt/schema gaps are documented, not fixed in production. |
| R07 acceptance evidence | [Corpus contracts](ACCEPTANCE_CORPUS_CONTRACT_DRAFT.md). Specifications, approved oracles and actual execution remain distinct. |

This table is a navigation/traceability map. No “latest file wins” rule resolves policy contradictions. An actual disagreement with owner-approved intent requires explicit owner resolution; an editorial correction can only restate an existing decision.

## 2. Editorial findings corrected under existing owner decisions

Six passages in two documents were reconciled, grouped into four findings below. No new scientific or implementation policy was selected.

| Finding | Before / ambiguity | Editorial correction and authority |
| --- | --- | --- |
| ED01 — Stale R01 work-item direction | The parent specification still instructed selecting axes versus tagged union. | Restated the later owner-selected Separate Typed Axes direction; exact types/transitions/projections remain open. [Parent specification](SCIENTIFIC_SPECIFICATION_DRAFT.md), section 9. |
| ED02 — Stale arithmetic-direction question | The parent precision paragraph still listed Decimal versus binary as an undecided primary direction. | Restated Decimal as primary refinement direction, with explicit approved statistical conversion boundaries and open context/encoding policies. [Parent specification](SCIENTIFIC_SPECIFICATION_DRAFT.md), precision section. |
| ED03 — Overbroad “no selected option” statement | A parent work-item footer could imply the two direction decisions never happened. | Distinguished owner-selected recommended directions from unapproved exact specifications and still-open gates. [Parent specification](SCIENTIFIC_SPECIFICATION_DRAFT.md), section 9 footer. |
| ED04 — Historical verdict/report wording | Three Technical Plan decision-history passages could be read alone as approving Partially Supported or retaining the old combined completeness field/report-edge ambiguity. | Annotated historical wording with the later unresolved-verdict clarification and separate claim/report gating. Current approved semantics and historical chronology are retained. [Technical Plan](../../../design_draft.md), T06a–T06c history. |

The review did not alter raw Goldfish reports, original source snapshots, prompt files, scientific/backend/frontend source or runtime settings. Partially Supported remains proposed/unresolved; no retrospective approval is inferred from earlier text or legacy enums.

## 3. Cross-contract semantic checks

The following observations describe alignment of the current documents, not executed acceptance of the product.

| Invariant | Document-level result and remaining limit |
| --- | --- |
| Orthogonal check dimensions | R01 separates applicability, execution and requirement determination from observations/provenance. Whole-record and boundary validation are specified; exact types/transitions still need approval. |
| Scientific conflict versus technical failure | R01/R02/R03/R04 retain performed conflicting evidence separately from missing/unperformed/error states. Exact scientific predicates remain open. |
| Incomplete but inspectable work | Lifecycle/report contracts permit valid incomplete progress/report views without falsely Complete verification. Unconfirmed scope still cannot produce final aggregation. |
| Researcher authority | R05 retains proposed/confirmed scope and immutable history; role/materiality and confirmation/scientific proof remain distinct. Exact invalidation/reuse and confirmation DTOs remain open. |
| Numerical precision | R02/Decimal separates original values, arithmetic context, scientific tolerances and display; explicit binary statistical boundary only. Exact context/rounding/tolerance policies remain open. |
| Statistical eligibility | R03 distinguishes quoted, descriptive and inferential outputs and requires approved methods/prerequisites. S01–S05 and all statistical implementations remain unselected. |
| Source identity and time | R04 separates retrieval/authenticity/content and historical/current bindings; later availability or numerical matches cannot silently rewrite history. Exact source predicates/temporal proof still need approval. |
| Council evidence | R06 requires actual role/phase eligibility and evidence correspondence; no voting, output-count proof or legacy-verdict promotion. Prompt/protocol/schema migration remains open. |
| Claim versus report status | Claims can retain completed work under report blockers; coverage, report verification, conclusion, source and temporal layers remain separate. Partially Supported adds no approved branch. |
| Publication safety | R01/R05/R06 specify current scope/permission/fencing checks and no partial-field bypass. Atomic guard and revocation consistency mechanisms remain unselected. |
| Acceptance evidence | R07 inventories 150 overlapping specification rows across ten families without calling them independent tests or measured coverage. None has executed under these contracts. |
| Gate/approval boundary | Design-refinement approvals do not close any of the 24 gates or authorize production implementation. PostgreSQL remains a candidate, not a selected product. |

## 4. Remaining formal-specification decision bundle

These are the existing unresolved decisions consolidated for the next design pass, **not new gates or reopened approved directions**. They can be reviewed as a batch. No option/default is silently selected by this review; detailed alternatives already recorded in the linked contracts remain proposals.

| Item | Concrete artifact/decision required before formal approval of the affected scope | Existing gates |
| --- | --- | --- |
| FD01 — Canonical record and lifecycle | Exact independent-dimension types/enums, allowed-combination and legal-transition tables, required/forbidden payloads, finality/revision rules and complete-record validation contract. Separate Typed Axes direction is already settled for refinement. | D01, E05, E07. |
| FD02 — Guarded identity/publication | Exact predecessor/attempt/fencing/authorization/revocation predicates, idempotency identity and acknowledged-commit behavior; database/object/permission coordination and valid incomplete/preliminary projections. | D01–D05, E05–E07. |
| FD03 — Decimal and numerical procedures | Context precision/range/rounding/exception/order, tolerance composition/bases/ties, unit and empty/missing/weight/median/distribution conventions, wire encoding and approved statistical conversion records. Decimal direction is not reopened. | D01, D07, E01, E03. |
| FD04 — Statistical eligibility | Resolve S01–S05 and exact design/sample/assumption/degeneracy/missing-data/raw-versus-summary/tail/level/multiplicity/error rules, with reviewed reference cases before library selection. | D07, E01, E05. |
| FD05 — Sources and historical proof | Concrete supported connectors/official-record/content matching, source-status and notice/freshness predicates, archive/attribution criteria and exact original/current methodology/data binding. Ember historical/chart gaps remain explicit. | D03, D07, E02, E04. |
| FD06 — Confirmation and amendment | Exact proposal/confirmation/snapshot DTOs, trusted attribution/time, ambiguity/no-material-scope handling, stale/concurrent conflict protocol, change dependencies/reuse and processing reauthorization. | D01, D04, D06, D09, E03, E05, E07. |
| FD07 — Council protocol and verdict mapping | Exact role/condition packets, schema/phase eligibility including insufficient-input outputs, Focused subsets, template/blinding/disclosure/order, prompt changes and legacy-to-canonical treatment. Define proposed Partially Supported or leave it explicitly unavailable; do not invent a mapping. | D01, D07, E04–E06. |
| FD08 — Acceptance oracles and review | Exact permitted fixtures, expected predicates/outputs/context, named owner/domain review and unavailable-review handling, corpus revisions and future execution-evidence schema. A written case is not a reviewed oracle or executed result. | D07, E01–E07, P05, P07. |
| FD09 — Products and public integration | Approved current comparisons for engine/queue, identity provider/session/origins, object store/cloud/secret/retrieval isolation; physical schema, `/api/v1/` DTO/error/cursor/legacy mappings and retirement date. No product is selected by the candidate labels. | D01–D04, D08, E06, E07, P01, P08. |
| FD10 — Operating/lifecycle values and acceptance | Owner workload, validated resource/rate/queue/retry/lease values, budget/currency/settlement authority, retention/deletion/rights, RPO/RTO/restore/rollback and diagnostics/alert thresholds, with later actual hosted evidence. Approved 2/1/2 planning concurrency remains unchanged. | D05, D06, D08, P01–P08. |

FD01–FD10 are design task/decision IDs under the existing gate register, not ten additional gates. Closing a document review does not close these decisions, and resolving a Decision artifact does not substitute for its Enablement/Pilot evidence.

## 5. Dependencies to keep explicit

- An unresolved canonical schema blocks formal public projections, not the ability to draft source/procedure semantics.
- R02 precision and R03 method choices determine numerical oracles; do not approve expected values using an implicit arithmetic/library default.
- R04 source and temporal proofs constrain whether R02/R03 observations can establish a claim, even when arithmetic is reproducible.
- R05 confirmed snapshot gates final aggregation; preliminary independent assessments cannot grant that confirmation.
- R06 needs reviewed packet/prompt/schema and phase eligibility. Four parseable responses do not establish completed scientific obligations.
- R07 needs actual approved fixture/oracle/review records before any separately authorized scientific acceptance execution.
- Implementation, external processing, paid calls, hosted pilot and gate closure require their own authority/evidence. No design review result supplies it.

## 6. Review boundary and next step

The identified stale wording was corrected by restating existing owner decisions. Remaining method, status, schema, product and lifecycle questions were deliberately **not** resolved during this self-review. No formal scientific specification approval, independent domain review, prompt migration, test execution, production change or capability enablement occurred.

Proceed to exact formal-specification proposals using FD01–FD10, starting with canonical record/lifecycle and guarded publication dependencies. Keep all proposals **Recommended for owner approval**, preserve Partially Supported as unresolved, and keep all 24 gates OPEN until their own requirements and approvals are satisfied. This review does not certify the design ready for implementation.

**Subsequent design authorization:** the owner approved proceeding with FD01–FD02 refinement. The [canonical schema/publication proposal](CANONICAL_SCHEMA_PUBLICATION_PROPOSAL.md) now provides candidate fields/enums, a typed validity relation and operation predicates. These remain unselected final schema/commit choices; no gate is closed by drafting them.
