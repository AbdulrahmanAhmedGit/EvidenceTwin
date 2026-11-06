# Complete the EvidenceTwin verification backend

* **Author:** Abdulrahman Ahmed
* **Date:** 2026-11-05
* **Status:** Proposed synthesized concepts brief after six completed BRAINSTORM reviews on 2026-11-05. The user approved review readiness; this synthesis and the implementation design have not been approved. Root working brief is untouched by the synthesizer.

## Overview

Extend the existing Flask backend from exploratory AI review to a cloud-hosted, account-based verification service for a controlled research pilot. Preserve the React contracts and existing application behavior where possible. Verification must depend on traceable evidence, reproducible checks and explicit acceptance criteria, never model agreement.

The reference architecture is EvidenceTwin Council — Professional Architecture V3.png: controller, evidence availability, source verification, dataset validation, statistical checks, evidence contract, Blind Optics and Neutral Twin, specialized independent reviewers, collected findings, cross-review, Evidence Judge and final audit report.

## Current foundation

The existing implementation provides local persistent analyses and uploads, six configurable provider adapters, isolated initial review conversations, cross-review and AI adjudication, cancellation/retry/recovery, audit records and exploratory reports. Provider configuration can be managed in the workspace UI. These are application capabilities, not proof that scientific verification has occurred.

Source/statistical verification, Blind Optics/Neutral Twin generation, benchmark evaluation and MCP were deliberately left unavailable pending specifications. This brainstorm must establish those specifications and the deployment boundaries before implementation.

## Deployment and access established by the user

### Primary V1 experience

Provide a cloud-hosted browser application for a controlled pilot with researchers, university and high-school research teams, scientific-program students, educators and supervisors. Users create accounts, manage research cases, submit claims and references, upload evidence, start Council analyses, monitor execution, inspect findings/disagreements, and read/export reports. They must not need local software or personal model configuration.

Support research-document attachments without silently expanding the verified input scope: arbitrary unstructured documents remain outside verified V1 unless their extraction and evidence-matching pipeline has been specified and validated. Storage of a document does not mean its content was scientifically checked.

### System responsibilities

- **React frontend:** primary research interface, accessed through the browser.
- **Flask API:** authentication, authorization, research-case/evidence management, documented API contracts and communication with the Scientific Core.
- **Independent Python Scientific Core:** specialized review orchestration and deterministic verification tools. It must not depend on Flask request/session objects or duplicate scientific behavior for different clients.
- **Persistent database:** accounts, case ownership, evidence metadata, execution state, verification records and reports.
- **Private file storage:** datasets, images, documents and permitted source snapshots, with ownership-aware access.
- **Asynchronous workers:** long-running analyses that survive web-request lifetimes and expose actual execution states.

The user has established these architectural responsibilities, not selected a cloud vendor, database product, storage provider, queue implementation or authentication vendor. Evaluate those choices in review/design rather than treating them as already approved.

### Access and privacy requirements

- Secure authentication and authorization; users cannot access another user's cases, files, reports, job state or execution history without explicit permission.
- HTTPS and server-side provider credential management.
- Access controls covering uploads, generated outputs, downloads and background execution, not just page navigation.
- Explicit retention and deletion policies consistent with reproducibility and audit requirements.
- Traceable execution history without logging secrets or leaking private research materials.
- Controlled pilot onboarding rather than an unrestricted public launch.

The current shared provider-configuration page cannot remain available to ordinary hosted researchers as a global setting. The design must specify operator-only provider configuration, credential storage and analysis limits. Whether the pilot needs team sharing, supervisor access or institutions as separate account boundaries remains unresolved; do not assume those permissions merely from the audience list.

### API and future clients

Document the Flask HTTP API from the beginning. Use one Scientific Core for the web application and future research clients. MCP is experimental or limited future work, not a requirement for V1 release. A dedicated external developer API, assistant Skills, workflow integrations and institutional deployments can follow the stable browser pilot; do not build separate verification engines for them.

### Migration implications

The current local SQLite/JSON records, private local uploads, single-process thread worker and optional authentication hook are a foundation, not the requested hosted multi-user deployment. The implementation design must define ownership migration for existing records, account enforcement, durable worker execution, file access and rollback. Preserve current local data and API behavior where possible, and explicitly document necessary contract changes.

