# EvidenceTwin V1 — Consolidated open decisions

Date: 2026-11-06. Author: Abdulrahman Ahmed. Working questions prepared from the approved concepts brief, current design draft, subsequent author decisions and the completed Goldfish review.

This is a batch review worksheet, as requested by the author. It replaces the one-question-at-a-time discussion format for this review. It does not replace or approve the design. All alternatives below are unranked brainstorming paths, not selected defaults. No application code, deployment configuration or scientific capability is changed by this document.

**Update 2026-11-06:** the author supplied [recommended responses to Q01–Q60](RECOMMENDED_DECISIONS.md), explicitly marked “Recommended for owner approval.” Every question now has a proposed policy answer; new choices are not yet adopted. That record separates the proposed policy direction from remaining procedure specifications, product comparisons and numeric/lifecycle approval gates. The original questions and alternatives below remain as traceable context, not a request to answer all 60 again.

**Incorporation authorized:** the owner approved using the package as the Technical Plan baseline while requiring **Recommended for owner approval** to remain its status. This authorizes design incorporation only. Individual recommendations do not become final implementation choices. Follow the [Decision, Enablement and Pilot gate register](TECHNICAL_PLAN_GATES.md); every gate remains OPEN. PostgreSQL is still a candidate, and unresolved mandatory scientific specifications/acceptance prevent capability enablement.

## How to answer

Reply with question IDs and your decisions, in any order. You can answer an entire group in prose, specify values, request a comparison, or leave an item open. For example: `Q13: A, but cached values must never satisfy formula-reproduction checks.` An unanswered item remains open. A decision can approve a policy without yet selecting its vendor or numeric limits.

Timing markers:

- **D:** resolve before the affected architecture or contract is finalized for implementation.
- **E:** resolve before enabling the affected scientific/data capability. Until then it remains explicitly unavailable.
- **P:** resolve before accepting hosted pilot users or work dependent on that policy.

Several items need a small policy table rather than a letter. Related decisions are deliberately grouped into one question where their values must agree. These are the currently identified open decisions, not a promise that later design review cannot uncover another gap.

## Already approved — do not reopen by default

- React/Flask web application, controlled cloud pilot and one framework-independent Python Core package executed by background workers.
- Shared relational application state plus private object storage; API/workers may initially share a host. Immutable version-aware evidence, stable IDs/hashes/ownership, coordinated recovery.
- External authentication through a replaceable adapter; backend token validation; issuer/subject mapping to internal user IDs; EvidenceTwin owns authorization and case ownership. Invitation-controlled registration.
- Database-backed persistent queue; atomic job/attempt/queue acceptance, claims, leases/heartbeats, safe recovery, bounded retries, cancellation and audit history. No broker required initially.
- Configurable initial limits: 2 executing analyses, 1 LLM request per analysis, 2 LLM requests globally. Shared enforcement and load/cost testing before increases.
- New public API contracts under `/api/v1/`, distinct from Core/prompt/evidence versions; bounded legacy migration through compatibility adapters.
- Verification measures completed scientific evaluation, not claim truth or AI agreement. Separate claim coverage, report verification and overall conclusion.
- Mixed conclusions may retain definite findings alongside uncertainty; an unresolved primary claim can still require Inconclusive. No agent-majority aggregation.
- Material-claim completion determines coverage. Mandatory report blockers force report Incomplete while preserving complete claim work. Failed and unperformed checks remain distinct.
- Researcher-confirmed Primary/Supporting/Contextual roles, materiality recorded separately, proposed/confirmed values and audit history retained. Unconfirmed classification blocks final aggregation; individual assessments can remain visible.
- Automatic eligible-XLSX-sheet discovery, separate sheet evidence units, disclosed exclusions and researcher-controlled scope. Combining sheets requires methodological justification and explicit confirmation.
- Historical evaluation is primary for historical claims; current evaluation is separate. Later revisions never silently rewrite earlier results.
- Five bounded V1 claim categories and CSV/XLSX/PNG/JPG/source-URL inputs. Image-only input cannot establish exact numerical/statistical verification. Source authenticity and claim correctness remain separate.
- MCP is optional/later. Benchmark scoring remains unavailable until a rubric is defined. Neither becomes an accidental release dependency through this worksheet.

