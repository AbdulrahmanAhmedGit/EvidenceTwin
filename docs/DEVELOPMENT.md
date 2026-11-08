# Development and setup

Use the repository lockfiles. Current frontend packages are React 19.3 / Router 7.18 / Vite 8; Node 24 was used for validation. Backend instructions use Python 3.14 and the existing project `.venv`, not the system interpreter. The current locked environment does not include `python-dotenv`; export server variables explicitly rather than relying on `.env` loading.

From `backend/`:

```sh
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

From `frontend/` in a second terminal:

```sh
npm ci
FLASK_DEV_ORIGIN=http://127.0.0.1:5000 VITE_API_BASE_URL=/api npm run dev -- --host 127.0.0.1 --port 5202 --strictPort
```

Open `http://127.0.0.1:5202/app`. The Vite proxy keeps cookies and API calls same-origin. Accounts-disabled mode is a single-user local operator workspace; keep both listeners on loopback. `VITE_API_BASE_URL` defaults to `/api`; never put secrets in browser environment variables. Credentialed account use across origins is not supported by the current CORS configuration; prefer the same-origin proxy.

The development proxy preserves the browser-facing `Host` header (`changeOrigin: false`). Flask compares it with the browser's `Origin` on writes. Rewriting the host to the Flask target causes valid saves to return 403 and display an account-access error. Keep the origin check enabled.

`EVIDENCETWIN_DATA_DIRECTORY` selects a private data root (default `backend/instance/`). Use a disposable explicit directory for experiments. Keep one application process per data directory. See [deployment/rollback](DEPLOYMENT_ROLLBACK.md) before switching modes or binaries.

To enable invitations, export `EVIDENCETWIN_ACCOUNTS=1` consistently for the server and CLI. From `backend/`:

```sh
.venv/bin/python -m evidencetwin_backend.accounts invite-researcher --name researcher
.venv/bin/python -m evidencetwin_backend.accounts invite-researcher --name operator --operator
.venv/bin/python -m evidencetwin_backend.accounts disable-researcher --name researcher
```

The standalone account CLI reuses account operations without starting Flask or acquiring the worker lock, so it can provision/revoke accounts while the service runs. Compatible `flask --app evidencetwin_backend:create_app` account commands require the workspace server to be stopped.

Invitation prompts for and confirms a password; do not put it in a command argument. Disabling revokes existing sessions. There is no public registration or automatic legacy ownership assignment. The server uses `EVIDENCETWIN_SESSION_SECRET` or a private `session.key`; preserve it with the data root. Cookies are HttpOnly, SameSite Strict, API-path scoped, with a 12-hour session lifetime. Set `EVIDENCETWIN_SECURE_COOKIES=1` for a separately reviewed HTTPS deployment.

Operators can configure six providers at `/app/settings/ai`: Ollama, OpenAI, Google, Anthropic, OpenRouter and DeepSeek. Alternatively set `EVIDENCETWIN_PROVIDER`, `EVIDENCETWIN_MODEL` and the provider's server-only API key (`GEMINI_API_KEY`/`GOOGLE_API_KEY` for Google). Provider secrets and `ai-settings.json` are private; never print, export or commit them. Saving a case does not call a provider. Running Council requires explicit consent, evidence and a configured provider; configuration alone does not prove reachability or model suitability.

From `frontend/`, use `npm run build`, `npm run lint`, `npm test`, then `npm run verify:fixtures` after building. From `backend/`, `.venv/bin/python -m pytest tests --ignore=tests/execution -q` excludes the isolated PostgreSQL suite. The PostgreSQL suite requires explicitly disposable infrastructure; retain the detailed [backend instructions](../backend/README.md), rather than pointing it at application data.

For visual fixtures only, start Vite with `VITE_ANALYSIS_FIXTURES=true` and visit `/app/analyses/sample-a1`; running/failed fixtures also exist. These are visibly labeled authored development examples. Production excludes them even when that flag is set. Normal API errors never fall back to fixture findings. `npm run test:preview` checks the isolated preview; existing broad `test:e2e` specs need deliberate workflow updates and are not current acceptance evidence.

Dedicated Playwright MCP, Context7 MCP and Chrome DevTools MCP were unavailable during this transformation. Browser feedback used installed Playwright CLI with Brave and disposable actual Flask storage; some inspection captures use labeled development fixtures. No paid-provider, scientific, hosted, physical-device, screen-reader or cross-browser acceptance is claimed. The owner performs final acceptance.

## Installed engineering MCPs

On 2026-11-08, the owner authorized installation of missing MCPs. Context7, Playwright MCP and Chrome DevTools MCP were installed under the local user tool directory and registered with Codex. They were invoked through a local stdio MCP client during this increment. Browser tools use isolated headless Chromium with no public debugging endpoint. This is development tooling, not a new EvidenceTwin product dependency or a product MCP service. Context7 supplied Pydantic 2.14.1 documentation for the installed 2.14.2 patch family. Local setup remains functional without these agent tools.

## Optional local report translation

Run LibreTranslate in a separate environment because its Flask dependencies differ from the research backend. The installed local service is at `~/.local/share/evidencetwin-libretranslate/venv`. English and Arabic models are stored under that directory's `data/`.

```sh
XDG_DATA_HOME="$HOME/.local/share/evidencetwin-libretranslate/data" \
XDG_CACHE_HOME="$HOME/.local/share/evidencetwin-libretranslate/cache" \
OMP_NUM_THREADS=2 "$HOME/.local/share/evidencetwin-libretranslate/venv/bin/libretranslate" \
  --host 127.0.0.1 --port 5002 --load-only en,ar --threads 2 \
  --char-limit 3000 --batch-limit 4 --disable-files-translation --disable-web-ui
```

Backend configuration uses `EVIDENCETWIN_LIBRETRANSLATE_URL` (default `http://127.0.0.1:5002`) and optional server-only `EVIDENCETWIN_LIBRETRANSLATE_API_KEY`. An unavailable service leaves the original report readable and shows an honest translation limitation.
