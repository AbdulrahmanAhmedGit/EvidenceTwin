# Backend runtime verification — November 5, 2026

The backend implements the exploratory application/Council flow derived from the
owner's VA.py, all.py, prompts and Architecture V3 diagram. Source/statistical
verification, Blind Optics/Neutral Twin, benchmark scoring and MCP remain
unavailable by explicit owner instruction pending scientific specifications.

## Executed checks

- Backend pytest: **182 passed**, including retained skeleton/contract tests,
  all six provider transport adapters, runtime jobs and unchanged frontend parsers
  loaded through actual HTTP. Provider HTTP responses are mocked in adapter tests;
  workflow tests use an explicit synthetic test provider and temporary storage.
- Frontend lint: passed.
- Frontend unit/component tests: **36 passed**.
- TypeScript/production build: passed.
- Python compileall: passed.
- pip check: no broken requirements.
- Machine-readable contract export: **25 definitions**.
- Editable package installation and isolated wheel build: passed. All **seven**
  owner prompts are packaged and byte-identical to snippets/prompts originals.
- Actual Flask/Vite proxy: health, capabilities and analysis reads return HTTP 200.
  Health identifies workspace mode; no provider configured; creation disabled.
- Browser inspection using installed Brave/Chromium through Playwright CLI:
  connected workspace at 1280px and 390px renders real backend capability state.
  Console contains **0 errors and 0 warnings**. No mock records were inserted into
  the persistent workspace for visual inspection.

Screenshots:

- [Desktop](../frontend/output/playwright/backend-runtime-workspace.png)
- [Mobile](../frontend/output/playwright/backend-runtime-mobile.png)

## Boundaries

No real provider generation request was made, and no API credential was copied
from snippets into backend configuration. Tests establish local application and
wire-contract behavior, not live provider/model access or scientific accuracy.
Choose EVIDENCETWIN_PROVIDER/EVIDENCETWIN_MODEL and configure a rotated server-side
key to enable actual generation. The previously hardcoded VA.py key was removed.
The original all.py pilot evaluation script and existing React source are unchanged.

The local worker uses one process and one private workspace directory. User/account
isolation and scientific services require the owner implementations listed in
[the backend guide](../BACKEND_IMPLEMENTATION_GUIDE.md). API route registration,
structured output validation and model agreement do not establish scientific truth.