## 1. Scientific procedures and decision rules

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q01 · D/E | Which exact deterministic numerical procedures are in the first supported matrix, and what input shapes/units does each accept? | Define explicit contracts for values, sums, means, percentages, percentage-point/relative changes, extrema and distributions within the agreed categories. Approve procedures individually or as a reviewed set. Broad method names are insufficient: an undefined denominator, weighting rule or aggregation scope must block the affected check. |
| Q02 · D/E | Which basic statistical procedures are allowed, with which prerequisites, assumptions and reference cases? | Specify the supported tests, p-value/CI/effect-size/correlation calculations and study-design checks. A narrowly reviewed allowlist is easier to validate; a broader set needs more reviewed examples. Do not infer suitability or invent sample sizes. Procedures without an approved specification stay unavailable. |
| Q03 · D/E | How are precision, rounding, tolerances and the word “approximately” established for each claim? | Researcher-confirmed claim precision, or a declared source/procedure rule with visible confirmation of ambiguity. Set decimal/rounding behavior and absolute versus relative tolerances. Unstated tolerances can change a Supported result to Contradicted; never choose them to force an expected answer. |
| Q04 · D/E | What is mandatory, optional or not applicable for each claim category, source type and review mode, and who approves policy changes? | Produce a versioned applicability matrix including report gates. Fixed reviewed rules give consistency; case-specific exceptions need an attributable approval policy and cannot quietly waive missing evidence. Define evidence for Not Applicable; an unavailable check cannot simply be relabeled optional. |
| Q05 · D/E | What operational materiality guidance and invalid-scope rules accompany researcher confirmation? | Define examples of consequential versus contextual findings, multiple primary claims, zero material claims and conflicting assignments. Choices include requesting correction or accepting explicitly limited independent assessments while blocking aggregation. Confirmation authority is already settled; this asks how invalid/ambiguous confirmed scope is handled. No empty-set “complete” result. |
| Q06 · D/E | How are claims bound to exact source passages, dataset columns/cells and metadata, and how are conflicting bindings resolved? | System-proposed bindings followed by confirmation, or approved deterministic binding rules with escalation for ambiguity. Define structured units/population/time/denominator fields and missing-evidence requests. A matching number alone is not enough; revisions must preserve the old binding rather than rewrite it. |

## 2. Source verification and historical identity

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q07 · D/E | Which source/document families have a supported retrieval and extraction pipeline in V1? | Specify original publisher HTML, official dataset downloads, repository records and any bounded research-PDF inspection. General URL submission is already supported conceptually, but arbitrary document verification is excluded. Narrow connectors limit coverage; generic extraction needs stronger matching/format tests. Unsupported content must stay explicit. |
| Q08 · D/E | For each supported source family, what concrete evidence satisfies every mandatory identity, integrity, content, provenance, notice and correspondence check? | Author a source-policy table naming official-record lookup methods, required metadata, matching evidence and unavailable-check behavior. Automated procedures versus documented human-reviewed evidence are possible support paths; neither a domain reputation nor a DOI match is sufficient alone. Do not reopen the already-approved mandatory check categories. |
| Q09 · E | How are correction/retraction notices discovered and their effects on a particular claim determined? | Publisher/repository records alone, or those plus approved independent notice records. More sources add matching/version conflicts. Define what counts as a completed notice check, how unknown notice status is shown and how corrections affect the relevant evidence. An authentic retracted source is not automatically inauthentic, nor is every claim automatically false. |
| Q10 · D/E | What proof establishes publication-time dataset and methodology identity, including archive evidence? | Define acceptable publisher release records, version identifiers, dated archives or attributable historical artifacts, and the review required for each. Broad archive acceptance improves coverage but raises identity/context risks. A later matching value, retrieval timestamp or Last-Modified header alone remains insufficient. Include the unresolved Ember historical binding. |
| Q11 · E/P | When and how is the “current” evidence snapshot refreshed, and which revision records are authoritative? | Researcher-triggered refresh versus an explicitly authorized scheduled refresh. Scheduling adds retrieval cost and repeated external processing. Either creates a linked new revision/result, preserves the previous current snapshot and records unknown revision reasons; no silent historical overwrite. |
| Q12 · D/P | What mechanism isolates source retrieval and parsing from private infrastructure and credentials? | Compare a constrained retrieval process with enforced egress against a separately isolated retrieval worker/network boundary. Both need destination/DNS/redirect checks and byte/time/decompression limits. A separate process without effective network isolation is insufficient; a shared worker with only URL string validation is also insufficient. Select concrete enforcement and tests. |

