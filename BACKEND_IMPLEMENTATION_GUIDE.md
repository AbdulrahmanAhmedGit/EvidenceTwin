> Current guidance — 2026-11-07: This document preserves the original local-runtime and isolated PostgreSQL implementation evidence. Its pre-case workflow, shared settings and authentication statements are historical. Read [documentation authority](docs/DOCUMENTATION_MAP.md), [current API](docs/API.md), [setup](docs/DEVELOPMENT.md), [workflow](docs/PRODUCT_WORKFLOWS.md) and [deployment/rollback](docs/DEPLOYMENT_ROLLBACK.md) for revisioned cases, invite-only sessions and operator controls. No hosted cutover or scientific enablement is implied. The original body follows unchanged.

# EvidenceTwin backend implementation and operation

## Current scope

The backend now implements the local, single-workspace exploratory analysis and
Council workflow using the supplied `snippets/VA.py`, `snippets/all.py`, and the
seven supplied prompt documents. React source and API contracts remain compatible.
The architecture reference is `EvidenceTwin Council — Professional Architecture V3.png`.

Working application behavior includes upload acceptance, persistent records,
queued/running processing, isolated reviewer calls, structured response/reference
validation, cross-review, model adjudication, audit records, generated exploratory
reports, record/report deletion, search/filter/pagination, descriptive comparison,
explicit example cases, and integration metadata. Nothing falls back to fixtures.

**Scientific source verification, statistical verification, Blind Optics/Neutral
Twin generation, benchmark evaluation, and MCP remain unavailable.** The owner
explicitly requested that services lacking scientific specifications stay
unavailable. Verified mode is rejected, even if a caller bypasses React controls.
A model judgment is retained in the Judge panel as an AI interpretation. It is
never promoted to a scientifically verified verdict badge: overview/report status
remains `not_evaluated`. Arithmetic in a model response is not a verified calculation.

## Configure providers in the workspace

Open **Settings → Configure AI APIs** (/app/settings/ai) to select a provider, enter a model and save its API key. Changes apply immediately without a restart. Settings persist privately on Flask and keys are never returned to React. See [UI configuration and storage](docs/AI_PROVIDER_CONFIGURATION.md). Environment setup below remains an optional deployment default.

## Install and run

```sh
cd backend
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
# A vision-capable model ID is explicitly selected by the operator.
export EVIDENCETWIN_PROVIDER=ollama
export EVIDENCETWIN_MODEL='your-vision-model-id'
# For local Ollama, use http://127.0.0.1:11434 (no key required).
export OLLAMA_HOST=https://ollama.com
# Set OLLAMA_API_KEY securely in the server environment for cloud access.
export EVIDENCETWIN_CORS_ORIGINS=http://127.0.0.1:5202,http://localhost:5202
.venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

In another terminal:

```sh
cd frontend
FLASK_DEV_ORIGIN=http://127.0.0.1:5000 VITE_API_BASE_URL=/api VITE_ANALYSIS_FIXTURES=false npm run dev -- --host 127.0.0.1 --port 5202 --strictPort
```

Open `http://127.0.0.1:5202/app`. No `.env` file is automatically read; export
variables through your shell/process manager. Keys belong exclusively in the
server environment. Never use `VITE_*` variables for credentials. Without a
configured provider/model, lists work and creation is truthfully disabled.
Configuration does not prove a provider account or selected model is accessible.
Provider errors remain failed review states, never successful scientific results.

The hardcoded credential discovered in `snippets/VA.py` was replaced by an
`OLLAMA_API_KEY` lookup. Rotate the previously exposed credential. The backend
never imports that script, runs pilot files automatically, or reads keys from it.

## Provider selection

`EVIDENCETWIN_PROVIDER` selects one provider for a backend instance, including all
its review roles. Each initial review is a separate conversation with the same
EvidencePacket and no other reviewer outputs. This is conversation isolation,
not independent scientific confirmation or necessarily different model families.

