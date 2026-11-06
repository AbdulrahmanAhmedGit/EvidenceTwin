# EvidenceTwin V1 — Proposed Q01–Q60 policy package

Author: Abdulrahman Ahmed. Recorded: 2026-11-06.

**Decision status: Recommended for owner approval.**

This is a normalized record of the author's submitted recommendations, not an approval record. The decisions already approved in the [Technical Plan](../../../design_draft.md) remain approved. New choices and refinements below are pending explicit owner approval. Product candidates are not product selections; proposed policies are not complete executable scientific specifications. No implementation, installation, migration, credential use or external execution is authorized here.

**Incorporation authorization (2026-11-06):** the owner approved using this package as the recommended V1 policy direction in the Technical Plan, while explicitly requiring the status **Recommended for owner approval** to remain. This is approval to incorporate the baseline, not final approval of each recommendation. All Decision, Enablement and Pilot gates remain open until their own requirements and approvals are satisfied. PostgreSQL remains a candidate; no scientific capability may be enabled with unresolved mandatory specifications or acceptance requirements. Production implementation/deployment is not authorized by incorporation.

Related worksheet: [Q01–Q60](OPEN_DECISIONS.md). All 60 questions now have a proposed policy response. Several still require procedure definitions, product comparisons, numeric values or lifecycle rules before their affected implementation/capability/pilot gate can close.

**Later owner clarification:** Partially Supported remains a proposed/unresolved claim verdict until its meaning, eligibility and aggregation behavior receive explicit review. Do not read earlier completeness discussions as approval of that label. Partial coverage and source Partially Verified remain separate concepts. Formal specification approval and all 24 gates remain pending; R01–R07 refinement is authorized as design work only.

## 1. Scientific procedures and decision rules

| ID | Proposed decision and required behavior |
| --- | --- |
| Q01 | Bounded numerical allowlist: count, sum, arithmetic mean, median, minimum/maximum, ratios/percentages, percentage-point differences, relative changes, explicit grouped aggregations, weighted means only with supplied weights/interpretation, and basic distribution summaries. Each procedure specifies schema, units, denominator, filtering, missing-value handling, precision and outputs. Unknown denominators, implicit weights, ambiguous units or unsupported aggregation block the affected check. |
| Q02 | Narrow statistics allowlist: descriptive statistics, Pearson correlation, Spearman rank correlation, mean/proportion confidence intervals when sampling assumptions are established, Welch independent two-sample t-test where suitable, and chi-square independence tests meeting expected-count requirements. Validate prerequisite evidence, design, sample size, independence assumptions and missing-data treatment. Advanced regression, survival/time-series inference and complex causal inference remain excluded. Never choose a test to obtain a convenient p-value. |
| Q03 | Preserve source precision; distinguish percentage points from relative percentages; derive rounding intervals from declared decimal precision. Confirm ambiguous “approximately” tolerances with the researcher; record absolute and relative tolerances separately. Never tune a tolerance to obtain a pass. Unresolved tolerance means unresolved numerical assessment. |
| Q04 | Versioned Scientific Applicability Matrix per claim category/source family/review mode: mandatory, optional and justified Not Applicable checks, inputs, outputs and failures. A scientific policy owner approves changes; material changes require independent review. Unavailable mandatory checks cannot be downgraded to optional. |
| Q05 | Researcher-confirmed scope; multiple Primary claims permitted, role separate from materiality. Zero material claims block report aggregation. Ambiguous/conflicting classification requires correction; independent claim assessments may remain visible. No empty-set verification. |
| Q06 | System-proposed evidence bindings with researcher confirmation. Bind claims to source pages/sections/passages, dataset IDs/columns, CSV rows/columns, XLSX sheets/ranges, units, population, time and denominator. Confirm ambiguities and preserve evidence version/revision history. A matching value alone is not a binding proof. |

## 2. Sources and historical identity