## 3. CSV/XLSX ingestion and scope

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q13 · D/E | How should formula-derived XLSX values be handled? | **A:** expose stored/cached results as labeled supplied values, preserving formulas and blocking checks needing unestablished correctness/freshness. **B:** exclude formula-derived values from numerical verification until traceable original values or a values-only export are supplied. A risks stale caches; B adds researcher work and an export still needs provenance. Neither executes macros, external links or arbitrary formulas. |
| Q14 · E | Which worksheet structures and visibility states are eligible for automatic inspection? | Inspect supported hidden sheets by default with disclosure, or inventory all sheets but require opt-in for hidden content. Define very-hidden/empty/malformed sheets, merged headers, multiple tables, named ranges and exclusion reasons. Visibility alone must not silently determine completeness; structured limits must be disclosed. |
| Q15 · D/E | What table schemas and header-resolution rules are supported, including legacy exploratory formats? | Define long/wide tables, multiple header rows, duplicate/blank names and typed schema confirmation. Compare requiring researcher correction with explicit annotated mappings. State whether existing JSON/WebP/PDF remain exploratory attachments. Guessing a header, flattening unrelated tables or silently dropping legacy inputs changes evidence meaning. |
| Q16 · E | What encoding, locale and numeric parsing rules apply? | Strict supported encodings/locales with explicit correction, or bounded detection followed by researcher confirmation. Specify decimal/thousands separators, dates, percentages and unit tokens. Automatic coercion is convenient but can change values; refusing all non-UTF-8 input reduces coverage. Preserve raw text and parsing decisions. |
| Q17 · E | How are missing/invalid values, duplicates, outliers and denominator-affecting exclusions handled? | Report without altering data, or allow explicit recorded transformations with researcher-confirmed scope and procedure prerequisites. Define missing-value tokens and counting rules. Unrecorded dropping/imputation can change calculations; identifying an outlier does not justify deleting it. |
| Q18 · D/E | How are approved transformations and dataset combinations represented and reproduced? | Define input/output evidence IDs, cell lineage, units, join keys/cardinality, filters and method rationale. Store a versioned transformation specification or a reviewed computation record with reconstructable inputs. Researcher confirmation for combining sheets is already required; it cannot substitute for a scientifically valid join or aggregation. |

## 4. Visualization and Council protocol

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q19 · D/E | How is an uploaded chart matched to its original source and numerical dataset? | Explicit researcher-confirmed chart/data bindings, or a validated extraction/matching pipeline with review of ambiguities. Define accepted chart formats, exact versus approximate readings and what happens when the original chart is inaccessible. Image pixels alone cannot establish exact statistical evidence. |
| Q20 · D/E | Which Neutral Twin chart families and rendering rules are allowed? | Author-reviewed rendering templates versus researcher-confirmed settings constrained by reviewed rules. Define baseline/scales, units, uncertainty, encoding and single-variable controlled changes. No universal “neutral” zero-baseline assumption; avoid changing data or hiding legitimate uncertainty. Record every assumption and transformation. |
| Q21 · D/E | What precisely does Blind Optics hide or reveal in each review condition? | Define the actual input packets, original/neutral pairing, claim/context visibility, ordering and prompt versions. Blinding can reduce framing exposure but remove context needed for interpretation. Full context can reintroduce shared framing. Existing owner prompts are not silently rewritten; approve protocol changes explicitly. |
| Q22 · D/P | How are provider/model assignments pinned across reviewers and phases? | One configured model for all isolated conversations, or operator-selected per-role models/providers. Heterogeneity adds cost/configuration and does not prove independence. Specify generation parameters, prompt/schema versions, vision support and unavailable pinned configurations; researchers still do not need their own credentials. |
| Q23 · D/E | Which review phases are mandatory report gates for Focused and Full Council modes, and what happens after a reviewer fails? | Preserve all four initial reviews plus cross-review/judge as mandatory for Full Council, or define an explicit applicability-aware protocol with accurately labeled reduced coverage. Reduced execution must not be presented as a full Council. Specify whether any cross-review may proceed with missing roles; do not silently relax the existing four-valid-review prerequisite. |
| Q24 · D/E | What structured evidence rules constrain the Evidence Judge and unresolved disagreement handling? | Deterministic eligibility/reference checks around an AI-proposed assessment, or an explicit escalation/review mechanism for conflicts the policy cannot resolve. Define supported verdict predicates, duplicate findings and invalid citations. Neither model confidence nor disagreement counts resolve a scientific issue; unresolved material conflicts remain visible. |

