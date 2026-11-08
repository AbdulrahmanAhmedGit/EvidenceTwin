# Frontend stabilization — November 3 audit fixes

Scope: correct the two confirmed medium-severity defects, restore report-filter state, and align native controls with the existing theme. No feature expansion, redesign, dependency changes or Flask/backend changes.

## Analysis response identity

`src/research-api.ts` now parses the response and requires an exact match between its `id` and the requested analysis ID before returning data. This follows the parse/compare/reject convention of the existing benchmark and comparison adapters. A client-side `AnalysisIdentityError` extends the existing `ApiError` and uses the message `Analysis response ID mismatch.` It does not invent an HTTP status or expose a foreign record ID.

Initial mismatches never enter the successful query cache, so scientific content, related section requests and job actions cannot use them. If a refresh rejects identity after a previously valid response, the shell also withholds cached metadata, disables dependent queries/actions, cancels outstanding section queries, closes an action-confirmation dialog, and stops interval polling. A later matching response restores the view. Ordinary network interruptions retain the established last-valid-record/reconnect behavior.

Unit coverage includes rejected identity, matching identity with an encoded request path, and recovery after rejection. Browser coverage checks all six analysis tabs, absence of related requests and mutations before acceptance, recovery into the report, and a background mismatch while cancellation confirmation is open.

## Comparison preselection

Browser navigation consistently uses `/app/compare?a={id}&b={id}`. Compare analyses from the overview now preselects the current analysis as A and retains it after refresh.

Legacy `analysisA` / `analysisB` browser parameters are accepted and replaced with canonical `a` / `b` parameters. Explicit canonical values take precedence, and clearing a selection cannot restore a legacy value. This is browser URL compatibility only: the already documented proposed API request `/api/comparisons?analysisA=...&analysisB=...` is unchanged.

## Report filters

Search, assessment, mode, creation-date bounds, sort and page now derive from URL query parameters. Refresh and browser back/forward restore the selected view. Changing a filter resets pagination in the same URL update; typing search uses history replacement. Unsupported enum/page values and invalid ISO dates fall back to safe defaults. Controlled fields update synchronously, while their own URL transitions are marked in browser history state so rapid edits cannot overwrite newer input. External navigation and browser back/forward restore controls from the URL. A dedicated rapid-typing/multi-filter regression supplements the existing report query, preview, export and deletion checks. Existing server-side filtering, debouncing, permission checks and deletion behavior are preserved.

URLs contain the selected filters; no new local-storage persistence was introduced.

## Native theme

The existing theme preference now sets the document's native `color-scheme` to light/dark and updates `meta[name="theme-color"]` to the corresponding existing background color. Explicit choices override the OS preference; System follows OS changes. There are no new colors, layouts or animations.

## Verification

Final results:

- `npm run lint`: passes with no reported warnings/errors. The report URL/history synchronization effect has one narrowly documented lint exception because it synchronizes controlled inputs with external navigation.
- `npm run build`: strict TypeScript compilation and production bundling pass.
- `npm test`: all 33 unit/component tests pass, including three new identity-boundary tests.
- `npm run test:e2e`: all 92 browser tests pass in the final full run (2.9 minutes). Eight new stabilization tests cover mismatch/recovery, stale-metadata/action blocking, all section gates, overview-to-comparison preselection, legacy links, report refresh/back/forward, invalid URL controls, rapid edits and native theme behavior. Existing bilingual/accessibility/responsive, error-recovery, report-export and deletion coverage also passes.
- Three isolated development-preview tests pass on dedicated port 5197 without disrupting the existing preview on 5193. Named fixtures still make no Flask calls, processing does not synthesize completion, and unknown IDs retain the real API boundary.
- `npm run verify:fixtures`: production scientific fixture exclusion passes.
- File hashes before/after confirm changes only to frontend source/tests/index and project documentation. No Flask/backend files or dependency manifests changed. Changed-file whitespace checks pass.

Browser requests are mocked; these results do not establish that a real Flask service implements the contracts. The earlier report-filter failure was corrected and covered by the rapid-edit regression before the successful final full run.

## Remaining integration gaps

- Owner Flask endpoints still need real integration validation. The returned analysis ID must exactly match the requested ID; identity errors should prompt investigation of server routing/caching, not relaxed validation.
- Server-side authorization, scientific processing, source verification, review execution, comparability, benchmark measurements and integration connection tests remain owner responsibilities. Client guards cannot establish scientific correctness or enforce server authorization.
- Section/report payloads retain their existing contracts. No new backend fields or endpoints are required by these fixes. Read/action capability flags still reflect actual backend support.
- Authentication/session handling, notifications, server-wide data controls and server PDF generation remain unavailable unless corresponding owner adapters are supplied. JSON export and browser print retain their existing behavior.
- Browser validation uses Chromium and authored request mocks. Specialist screen-reader, Firefox/WebKit, real-device and production infrastructure verification are not claimed.
- The benchmark draft remains explicitly in-memory and is cleared on refresh, as documented in the existing UI. This stabilization does not add draft features or expand its scope.