| ID | Proposed decision and required behavior |
| --- | --- |
| Q07 | Supported source families: official publisher HTML, official CSV/XLSX downloads, official repository/versioned metadata records, and bounded text-based research PDF inspection. Scanned/OCR PDFs, arbitrary formats and unsupported site structures remain unavailable until validated. Unsupported sources may be recorded as references without a verified label. |
| Q08 | Source-family matrix covers identity, official record, canonical location, title/metadata, author/organization where applicable, publication date/version, integrity, exact bytes/hash, content correspondence, provenance/retrieval and applicable notices. Domain/DOI/HTTPS/title matches alone are insufficient. Every required check records a result or explicit unavailability. |
| Q09 | Publisher/repository notices are primary; independent registries aid discovery without automatically proving notice applicability. Record notice date/type, affected version/claims and individual impact. Authentic-but-retracted is distinct from inauthentic; unknown notice status is not “no notice.” No exhaustive external notice-monitoring promise. |
| Q10 | Accept attributable historical artifacts: official version IDs, versioned repository/DOI records, official dated archives with provenance and publisher-attributed historical files with content/metadata. Later numerical matches, retrieval time and Last-Modified alone cannot establish publication-time identity. Ember remains historically incomplete until the binding is established. |
| Q11 | Researcher-triggered current refresh only; defer scheduled refresh. Create a new snapshot/current assessment and explicit revision comparison; retain the previous snapshot, retrieval metadata and identified version. Never overwrite historical verdicts. |
| Q12 | Separately isolated retrieval worker/network boundary with enforced egress: HTTP(S) only, DNS/private-IP controls, redirect/connection-time destination validation, response/decompression limits, timeouts and content validation. No application credentials/internal-service access. Process separation alone is insufficient. |

## 3. CSV/XLSX ingestion

| ID | Proposed decision and required behavior |
| --- | --- |
| Q13 | B: exclude formula-derived values from numerical verification until correctness is established. Preserve formula text/cached results as labeled inspection metadata. Require traceable original values or a values-only export with sufficient provenance. Do not execute arbitrary formulas, macros, links or workbook code. A cached value proves neither formula correctness nor freshness. |
| Q14 | Inventory and inspect supported visible, hidden and very-hidden sheets within limits; disclose visibility, dimensions and structure. Allow researcher exclusions and explain unsupported/excluded content. Visibility never silently determines evidence completeness. |
| Q15 | Conservative table baseline: long/wide tables, single-row headers and separate tables with identifiable boundaries. Researcher-confirm mappings for multirow/merged/duplicate/blank headers, ambiguous boundaries and irregular legacy formats. Never guess or silently combine tables. JSON/WebP/PDF may remain exploratory artifacts unless specific ingestion capabilities are separately approved. |
| Q16 | Bounded encoding/locale detection, with confirmation of ambiguity. Preserve raw text and parse decisions; explicit validated date formats; distinguish percentage strings from ordinary decimals. Support only validated common encodings and never silently coerce ambiguous numbers/separators. |
| Q17 | Identify missing/invalid values, duplicates, possible outliers and denominator-affecting exclusions. No automatic deletion, imputation or deduplication. Transformations require confirmation, versioning and reproducibility. An outlier is not automatically erroneous. |
| Q18 | Versioned transformation specifications record input/output evidence IDs/versions, rows/columns, filters, exclusions, units/conversions, joins/cardinality, aggregation, implementation version and required approval. Combinations need methodological justification. Ambiguous keys, unjustified many-to-many joins and unknown units block the operation. |

## 4. Visualization and Council protocol

| ID | Proposed decision and required behavior |
| --- | --- |
| Q19 | Researcher-confirmed PNG/JPG chart/data bindings with system suggestions and confirmation of ambiguities. Preserve image hashes/source references. Separate exact data from approximate visual readings. Image-only input supports a visual audit, not exact numerical/statistical verification. An inaccessible original source can leave mandatory source verification incomplete even if visual review continues. |
| Q20 | Reviewed line/bar/scatter templates for standardized comparison renderings. Preserve data, units and relevant uncertainty; record axes/baselines and every controlled transformation. No universal zero-baseline rule and no claim of objectively perfect neutrality. Enable only supported families. |
| Q21 | Isolated role-specific packets with the same relevant claim and minimum necessary metadata; no other reviewer conclusions or unnecessary original interpretation. Independently prepare visual inputs. For paired reviews, randomize order and avoid original/neutral labels. Later cross-review may see both conditions/evidence. Owner prompts/protocol changes require explicit review and versioning. |
| Q22 | Operator-configured per-role provider/model assignments pinned per analysis. Record provider/model and available version, generation parameters, prompt/schema versions; validate vision support. No researcher keys required. Diversity is not independence proof; missing pinned configuration yields explicit unavailability, never silent substitution. |
| Q23 | Full Council requires four valid initial reviews, cross-review using all four and mandatory Evidence Judge. Missing/invalid required reviews block completion; retries follow safe policy. Focused Review declares a smaller role subset and never appears as completed Full Council. |
| Q24 | AI synthesis bounded by deterministic eligibility/reference validation: claim IDs, evidence/citation existence and correspondence, permitted verdicts, rationale fields, duplicates and unresolved disagreements. No invented evidence, confidence proof or majority voting. Unresolvable material disagreement remains visible and escalates for researcher review. |

