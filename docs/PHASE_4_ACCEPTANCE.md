# Phase 4 acceptance — analysis inspection and scientific interfaces

Reviewed 2026-11-03. Phase 4 frontend work is implemented and verified against deterministic request mocks and an explicitly labeled local preview adapter. No live Flask scientific service, AI execution or independent scientific validation is claimed.

## Delivered

All six analysis routes now share a coherent header, source/mode/status distinctions, contextual metadata, copyable page links and accessible navigation:

- Overview: original claims, backend assessment, separately classified calculations/source-backed findings/interpretations/unverified information, citations, supplied issues, limitations, review summaries, image previews and suggested interpretation.
- Processing: actual reported stages or high-level status, indeterminate activity, time since a supplied start, partial failures, last-received-state notice after interruption, refresh/reconnect and capability-gated cancel/retry confirmation. No generated progress percentage or invented stage completion.
- Evidence: category navigation, source inspection and actual checked scope, file links/previews, bounded searchable/sortable/paginated tables, variable metadata/units/missing values, study/check/uncertainty inspection, and readable/JSON evidence contracts. Missing values, source verification and unsupported inference remain distinct.
- Visualization Laboratory: original/neutral side-by-side, compatible overlay and keyboard slider, recorded differences, zoom/pan/reset, full-screen dialog, supplied legend, exact-value row inspection, tabular alternative, actual image copy/download, immutable source assets, rendering parameters, supplied generation status/uncertainty warnings and interpretation-change caveats. Incompatible dimensions, absent twins, image failures and blocked clipboard/download operations are explicit.
- Council: four specialized reviewer roles, reported execution status/model/provider, independence metadata, findings/citations/claims/uncertainty and structured reviewer dialogs. Initial reviews, cross-review and judge outputs remain separate. Disagreement ledgers show supplied positions, supporting/contradicting evidence, reported resolution state and rationale; no vote or accuracy score is computed.
- Audit: chronological events, component/type/status/search filters, bounded pagination, supplied duration/input/output/error details, safe event JSON and permitted filtered downloads. Recognized credential fields are redacted; backend logs must still exclude secrets before transmission.
- Report: only supplied nonempty sections/references, document typography, report contents/deep links, section copying, permitted JSON export and browser print styles. No fake references or server PDF export are introduced.

## Backend and fixture boundaries

The executable schemas/adapters are in `frontend/src/research-api.ts`. Source/asset/reference URLs reject executable schemes and embedded credentials. Section permissions default false. Invalid row widths, mismatched server-page columns and missing page metadata are not silently rendered as correctly labeled data.

The explicit development flag selects only sample-a1, sample-running and sample-failed under `/app/analyses/`. Static fixture states never execute an analysis, contact Flask for those views, or progress to completion on a timer. Other IDs use the real API boundary. Production guards exclude the fixture module and its scientific assets, even when the flag is set at build time. Educational public input cases remain separate from result previews.

## Verification evidence

- Strict TypeScript production build and lint pass.
- 22 unit/component tests pass, including malformed scientific-response handling, missing assessments/uncertainty, credential redaction, unsafe URLs and absence of an API-error fixture fallback.
- Full normal browser suite: **64 tests passed**, including prior public/workspace regressions and the Phase 4 inspection journeys.
- Isolated local-preview suite: **3 tests passed**, checking zero API requests on named fixture routes, static processing that does not invent completion, and real API error handling for other IDs.
- Production build with VITE_ANALYSIS_FIXTURES=true passes `npm run verify:fixtures`; development scientific payloads/SVG assets are absent.
- Automated WCAG-tagged inspection checks cover all six views in English/Arabic and light/dark. Keyboard comparison, dialog focus/escape/return, citation navigation, deep links, printing, image clipboard and actual download bytes are exercised.
- Layout checks cover evidence, visualization, Council and report at 360, 390, 768, 1024, 1440 and 1920 pixels in both directions. Loaded-page screenshots, rather than lazy-loading placeholders, are captured under frontend/output/playwright.
- Desktop Laboratory, Arabic mobile Council and print layout were visually reviewed. Backend text retains its supplied language with automatic direction; source images are not mirrored or recolored by theme.

These checks validate frontend behavior with Chromium and controlled data. They do not establish real scientific results, live Flask compatibility, formal accessibility certification, specialist screen-reader acceptance, or cross-browser/cross-origin deployment validation.

## Next stage

Phase 5 remains: finish analysis comparison, benchmarking, report management and integration management, then full-product acceptance, performance and cross-browser review. Existing later-stage routes must not be considered complete merely because they render. The scientific backend remains exclusively the owner's responsibility.

## Subsequent stage update

Phase 5 frontend work has since been completed. The remaining-work paragraph above is the Phase 4 historical snapshot. See PHASE_5_ACCEPTANCE.md for the current research-tool implementation and validation limits.