## Anchored working hypothesis for review

EvidenceTwin V1 will be a controlled, cloud-hosted research pilot with account-isolated cases and a browser-first React interface backed by a documented Flask API. One independent Python Scientific Core will verify the specified quantitative claim categories using traceable source records, validated CSV/XLSX data, applicable deterministic checks and documented chart inspection, with isolated AI reviews assisting assessment rather than establishing truth. Reports will separate source status, check coverage and claim outcome, distinguish contradiction from missing evidence, preserve reproducibility, and leave unsupported methods and MCP outside verified V1 capabilities.

The next Goldfish review should challenge whether this scope can be delivered reliably, which source policies and statistical procedures are sufficiently specified, whether privacy and execution boundaries are complete, how migration can preserve existing work, and what cost/quota controls a hosted pilot needs. These open design choices must not be silently filled in as user decisions.

## User-defined verification requirements

1. Identify each original claim, preserving its scope, definitions, units, timeframe and measurable assumptions.
2. Retrieve original sources and examine their authenticity, publication dates and methodology. Check whether supplied visualizations represent the original data accurately. Report what was actually checked and what could not be established.
3. Link every important finding to a specific accessible source, dataset or evidence reference. Explicitly report missing or unverifiable evidence.
4. When raw data is available, reproduce relevant calculations deterministically. Examine numerical consistency, statistical assumptions, uncertainty and potential bias. LLM output alone is not a reproduced calculation.
5. Check comparability of definitions, units, populations, denominators, methodology and time periods before making numerical or scientific comparisons.
6. Inspect specialized reviewer contributions for duplication and disagreement. Explain resolutions and the effect of unresolved conflicts. Agent agreement must not be treated as scientific proof.
7. Preserve original inputs, source references, data versions, model/prompt versions, calculations, validation results and audit history so another researcher can reproduce the analysis.

## Required report outputs

- A clear claim assessment that distinguishes Contradicted from Insufficient Evidence. Report verification coverage separately. The full status taxonomy and its mapping to existing API verdicts still need a design decision; these two outcomes are not the only possible outcomes for all claims.
- Claim-by-claim assessments of what is supported, contradicted or uncertain.
- Traceable evidence references for every major finding.
- Source provenance and documented verification results.
- Reproducible calculations and outputs where applicable.
- Methodological issues, potential biases, uncertainty and limitations.
- Reviewer disagreements and how they were handled.
- Specific additional evidence needed for stronger conclusions.
- A clear distinction between what evidence demonstrates, what it suggests and what cannot currently be established.

## V1 scientific scope established by the user

Prioritize reliability over coverage. Support bounded, structured, quantitative claims whose evidence and calculations can be traced and reproduced. The following categories are requirements, not a claim that their implementations already exist.

### Claim categories

1. **Numerical and descriptive:** reported values, totals, averages, percentages, changes between measurements, relative changes versus percentage-point changes, minimums, maximums and distributions.
2. **Comparative:** comparisons between groups, periods, populations or datasets. Check whether units, denominators, definitions and methods make the comparison meaningful before computing or interpreting a difference.
3. **Visualization-based:** correspondence between a chart and its supplied data; axes, scales, baselines, visual encoding, labels, units and supplied uncertainty; presentation choices that exaggerate or minimize differences.
4. **Basic statistical:** reported significance, p-values, confidence intervals, effect sizes, correlations and test appropriateness for the study design. Run a check only when its required raw data or statistical inputs, methodology and assumptions are supplied. The exact initial procedure allowlist and its acceptance tests still require specification.
5. **Methodological and interpretative:** flag unsupported causal conclusions, potential confounding, sampling limitations and unjustified generalizations. These reviews do not establish complex causal effects; distinguish documented limitations from hypothetical possibilities.

### Input formats

- CSV is the primary numerical dataset format.
- XLSX supports tabular workbooks with multiple sheets. Sheet selection, formula handling, cross-sheet relationships and preservation of workbook provenance need explicit design rules.
- PNG/JPG provide scientific charts, graphs and visualizations.
- Source URLs identify original research publications, institutional reports and publicly accessible datasets.
- Prefer charts accompanied by their underlying numerical data.
- An image alone permits a limited visual audit, never exact numerical or statistical verification. Do not recover guessed data points and silently treat them as original observations.