| Provider | Credential environment variable | Transport |
| --- | --- | --- |
| ollama | OLLAMA_API_KEY for cloud; optional locally | /api/chat |
| openai | OPENAI_API_KEY | Responses API; store=false |
| google | GEMINI_API_KEY or GOOGLE_API_KEY | generateContent |
| anthropic | ANTHROPIC_API_KEY | Messages API |
| openrouter | OPENROUTER_API_KEY | chat/completions |
| deepseek | DEEPSEEK_API_KEY | chat/completions |

All require `EVIDENCETWIN_MODEL`. No model catalog or guaranteed model
availability is invented. Select a model with image input support for charts.
Provider-specific URLs are fixed; only Ollama's origin is configurable. Credentials
are never put in URLs or API responses. HTTP redirects are refused. Generation
calls are not automatically retried, preventing silent duplicate billing.

Ollama local schema enforcement defaults on; cloud enforcement defaults off
because cloud structured outputs are not guaranteed. Both paths include the
schema in instructions and strictly validate the resulting JSON using Pydantic.
`OLLAMA_SCHEMA_MODE=1` explicitly enables the format parameter when supported.
Other provider adapters request JSON via instructions (plus Gemini JSON MIME).
Malformed, truncated, refused, unknown-reference or wrong-identity outputs fail.
No raw remote error bodies are logged or returned. Provider requests time out and
responses are bounded at 4 MiB. Numeric token usage is retained when supplied;
computational cost, accuracy and scientific confidence are never fabricated.

