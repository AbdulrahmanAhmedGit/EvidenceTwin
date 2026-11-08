# Flask integration guide

Build the frontend with `cd frontend && npm ci && npm run build`. Serve `frontend/dist` using an existing deployment web server. Route non-asset browser paths to index.html, but never rewrite `/api/*` errors to the SPA. This supports nested-route refreshes and deep links.

Prefer same-origin hosting. For local development, add a Vite `server.proxy` entry mapping `/api` to the owner's actual Flask origin; preserve the API path unless that backend contract explicitly differs. No Flask port or endpoint availability is assumed.

Alternatively set `VITE_API_BASE_URL` to the public API origin. CORS must allow the exact frontend origin. Current requests use same-origin credentials; cross-origin cookie authentication requires an explicit adapter change and matching credential/CORS/CSRF policy from the backend owner. Do not use wildcard credentialed CORS or place API provider keys in client environment variables.

GET requests have a 15-second timeout. Analysis reads accept query cancellation signals. Mutation errors preserve mounted form state. Input acceptance requires an analysis ID. Health alone does not establish availability of scientific services.

An explicit development-only fixture adapter is available for named analysis previews; see Phase 4 below. It is never an API error fallback and is excluded from production. Educational case inputs remain visibly labeled.

Run unit tests with `npm test`; browser checks with `npm run test:e2e`. Playwright Chromium must be installed (`npx playwright install chromium`). Mocked checks validate frontend behavior only, not a live Flask service.

## Phase 3 capability and draft behavior

To test submission against your Flask service, advertise `analyses.create: true` from the capability endpoint and list supported `modes`, `reviewDepths` and `maxClaims`. Return an accepted string ID from the multipart creation endpoint, then implement the detail/status contract. Enabling Verified Mode does not bypass server evidence validation. Default unsupported actions remain disabled and explained.

The builder retains drafts and files during same-tab client navigation. Saving text across refreshes is opt-in; no file is persisted. Disable the checkbox, discard the draft or use Settings → Clear local research draft to remove saved text. Browser storage denial is reported. Upload transport progress is indeterminate; scientific processing starts only after server acceptance.

## Phase 4 inspection and local previews

Implement the section contracts in FRONTEND_API_CONTRACT.md, or adapt `src/research-api.ts` to the owner's actual Flask responses. All scientific values, assessments, processing stages, reviewer independence and disagreements must come from those responses. Missing outputs produce explicit unavailable states. Export affordances depend on per-section permissions; authorization remains a backend responsibility.

An explicit development-only preview is now available:

```sh
cd frontend
VITE_ANALYSIS_FIXTURES=true npm run dev -- --host 127.0.0.1 --port 5193 --strictPort
```

Open `/app/analyses/sample-a1` for the labeled authored analysis, `/sample-running` for a static processing state or `/sample-failed` for a failure state, using the same `/app/analyses/` prefix. These are fixed interface fixtures: no AI execution, source authentication or scientific experiment occurred. Only those exact IDs select the fixture adapter. Other IDs use the API and never fall back after failure.

Keep VITE_ANALYSIS_FIXTURES false or unset for normal API development. Production ignores the flag because the adapter import is guarded by `import.meta.env.DEV`; fixture data and SVG assets are excluded from production bundles. Verify this even with the flag enabled:

```sh
VITE_ANALYSIS_FIXTURES=true npm run build
npm run verify:fixtures
```

`npm run test:preview` runs an isolated server on port 5193 to verify zero API calls for fixture routes and no synthetic processing completion. `npm run test:e2e` uses port 5191 and API request mocks. Stop a manually running preview on 5193 before running preview tests; tests intentionally do not reuse an unknown server.

Image downloads require real supported image content types. If Flask assets use a different origin, configure CORS for the intended frontend and decide credential/CSRF policy with the owner; the default client uses same-origin credentials. Canvas clipboard operations may fail under browser/origin restrictions and are reported honestly. Do not include tokens or provider secrets in audit/contract/reviewer metadata, even though display helpers redact recognized credential fields.

## Phase 5 connections and development proxy

Research-tool contracts and permissions are documented in FRONTEND_API_CONTRACT.md. Adapt `features/research/api.ts` for the owner's existing API rather than modifying Flask to match the frontend automatically. Enable `research.comparison` and `research.benchmarks.create` only after the matching services are supported. Missing capabilities do not trigger simulated execution. Read-only retrieval still makes real requests so an empty response can be distinguished from authorization or offline errors.

A development proxy is now configurable without source edits:

```sh
cd frontend
# Replace this example with the owner's actual listening origin.
FLASK_DEV_ORIGIN=http://127.0.0.1:5000 npm run dev
```

The optional variable may also go in an uncommitted `.env.local`. Leave `VITE_API_BASE_URL=/api` for this proxy. Requests retain `/api` paths. The target must be an HTTP(S) origin with no path, query or credentials. This configures Vite only and does not assert that a server exists on the example port. Production needs its own web-server `/api` forwarding and SPA fallback; Vite's development proxy is not part of the production build.