The existing application also accepts some exploratory input formats. Adding XLSX and deciding how legacy exploratory formats remain supported must be handled explicitly rather than silently breaking existing clients.

### Metadata required as applicable to each check

- Variable definitions and units.
- Population and sample size.
- Relevant time period.
- Data collection methodology.
- Source and publication date.
- Denominators and aggregation methods.
- Statistical assumptions relevant to the requested procedure.

Request missing metadata or extract it with traceable evidence references. Extraction is not verification. Do not invent missing values or silently accept model-generated assumptions as established facts. Essential missing inputs yield an insufficiency assessment for the affected check or claim.

### Explicit exclusions

- Complex, domain-specific causal inference.
- Claims requiring specialized clinical or experimental validation.
- Predictions and future outcomes.
- Complex meta-analyses.
- Claims without accessible, traceable evidence as verified conclusions. Such submissions may still receive a clearly limited visual/exploratory audit or an insufficiency report where supported.
- Arbitrary unstructured scientific documents without a reliable extraction and verification pipeline.

### Minimum end-to-end acceptance

For an in-scope claim, define the exact assertion; identify and verify its original sources under an explicit source policy; validate dataset and metadata; reproduce applicable numerical calculations; examine associated visualizations where supplied; run isolated specialized AI reviews; identify contradictions, missing information and unresolved disagreements; and produce a traceable report with references, calculations, limitations and a defensible claim assessment.

Record applicability and completion per check. Do not interpret an unavailable or inapplicable visualization, statistical procedure or source check as a completed verification. Define claim-specific required checks before implementation; not every numerical claim inherently requires a statistical test.

## Source verification policy established by the user

Source verification establishes documented identity, integrity, content correspondence and provenance under a defined policy. It does not establish that the source's scientific conclusions are correct. An authentic publication can contain errors or methodological weaknesses, and may not support a claim made using its data.

### Required source checks

1. **Identity and authenticity:** establish the claimed publisher, institution, research organization or repository; verify canonical location and relevant DOI/publication/repository identifiers; confirm an official record where applicable; distinguish original publications and datasets from summaries, mirrors and reposts. Accessibility, HTTPS and familiar domains alone are insufficient.
2. **Document integrity and version:** match title, authors, publication date and identifier; record the analyzed version/revision; check corrections, retractions and updates; retain a cryptographic hash where possible, retrieval timestamp and original URL. A hash identifies retrieved bytes; it does not alone establish authenticity.
3. **Actual content and metadata:** retrieve and inspect the relevant source content; locate the referenced claims, figures, tables or datasets; preserve the context of excerpts and extracted values; check applicable authorship, dates, units, population, timeframe and methodology. Flag unreadable, missing, incomplete or inaccessible content.
4. **Dataset provenance:** identify the original provider, dataset identifier/version, documentation, collection methods, variable definitions, units and transformations. Trace important values to original records where possible. Distinguish observations from processed, aggregated or derived data.
5. **Publication context and notices:** record peer-review/publication/preprint/institutional-report status; examine publisher identity and context; record methodological and provenance limitations and known correction/retraction notices. Reputation and peer review do not establish scientific correctness.
6. **Source-to-submission correspondence:** check whether uploaded charts, reported values and excerpts correspond to the identified source. Detect changed units, labels, periods, denominators, incomplete excerpts and undocumented transformations. Flag unexplained discrepancies for review.

### Source-level statuses

- **Verified:** all mandatory identity, authenticity, integrity and content checks pass, with sufficiently traceable provenance under an explicitly defined policy.
- **Partially Verified:** identity is established but important verification checks remain incomplete.
- **Unverified:** available information cannot establish authenticity or provenance.
- **Inaccessible:** the source cannot currently be retrieved or inspected. This does not by itself establish that it is fake or unreliable.

Record optional checks and unavailable information explicitly. A source may be Verified only when every mandatory check for its applicable source policy has passed. The exact mandatory/applicable check matrix by source type remains a design specification to produce; do not silently treat an unavailable required check as passed. A trustworthy record of a retraction or a reliable-content discrepancy also needs explicit decision semantics rather than an invented source-status mapping.

### Per-source verification record

