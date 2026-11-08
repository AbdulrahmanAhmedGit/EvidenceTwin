# Phase 3 acceptance — workspace and analysis submission

Reviewed 2026-11-03. Phase 3 frontend workflows are implemented. Flask integration is verified with request mocks, not a live scientific backend. This does not declare Phases 4 or 5 complete.

## Delivered routes and behavior

- `/app`: actual record retrieval, service/provider/job configuration states, local-draft continuation, recent records, supplied awaiting-input records, educational cases, and a capability-gated activity feed. Unknown or unavailable services are explicit.
- `/app/analyses`: server-side search, status/mode/assessment filters, date/title/status sorting, pagination, list/grid view, selections, capability-gated deletion/retry, delete confirmation, partial-deletion recovery, and report links only when reported available. Filter/view state survives refresh through URL parameters. Empty lists, empty results, authorization requirements and connection failures differ.
- `/app/analyses/new`: five-step validated workflow with local file picking/drop, previews, remove/replace, duplicate/type/size validation, source/study/population/uncertainty/context fields, multiple editable claims, requested verification mode/review depth, and complete pre-submission summary. All author-visible controls are localized.
- `/app/library` and `/app/library/:caseId`: searchable educational cases, domain/context/design metadata, structured input tables, local chart illustrations, missing-source limitations and explicitly selectable example claims. No source or interval bounds are invented.
- `/app/settings`: light/dark/system theme, English/Arabic, density, reduced motion, new-draft defaults, preferred chart view, connection diagnostics and confirmed local-draft clearing. Authentication, server-wide data export/deletion and notifications remain explicitly unconfigured.

## Draft and submission guarantees implemented in the frontend

Text and File references survive same-tab SPA navigation. Across refreshes, text is saved only after an explicit opt-in; files and file metadata are excluded. Storage failures are reported. Saved text restores at Evidence so missing files must be reattached. Users can revoke persistence, discard a draft, or clear it through Settings.

Submission requires positive capability support for create, requested mode, review depth and claim count. This is configuration eligibility, not scientific verification. Actual evidence sufficiency remains backend policy. The API client returns a validated accepted ID; the wizard owns navigation. Failed or unconfirmed submissions preserve inputs, with a warning to inspect history before retrying an unconfirmed request. Pending state is shared across route remounts. Upload is indeterminate rather than a fabricated percentage.

## Navigation, accessibility and motion

Labels, error associations, error-summary focus, step-heading focus, current-step semantics, RTL layout, localized status text and native confirmation dialogs are implemented. Sidebar sections stay active on nested routes and settings breadcrumbs identify the correct page. Motion and density preferences apply immediately; system theme tracks OS changes. An application error boundary supports render-error recovery without presenting an error as a scientific outcome.

## Verification

- Strict TypeScript production build and lint pass.
- 15 passing unit/component tests cover API incompatibility/acceptance, HTTP 204, file constraints, claim/source validation, draft serialization and application-error recovery.
- The full 39-test browser suite passed after the Phase 3 changes. Post-review localization refinements were verified with targeted browser checks. It covers successful mocked acceptance, failed submission/input preservation, capability gating, draft opt-in/revocation/refresh, in-memory file preservation, settings, list management and existing public journeys.
- Automated WCAG-tagged checks cover six workspace routes in English/Arabic and light/dark, plus a wizard validation state. Public regression accessibility checks remain in the suite.
- Workspace layout checks wait for loaded pages and cover builder/history/settings at 360, 390, 768, 1024, 1440 and 1920 pixels in both languages. Desktop builder and Arabic mobile settings were visually inspected; screenshots are generated under frontend/output/playwright.

Automated checks are not formal accessibility certification. Manual specialist screen-reader review, non-Chromium validation and live Flask scientific execution are not claimed.

## Remaining project work (snapshot at Phase 3 acceptance)

Phase 4 has since been completed; see PHASE_4_ACCEPTANCE.md for its current acceptance record.

Phase 4: complete and deepen the analysis inspector, processing, Visualization Laboratory, Council/disagreement, audit and report experiences and their tests. Add the isolated development result adapter if needed for those previews; production must never fall back to scientific fixtures.

Phase 5: complete comparison, benchmarks, reports management and integration management, then perform full-product acceptance, performance and cross-browser review. Existing scientific-result pages and later research-tool routes must not be considered complete merely because they render.
