# EvidenceTwin frontend

React 19.3, React Router 7.18, TypeScript and Vite 8. Run from this directory:

```sh
npm ci
FLASK_DEV_ORIGIN=http://127.0.0.1:5000 VITE_API_BASE_URL=/api npm run dev -- --host 127.0.0.1 --port 5202 --strictPort
npm run build
npm run lint
npm test
npm run verify:fixtures
```

See [setup](../docs/DEVELOPMENT.md), [architecture](../docs/ARCHITECTURE.md), [workflow](../docs/PRODUCT_WORKFLOWS.md), [API](../docs/API.md), and [design system](../DESIGN.md). Flask lives in `../backend/`; Vite only proxies it and does not start it. Production never substitutes fixtures for an API failure.

`npm run test:e2e` runs the older broad Playwright specs. They still describe portions of the previous workflow and require deliberate revision before serving as acceptance of the new case journey. `npm run test:preview` is an isolated authored-fixture check. See the development guide for the visibly labeled development-only preview and production-exclusion boundary.