- Source ID, original URL and canonical URL.
- Publisher, source type, publication date and exact version where available.
- Retrieval timestamp and content integrity information, including file hash when available.
- Identity/authenticity results with their supporting records.
- References to relevant source content and submitted evidence.
- Dataset provenance, identifiers and transformations where applicable.
- Correction/retraction status, including when the notice check could not be completed.
- Limitations and a check-level record of passed, failed and unperformed checks.

Preserve enough evidence for another researcher to inspect why a check received its result. Model statements about a source are not substitutes for retrieved records or actual content matching.

### Separation from claim adjudication

The source record answers where evidence came from and which provenance checks completed. Claim assessment answers what that evidence supports, contradicts or leaves unresolved. A Verified source must never automatically yield a supported claim; inaccessible or unverified sources must never automatically yield a contradicted claim.

## Clarified claim assessment requirements

### Contradicted

Use this outcome when relevant evidence is available and sufficiently reliable, the checks needed for the disputed part of the claim have completed, and reproduced calculations or verified sources directly conflict with that part of the claim. Cite the conflicting evidence and identify exactly which assertion it contradicts. Do not generalize a contradiction of one assertion to unrelated assertions.

### Insufficient Evidence

Use this outcome when essential data, original sources, methodological details, sample sizes, test results or other required evidence are missing, inaccessible or inadequate to evaluate the claim. Explain the missing input and what additional evidence would permit the check. Missing evidence must never be interpreted as proof that the claim is false.

### Required fields for every claim

- Claim assessment, with Contradicted and Insufficient Evidence explicitly distinct.
- Verification coverage: checks completed and checks that could not be performed.
- Supporting evidence, if any.
- Contradicting evidence and the specific assertion it conflicts with.
- Missing evidence.
- A concise, evidence-linked explanation of the verdict, not private model reasoning.
- Next verification steps or evidence requests.

### User-provided acceptance examples

These are hypothetical requirements examples, not measured research results or production fixtures:

- A claim says an increase is 20%; the original dataset is available and a reproduced calculation gives 5%. The numerical assertion is Contradicted by the calculation and its input references.
- A claim says a treatment caused a statistically significant improvement, but the dataset, sample size and test results are absent. The relevant assessment is Insufficient Evidence, with those missing inputs identified. The missing inputs do not establish that the treatment claim is false.

## Analysis after Goldfish brainstorming

Six fresh-context reviewers completed their required public-source and installed-standard readings. The deduplicated report records 0 concept-level Blockers, 14 Major design requirements and 1 Nit. This does not establish implementation or pilot readiness. See [review report](goldfish_review_report.md) and its six raw reports/read receipts. Parent-turn isolation was requested; host-instruction exclusion remains unverified. Four available live-agent slots included the primary and synthesizer, so reviews ran in three independent batches of two.

The established requirements above are preserved. The following remain open design questions, not approved decisions:

- The user has established distinct Contradicted and Insufficient Evidence outcomes and separate verification coverage. The complete taxonomy, mixed-claim aggregation and mapping to existing API verdicts remain unresolved. A verified computation and authenticated source provenance must also remain distinguishable.
- The user has defined the source-verification criteria and four source statuses. Implementation still needs explicit source-type policies, supported official-record lookups, content-matching methods and limits. Retrievability or a DOI match alone must not establish authenticity or methodological validity.
- The initial claim categories and CSV/XLSX/PNG/JPG/source-URL inputs are established. Exact statistical procedures, applicability rules and expected numerical outputs still need specification. Missing inputs must prevent the relevant inference rather than trigger guessed values or assumed methods.
- Comparability decisions need evidence about definitions, units, study populations, denominators, methods and dates; shared units alone are insufficient.
- Neutral visualization requires documented transformations and assumptions. A neutral rendering is not evidence of scientific correctness.
- Reproducibility needs a defined retention, versioning and export policy, including access to sources that later change or disappear.
- Cloud-hosted, account-based pilot operation and API-first Scientific Core separation are established. Authentication implementation, account/team boundaries, retention/deletion rules, workload limits and benchmark ground truth remain design decisions. MCP is not a V1 release requirement.

## Goals vs. Non-Goals

### In-scope goals established by the user

