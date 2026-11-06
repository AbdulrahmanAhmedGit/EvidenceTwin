# Frontend architecture

Vite serves a strict TypeScript React SPA. React Router owns public and workspace routes. TanStack Query owns health, capability, analyses, activity and analysis-detail requests. Analysis status polls every five seconds only while queued or running. `src/api.ts` centralizes HTTP, timeout and normalized errors; scientific/domain adapters validate responses with Zod. The API client returns data and never navigates.

Public content is in `content/public.ts`, educational case metadata in `content/cases.ts`, and owner-editable contributors in `content/contributors.ts`. Articles, guides and visual explanations are reusable modules. Fonts ship as local WOFF2 assets with license copies. CSS variables provide light/dark palettes; logical properties support RTL. Locale-aware authored content is complete for the public site and Phase 3 workspace routes. Scientific inspection UI is also bilingual; backend content retains its supplied language. Phase 5 research-tool controls are also bilingual.

Workspace history, settings, creation and analysis inspection are lazy-loaded. `WorkspaceHome.tsx` owns list/dashboard presentation. `workspace-api.ts` defines analyses, capability and activity contracts. Creation is extracted under `features/analyses/` and preferences under `features/settings/`. Further shell/component extraction can accompany later stages.

## Draft state and submission

A small `useSyncExternalStore` draft store preserves text and File references across SPA navigation. It saves only schema-validated text after explicit opt-in; files and file metadata are excluded from browser persistence. Saved text restores at Evidence. Storage failures are reported. Successful acceptance clears the draft and retains an accepted-ID receipt in memory. Shared pending state prevents concurrent sends across route remounts.

The wizard owns step validation, error focus, capability gating, input preservation and navigation. Requests use 15-second read timeouts and a 120-second creation timeout. Multipart upload is indeterminate because fetch does not expose reliable transport progress. No synthetic percentage or automatic mutation retry is used. Verified Mode eligibility remains a backend decision.

## Preferences and safety boundaries

Subscribed preferences apply language, theme, motion and density immediately. System theme tracks OS changes. A storage-denied session fallback keeps safe preferences functional; research text has a separate explicit-consent persistence path. Diagnostics copy only known public configuration fields. No authentication adapter or provider secrets are embedded. An error boundary provides render-error recovery without turning failures into scientific results.

There is no production result fixture fallback. Explicit development-only analysis previews are available. Educational inputs are labeled. Backend-dependent features require adapters/capability support and must remain unavailable otherwise. Flask, scientific processing and AI orchestration remain the owner's responsibility.

## Remaining work

Phase 5 adds comparison, benchmarks, reports management and integration management. Validation evidence and remaining limits are recorded in PHASE_5_ACCEPTANCE.md. Scientific interfaces use typed adapters and request mocks or explicit development previews; actual Flask scientific execution remains unverified and owner-managed. Chromium automation does not establish specialist screen-reader or cross-browser certification.

## Phase 4 inspection modules

`AnalysisWorkspace.tsx` owns the analysis shell, lifecycle query, bounded processing updates and acknowledged job actions. Evidence, Visualization Laboratory, Council, audit and report are lazy feature modules under `features/inspection/`. Read adapters validate identity/status/source provenance, typed scientific findings, dataset alignment, reviewer execution metadata, recorded visual changes, audit events and report sections before presentation. Missing data is rendered explicitly rather than inferred.

The developer preview adapter is dynamically imported only in a DEV-and-flag branch for three exact IDs. It is separate from production API reads and never catches a failed request to produce sample results. Tests verify both the no-API preview behavior and production artifact exclusion. Local display operations do not alter source data or generate server neutralizations.

Per-section download flags are UI policy hints, not authorization enforcement. JSON views and exports redact known credential fields; the backend must never return private tokens. Image downloads fetch actual supported image blobs through the API client. The report uses browser printing without pretending a server PDF service exists.

## Phase 5 research modules

`features/research/` contains lazy route modules for comparison, benchmarks, reports and integrations. Its `api.ts` owns response/input schemas, public URL constraints, comparison-pair validation, measured-rate denominator rules and centralized API calls. `hooks.ts` owns query-backed research capabilities and debounced search. `shared.tsx` provides pagination and truthful copy/capability feedback. Existing public/workspace/inspection presentation and tokens are preserved.

Analysis selectors retain their visible result list during refetch and temporarily disable selection until updated records arrive. Comparison IDs use URL parameters. Reports and benchmarks use server-side list filters/pagination; per-case benchmark display uses bounded DOM pagination. A benchmark draft remains in tab memory across client navigation, with no silent local-storage persistence. Only server acceptance navigates to a run. Downloads and tests require per-record capability/permission. JSON export uses existing credential-redaction utilities.

Research route chunks remain separate from the initial application. Motion uses short disclosure/page transitions with system/application reduced-motion suppression. Authored chrome is bilingual; supplied scientific content is displayed with automatic text direction and is never automatically translated or altered.

The optional `FLASK_DEV_ORIGIN` Vite setting proxies `/api` in development only. It is not exposed as a client environment variable. No backend is started or created by this option. Unknown workspace paths now render a genuine 404 rather than falling into a benchmark scaffold.
