# EvidenceTwin — quick five-phase audit

Date: 3 November 2026. Scope: current frontend source, existing acceptance records, fresh build/lint/unit checks, browser regression, and focused independent reproductions. Application source and Flask were not changed by this audit.

## Overall finding

All five frontend phases have substantial implemented routes and workflows. The quick audit is positive, but the frontend is not issue-free: two reproducible functional/integration defects should be corrected before final frontend handoff. Passing the existing test suite does not cover these missing scenarios. Live scientific service readiness is not established.

| Phase | Quick assessment | Evidence / remaining boundary |
| --- | --- | --- |
| 1 — Foundation, navigation, design system | Implemented; checked | Routing, mobile menu, focus restoration, sidebar collapse, themes, Arabic/RTL and reduced-motion tests. Minor native dark-theme polish noted below. |
| 2 — Public website and docs | Implemented; checked | Public-route, documentation search/copy/deep-link, bilingual accessibility and responsive coverage. Privacy/Terms are editable drafts requiring owner review. |
| 3 — Workspace and analysis creation | Implemented; checked | Dashboard/history, cases/settings, upload selection, five-step validation, opt-in draft persistence, preserved inputs and capability-gated submission. Server acceptance is mocked in tests. |
| 4 — Analysis inspection | Implemented; two confirmed follow-ups | Evidence, Laboratory, Council/disagreements, audit and print/JSON report checks pass. Analysis identity validation and outbound comparison preselection need correction. |
| 5 — Research tools and final validation | Implemented; checked within frontend scope | Comparison, benchmark configuration/results, report management and integration tests. Actual measurements, comparability, server permissions and connections remain owner-supplied. Report-filter persistence is an optional improvement. |

## Confirmed findings

### Medium — analysis response identity is not validated

`frontend/src/research-api.ts:22` parses the analysis shape but does not require returned `id` to equal the requested ID. `AnalysisWorkspace` then renders that response under the requested route and builds its actions/section links using the route ID.

Browser reproduction: request `/app/analyses/expected-record`, mock a schema-valid response with `id: unexpected-record`; the page displays the mismatched record title instead of rejecting it. A misrouted or incorrectly cached backend response could therefore display one record with another record's navigation/actions. This is an integration-integrity defect, not proof of a real backend data leak.

Recommended fix: reject mismatched analysis IDs before presentation, as the benchmark/comparison adapters already do. Add a regression test covering mismatch, including protection from actions and section retrieval.

### Medium — “Compare analyses” loses the current analysis

`frontend/src/AnalysisWorkspace.tsx:45` generates `/app/compare?analysisA={id}`, while `frontend/src/features/research/Comparison.tsx:10` reads `a` and `b`.

Browser reproduction: follow Compare analyses from an analysis overview. The destination URL contains `analysisA=expected-record`, but selected A is null and the page asks to select two analyses.

Recommended fix: use the same parameter contract (`a` and `b`) in the outbound link and comparison page; optionally accept legacy aliases. Add a journey that starts at an analysis overview and confirms A is preselected.

## Lower-priority polish

- `frontend/src/features/research/Reports.tsx:12`: report search/filter/sort/page state uses component state and is lost on refresh; URLs cannot share the filtered view. Unlike analysis history and comparison selection, it is not synchronized to query parameters. A browser reproduction confirmed search text resets from `audit-filter` to empty after reload. This does not break the current filtering controls.
- `frontend/src/App.tsx:29`, `frontend/index.html:3`: the application palette changes, but no explicit native `color-scheme` or matching `theme-color` is configured. Browser-native controls/scrollbars can retain the OS/browser appearance. In Chromium with a light OS preference and the app set to dark, the root was dark while the search input computed `color-scheme: normal`. This is theme polish, not an automated contrast failure.
- Benchmark configuration explicitly warns that refreshing clears its in-memory draft. A refresh/close warning would further reduce accidental loss without silently storing research content.

## Fresh verification

Fresh results: production build passes; production fixture exclusion passes; lint passes with no reported warnings/errors; all 30 unit/component tests pass; all 84 existing browser tests pass in 3.0 minutes. The full browser run includes bilingual/light-dark accessibility matrices, six responsive widths, navigation/reduced motion, creation/error recovery, scientific inspection and research-tool workflows. The three isolated fixture-preview tests were not rerun in this quick audit; their earlier result remains documented in PHASE_5_ACCEPTANCE.md. The two functional findings above were reproduced independently in Chromium using authored request mocks; neither constitutes real Flask/scientific validation.

## Handoff requirements

1. Correct the two confirmed defects and add regression coverage.
2. Connect and validate the owner's actual Flask contracts, scientific jobs, authorization, measurements and integration availability.
3. Finalize draft legal policies and real contributor/configuration metadata.
4. Complete specialist screen-reader, Firefox/WebKit, real-device and deployment checks before claiming broader launch readiness. Automated Axe/Chromium coverage is not formal WCAG certification.

No production fallback to sample scientific results was found. Missing services remain unavailable or capability-gated. No scientific performance or accuracy claim was validated by this audit.

Review checklist: [Vercel Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md). Local project requirements take precedence over generic stylistic guidance.

## Subsequent stabilization

The two confirmed medium-severity findings above, report-filter persistence and native theme alignment have since been addressed. This audit preserves the original observations; see [FRONTEND_STABILIZATION.md](FRONTEND_STABILIZATION.md) for the current fixes, tests and remaining integration gaps. Benchmark refresh behavior remains an explicitly documented limitation and was not expanded in this scope.