## 5. Accounts, permissions and identity lifecycle

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q25 · D/P | Which external identity provider/protocol should be compared and selected, under which deployment constraints? | Supply region, cost, recovery, invitation and portability requirements for a current product comparison. No provider is selected here. The adapter must yield backend-validated issuer/subject identity and remain separate from EvidenceTwin permissions; a provider feature list is not an authorization design. |
| Q26 · D/P | What session/credential transport, expiry, revocation and browser-origin topology will V1 use? | Backend-managed secure session cookies versus an explicitly designed bearer-token flow. Define sign-out/account-switch cache clearing, CSRF where applicable, token validation, renewal and revoked-session handling. Cookies need request-forgery controls; browser tokens need a defined exposure/storage boundary. Provider recovery does not revoke all application access automatically. |
| Q27 · D/P | Who issues pilot invitations, how are they redeemed, and when do they expire or become invalid? | Operator-issued named invitations versus approved organization/team invitation authority if sharing is enabled. Define one-use binding, duplicate identities, expiry, revocation and failed redemption. An authenticated external account without a valid pilot entitlement must not self-register merely by using a matching email. |
| Q28 · D/P | What are the exact researcher/operator permissions, including operator access to research content? | Separate configuration/operations privileges from content access, or define attributable limited support access with an explicit authorization mechanism. Specify who can read audits, export/delete evidence and manage provider settings. “Operator” must not silently mean unrestricted access to private studies. |
| Q29 · D/P | What are the account-linking, provider-migration, suspension and deletion state transitions? | Specify proof of control for links, stable internal ownership through provider changes, suspended-session handling and effects on queued/running jobs. Compare immediate stopping with a documented bounded completion policy where permitted. Email alone never links accounts; deletion cannot silently orphan evidence or leave active access. |
| Q30 · D/P | Does V1 permit any team/supervisor sharing, and if so, with which roles and revocation semantics? | Private per-user cases only versus explicitly scoped team memberships/shares. Sharing adds authorization paths, transfer rules and worker revocation behavior. Private-only reduces collaboration but is simpler to audit. Researchers, students and supervisors as target users do not themselves establish shared access. |

## 6. Private processing, retention and reproducibility

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q31 · D/P | What evidence may be sent to external AI providers, and what approval/disclosure is required? | Per-analysis confirmation of disclosed data categories versus a declared pilot processing policy with case-specific restrictions. Define handling when evidence cannot leave the service and when providers/configuration change. These are product decisions requiring real provider terms/configuration review, not invented privacy guarantees. |
| Q32 · D/P | Where are provider credentials stored, who can rotate them, and what happens to pinned queued/running attempts? | Deployment-managed secret storage versus a separately protected application secret store, selected after operational comparison. Define non-secret credential/configuration references and revoked-key behavior. Silent substitution of provider/model changes reproducibility; logging or returning keys is never acceptable. |
| Q33 · D/P | What retention periods apply to originals, source snapshots, derived data, attempts, report versions and diagnostics? | Retain while a case is active with specified deletion/expiry rules, or explicit class-specific retention windows. Provide actual durations and ownership of the policy. Source snapshot rights/restrictions may differ from user uploads; hashes alone do not preserve reproducibility. |
| Q34 · D/P | How does deletion propagate to derivatives, worker copies, exports under service control and backups? | Immediate active-store deletion plus documented backup expiry, or a defined pending-deletion/grace workflow. Specify retained audit/tombstone fields and protection against restore resurrecting deleted access. Immutability does not prohibit authorized deletion; do not promise deletion from researcher-downloaded copies. |
| Q35 · D/P | What may a researcher export, in which formats, with what evidence and permissions? | Report/JSON plus authorized artifacts, or a complete reproducibility bundle with permitted originals and manifests. Define source-content restrictions and failed export behavior. Browser printing already exists; do not assume server PDF generation or public sharing is implemented or required. |
| Q36 · D/E | What constitutes a sufficient reproducibility manifest, including software and stochastic AI output? | Define retained procedure/software versions, parameters, transformations, prompt content/version, model identifiers, input scope, checks, outputs and environment references. Choose reconstructable environment specifications versus retained execution images where justified. Inspection of historical AI output is not a promise to regenerate identical text. |