Report management exports supplied JSON when both record and report permissions allow it. Reports use inclusive date query fields; decide timezone/filter policy at the backend boundary. Integration copy actions contain public endpoint/tool metadata only. Credential-bearing public integration URLs are rejected. Report deletion and connection tests require backend confirmation and are never automatically retried.

Benchmark request cancellation stops waiting in the browser; it cannot cancel a server job. Check existing runs before manually repeating an uncertain submission. Scientific calculations, rates/denominators, comparability decisions, durable run records and actual integration availability must be supplied by the backend. Test request mocks are confined to E2E code and do not provide runtime research-tool fixtures.

## November 3 frontend stabilization

Analysis responses are now rejected if `response.id` differs from the requested route ID, before scientific data can reach a successful query cache. A background identity rejection also blocks cached-record actions/dependent requests until a matching response is received. Investigate routing/caching if this error appears against Flask; do not bypass the guard. Network-error reconnection continues to preserve the last valid record.

Browser comparison links use `a` / `b`; legacy browser links are accepted. The API comparison contract remains unchanged. Report filters are shareable/restorable through query parameters, without introducing local-storage persistence. Native form controls and browser chrome now follow existing theme preferences. See FRONTEND_STABILIZATION.md for regression evidence and remaining integration limits. No Flask changes are required by these frontend corrections.

## Runnable Flask skeleton

The separate `backend/` factory/Blueprint skeleton now supplies real health and disabled capabilities, with all business/scientific routes returning HTTP 501. The React source is unchanged. Follow [BACKEND_IMPLEMENTATION_GUIDE.md](../../../BACKEND_IMPLEMENTATION_GUIDE.md) for installation, exact-origin CORS, upload/auth extension points and every owner handler TODO. Use the existing FLASK_DEV_ORIGIN proxy configuration above. A reachable skeleton intentionally produces unavailable record states and disabled execution; it is not completed scientific integration.

## November 5 local backend runtime

Flask now persists local exploratory analyses and executes configured reviewer
providers using the existing React contracts. Use the current
[backend guide](../../../BACKEND_IMPLEMENTATION_GUIDE.md), not historical skeleton-only
availability notes, for startup and capability configuration. Set the Vite browser
origin in EVIDENCETWIN_CORS_ORIGINS, including when using the development proxy.
Requests default to real API mode and never fall back to scientific fixtures.
Scientific verification, neutralization and benchmark scoring remain disabled.


## PostgreSQL execution infrastructure handoff

The approved isolated infrastructure increment adds `backend/evidencetwin_backend/execution/`, reviewed Alembic migrations and a disposable PostgreSQL test harness. Existing Flask routes, React adapters, SQLite data, provider settings and prompts remain unchanged. No frontend request has been silently switched to this queue.

Internal boundaries are `Database` (Core/Read Committed transactions), `Repository` (submission/claim/heartbeat/publication/cancellation), `Recovery` (retirement/retry/reconciliation/settlement), `Supervisor` (known same-host child exit) and `Worker` (explicit trusted task orchestration). Their dataclasses are internal contracts, not `/api/v1/` response DTOs. Real HTTP/auth/ownership/storage bridges and legacy migration require separate implementation/approval.

Adapters are explicit and unavailable by default: authorizer; pinned snapshot/configuration source; candidate validator; artifact readiness; execution-stop proof; settlement evidence; and spending authorization. Never register the test adapters in production. Guard rows coordinate future authoritative service writes; they do not implement authentication or source verification. User/account identity must eventually come from the approved backend-validated identity adapter, not caller-provided role strings.

Accepted results bind immutable snapshot/policy/configuration and current authority, attempt, fence, lease, predecessor and operation identity. Validation/artifact preparation happens outside short transactions. Current locked guards are checked again at publication. Equivalent authorized replay returns the prior outcome without requiring the old attempt to remain current; revoked accounts cannot retrieve it. Conflicting keys cannot overwrite the original operation.

Database/queue concerns remain separate from source authenticity, statistical validity, scientific applicability and report completeness. No existing unavailable scientific capability flag was enabled. The first increment exposes no new HTTP endpoint and makes no paid calls. All 24 gates remain OPEN.

Known integration gaps: owner-confirmed claim/binding snapshots; authenticated internal ownership and invitation/session lifecycle; real private-object metadata/readiness/deletion/download flow; Scientific Core validation; provider dispatch/cancellation/usage/budget/rate-limit bridge; hosted remote process-stop proof; full `/api/v1/` DTO mapping; legacy ownership import/cutover; and pilot retention/backups/RPO/RTO/operational acceptance. These cannot be replaced with permissive adapters or sample success responses.

The locally verified route uses private PostgreSQL 18.6, Python 3.14.4 and the locked dependency set. Native client utilities are required for backup/restore tests. The optional Compose test profile is supplied but unexecuted here. No cloud service or system database service was deployed or changed. The detailed completion report and EX specification traceability are in [the backend implementation guide](../../../BACKEND_IMPLEMENTATION_GUIDE.md#isolated-execution-infrastructure-completion-report).