- Complete the verification workflow and report outputs described above.
- Ground conclusions in traceable evidence and reproducible checks.
- Expose missing evidence and unresolved uncertainty honestly.
- Preserve the existing Flask/React architecture and relevant API compatibility unless a necessary change is documented.

### Remaining scope decisions

- Implementable source-policy matrices and provider/document support within the source criteria above; methods for establishing official records, content correspondence and notice status.
- Exact supported statistical procedures and deterministic test specifications within the established V1 categories.
- XLSX sheet/formula handling and compatibility with existing exploratory input formats.
- Blind Optics/Neutral Twin acceptance criteria.
- Benchmark evaluation rubric and reference judgments.
- Optional MCP scope and later external-client workflows; neither blocks the first browser-based pilot.
- Authentication and account/team permissions within the established hosted pilot.
- Cloud infrastructure choices, durable execution/recovery, migration and rollback.
- Pilot usage expectations, provider budgets, quotas and per-user job limits.
- Retention/deletion/export policy, including handling of private source snapshots and reproducibility records.
- API compatibility for source statuses: the current frontend represents unavailable sources with an existing enum. Define how the requested Inaccessible status is exposed without silently breaking current clients.

### Non-goals

- Broad verification of arbitrary scientific statements beyond the V1 scope above.
- Treating AI consensus as truth.
- Fabricating sources, raw data, uncertainty intervals, significance tests or evaluation metrics.
- Claiming that transport/schema checks establish scientific validity.

## Alternatives Weighed

- Rejected by the user: treating missing evidence as evidence that a claim is false. Missing required evidence must yield an explicit insufficiency assessment.
- Rejected by the user: using the same outcome for a traceably contradicted claim and a claim that cannot be evaluated.
- Rejected by the user: requiring researchers to install local software or configure AI models to use the primary hosted application.
- The cloud/API/Core responsibilities and controlled-pilot direction are established. Concrete infrastructure choices, full status taxonomy and implementation design have not yet been approved.

## Key Decisions & Staging for Next Steps

1. Preserve the clarified contradiction/insufficiency distinction and separate check coverage. Define the remaining status semantics and measurable acceptance criteria.
2. Use the established V1 claim/input scope, source criteria and hosted-pilot boundaries to anchor review; preserve unresolved implementation choices explicitly.
3. Review readiness was explicitly confirmed and all six independent BRAINSTORM reviews completed. Review output is static source analysis; no provider calls, scientific tests or hosted validation were performed.
4. Refine the proposed requirements below and finalize the brief before an implementation design. Approval to review is not approval of unspecified scientific behavior or implementation.

## Proposed requirements synthesized from the six lenses

These proposals strengthen the existing working hypothesis. They are not new user approvals, implemented capabilities or an exhaustive implementation specification. The report provides concrete current-source references and consequences for each requirement.

### Scientific support and Core boundary

Specify a bounded support matrix joining claim category, input shape, procedure and source type. For each supported combination, define prerequisites, applicable/mandatory checks, exact outputs, failure and insufficiency behavior, method/policy version and reference cases. Keep the user's five claim categories visible while staging their supported combinations. Clearly distinguish source-content support from arbitrary-document ingestion; retain unsupported inputs only with explicit exploratory limits. Define bounded ingestion, source-policy, deterministic-procedure and visualization interfaces rather than growing one monolithic workflow.

Use one independent Python Core with versioned input/result models for assertions, evidence versions, check definitions/executions, findings and assessment decisions. The Core should not depend on Flask, Werkzeug errors, request/session state, browser URLs or presentation DTOs. A Python package called by workers is a candidate starting point; separate network deployment requires an operational reason. Flask remains responsible for authenticated HTTP operations and adapters. Reports and all inspection panels consume the same persisted scientific results; they must not independently recompute verdicts.

A typed check record should identify its subject/assertion, policy/procedure version, prerequisites, applicability, execution outcome, scientific result, evidence/artifact references and reason for failure or omission. Distinguish technical execution from scientific outcome. A completed job or fetched page is not a passed check; a source-status result is not claim support. Derive coverage and assessment under explicit rules, including mixed claims and unresolved disagreements. Define the remaining taxonomy and compatibility strategy before enabling new scientific statuses.

### Researcher journey and resource identities

