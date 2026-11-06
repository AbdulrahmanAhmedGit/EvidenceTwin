# EvidenceTwin Council

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Researchers, university and high-school research teams, scientific-program students, educators and supervisors evaluating scientific claims and their supporting evidence. The primary delivery goal is a controlled browser-based research pilot. Researchers should not need local software or personal AI-provider configuration to use the hosted pilot.

## Product Purpose

Help users identify what evidence supports, contradicts or leaves unresolved about a scientific claim. Users manage research cases, submit claims and references, attach evidence, start Council analyses, monitor execution, inspect findings and disagreements, and read or export reports.

Success means traceable findings, reproducible calculations where applicable, explicit verification coverage and actionable missing-evidence requests. AI agreement alone never establishes scientific truth.

## Positioning

The approved product mechanism combines evidence provenance, bounded deterministic checks, visualization inspection and independent specialist AI reviews with cross-review and adjudication. Reports distinguish source status, performed checks and claim outcomes. A contradicted assertion and an assertion lacking sufficient evidence must remain distinct.

This describes the approved product direction, not a claim that every mechanism is implemented or scientifically validated.

## Operating Context

- The existing application uses React/TypeScript with Vite and a Flask backend. Preserve relevant frontend/API contracts and existing behavior unless a necessary change is explicitly documented.
- The target hosted architecture separates the browser interface, authorization and case management, an independent Python Scientific Core, persistent records, private evidence storage and durable asynchronous execution.
- Preserve original inputs, evidence revisions, source references, methods, model/prompt versions, performed calculations and audit history so another researcher can inspect how a conclusion was reached.
- The approved requirements baseline is `concepts_brief.md`. Detailed proposals and unresolved implementation decisions live in `design_draft.md` and `docs/designs/backend-completion/`; a proposed design is not automatically an approved product fact.

## Capabilities and Constraints

### Existing foundation

The repository documents local persistent exploratory analyses and uploads, configurable server-side AI providers, independent initial Council reviews, cross-review, model adjudication, cancellation/retry/recovery, audit records and exploratory reports. The frontend includes public documentation, research workspaces, analysis creation, evidence and visualization inspection, Council views, reports and capability-aware research tools.

UI availability and successful execution do not establish scientific verification. Source/statistical verification, validated Neutral Twin generation and benchmark scoring must remain explicitly unavailable until their scientific implementations and acceptance criteria are fulfilled. Isolated execution-infrastructure tests do not establish hosted integration or scientific accuracy.

### Approved pilot direction

- Prioritize bounded structured quantitative claims: numerical/descriptive, comparative, visualization-based and basic statistical checks within explicitly supported methods and input combinations. Broader scientific assertions require separately specified support.
- Planned evidence inputs include CSV/XLSX datasets, PNG/JPG charts and source URLs. Attaching an arbitrary research document does not mean its contents were extracted or verified.
- Separate source provenance/authenticity, calculation results, verification coverage and claim assessment. Missing or inaccessible evidence must not be presented as proof that a claim is false.
- Separate historical reproduction from current verification and retain immutable result histories.
- Enforce ownership-aware access to cases, files, reports, jobs and execution history in the hosted pilot. Provider credentials and shared provider administration belong on the server and with authorized operators.
- Keep unavailable capabilities honest. Production must never substitute sample scientific results for API failures. Educational examples and development fixtures must be visibly identified.
- Preserve research inputs and current local data when evolving architecture; migration and rollback require explicit plans.
- MCP and broader external-client integrations are future/experimental work, not V1 release requirements.

### Open decisions

Cloud vendors and hosted infrastructure, authentication implementation, team/supervisor/institution permissions, retention/deletion/export policies, workload and budget limits, exact supported scientific procedures, source-policy matrices, full assessment taxonomy/API mappings, and benchmark reference judgments remain subject to the relevant reviewed specifications. Do not turn draft defaults into approved commitments.

## Brand Commitments

- Use the EvidenceTwin / EvidenceTwin Council identity and the owner-supplied official logo assets under `frontend/public/brand/`.
- Preserve official artwork, proportions and orientation, including in RTL layouts; do not redraw or recolor the supplied marks. Existing usage guidance is in `docs/BRAND_INTEGRATION.md`.
- Use precise, evidence-linked language. Clearly distinguish demonstrated findings, interpretations, uncertainty, unavailable checks and future capabilities. Do not invent research claims, customer proof or validation results.

## Evidence on Hand

- `concepts_brief.md`: approved V1 product requirements, audience, scientific boundaries and unresolved decisions.
- `EvidenceTwin Council — Professional Architecture V3.png`: supplied architecture reference, not proof of completed implementation.
- `BACKEND_IMPLEMENTATION_GUIDE.md` and `backend/README.md`: implementation scope and runtime boundaries; distinguish local operation from planned hosted capabilities.
- `docs/BACKEND_RUNTIME_VERIFICATION.md` and frontend acceptance/review reports under `docs/`: recorded checks with their stated scope and limits. These records are historical evidence, not a fresh verification run.
- `frontend/public/brand/`: official identity assets; `docs/BRAND_INTEGRATION.md` records their provenance.
- Authored educational cases and development-only scientific fixtures demonstrate interface behavior; they are not independent scientific measurements or verified live findings.
- The approved brief selects Ember's 2025 global clean-electricity share as an initial real case. Historical reproduction remains incomplete until publication-time inputs/methodology and an accessible original chart are established; do not promote it to a validated success story.

## Product Principles

1. Ground major conclusions in inspectable evidence and reproducible checks.
2. Keep uncertainty, contradiction, missing evidence and check coverage distinct.
3. Preserve research provenance, privacy and reproducibility throughout the workflow.
4. Make actual capabilities and execution states clear; never manufacture completion or results.
5. Make the research workflow usable in English and Arabic without changing the meaning of supplied scientific content.

## Accessibility & Inclusion

Preserve English/Arabic support with correct RTL layout and readable mixed-direction scientific content. Retain responsive reflow, keyboard navigation, visible focus, accessible form errors and status feedback, reduced-motion preferences and light/dark theme support. Supplied scientific content retains its original meaning and language rather than being silently rewritten or translated.

`docs/ACCESSIBILITY_REVIEW.md` records existing browser checks and limitations. Those checks do not establish complete WCAG certification or real screen-reader/device coverage.
