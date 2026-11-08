# Phase 5 — Research tools and final frontend validation

Phase 5 completes the frontend research-tool routes. The scientific backend remains owner-managed and unverified. This report records frontend evidence; it does not assert a deployed service, scientific validation or formal accessibility certification.

## Delivered workflows

- `/app/compare`: independent searchable/status-filtered, paginated analysis selectors; A/B IDs preserved in deep links; backend-supplied comparability warnings, reasons, dimensions and missing values; links back to evidence-bearing analyses. Selection remains stable during filter refetch. Comparison requires positive capability support. No overall winner or accuracy score.
- `/app/benchmarks`: searchable, sortable, status-filtered run index with actual case counts, reported conditions/progress and links. Offline, authorization and empty results remain distinct.
- `/app/benchmarks/new`: validated name/objective, case selection, at least two conditions, configuration/rubric references, repetitions, seed, preserved controls and output options. State remains in tab memory across SPA navigation, with no silent persistent storage. Only backend acceptance navigates to a run. Missing capability permits local configuration validation without execution.
- `/app/benchmarks/:benchmarkId`: actual status polling, measured metric definitions/units/counts/denominators, missing metrics, limitations, per-case failures/disagreements and analysis links, accepted configuration and permitted JSON download. Product evaluation is separated from the original NYAS student experiment. No statistical improvement is inferred.
- `/app/reports`: server-side search, assessment/mode/date filters, sort/pagination, native-dialog preview, real report navigation, permitted JSON export and confirmed backend deletion with failure recovery. Export requires record and detail permission. No fictional reports or server PDF service.
- `/app/integrations`: backend-reported categories/statuses/requirements/instructions/authentication descriptions/tools; safe public endpoint descriptions; documented setup links; permission-gated connection tests that distinguish HTTP acknowledgement from reported test failure. No fake packages or automatic assistant invocation.
- Unknown workspace URLs now produce a real 404. Existing shell navigation, theme/language preferences, reduced motion and earlier frontend workflows are preserved.

## Integration boundaries

New runtime calls are centralized in `features/research/api.ts`. Zod validates responses, benchmark input, comparison identity, public credential-free URLs and metric semantics. Measured rates require denominators; null remains unavailable. Mutations are never automatically retried. Frontend capability flags are not authorization controls.

The optional `FLASK_DEV_ORIGIN` Vite development proxy preserves `/api` paths without starting or modifying Flask. Production SPA fallback, same-origin API forwarding, CORS/credential/CSRF behavior and private secrets remain deployment/backend responsibilities. See FRONTEND_API_CONTRACT.md and INTEGRATION_GUIDE.md.

No research-tool runtime result fixtures were added. Authored request mocks live in E2E tests only. The existing named inspection preview remains explicitly development-only and is not an API-failure fallback.

## Verification record

Completed checks:

- `npm run build`: strict TypeScript and production bundling pass. New research modules are route-split; individual research chunks are approximately 6–19 kB before gzip. No dependency additions were needed.
- `npm run lint`: passes with no reported warnings/errors.
- `npm test`: 30 unit/component tests pass in six files. New coverage includes benchmark validation, metric units/denominators, missing capabilities/values, public URL constraints and comparison identity.
- `npm run test:e2e`: full 83-test regression passes, including public pages, creation, settings, evidence, Laboratory, Council, audit, reporting and the initial 19 research tests.
- After final local-validation feedback, count-unit wording and public request example changes, `npm run test:e2e -- research.spec.ts`: all 20 research tests pass. The resulting normal browser suite contains 84 distinct tests. The full suite was not unnecessarily repeated after these scoped changes.
- Three isolated development-preview checks pass on a temporary dedicated port (5197), preserving the existing user preview on 5193. Named fixtures make no Flask calls; static processing does not advance; unknown IDs use the real API boundary.
- `VITE_ANALYSIS_FIXTURES=true npm run build` followed by `npm run verify:fixtures`: production artifacts exclude the scientific fixture sentinel, dummy credential and fixture SVG assets.
- Research layout checks cover six routes at 360, 390, 768, 1024, 1440 and 1920 pixels in both languages and themes (144 width/route/locale/theme checks), with no document overflow. Axe checks cover the new pages and report-preview dialog, and the research page matrix reports no runtime page errors.
- Rendered desktop/mobile screenshots were inspected for comparison, benchmark configuration/results, reports and integrations under `frontend/output/playwright/phase5-*`. The layouts retain paired-analysis labeling, explicit missing metrics and readable mobile forms.
- Production-preview smoke check: all 33 requested route samples, named production fixture ID and not-found paths return the SPA and render meaningful content without runtime page errors or a fixture banner. Nested navigation loads from built assets. No live Flask service was involved.
- Keyboard/focus checks include native-dialog Escape/focus restoration and the established navigation, chart, wizard and reduced-motion journeys. No synthetic scientific progress is added.

Automated browser tests use Chromium and request mocks. Axe checks and interaction tests supplement visual review; they do not replace specialist screen-reader testing or prove full WCAG conformance.

## Known limits and owner handoff

- No Flask endpoints, scientific verification, AI-provider execution, statistical evaluation or real assistant connection was supplied or independently tested.
- Authentication/session management and provider secrets are not implemented in the browser. Server-wide export/deletion and notifications remain explicitly unavailable without owner adapters.
- JSON and browser print are implemented; no server PDF-generation service is advertised.
- Benchmark conditions, rubric/model references, case eligibility, controls and reproducibility need backend enforcement. Aborting an acceptance request stops browser waiting, not server execution.
- Public Privacy and Terms remain editable drafts. Contributor metadata requires owner-supplied information.
- Backend scientific narrative is displayed as supplied, with automatic direction; it is not automatically translated. Authored interface controls support English and Arabic.
- Chromium verification does not establish Firefox/WebKit, specialist screen-reader, real-device or production infrastructure behavior. No performance/accuracy claims or formal security/accessibility certification are made.