## 7. Queue mechanics, shared controls and recovery

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q37 · D/P | Which database-backed queue implementation and atomic claim/concurrency mechanism will be used? | Existing maintained database-queue integration versus a small explicit transactional repository, after database-engine comparison. Define fencing, attempt/step uniqueness and shared analysis/LLM permits. Libraries reduce custom work but must meet contracts; custom claims need more concurrency tests. Process-local locks are insufficient. |
| Q38 · D/P | What polling, lease, heartbeat, timeout and stalled-worker settings apply? | Specify configurable values and the relationship between them, including temporary DB/network failures. Short leases recover quickly but can overlap real work; long leases delay recovery. Lease expiry alone cannot prove a provider call ended. Test under clock/delay/failure scenarios. |
| Q39 · D/P | Which failures may retry automatically, with what bounds/backoff and terminal states? | Define a failure-class table for safe calculations, retrieval, database conflicts, provider rejection and schema failures. Automatic safe retries reduce intervention; repeated invalid input or permanent errors waste resources. Uncertain accepted LLM calls remain outside blind automatic replay. |
| Q40 · D/P | Who resolves uncertain paid-call outcomes, and when may a replacement request be authorized? | Operator reconciliation against available provider records versus an explicit researcher/operator-authorized new paid attempt after disclosure. Define usage reservations, evidence of settlement and duplicate-risk accounting. No option guarantees exactly-once external execution; mere lease expiration is not reconciliation. |
| Q41 · D/P | How are cancellation and late/uncertain calls reflected in job state and shared permit accounting? | Separate logical cancellation from known external settlement; specify when reservations can safely be released and how late outputs are retained/discarded. Early release improves queue movement but risks exceeding real provider concurrency; retaining forever can halt the pilot. The policy needs bounded operator-visible resolution, not an invented success signal. |
| Q42 · D/P | What are queue admission bounds and fairness rules? | FIFO with per-account pending/active caps versus account-fair dispatch with explicit ordering. Define overload response and queued expiry if any. A persistent queue is not unlimited storage; unfair submission bursts can starve other pilot users even with only two running analyses. |

## 8. Pilot workload, limits, cost and observability

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q43 · D/P | What workload should infrastructure and load tests represent beyond the approved concurrency caps? | Supply invited/active users, submissions per day, typical/worst evidence sizes, source counts and retained revisions. A small controlled envelope simplifies provisioning; larger assumptions need more capacity and cost evaluation. The two-analysis target alone does not size storage or polling load. |
| Q44 · E/P | What exact resource limits apply to uploads, parsing, retrieval, computation and rendering? | Set per-file/request/workbook/expanded-byte limits, sheet/row/column/cell bounds, image pixels, execution memory/CPU/time and artifact sizes. Define reject-versus-inspect-subset behavior with visible coverage. Current local limits are not approved hosted limits; compressed size alone does not bound parser memory. |
| Q45 · D/E | How much evidence/context can each LLM phase receive, and how is any subset selected and disclosed? | Bounded explicit previews plus structured deterministic results versus an approved evidence-selection procedure with citations. Define per-role tokens/images and cumulative cross-review/judge context. Never describe a 200-row preview as the whole scientific dataset or assume truncation preserves important evidence. |
| Q46 · D/P | What monetary budgets/reservations, alerts and hard stops apply per attempt, account and pilot? | Specify currency, periods, approval authority and behavior when estimates/usage are missing. Operator-set hard caps versus additionally scoped account quotas are possible. Pricing estimates are not actual billing; cancelled/failed/late/uncertain calls still consume or reserve resources. No amounts or provider prices are assumed. |
| Q47 · D/P | What request/token rate limits apply beyond the approved simultaneous-request caps? | Define shared provider/account/model rate buckets, cooldown and provider-throttle handling from actual capacity/configuration. A request concurrency limit cannot bound requests or tokens per minute. Unknown provider limits require conservative explicit configuration, not claims of capacity. |
| Q48 · D/P | Which diagnostics, alerts and intervention thresholds are required? | Specify queue age/depth, stage/provider latency, worker heartbeat/lease loss, memory, failure rates, usage/cost and configuration changes, with researcher/operator access boundaries. Define safe structured error codes/correlation and retained fields. Thresholds need workload assumptions or measurements; a healthy API is not proof of healthy workers. |