Distinguish account-owned research cases from educational catalog examples, immutable evidence revisions, analysis configurations, execution attempts and report versions. Define stable identifiers, links and lifecycle relationships. Current `/cases` and creation `caseId` have sample-catalog semantics; a new private-case model must preserve or explicitly version that contract. Illustrative values must never be silently attached to actual research.

Show each normalized assertion with its units, population, timeframe, denominator and exact evidence bindings: source passage, dataset version, sheet, range, columns and rows as applicable. Identify user-supplied versus extracted values and unresolved or conflicting metadata. Essential unresolved associations yield insufficiency for the affected check rather than invented mappings.

Give a missing-evidence request an identified claim/check, reason and acceptable response format. Define how supplied corrections create an attributable evidence revision and new assessment. Same-input retry, resumption and amended-evidence submission are distinct operations. Previous evidence, results and cited report versions remain attributable; current revisions must not rewrite historical conclusions.

Present execution state, source provenance, check coverage, claim assessment and AI interpretation consistently. Show failed, unperformed and inapplicable checks explicitly, with actionable next steps. Errors should distinguish researcher input correction from unsupported methods, access restrictions, budget exhaustion, operator/provider problems and invalid AI output. Researchers should not be instructed to fix operator credentials.

### Hosted ownership, provider authority and privacy

Require authenticated principals and owner/case-scoped repository operations across direct reads, lists/totals, activity, comparison, reports, audit, artifacts/downloads and workers. Enforce authorization on the server, including derived resources; opaque IDs and UI permissions do not provide isolation. Decide team/supervisor/institution sharing explicitly. Migrate legacy ownership through a manifest or quarantine; unassigned records cannot become visible through registration or first login.

Restrict provider settings read/save/test to authorized operators on both API and UI. Define hosted credential storage, rotation, worker access and audit of non-secret configuration changes. Pin accepted jobs to immutable non-secret configuration references and specify behavior when credentials become unavailable. Never copy keys into execution manifests, telemetry or exports.

Explain at onboarding/submission which evidence categories are transmitted to the selected provider and the relevant handling/retention boundaries. Retain the applicable processing configuration in the audit record. Define the supported path when private evidence cannot be sent. Account isolation and private storage do not themselves describe external processing. The user has not selected a particular consent model, provider or institutional policy.

### Bounded ingestion and source retrieval

Retain original bytes and version every parsed representation and transformation. Define numeric/missing-value parsing, XLSX sheet/range selection, formula versus cached-value handling, cross-sheet dependencies, macros/external relationships and cell provenance. Preserve explicit legacy exploratory format behavior. Bound expanded workbook bytes, cells/sheets, CPU, memory and runtime as well as uploaded bytes.

Show limits and processing scope before launch. Every calculation and reviewer contribution records the exact inputs, selected range/rows, exclusions and transformations it used. Current AI context previews must not silently become deterministic calculation inputs; full-data computation and bounded review context are distinct. An image-only audit remains explicitly limited.

Design retrieval as a restricted server-side component with destination/IP checks, redirect revalidation, restricted egress, credential isolation, bounded request time/size/type/decompression and source request quotas/retries. Use the supported source-policy matrix to specify what can actually be inspected. Failed retrieval and unavailable notice checks must not become passed provenance checks, scientific contradiction or an accusation of a fake source.

### Durable execution and economics

Specify atomic job acceptance/enqueue, persisted attempts and steps, execution ownership, leases/fencing, checkpoints, cancellation, duplicate delivery and stale-result handling. Persist an immutable execution manifest covering input versions, methods/policies, software/prompt versions and non-secret provider configuration. Distinguish safe deterministic recomputation from an uncertain external call accepted before a crash. Preserve the protection against silent duplicate billing; a durable queue alone cannot promise exactly-once provider execution.

Bound per-role input/output tokens and images, accumulated cross-review context, per-attempt/account budget reservations and global provider concurrency/rate/spending. Council currently multiplies provider work beyond initial reviews. Track dispatch, actual supplied usage, failure, cancellation and discarded late outputs separately from accepted scientific results. Unknown usage remains unknown; monetary estimates must be labeled and reconciled. Pilot volume, budgets, quota behavior and global stop thresholds need explicit decisions.

### Reproducibility, operations and migration