## 5. Accounts and access

| ID | Proposed decision and required behavior |
| --- | --- |
| Q25 | OpenID Connect Authorization Code Flow with PKCE. Compare providers for region/availability, price, recovery, invitations, security, portability and operations. Keep product choice open until comparison approval; preserve EvidenceTwin internal IDs/authorization. |
| Q26 | Backend-managed browser sessions: Secure/HttpOnly cookies, appropriate SameSite, CSRF protection, server-side revocation, sign-out/account-switch state clearing and backend validation. Define expiry/renewal. No long-lived identity credentials in local storage. Review cross-site origin/cookie/CSRF requirements before implementation where applicable. |
| Q27 | Operator-issued named one-time invitations with unique IDs, securely stored tokens, expiry/revocation, issuing operator and redemption audit. Redeem only after external authentication. Issuer/subject define identity mapping; email matching alone never establishes ownership. |
| Q28 | Researchers access authorized cases/artifacts. Operators manage invitations, deployment/queue/provider configuration and diagnostics without automatic unrestricted research-content access. Exceptional support access is explicit, time-limited, attributable and audited. |
| Q29 | Internal lifecycle states: invited, active, suspended, deletion-requested, deleted. Linking proves both identities; provider migration preserves internal ownership. Suspension revokes sessions/blocks new work; queued-job disposition remains policy-controlled, running calls follow cancellation/settlement. Deletion follows approved lifecycle. No email-only linking. |
| Q30 | Private per-user cases in V1; no default team/supervisor sharing. Later collaboration needs explicit memberships, case permissions, revocation, transfer and audit design. Target audience does not imply access rights. |

## 6. Private processing and reproducibility

| ID | Proposed decision and required behavior |
| --- | --- |
| Q31 | Explicit per-analysis external-processing authorization before execution, disclosing data categories, providers, stages, actual terms/configuration and limitations. Minimize transmitted evidence. If a case cannot leave the service, affected AI capability stays unavailable or needs an explicitly approved alternative. No silent rerouting. |
| Q32 | Deployment-managed secrets outside source and ordinary DB records; execution-only access, non-secret references, audited rotation/configuration and no secret responses/logging. Pin configuration references. Revoked credentials pause/fail queued work explicitly; uncertain running calls reconcile before replacement. |
| Q33 | Class-specific retention: active case/evidence remains available until authorized deletion/account termination subject to source restrictions; derivatives/report revisions follow case lifecycle; diagnostics and backups have separate shorter/defined policies. Actual durations for each class require pre-pilot owner approval. Do not silently remove evidence needed by an active reproducibility record. |
| Q34 | Propagate deletion through service-controlled originals, snapshots, derivatives, reports/exports, worker temporaries, caches, active references and applicable access grants/credentials. Tombstones/deletion records prevent restore resurrecting access. Backups expire under approved schedule. No promises about external downloaded copies; immutability cannot defeat authorized deletion. |
| Q35 | Structured reproducibility export: JSON report, claims/verdicts, evidence manifest, dataset/source references, hashes/versions, transformations, relevant calculations and authorized uploaded artifacts. Browser print initially; no implied server PDF/public sharing. Redistribute restricted source content only when permitted. |
| Q36 | Versioned manifest retains originals/hashes, snapshots/provenance, parser/extraction/Core/dependency-environment references, claim/classification revisions, transformations, procedures/parameters, prompt/schema/provider/model/configuration, reviewer outputs/validated results, timestamps and available request IDs. Disclose nondeterminism. Historical AI inspection does not guarantee identical regeneration. |