## 9. Products, public contracts and compatibility

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q49 · D/P | Which relational database engine and operating model should be selected? | Compare engines and managed versus self-operated hosting against multi-process atomic claiming, transactions, scoped/indexed queries, backup, cost and operating skills. Current local SQLite is not presumed suitable without validation. Product comparison needs current primary-source documentation; no engine recommendation or selection is made here. |
| Q50 · D/P | Which private object-store provider and evidence metadata/reference layout should be selected? | Compare managed or self-operated object storage; define object/version identifiers, hash algorithm, ownership records, schema/index layout and accepted-write/publication reconciliation. Version-aware storage does not replace application revisions. Missing-object and orphan-object handling must agree with backups and deletion. |
| Q51 · D/P | What cloud/region, hosting topology and network origins fit the pilot's budget and operating constraints? | API/workers on one host initially versus separately operated processes/hosts, with the same logical stores. Define TLS, private service access, egress and frontend/API origins. Separation adds operations; co-location shares resource/failure limits. No vendor, region or availability target is selected. |
| Q52 · D | What are the exact `/api/v1/` endpoint schemas and canonical-to-wire mappings? | Specify new case/revision/classification/attempt/report identities, source/check enums, independent completeness/conclusion/temporal fields, capabilities and public projections. Compare conservative DTOs tailored to current views with broader versioned evidence records. Neither directly exposes Python models, loses verdict distinctions nor silently adds fields old views cannot render. |
| Q53 · D/P | What stable error, pagination and authorization-context contracts accompany the new API? | Define machine-readable safe causes/retryability, requested-record identity checks, bounded dataset/audit/history queries, sort stability and permission failure behavior. Preserve existing semantics where valid versus explicit new versioned shapes where necessary. HTTP success cannot imply scientific success; a page size alone cannot bound full-record loading. |
| Q54 · D/P | What are the legacy API support window, retirement conditions and compatibility limits? | Date-bounded deprecation versus release/usage-based retirement with a hard deadline. List old/replacement endpoints and unsupported legacy scientific fields. Time-only removal can strand clients; indefinite compatibility is excluded. Define rollback and migration ownership; legacy adapters share application/Core logic. |

## 10. Migration, recovery and acceptance evidence