Official wire references checked during implementation:
[Ollama chat](https://docs.ollama.com/api/chat),
[Ollama structured outputs](https://docs.ollama.com/capabilities/structured-outputs),
[OpenAI Responses](https://platform.openai.com/docs/api-reference/responses),
[Gemini generateContent](https://ai.google.dev/api/generate-content),
[Claude vision](https://platform.claude.com/docs/en/build-with-claude/vision),
[OpenRouter chat](https://openrouter.ai/docs/api/api-reference/chat/send-chat-completion-request),
[DeepSeek vision](https://api-docs.deepseek.com/guides/vision/).

## Architecture and data ownership

- Existing domain Blueprints preserve the routes, method names and API prefixes.
- `services/runtime.py` handles validated HTTP input and application operations.
  `install_runtime` binds implemented handlers to the registered Blueprint
  endpoints; no alternate frontend or backend framework is added.
- `services/store.py` persists JSON records transactionally in SQLite, using only
  the Python standard library. Private uploads use generated opaque filenames.
- `services/workflow.py` owns bounded local execution, state transitions,
  cancellation, retries and honest report production.
- `services/provider.py` contains shared strict review/cross-review/judge schemas,
  reference checks and Ollama transport adapted from VA.py.
- `services/transports.py` contains the other providers adapted from all.py.
- `prompts/*.md` are unchanged copies of the owner's instructions. They are
  included in package builds. No generated alternative scientific prompts replace
  them; the adapter adds schema, evidence-scope and untrusted-input boundaries.
- `contracts/` retains the TypeScript-compatible request/response definitions.

Storage defaults to `backend/instance/` and is ignored by version control.
`EVIDENCETWIN_DATA_DIRECTORY` changes it. The directory contains
`workspace.sqlite3`, `uploads/<analysis-id>/<file-id>` and `worker.lock`.
SQLite records and uploaded files have private filesystem permissions.

**Run one backend application process per data directory.** A file lock rejects a
second worker, preventing duplicate recovery/execution. Request threads are
supported. A bounded ThreadPoolExecutor runs at most `EVIDENCETWIN_WORKERS` calls
concurrently (default 2); at most `EVIDENCETWIN_QUEUE_LIMIT` analyses are accepted
(default 16). This is a local worker, not a distributed/durable task broker.
Accepted records survive restarts; queued/running jobs become failed with an
interruption notice. No billable model call is silently replayed. Retry is explicit.
Cancellation immediately changes the record, but cannot revoke an already-sent
provider call. Attempt tokens prevent late outputs from overwriting cancellation
or retry state. Running analyses cannot be deleted; cancel first.

No authentication or multi-user isolation is invented. The existing
`AUTHENTICATE_REQUEST` callable remains the authentication/authorization boundary
for every non-public route, including uploaded file reads. It must return None
or raise Unauthorized/Forbidden. This is a local single-workspace backend until
the owner provides real account and per-record access control. Do not expose it
as a public multi-user service. Use a single-worker production WSGI server and
reverse proxy with owner authentication when deploying beyond localhost.

## Architecture V3 pipeline mapping

1. Controller accepts validated exploratory evidence and records missing inputs.
2. Source verification: unavailable; URLs are never fetched by this implementation.
3. Dataset validation: only CSV shape/encoding/transport checks are implemented.
4. Statistical checks: unavailable; no p-values or significance inferred.
5. Evidence contract: supplied inputs, hashes, constraints and missing services.
   No input record is mislabeled source-verified.
6. Blind Optics / Neutral Twin: unavailable; original assets remain immutable.
7. Focused mode runs the Visual Analyst. Council mode runs all four isolated
   reviewers sequentially; all completed initial outputs remain separately stored.
8. Cross-review runs only after all four initial responses pass validation.
9. Evidence Judge runs only after cross-review passes validation. Its verdict is
   stored as unverified model adjudication in its structured report.
10. The final audit report includes only actually executed reviews and limitations.
    Partial review failures are retained and prevent unearned completion claims.

The verified path stays disabled until the owner supplies the Scientific Core,
evidence sufficiency policy, provenance rules and neutralization procedure.
Missing inputs never turn into made-up evidence. The Counterfactual Analyst
receives explicit missing-twin information rather than a guessed replacement.

## Input and upload policy

Creation accepts multipart `metadata` JSON matching `AnalysisCreateMetadata` and
repeated `files` parts. Claims are explicit and nonblank; the primary claim must
match the first claims entry. Up to 10 distinct claims are supported. Only
exploratory mode is accepted. No evidence means validation fails unless a named,
explicit illustrative case was selected. Submitted source URLs are HTTP(S)
metadata without embedded credentials, not fetch instructions.

Files: at most 10 files, 20 MiB per file, 5 images; total request default 64 MiB.
PNG/JPEG/WebP are decoded/verified using Pillow; extension and decoded media type
must agree. Pixel counts above 16 million and decompression bombs are rejected.
CSV is UTF-8, at most one CSV or structured JSON dataset per analysis, 5,000 data rows, 100 unique nonblank columns,
consistent row widths and bounded cell sizes. Values remain supplied strings;
no numeric imputation occurs. Structured JSON accepts an object with columns/rows and optional variables/notes matching the Dataset contract; no user-supplied pagination metadata is accepted. PDFs must have a PDF signature; they are retained
but not parsed or sent as text evidence. This limitation is disclosed to models.
Duplicate bytes are rejected. All files are SHA-256 hashed.

Review context includes at most 200 supplied dataset rows and explicitly records
truncation and totalRows. Complete accepted rows remain accessible in the paged
inspector. Context above 150,000 JSON characters is rejected. Images are mapped
explicitly to evidence IDs and filenames. Originals are served through a
record-aware authenticated route with nosniff; documents download as attachments.
No public static upload directory, SVG/script uploads, arbitrary file paths or
remote URL downloads are introduced.

## Endpoint handoff

Typed schemas are in `backend/evidencetwin_backend/contracts/`. Original precise
frontend expectations remain in `docs/FRONTEND_API_CONTRACT.md`. Skeleton-only
per-function contracts are archived in `docs/BACKEND_SKELETON_REFERENCE.md` and
are historical, not the current availability list.

All paths below are under `/api`. Runtime implementations use the named method
in `Runtime` unless noted; the matching Blueprint function retains the same name.

| Blueprint | Method and route | Python function | Input → output | Runtime / frontend consumer |
| --- | --- | --- | --- | --- |
| system | GET /health | health | none → HealthResponse | Real liveness; connection badge |
| system | GET /capabilities | capabilities | none → CapabilitiesResponse | Actual configured capabilities; all capability hooks |
| system | GET /activity | list_activity | ActivityQuery → ActivityResponse | Real saved events; dashboard |
| analyses | POST /analyses | create_analysis | multipart AnalysisCreateMetadata + files → AcceptedID, 202 | Real acceptance/queue; builder |
| analyses | GET /analyses | list_analyses | AnalysisListQuery → AnalysisList | Persistent records; dashboard/history/selectors |
| analyses | GET /analyses/{id} | get_analysis | path ID → Analysis | Exact record/current state; polling |
| analyses | DELETE /analyses/{id} | delete_analysis | path ID → 204 | Confirmed record/upload deletion; history |
| analyses | POST /analyses/{id}/retry | retry_analysis | path ID → {}, 202 | Failed/cancelled only; history/workspace |
| analyses | POST /analyses/{id}/cancel | cancel_analysis | path ID → {}, 202 | Queued/running only; processing |
| evidence | GET /analyses/{id}/evidence | get_analysis_evidence | path ID → SectionResponse | Supplied evidence/provenance; inspector |
| evidence | GET /analyses/{id}/dataset | get_analysis_dataset | DatasetQuery → Dataset | Search/sort/25-row pages; dataset viewer |
| evidence | GET /analyses/{id}/files/{file_id} | file_asset | two path IDs → original bytes | Authorized image/document asset |
| visualizations | GET /analyses/{id}/visualizations | get_analysis_visualizations | path ID → SectionResponse | Original + explicit unavailable twin; lab |
| council | GET /analyses/{id}/council | get_analysis_council | path ID → SectionResponse | Actual reviews/disagreements; Council |
| audit | GET /analyses/{id}/audit | list_analysis_audit | path ID → SectionResponse | Actual timestamps/events; audit |
| reports | GET /analyses/{id}/report | get_analysis_report | path ID → SectionResponse | Real exploratory report or 404 |
| reports | GET /reports | list_reports | ReportListQuery → ReportList | Search/date/mode/status/paging; report library |
| reports | GET /reports/{id} | get_report | report ID (= analysis ID) → SectionResponse | Full saved report |
| reports | DELETE /reports/{id} | delete_report | report ID → 204 | Deletes report, preserves analysis/evidence |
| comparisons | GET /comparisons | compare_analyses | ComparisonQuery → ComparisonResponse | Descriptive metadata; comparability unknown |
| benchmarks | GET /benchmarks | list_benchmarks | BenchmarkListQuery → BenchmarkList | Actual stored records; initially empty |
| benchmarks | POST /benchmarks | create_benchmark | BenchmarkCreate → 501 | Evaluator unspecified; no fake run accepted |
| benchmarks | GET /benchmarks/{id} | get_benchmark | path ID → BenchmarkResponse / 404 | Saved records only; no fabricated metrics |
| integrations | GET /integrations | list_integrations | none → IntegrationList | API/configured provider/planned MCP/Skills |
| integrations | POST /integrations/{id}/test | test_integration | ID → IntegrationTestResponse / 501 | API liveness, Ollama catalog probe; no paid generation probe |
| cases | GET /cases | list_research_cases | none → {items: authored cases} | Explicit sample catalog; frontend still has local case content |
| cases | GET /cases/{id} | get_research_case | ID → authored sample case | Reserved catalog interface; clearly sample=true |

No `/status`, SSE, MCP, fake sign-in or undeclared provider-secret endpoint is
introduced. React polls the existing analysis record. `a`/`b` are browser page URL
parameters; the existing HTTP comparison contract remains `analysisA`/`analysisB`.

HTTP errors are consistent `{error:{code,message,operation?}}`: 400 malformed
transport, 401/403 auth, 404 absent record, 409 state conflict, 413 request limits,
415 unsupported type, 422 invalid metadata/files/query, 501 unsupported scientific
operation, 503 unconfigured provider/full queue, and 500 sanitized internal errors.
Provider failures after acceptance are saved failed review/job states. API success
means the stated application operation occurred, never independent verification.

## Environment and integration

| Variable | Default / meaning |
| --- | --- |
| EVIDENCETWIN_RUNTIME | 1; set 0 for original contract-only skeleton, all domain routes 501 |
| EVIDENCETWIN_PROVIDER | ollama; one of the six providers above |
| EVIDENCETWIN_MODEL | empty; operator-selected vision model ID |
| OLLAMA_HOST | https://ollama.com; credential-free origin; remote HTTP disallowed |
| OLLAMA_SCHEMA_MODE | local 1 / cloud 0; explicit format support |
| EVIDENCETWIN_PROVIDER_TIMEOUT | 180 seconds per provider call |
| EVIDENCETWIN_DATA_DIRECTORY | backend/instance |
| EVIDENCETWIN_WORKERS | 2, local worker threads |
| EVIDENCETWIN_QUEUE_LIMIT | 16 accepted outstanding analyses |
| EVIDENCETWIN_CORS_ORIGINS | empty; exact comma-separated origins |
| EVIDENCETWIN_MAX_CONTENT_LENGTH | 67108864 bytes |
| EVIDENCETWIN_MAX_FORM_MEMORY_SIZE | 524288 bytes for multipart text fields |
| EVIDENCETWIN_MAX_FORM_PARTS | 32 |

CORS does not allow cookies by default. OPTIONS negotiates methods only. Browser
POST/DELETE requests carrying an Origin must match the backend origin or an
explicitly allowed frontend origin; configure the Vite origin even when using a
proxy (Vite changes the upstream Host). CLI requests without Origin still work.
Authentication remains a separate owner-controlled hook. Credentialed cross-origin
sessions require deliberate future cookie/CSRF/CORS design; never just wildcard
origins. Production should forward `/api` to Flask and use the existing SPA fallback
for other deep links. Generated file URLs are same-origin `/api` paths.

## Verification

```sh
cd backend
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
.venv/bin/python -m compileall -q evidencetwin_backend
.venv/bin/python -m evidencetwin_backend.export_contracts --output /tmp/evidencetwin-contracts
```

The original structural/contract/CORS tests explicitly select skeleton mode.
New runtime tests select runtime mode and temporary storage. Provider tests mock
remote transport and exercise all six wire adapters. Workflow tests use an explicit
synthetic test provider, verify isolation/order/reference integrity, partial
failures, retries, cancellation, queue limits, uploads, assets, persistence,
restart recovery, reports, filters and comparison. A real HTTP bridge loads the
unchanged TypeScript adapters and validates actual Flask runtime responses.
These tests do not establish live provider account access or scientific accuracy.
No scientific sample findings are served by production endpoints.

## Owner implementation checklist

- [x] Local persistence and upload handling.
- [x] Actual bounded jobs and recoverable states.
- [x] Six configurable provider adapters and packaged owner prompts.
- [x] Isolated review, cross-review, judge, audit and exploratory reports.
- [x] Strict model schemas, ID and evidence-reference integrity checks.
- [x] Existing frontend contract parsing through actual HTTP.
- [ ] Supply Scientific Core and source authenticity/provenance policy.
- [ ] Specify evidence sufficiency and missing-evidence collection for verified mode.
- [ ] Specify deterministic calculations/statistical checks and assumptions.
- [ ] Specify Blind Optics/Neutral Twin transformations and asset provenance.
- [ ] Specify benchmark gold labels, scoring rubric, controls and evaluation runner.
- [ ] Provide real account authentication and per-record authorization for multi-user use.
- [ ] Supply MCP/Skills server implementation and approved installation guidance.
- [ ] Validate chosen provider/model access with rotated server-side credentials.

Enable verified capabilities only after the corresponding services and scientific
checks are implemented and tested. Keep deterministic/source-backed findings in
separate contract fields from model interpretation. Never enable a flag simply
because a route is registered or several models agree.

Latest executed verification: **182 backend tests**, **36 frontend tests**, lint,
production build, Python compile/dependency checks, schema export, package build
and a live Flask/Vite browser inspection passed. Provider calls were mocked for
regression tests; no live model account/scientific validation is claimed. See
[the verification report](docs/BACKEND_RUNTIME_VERIFICATION.md) for scope and
screenshots.


## Isolated execution infrastructure completion report

Completed 2026-11-06 under the explicit authorization to implement the exact Coding Readiness Report inventory. **All 24 design/enablement/pilot gates remain OPEN.** The policy/design status remains Recommended for owner approval where applicable. Infrastructure test success does not close any scientific or hosted-pilot gate.

### Delivered scope

Created all **28 approved files** and modified only the **five approved existing files**. No extra application source/configuration file was introduced. Git metadata was initialized separately for the additionally requested private repository: [AbdulrahmanAhmedGit/EvidenceTwin](https://github.com/AbdulrahmanAhmedGit/EvidenceTwin). Its visibility was verified PRIVATE. Git metadata exclusions keep environments, instance data, uploads, databases, caches, snippets and downloaded research snapshots out of the source commit. Repository creation/push is not deployment.

The 28 files comprise eleven import-safe execution modules, four explicit Alembic/configuration files, one opt-in disposable test profile and twelve test/helper files. Modified files: backend/pyproject.toml, backend/requirements.lock, backend/README.md, docs/INTEGRATION_GUIDE.md and this guide. The exact source inventory matches the approved report. No existing source was deleted.

- Core metadata contains all 16 execution tables and reviewed constraints/indexes. Immutable migration DDL is readable and frozen independently from mutable application metadata.
- Repository implements durable atomic submission/claim, conservative fair FIFO dispatch, scoped idempotency, whole-record paired validation, pinned guards, current-authority read/replay checks, database-time heartbeat and conditional publication.
- Recovery implements all planned lifecycle edges: bounded replacement attempts, expiry retirement, pending/running cancellation, controller finalization, scheduling stop, uncertain external operation records, safe settlement and retained reservations.
- Shared capacity is database-controlled across processes for analyses, per-analysis LLM calls, global calls and provider scope. There are no process-local semaphore substitutes.
- Worker/Supervisor support explicitly configured trusted single-process tasks, child termination/reaping, polling and heartbeat reconciliation. They do not import arbitrary task code from CLI. The installed CLI fails closed with exit 2 when adapters/tasks are unavailable.
- Production authorizer, validator, artifact, spending and settlement adapters are unavailable by default. Test doubles are confined to tests/execution. No scientific or paid-provider task was registered.

### Actual environment and verification

Python **3.14.4**, PostgreSQL **18.6**, SQLAlchemy **2.1.8**, Psycopg/psycopg-binary **3.3.8**, Alembic **1.20.1**, Mako **1.4.3**, existing Flask **3.1.3** and pytest **9.2.0**. Required dependencies were installed into the existing backend virtual environment; the exact tested set is locked. The editable package/worker entry point was installed. `pip check` reports no broken requirements. Python compilation checks passed for execution code, migrations and tests.

Final full-suite command: backend/.venv/bin/python -m pytest backend/tests -q, with an explicit ET_EXECUTION_TEST_CLUSTER_DSN referencing the newly created private disposable cluster. Result: **351 passed, zero failures, zero errors, zero skips, 26.46 seconds**. Of these, **147 are new execution tests**, including parametrized transition checks; all **204 pre-existing backend tests** passed unchanged. These counts are not independent scientific acceptance cases or measured production reliability.

Migrations were executed exclusively against unique disposable et_test_* databases. Tested actual upgrade, repeat upgrade, downgrade/re-upgrade, Core metadata/column/constraint/index fidelity and DML-role privilege restrictions. The initial server run exposed Alembic's version-table search-path issue; version tracking is now explicitly public while execution tables remain qualified et_execution, and migration regression tests pass.

Tests used independent spawned Python processes and fresh database connections for competing claims, global capacity and provider reservations, cancellation/publication and claim/cancellation races, and competing recovery controllers. A real PostgreSQL deadlock exercised automatic bounded database-only retry. A terminated backend connection exercised indeterminate connection handling. Heartbeat/final-ack loss and audit-failure tests are explicitly controlled fault injections, not proof of real-provider delivery semantics.

Actual child task process termination/reaping was tested, plus heartbeat operation-key reconciliation, two missed heartbeats, monotonic fence rejection, persisted retry deadlines, permanent-failure no-retry behavior and provider Retry-After precedence. Private test pg_dump/pg_restore verified restored snapshot hashes and owner references. This is not a production DB/object-storage recovery acceptance result.

### EX specification traceability and evidence limits

| Specifications | Implemented evidence | Boundary |
| --- | --- | --- |
| EX01–EX04 | Schema migration/replay/downgrade, static metadata fidelity, bad row checks, composite FKs and one executable attempt. | No production schema migration. |
| EX05–EX07 | Injected precommit rollback, equivalent submission, changed-command conflict and no duplicate row. | Fault injection is controlled. |
| EX08–EX09 | All Job source/destination pairs, 19 approved event/actor rows and paired candidate rejection. | Not a scientific verdict matrix. |
| EX10–EX13 | Independent-process claim ownership, two-analysis cap, third job persistence, per-account dispatch, locked FIFO head and admission bound. | Not representative-load latency/fairness SLA. |
| EX14–EX17 | Actual child stop, guarded expiry/replacement, durable steps, explicit dependency reuse, fencing and time sampling after lock wait. | Remote host/process isolation is not provided. |
| EX18–EX20 | Stored heartbeat acknowledgement replay, unknown-ack reconciliation, configured missed threshold, stale success/failure/output rejection. | Some network/ack loss is modeled injection. |
| EX21–EX24 | Real process publication/cancellation, pending claim/cancel and recovery-controller races; finalization without worker acknowledgement. | Logical cancellation does not cancel a remote request. |
| EX25–EX28 | Three total execution attempts, stored jitter/deadline/Retry-After, permanent no-retry, actual deadlock, bounded exhaustion, connection termination, pool/statement timeout. | OS/network commit completion is not guaranteed by a timeout. |
| EX29–EX33 | Modeled dispatch intent, real cross-process request-reservation limits, uncertain permit retention, authorized replacement bounds, late settlement and idempotent release. | No paid request sent; no real provider settlement tested. |
| EX34–EX37 | Pinned policy/snapshot identity, malformed guard kind, revocation during validation, staged artifact/deletion/missing-object rejection and full payload validation. | Scientific eligibility is fail-closed adapter responsibility; no scientific check is implemented. |
| EX38–EX41 | Default adapter unavailable, non-enumerating ownership checks, revoked replay denial, missing artifact publication refusal and canonical bounds. | Export/download HTTP paths are deliberately not wired. |
| EX42–EX45 | Safe audit-failure uncertainty, restricted runtime role, unchanged full legacy suite and Core/Read Committed/timeout inspection. | Complete infrastructure outage and hosted authorization acceptance remain open. |
| EX46 | Actual disposable PostgreSQL backup/restore preserves manifest hash and ownership. | No real object-store restoration, retention/deletion reconciliation, RPO/RTO or P05 acceptance. |

The 46 design rows have infrastructure evidence or an explicit boundary above. Do not count this as execution of the separate 150 overlapping scientific contract specifications. No scientific reference corpus or Ember scientific acceptance case was run.

### Operation, safety and recovery contracts

Database-only retries: three total executions for known rolled-back 40P01/40001; full-jitter 50/100 ms bounds (200 ms cap); fresh guards and same immutable operation identity. Heartbeats execute once per operation and reconcile the same key after uncertainty. Connection/COMMIT ambiguity does not blindly replay work. Lock/contention, permanent schema/configuration failures and key conflicts are distinguished. A two-second command budget combines client deadline checks and configured pool/server/connect limits; it is not a hard real-network completion guarantee. Query/connection exceptions are normalized to safe codes and do not return raw SQL or credentials.

Execution defaults remain lease 30 s, heartbeat 5 s, heartbeat deadline 2 s, two missed heartbeats, default poll 2 s within the approved 1–3-second range, three total execution attempts, base 2 s/cap 15 s/full jitter. New conservative admission limits 16 outstanding jobs globally/four per account are development settings; retries retain the original admitted job identity. Provider retry not-before dates may extend beyond local jitter cap and are persisted once. Every retry requires an explicit eligible failure cause; a permanent/input/configuration failure is not retried merely because a Boolean requested it.

Current queued/job/attempt state, exact owner/epoch/lease/version, immutable manifest and policy/configuration guards are enforced on writes. Equivalent successful replay is resolved before fresh-worker guards, after current response authorization; account revocation therefore also blocks historical replay access. Publication preparation/validation/readiness occurs outside transactions and is rebound to locked current guards. Conflicting/rejected operations have safe audit attempts without overwriting an accepted operation. Audit persistence is explicitly uncertain when the database is unavailable.

Accepted completed steps remain durable. Reuse is limited to the same authorized job/snapshot with exact dependency binding and immutable source output. No automatic cross-job reuse, source substitution or model fallback exists. Artifacts are accepted only by committed relations; physical existence or a hash alone never establishes scientific truth or source authenticity.

Analysis capacity releases only with accepted stop proof. A final logical workflow may conservatively retain its reservation without such proof. Remote/unknown process loss and unresolved provider calls keep their respective permits. Known same-host child exit does not prove external settlement. Trusted first-increment tasks are single-process; arbitrary descendant spawning/escape and remote host failover require a later isolation/termination adapter. No production task is enabled that relies on unproven process-tree isolation.

### Startup and interfaces

See backend/README.md for explicit setup/test-cluster instructions. PostgreSQL was launched in a newly created private temporary directory, with a private Unix socket and TCP disabled; no system service was started/restarted or reconfigured. Fixtures create their own database/role per test and remove them. Alembic env refuses non-disposable names/destinations. A Compose test profile is supplied but was not executed because the native PostgreSQL route was used; image-digest pinning/that route's execution remain explicit follow-up verification before adopting it.

The existing Flask application, local SQLite data, uploads, AI settings, provider transports/prompts, frontend routes and scientific logic remain untouched. The new worker is not silently installed into the Flask request lifecycle. No new public API/authentication flow was added. The owner must connect reviewed trusted adapters and versioned API DTOs under a separate integration scope.

### Remaining integration and pilot gates

- Real external identity/session/invitation integration and researcher-owned case access, including current guard synchronization.
- Versioned claim/classification/evidence/source snapshots, researcher confirmation and Scientific Core validation; Partially Supported remains unresolved.
- Real private-object storage/readiness/deletion/authorized download and reproducibility export adapters.
- Actual provider dispatch, per-role configuration, consent, budgets, rate limits, usage/settlement/cancellation evidence and prompt/protocol acceptance.
- Hosted worker isolation/termination, production queue/admission/timeouts, workload/load/cost evaluation and failure alerts.
- Data retention, source redistribution rights, backup restoration/deletion ledger, RPO/RTO and legacy ownership/import/cutover.
- Full `/api/v1/` bridge and frontend end-to-end integration; benchmark/MCP/scientific capability enablement remain excluded.

These are explicit unavailable integration boundaries, not substituted successes. No cloud deployment, existing-data migration, paid provider call or scientific capability enablement occurred. All 24 gates remain OPEN after implementation. Request a separate scope before connecting hosted users, real provider/scientific workflows or migrating real data.
