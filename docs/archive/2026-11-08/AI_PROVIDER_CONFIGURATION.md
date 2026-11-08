# Configure AI APIs in the workspace

Open **Settings → Configure AI APIs**, or /app/settings/ai.
The same link appears in workspace Integrations.

1. Select Ollama, OpenAI, Google Gemini, Anthropic, OpenRouter or DeepSeek.
2. Enter the exact vision-capable model ID available to your account.
3. Enter the provider API key. For local Ollama, set its endpoint
   (for example http://127.0.0.1:11434); no key is required for an unauthenticated
   local server.
4. Choose **Save and use provider**. Flask applies the provider immediately for
   future submissions. Queued/running analyses retain their original provider;
   their Council cannot switch providers halfway through.
5. Optionally choose **Check model catalog**. This performs model discovery,
   not generation or scientific verification. A listed model does not establish
   generation permissions, quota, vision support or scientific accuracy.
   Actual provider errors remain visible in analysis states.

Blank replacement-key fields preserve existing keys. A saved server key can be
replaced or removed; removing it may reveal a configured environment key again,
as indicated in the interface. Saved credentials are never returned by the API or
prefilled in the browser. Switching provider clears an unsaved key. Failed saves
preserve entered fields so the user can retry.

## Storage and access

Configuration is stored in provider-settings.json inside EVIDENCETWIN_DATA_DIRECTORY
(default backend/instance/), with mode 0600 and atomic replacement.
It is **not application-encrypted**. Access to the server filesystem remains
access to these credentials. The directory is ignored by version control.
Credentials are not persisted in browser localStorage, sessionStorage, query caches,
generated reports or application logs. Newly typed keys live in component memory
until saved; the input is then cleared.

The existing owner AUTHENTICATE_REQUEST hook protects all configuration endpoints
when enabled. Otherwise this remains the existing localhost, single-workspace
application; configuration affects the whole workspace. Browser mutations require
a same-origin or explicitly allowed Origin. No new login/account system is added.

The active provider and non-secret metadata persist across restarts. UI values
override startup environment defaults. Environment keys remain fallbacks; each
provider can retain its own saved model/key. No credentials are copied from snippets.

## HTTP contracts

| Method / path | Input | Output |
| --- | --- | --- |
| GET /api/settings/ai | none | AISettingsPublic |
| POST /api/settings/ai | AISettingsInput JSON | AISettingsPublic after durable save |
| POST /api/settings/ai/test | none; tests active saved provider | status, message, checkedAt |

AISettingsInput has provider, nonblank model, optional apiKey, optional removeKey,
and optional ollamaHost (Ollama only). apiKey and removeKey cannot both be supplied.
AISettingsPublic has activeProvider and provider records containing id, name,
model, configured, keyConfigured, keySource (server/environment/none), requiresKey,
and optional ollamaHost. It deliberately has no API key field.

Schemas live in backend/evidencetwin_backend/contracts/ai.py and the frontend
settings API module. Skeleton-only deployments lack these runtime endpoints;
the page presents a recoverable backend error.

Scientific capabilities remain unchanged: exploratory review only. Scientific
verification, neutral generation and benchmark scoring stay unavailable.

## Verification

Backend tests cover private-file permissions, persistence, preservation/replacement/
removal, invalid input, auth/origin protection, environment fallbacks and switching
providers during a running Council. Provider tests verify catalog GET requests.
Frontend tests cover validation, key clearing, retry, switching, Arabic and checks.
Two browser regressions cover save/reload/key-storage behavior, Arabic RTL/mobile/
dark theme and Axe checks. Test credentials and provider responses are synthetic;
no live credentials or generation are used.

Executed verification: **204 backend tests**, **42 frontend tests**, lint,
production build, fixture-exclusion check and **two browser regressions** passed.
The browser regressions include Axe checks. The live Flask page was inspected at
1280px and 390px with zero console errors/warnings; no real credentials were
entered or provider generation invoked during inspection.

Screenshots: [desktop](../../../frontend/output/playwright/ai-settings-desktop.png),
[mobile](../../../frontend/output/playwright/ai-settings-mobile.png).