| ID / timing | Open question | Paths to examine, tradeoffs and failure conditions |
| --- | --- | --- |
| Q55 · D/P | How are existing local records assigned ownership and distinguished from educational cases? | Explicit owner/import manifest versus quarantine until attributed. Define old analysis/report/file IDs, sample identity and archived exploratory status. The first login must not automatically own all old records, and existing AI interpretations must not become verified findings on import. |
| Q56 · D/P | What are the staged database/file/API/worker cutover and rollback procedures? | Controlled write pause/drain versus an explicitly reconciled staged transition. Define who owns active jobs, restore material and handling of new work accepted after cutover. Never run old and new executors against the same attempts; reverting only the database cannot undo provider calls or recover deleted objects. |
| Q57 · D/P | What recovery objectives, backup schedules/retention and restore-test evidence are required? | Supply acceptable data-loss window and restoration time, coordinate database snapshots with exact object versions and verify ownership/hashes/deletion rules after restore. Compare snapshot/manifest strategies after products are selected. A backup file existing is not proof that an evidence-consistent restore works. |
| Q58 · D/E | Who approves scientific reference judgments and expected outcomes for the acceptance suite? | Owner-authored reviewed cases versus independent domain review of selected cases, with traceable calculations, source policies and disagreement expectations. Define evidence for the Ember historical/chart gaps and additional numerical/statistical/XLSX/visual cases. Mocked endpoints or one reproducible ratio cannot validate the whole scientific product. |
| Q59 · D/P | What tests and observations are mandatory before capability enablement and pilot release? | Define pass criteria for policy/procedure tests, contract checks, tenant isolation, worker races/recovery, browser English/Arabic flows, limits, representative load/cost and restore/rollback. All five categories remain the declared scope; specify the implemented support matrix and honest unavailable states. No invented accuracy target, latency guarantee or measured improvement. |
| Q60 · D/E | What is the minimum evaluation protocol, and how is unfinished benchmark functionality staged? | A reviewed acceptance corpus with per-case expectations versus an additional formally specified benchmark rubric when ready. Name rubric/reference owners, denominators, failure-case access and conditions/repetitions if benchmarks are enabled. Scientific acceptance is required; a full benchmark product and MCP are not automatically V1 prerequisites. Keep the NYAS student experiment distinct. |

## Suggested response format

You can answer groups together without repeating the questions:

```text
Scientific rules: Q01 …; Q02 …; Q03 …; Q04 …; Q05 …; Q06 …
Sources/history: Q07 … through Q12 …
Data ingestion: Q13 … through Q18 …
Charts/Council: Q19 … through Q24 …
Accounts/access: Q25 … through Q30 …
Privacy/lifecycle: Q31 … through Q36 …
Jobs/recovery: Q37 … through Q42 …
Limits/cost: Q43 … through Q48 …
Products/contracts: Q49 … through Q54 …
Migration/acceptance: Q55 … through Q60 …
```

When answers establish the policies, update the Technical Plan and compare unresolved products/mechanisms under those constraints. Obtain the final Technical Plan section approval before Alternatives Considered and Detailed Implementation. Later design finalization still needs its destination/approval gate; this worksheet does not grant production implementation authority.

## Traceability

| Current design/review area | Worksheet coverage |
| --- | --- |
| T01 Core package, already selected | Remaining packaging/reproducibility and deployment details: Q36, Q51, Q56. No new Core service decision. |
| T02 storage products/schema/recovery | Q33–Q36, Q49–Q50, Q55–Q57. |
| T03 identity/accounts | Q25–Q30, Q51–Q53. |
| T04 queue implementation/recovery | Q37–Q42, Q49, Q56. |
| T05 API compatibility | Q52–Q54. |
| T06 scientific support and resolved assessment semantics | Q01–Q12, Q19–Q24, Q58–Q60. Existing conclusion/completeness choices stay approved. |
| T07 ingestion/optics | Q13–Q21, Q44–Q45. T07a sheet discovery stays approved; Q13 is pending T07b. |
| T08 privacy/reproducibility/lifecycle | Q28–Q36, Q50, Q55–Q57. |
| T09 operating envelope | Q37–Q48, Q57, Q59. Approved concurrency caps stay fixed unless explicitly revised. |
| Goldfish M01–M14 and N01 | Support/policies Q01–Q24; canonical records Q06/Q18/Q36/Q52; ownership/access Q25–Q30/Q55; provider privacy/budgets Q31–Q32/Q40–Q47; ingestion/retrieval Q07–Q18/Q44–Q45; lifecycle Q33–Q36/Q57; migration Q54–Q57; diagnostics/workload Q43–Q49/Q53/Q59. Optional integrations remain outside the critical path. |

Sources: [current design](../../../design_draft.md), [approved concepts](../../../concepts_brief.md), [completed Goldfish review](2026-11-05-goldfish/goldfish_review_report.md), [Ember acceptance evidence](ember-2025-acceptance/acceptance_case.md). This consolidation is not a new independent Goldfish review, a product-comparison study or an executed scientific test.