Define an immutable artifact manifest resolving original/source versions, transformations, procedure/code/environment parameters, prompt contents or recoverable immutable versions, outputs and report versions. Hashes alone do not retain contents. Explain which calculations can be deterministically replayed and which historical stochastic AI executions can only be inspected. Define retention/deletion/export across originals, snapshots, derivatives, attempts, worker copies and backups, including the limits of reproducibility after deletion.

Separate authorized researcher audit from operator telemetry with emission allowlists, safe reason codes and retention by event class. Correlate API acceptance, attempts, operations and artifacts without logging private research or raw provider errors. Distinguish liveness, readiness and worker progress; observe queue age/depth, operation duration, lease loss, stalled work and recovery. Choose alert thresholds from pilot expectations and measured behavior. Define an operator/support workflow using safe correlation references.

Plan data/files/worker cutover together: inventory IDs, hashes and byte counts; assign ownership; reconcile copied files; preserve recovery material; drain/freeze old execution; then switch readers/writers/workers under explicit schema compatibility. Version persisted records and scientific policies, document supported readers and rollback limits, and define treatment of new writes/jobs an old release cannot read. Re-evaluation creates a new result version; migration must not reinterpret exploratory history as scientific verification.

Establish a pilot envelope for users, active jobs, polling load, artifact size and retained attempts. Store indexed authorized summaries separately from large evidence/output artifacts and apply filtering/pagination in scoped database queries. Use that envelope to evaluate infrastructure rather than choosing vendors without capacity assumptions.

## Proposed staging and examinations

1. **Decide semantics and boundaries:** finalize taxonomy/aggregation, resource identities, first support matrix, source policies, procedure preconditions and Neutral Twin/Blind Optics acceptance criteria; record unresolved product decisions.
2. **Design a narrow scientific slice:** define canonical Core models and adapters plus reference cases for deterministic calculation, source matching, comparability and missing evidence. This stages delivery inside established scope; it does not silently remove claim categories.
3. **Design hosted safety and migration:** ownership, operator controls, external processing, durable attempts, budgets, artifact lifecycle and reversible cutover must be concrete before opening the pilot.
4. **Validate implemented combinations:** known numerical reference cases; original-source identity versus content support; missing/inaccessible evidence; mixed claims; correction/retraction semantics; incompatible comparisons; workbook selection and formula policy; chart distortion and image-only limits; reviewer disagreement and source/check failures. Preserve the user's hypothetical 20% versus reproduced 5% contradiction and treatment-data insufficiency examples as requirements, not measured results.
5. **Validate hosted operation:** cross-account denial including totals/files/jobs; operator-only settings; accepted job surviving web lifetime; duplicate/redelivered/cancelled attempts; crash around external dispatch; retained billing accounting; evidence amendment versus retry; file integrity/rollback; healthy HTTP with stalled workers; and safe researcher/operator diagnostics. Set expected behavior from selected policies, not invented success metrics.

A small reviewed reference suite is necessary before verified capabilities are enabled; a full benchmark-management product can remain unavailable until its evaluation protocol and reference judgments exist. Define rubric ownership and independent review of judgments. No quantitative accuracy, cost, latency or reliability target has been established by these reviews.

## Outstanding decisions and assumptions

The user still needs to select or refine: complete claim outcomes and mixed-claim display; first scientific procedure/source support combinations; source-type mandatory checks and correction/retraction semantics; workbook formula/sheet policy; Neutral Twin/Blind Optics criteria; team/supervisor/institution permissions; legacy ownership assignment; external-processing and retention/deletion policy; pilot scale/budgets/operators and delivery expectations. Authentication, cloud, database, object storage and queue products remain subsequent design choices within those boundaries.

No estimate is invented for cost, headcount or timeline. After the first supported combinations and workload envelope are chosen, produce explicit resource assumptions, estimates, risks and mid/final examinations as required by the Heilmeier standard. A vendor or budget decision should not be implied by a technical mitigation proposal.

MCP, assistant Skills, SDKs, institutional deployment, SSE, additional export formats and full event sourcing remain outside the critical path absent a concrete requirement. Reuse existing polling, inspection routes and exploratory safety controls where their semantics remain accurate. This does not waive authentication, scientific acceptance or compatibility work.