## 7. Queue and recovery

| ID | Proposed decision and required behavior |
| --- | --- |
| Q37 | Prefer a small explicit transactional queue repository using native DB atomic claims/shared controls, unique jobs/attempts/steps, fencing, shared analysis/provider permits and auditable transitions. A maintained library is an alternative only if it demonstrates all requirements. Process-local locks are insufficient. Engine/claim SQL/schema remain unselected. |
| Q38 | Configurable tested polling, heartbeat, lease, worker/execution/network/DB timeouts with explicit relationships; use DB time where possible and stale-write fencing. Heartbeats occur before lease expiry under supported conditions. Lease expiry does not establish provider-call settlement. Exact values remain open pending tests. |
| Q39 | Only classified transient failures retry automatically: safe pre-acceptance network failures, throttling under provider guidance, safe temporary provider/server failures and DB serialization conflicts. No automatic retry for invalid input, unsupported format, permissions or permanent schema/configuration errors. Uncertain paid requests reconcile first. Bounded exponential backoff/terminal states required. |
| Q40 | Operator-led uncertain-call reconciliation, preserving available request IDs and provider usage/request records. Record whether execution/charge is established. If uncertainty remains, require attributable replacement authorization and duplicate-cost-risk accounting. Lease expiry is not proof of failure. |
| Q41 | Logical cancellation distinct from settlement: pending jobs cancel immediately, local work stops cooperatively, undispatched provider calls stop, in-flight calls remain tracked. Do not release permits merely on cancellation request. Record late results and exclude them from cancelled analyses unless explicitly reconciled/authorized. Bounded operator intervention handles uncertainty. |
| Q42 | FIFO within accounts and fair dispatch across accounts; configurable per-account/global pending caps, explicit overload responses and audited expiry/cancellation where applicable. Existing concurrency caps unchanged. Numeric queue limits await workload input. |

## 8. Workload, limits, costs and operations

| ID | Proposed decision and required behavior |
| --- | --- |
| Q43 | Controlled invitation-only workload. Tests cover approved 2-analysis/1-per-analysis/2-global concurrency, queued submissions, restarts/recovery, normal/burst load and small/large supported evidence. Invited/active users, daily volume and retained evidence still need owner values before sizing. |
| Q44 | Configure all boundary limits: upload/expanded bytes, sheets/rows/columns/cells, image dimensions/pixels, retrieval bytes, parse CPU/memory, worker duration and artifact sizes. Reject or explicitly disclose partial inspection according to policy; block claims dependent on excluded evidence. No silent truncation. Validate actual numeric limits on representative hardware before enabling capabilities. |
| Q45 | Bounded traceable reviewer packets: relevant claims/passages, metadata, deterministic results, targeted excerpts, visuals and limitations. Process large datasets deterministically; record selections/previews/omissions/transforms. No preview-as-complete claim. Configure contexts per provider/model/role. |
| Q46 | Operator hard budgets per analysis/global pilot, reservations before paid calls, alerts/stops and uncertainty reconciliation; optional account quotas. Amounts/currency require approval after current provider/hosting price comparison. No unbounded spending; charged/estimated/unknown usage must remain distinct. |
| Q47 | Shared simultaneous/request-window/token-window/provider-model/daily controls as supported, with throttling guidance, cooldowns/circuit breakers. Concurrency is not a rate limit. Exact rates depend on actual configuration/capacity. |
| Q48 | Role-separated observability: queue depth/age, heartbeats/lease loss, stage/provider latency, failures/retries/uncertain calls, CPU/memory/storage, tokens/cost and configuration events. Researchers see own progress/safe errors; operators see authorized diagnostics. No private evidence/secrets in ordinary logs. Thresholds require representative measurements. |

## 9. Products and API contracts

