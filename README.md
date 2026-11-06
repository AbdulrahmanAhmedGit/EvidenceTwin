# EvidenceTwin Council

React/TypeScript frontend for evidence-grounded scientific review. Scientific services belong to the owner's Flask backend.

## Run

```sh
cd frontend
npm ci
npm run dev
npm run build
npm test
npm run test:e2e
```

Node 24 was used for validation. API defaults to same-origin `/api`. Set `VITE_API_BASE_URL` before starting/building to use a different origin. Never put secrets in Vite environment variables.

## Implementation status

The five frontend implementation stages are delivered: foundation/navigation, bilingual public website/documentation, workspace and analysis creation, scientific inspection interfaces, and research tools (comparison, benchmarks, reports management and integrations). Backend-dependent workflows remain capability/permission-aware and were tested with request mocks, not a live Flask scientific service.

After official brand integration, build and lint pass, with 36 unit/component tests and a full 101-test browser regression. Isolated fixture-preview checks remain separate from normal API mode. Responsive and accessibility checks cover English/Arabic and light/dark themes. These checks do not establish specialist screen-reader, cross-browser or production infrastructure certification.

See [development stages](docs/DEVELOPMENT_STAGES.md), [Phase 5 acceptance and remaining limits](docs/PHASE_5_ACCEPTANCE.md), [architecture](docs/FRONTEND_ARCHITECTURE.md), [API contracts](docs/FRONTEND_API_CONTRACT.md) and [Flask integration](docs/INTEGRATION_GUIDE.md). Production never falls back to sample scientific results. The owner must connect actual Flask endpoints and review draft legal content before launch.

A separate Flask backend under `backend/` now supports persistent local exploratory analyses, six configurable AI providers, isolated Council reviews, cross-review, model adjudication, audit and exploratory reports. Scientific source/statistical verification, Neutral Twin generation and benchmark scoring remain explicitly unavailable. See [Backend Implementation Guide](BACKEND_IMPLEMENTATION_GUIDE.md) for setup, scope and provider configuration.


## Local inspection preview

```sh
cd frontend
VITE_ANALYSIS_FIXTURES=true npm run dev -- --host 127.0.0.1 --port 5193 --strictPort
```

Open `/app/analyses/sample-a1`. This is a visibly labeled authored fixture, not live verification. `/app/analyses/sample-running` remains a static processing example; `/app/analyses/sample-failed` demonstrates failure. Leave the flag unset for normal API mode. Production excludes these fixtures even if the flag is set. Run `npm run test:preview` for isolated preview checks and `npm run verify:fixtures` after building to inspect production exclusion.

## Optional Flask development proxy

Set `FLASK_DEV_ORIGIN` to the owner's actual HTTP(S) origin and keep `VITE_API_BASE_URL=/api`. For example, `FLASK_DEV_ORIGIN=http://127.0.0.1:5000 npm run dev` configures Vite forwarding only; it does not start Flask. Production requires web-server API forwarding and an SPA fallback for non-API deep links. See the integration guide for CORS and credential boundaries.

## Latest quick audit

See [five-phase audit](docs/QUICK_FIVE_PHASE_AUDIT.md) for the current review. The two confirmed defects have since been corrected, with identity/recovery and comparison-preselection regressions added. Report-filter URL state and native theme behavior were also stabilized. See [stabilization report](docs/FRONTEND_STABILIZATION.md) for current verification and remaining integration gaps. The audit itself remains a historical snapshot.

## Official brand assets

The supplied EvidenceTwin SVGs are integrated unchanged through a reusable theme-aware BrandLogo component. Public navigation/footer, workspace sidebar/mobile header, report masthead and recovery views use the official artwork. SVG/PNG favicons and an Apple touch icon derive from the official symbol. See [brand integration and verification](docs/BRAND_INTEGRATION.md) for added files, sizing/accessibility rules, screenshots and icon regeneration. No PWA functionality was added.

## Flask backend

See [BACKEND_IMPLEMENTATION_GUIDE.md](BACKEND_IMPLEMENTATION_GUIDE.md) for startup, current endpoint contracts, runtime configuration, CORS/upload/auth boundaries and the remaining scientific implementation checklist. Existing React source and adapters are unchanged. Flask reachability, provider configuration and scientific verification remain separate states.

## Configure AI APIs in the UI

Open /app/settings/ai from Settings or Integrations. Select a provider, enter your vision model ID and API key, then choose **Save and use provider**. No restart is required. See [configuration and private storage details](docs/AI_PROVIDER_CONFIGURATION.md).