| ID | Proposed decision and required behavior |
| --- | --- |
| Q49 | PostgreSQL is the preferred database candidate, not the selected engine. Compare managed/self-operated options for atomic multi-worker claims, transactions, indexing/scoping, recovery, price and operations before final approval. Hosted suitability of existing local SQLite is not assumed. |
| Q50 | Private version-aware object storage through an S3-compatible interface is the preferred candidate approach; provider unselected. Include private containers, stable/versioned IDs, hashes, encryption at rest/in transit, app-owned manifests, controlled short-lived authorized downloads, orphan reconciliation and backup/deletion coordination. Native versioning does not replace application revisions. |
| Q51 | Simple single-region topology: separately hosted React, Flask API and independently executable worker process, shared logical DB/private objects, restricted internal access. API/workers may share a host. Select vendor/region after budget/residency/latency/availability/pricing/operations comparison. No vendor/region chosen. |
| Q52 | Explicit `/api/v1/` DTOs for internal account/profile, cases/revisions, claims/classifications, evidence/snapshots, jobs/attempts, checks, assessments, reports/exports. Keep coverage/report verification/conclusion/temporal/evidence fields independent. Do not directly expose internal Python/Pydantic domain objects. Deliberate Pydantic public DTO validation remains compatible with this boundary. |
| Q53 | Standard errors: stable code, safe message, retryability, request/correlation ID and applicable field details; no stack/evidence leaks. Cursor pagination/stable order for large histories/datasets/audits. Scope every access and avoid leaking cross-account record existence. HTTP success is not verification. New v1 cursor contracts need explicit adapters; existing page-based APIs are not silently reinterpreted. |
| Q54 | Time-bounded legacy adapters sharing application/Core logic, documented replacements/deprecation, usage monitoring and migration/rollback. Set/communicate exact retirement date before migration release. No indefinite compatibility or immediate unannounced removal. |

## 10. Migration and acceptance

| ID | Proposed decision and required behavior |
| --- | --- |
| Q55 | Explicit verified-owner import manifest; quarantine unknown ownership, separate samples, preserve IDs/hashes where possible and record legacy provenance. Never assign everything to first login. Imported AI interpretations remain unverified, not promoted by migration. |
| Q56 | Staged migration with controlled write pause: inventory, DB/files backup, dry run, reconcile ownership/counts/IDs/hashes, pause old writes, drain/resolve jobs, final import/validation, switch traffic and run acceptance/recovery checks. No dual worker ownership. External calls cannot be undone by DB rollback; after new writes use controlled forward reconciliation rather than blind snapshot replacement. |
| Q57 | Coordinated snapshots/PITR where supported, object-version protection/manifests, documented restores, ownership/hash/deletion-ledger reconciliation and regular restore tests. Owner approves numeric RPO/RTO before pilot, supported by actual infrastructure/test results. Backup existence is not recovery proof. |
| Q58 | Owner-approved versioned reference corpus covering numerical/descriptive/comparative/statistical/visual/missing/contradictory/historical/XLSX/source-failure cases, with independent domain review of material scientific judgments where possible. Ember arithmetic is retained but historical identity remains incomplete until established; image-only statistical claims remain limited. No claim of a completed scientific acceptance run. |
| Q59 | Capability-specific acceptance: scientific/source/data tests, contracts, cross-account permissions, queue concurrency/recovery, malformed/resource bounds, Arabic/English responsive browser flows, representative load/cost and backup/restore/rollback. Each capability declares its actual matrix. Unsupported capabilities stay unavailable; no unmeasured accuracy/latency/reliability guarantees. |
| Q60 | Reviewed versioned acceptance corpus first; benchmark product disabled until a separate rubric covers dimensions, scoring/weights/denominators, reference judgments, calibration/repeatability and enablement. Record owner/independent review and expected inputs/calculations/verdicts/source/uncertainty/failure states. Keep NYAS student evaluation distinct. MCP remains optional. |

## Remaining gates even if the policy direction is approved

| Gate | Still needed | Timing |
| --- | --- | --- |
| Executable scientific specifications | Exact procedure formulas/variants, schemas, applicability rules, assumptions, output contracts and reviewed test cases. In particular, a list of CI/test names does not specify CI construction, tie handling, expected-count thresholds or statistical adequacy. | Before implementing/enabling each scientific procedure. |
| Precision policy | Rounding mode, interval boundaries, numerical precision and researcher-confirmation record for ambiguous tolerances. | Before the affected numerical verdict. |
| Source matrices and temporal proof | Concrete connectors/identity/notice/correspondence tests, archive acceptance and method/version bindings. Ember publication-time identity and accessible original-chart inspection remain gaps. | Before the corresponding source/historical/visual capability can pass. |
| Chart/protocol details | Actual reviewed templates, controlled changes, role packets, randomized-condition manifests, prompt changes and applicability rules for unavailable chart conditions. | Before visual/Council protocol enablement. |
| Product comparisons | Identity provider, database engine/operating model, object-store provider, cloud/region, secret-management mechanism and concrete retrieval isolation. PostgreSQL/S3 compatibility are proposals/candidates, not final selections. | Before affected integration/deployment implementation. |
| Account lifecycle parameters | Session/invitation expiry/renewal, support-access authorization, specific suspension/queued-job behavior and identity-migration procedures. | Before hosted account use. |
| Processing authorization | Actual configured provider terms, permitted evidence categories, minimized packets and reauthorization behavior if pinned configuration or evidence changes. | Before external processing of an analysis. |
| Workload/resource values | Invited/active users, daily/retained volume, pending caps, bytes/sheets/rows/cells/pixels/context, CPU/memory/duration, leases/heartbeats/polling, retries/backoff and provider rate values. Values need explicit configuration and validation; existing local defaults are not hosted approvals. | Before sizing or accepting affected work; validate capability limits before enablement. |
| Spend/uncertainty controls | Currency/amounts, current price inputs, reservation bounds, operator intervention deadline/authority and settlement/permit-release rules. A local estimate alone cannot guarantee an external invoice ceiling; dispatch limits must state what is actually enforceable. | Before paid execution. |
| Retention/deletion/recovery values | Per-class retention including diagnostics/backups, deletion timing, restore reconciliation, RPO/RTO and restore-test schedule. Source-content retention/export permissions must be established. | Before hosted pilot. |
| Wire and migration details | Exact DTOs/enums/endpoints, cursor contracts, legacy mappings, deprecation date, import ownership manifest and tested cutover/forward-reconciliation procedures. | Before migration release. |
| Validation authority and evidence | Named scientific policy/reference reviewers, material-change review process, expected-case judgments, enablement criteria and actual scientific/operational/browser/load/recovery results. Independent-review availability must be explicit. | Before capability/pilot acceptance, according to its matrix. |

## Clarifications retained for technical drafting

- Proposed `report_verification_status` is independent of `claim_coverage_status` and `overall_conclusion`; source status and historical/current results remain distinct. No later recommendation silently reverses those approved semantics.
- “Checks passed” must distinguish a successfully performed check that finds a claim contradicted from an infrastructure/policy requirement failing. Contradictory evidence does not itself make a defensible completed claim assessment incomplete.
- Generic network/server failures do not prove that a provider did not accept a request. The retry table must be implemented with dispatch/settlement evidence, preserving no-blind-replay behavior.
- Researcher-confirmed classification before the confirmed execution scope remains required; preparatory extraction/classification and independently displayed claim assessments do not authorize final report aggregation.
- Researchers may confirm source/data bindings and transformations without thereby proving authenticity or scientific validity. Deterministic/policy checks remain independent.
- Cursor pagination is a proposed v1 contract change, not an authorization to break existing page-based clients. Compatibility adapters must not fabricate fields or scientific certainty.
- Paired visual randomization must be recorded in the execution manifest so actual assignments remain auditable. It does not remove the same-input and controlled-change requirements.
- Full Council stages may complete as recorded executions while the report remains scientifically incomplete due to unmet source/data/procedure gates. Four valid model responses alone are not verification.
- Encryption at rest, signed downloads, point-in-time recovery and revocation behavior need actual configured mechanisms and tests. Listing them in this proposal does not establish that they exist.

## Approval boundary and next step

The owner has authorized incorporating this package as the recommended policy direction while preserving **Recommended for owner approval**. It does not select unchosen vendors, approve unspecified numbers, finalize individual recommendations, complete scientific specifications, pass tests or authorize production implementation.

The Technical Plan now incorporates the baseline and links an [open gate register](TECHNICAL_PLAN_GATES.md). Resolve and approve each affected gate before implementation, enablement or pilot use, as applicable. Alternatives Considered and Detailed Implementation remain later design sections with their own approval gates. This record is not a new independent Goldfish review.
