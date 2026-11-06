> Historical November 3 skeleton reference. Current runtime behavior and availability are documented in [the backend guide](../BACKEND_IMPLEMENTATION_GUIDE.md).

# EvidenceTwin — Backend Implementation Guide

This is a runnable **Flask integration skeleton**, not a scientific implementation.
The owner implements every scientific/business operation independently. No existing
Python backend or scientific files were present when this skeleton was prepared.
No frontend source, API adapters, Zod schemas or dependencies were changed.

## Current status and ownership

- Real: application factory, 11 explicit domain Blueprints, liveness/API-version
  metadata, truthful disabled capabilities, JSON errors, exact-origin development
  CORS, transport limits, an optional owner authentication hook, typed wire DTOs,
  schema export and structural tests.
- Unimplemented: all analysis creation/retrieval/deletion/retry/cancellation,
  scientific evidence/source checks, calculations, datasets, visualizations,
  Council/cross-review/judging, audit retrieval, reports, comparisons, evaluations,
  real integration connections and case-catalog retrieval. These return **HTTP 501**.
- No database, persistence schema, queue, scientific algorithm, model provider,
  background job, authentication system, MCP server or fake research output is
  included. Services/ is the empty owner implementation boundary.
- There are **24 current frontend method/route operations**, plus **two explicitly
  reserved case-catalog routes**. Only GET health and capabilities return actual
  success payloads. OPTIONS/HEAD use normal HTTP semantics, not fabricated jobs.

## Install, test and run

Python 3.14 was used for validation. The package requires Python 3.12 or newer with
compatible dependency wheels. Install into the project virtual environment:

```sh
cd backend
python3.14 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pytest -q
.venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

`requirements.lock` records the tested runtime/test dependency versions;
`requirements-dev.txt` installs those versions and the editable package.
`pyproject.toml` declares the small runtime dependency set (Flask, Flask-Cors and
Pydantic) and optional test tooling. No global Python environment is modified.

Health should return HTTP 200 with status=ok, apiVersion=0.1.0,
mode=integration_skeleton, scientificServices=unavailable. This proves Flask
liveness only. GET /api/analyses should return HTTP 501 with the error below.
Use a production WSGI server/reverse proxy selected by the owner for deployment;
the development server is not a deployment solution. Keep debugging off outside
local development.

## Folder map

```text
backend/
  evidencetwin_backend/
    __init__.py              create_app(config=None)
    config.py                environment/transport/CORS settings
    errors.py                consistent JSON error helpers and handlers
    catalog.py               endpoint handoff/test inventory, no route dispatcher
    blueprints/              explicit named transport handlers
    contracts/               typed request/response DTOs and named schema registry
    export_contracts.py      JSON Schema export, no runtime data
    services/                owner business/Scientific Core boundary; no services yet
  tests/                     structural, contract, CORS and frontend-adapter tests
  pyproject.toml
  requirements.lock
  requirements-dev.txt
  .env.example
```

The factory creates no global database/job client and performs no provider calls.
Every domain handler is a plain named Python function, with actionable OWNER TODOs
covering responsibility, input, output, service module and frontend consumer.
Blueprints parse/serialize transport when implemented; owner services own business
rules and invoke the owner's Scientific Core. The service module names in TODOs
are implementation locations to create, not already operational adapters.

## Source of truth and wire contracts

The inspected sources are:

- [FRONTEND_API_CONTRACT.md](FRONTEND_API_CONTRACT.md).
- `frontend/src/api.ts`, `workspace-api.ts`, `research-api.ts`.
- `frontend/src/features/research/api.ts` and research hooks.
- AnalysisBuilder, AnalysisWorkspace, EvidenceInspector, workspace/report/
  benchmark/integration flows and the actual local case-library content.

DTOs use strict Pydantic-backed TypedDicts. CamelCase fields match the wire format;
NotRequired means omission is permitted, not that null is permitted. Required
nullable values such as comparison a/b and metric value retain explicit nulls.
No default verdicts, calculated values, source verification or execution flags are
injected. Unknown fields are rejected by the owner validation helper rather than
silently persisted. This is intentionally stricter than Zod's unknown-key stripping.

| Contract module | Principal request/response definitions |
| --- | --- |
| contracts/system.py | HealthResponse, CapabilitiesResponse, ActivityResponse |
| contracts/analyses.py | AnalysisCreateMetadata, AcceptedID, Analysis, AnalysisList, ActionAcknowledgement |
| contracts/inspection.py | SectionResponse, Dataset, Source, Visualization, Reviewer, Disagreement, AuditEvent, ReportSection |
| contracts/research.py | BenchmarkCreate, BenchmarkList, BenchmarkResponse, Metric, ComparisonResponse, ReportList, IntegrationList, IntegrationTestResponse |
| contracts/queries.py | AnalysisListQuery, DatasetQuery, ComparisonQuery, BenchmarkListQuery, ReportListQuery, ActivityQuery |
| contracts/common.py | enums, timestamps, safe links, pagination, JSON types, validate_contract |
| errors.py | ErrorResponse / ErrorDetail |

Export machine-readable definitions without starting Flask or exposing data:

```sh
cd backend
.venv/bin/python -m evidencetwin_backend.export_contracts --output /tmp/evidencetwin-contracts
```

Use `validate_contract(Schema, payload)` before returning an owner-produced JSON
payload. Pure input-shape validation is supported, including numeric query strings,
ISO dates, dataset column alignment and the frontend's metric denominator bounds.
It does **not** verify provenance, statistical significance, scientific correctness,
independent execution, causal inference or whether a measurement was actually made.
All those remain owner logic. Opaque study/contract/report JSON must already be
sanitized and authorized before it reaches the browser; frontend redaction is not
server isolation.

Until implementation, domain stubs deliberately do not parse or accept business
payloads: even a malformed JSON body normally receives 501 because the operation
is unavailable. Global transport limits/authentication errors take precedence.
When implementing, parse the expected media type, map malformed syntax to 400,
unsupported media to 415 and invalid request fields to 422 using the same JSON
error helper. Do not return 200 empty objects/lists merely to quiet frontend errors.

## Consistent errors and HTTP methods

```json
{
  "error": {
    "code": "not_implemented",
    "message": "Create analysis is not implemented yet.",
    "operation": "analyses.create_analysis"
  }
}
```

`operation` is included for a matched handler and omitted for an unknown route.
Error codes currently include not_implemented (501), bad_request (400),
authorization_required (401), access_denied (403), not_found (404),
method_not_allowed (405), request_too_large (413), unsupported_media_type (415),
invalid_request (422) and internal_error (500). Exceptions/invalid payload contents
are not echoed. Unexpected failures log only their exception type, not raw private
provider errors. Preserve Allow headers on 405. Replies are JSON with no-store
and nosniff headers.

GET routes automatically support HEAD (same status, no body). OPTIONS returns
normal method-negotiation metadata with an empty body; it does not run the domain
handler. Both /api/analyses and its trailing-slash form resolve without a redirect.
The API never falls back to React's index.html. Unknown API paths return JSON 404.

## Connect the unchanged React frontend

Preferred development setup: keep React requests same-origin through its existing
Vite proxy. In a second terminal, from the repository root:

```sh
cd frontend
FLASK_DEV_ORIGIN=http://127.0.0.1:5000 npm run dev
```

Keep VITE_API_BASE_URL=/api (the default) and VITE_ANALYSIS_FIXTURES unset/false.
No frontend file edits are needed. Production needs the owner's existing web
server to forward /api to Flask and serve SPA deep links separately; Flask does
not serve a second frontend.

An alternative cross-origin development setup uses
VITE_API_BASE_URL=http://127.0.0.1:5000/api plus an explicit backend CORS allowlist.
React currently uses credentials=same-origin; cross-origin cookies are therefore
not sent. No fake authentication or automatic credential fallback is included.

Expected live UI state: Backend reachable; scientific services unavailable;
submission/comparison capabilities disabled; research-list reads produce their
unavailable/error states rather than fabricated empty records. Health, service
support and an implemented scientific operation are intentionally distinct.

## Configuration and CORS

`.env.example` is a documented template, not an automatically executed/loaded file.
Export variables through the shell or deployment configuration:

| Environment variable | Default | Purpose |
| --- | --- | --- |
| EVIDENCETWIN_CORS_ORIGINS | empty | Comma-separated exact HTTP(S) frontend origins; no paths, credentials or wildcards |
| EVIDENCETWIN_MAX_CONTENT_LENGTH | 67108864 (64 MiB) | Whole-request transport size, including multipart overhead |
| EVIDENCETWIN_MAX_FORM_MEMORY_SIZE | 524288 (512 KiB) | Non-file multipart field limit when parsed |
| EVIDENCETWIN_MAX_FORM_PARTS | 32 | Multipart parser part-count limit |

Limits must be positive integers. CORS is disabled by default; with the Vite proxy,
it is unnecessary. For direct cross-origin development, for example:

```sh
EVIDENCETWIN_CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173   .venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5000
```

Origins are validated then regex-escaped/anchored for exact matching, including
IPv6 origins. Allowed CORS methods are GET/HEAD/POST/DELETE/OPTIONS; Content-Type
and Authorization are allowed request headers. Disallowed origins receive no CORS
access header. Credentials remain disabled. CORS is a browser policy, not server
access control. Preflight OPTIONS does not require an authentication hook.
Do not enable wildcard credentials or reflect arbitrary origins.

## Authentication extension point

`create_app({"AUTHENTICATE_REQUEST": owner_callable})` accepts an owner authenticator.
It must return None only when the request can proceed, or raise Werkzeug
Unauthorized/Forbidden. It may attach a genuinely verified principal to Flask g.
Invalid return values fail closed with an internal error. The default is None,
meaning no authenticator is configured; all domain operations still return 501.
No user/session/principal/token is fabricated. Health/capabilities remain minimal
public metadata and OPTIONS remains available for preflight.

Before implementing protected data or mutations, supply real authentication and
resource authorization. Per-record capabilities/permissions are UI hints, not
authorization enforcement. Cookie sessions, CSRF, bearer-token adapters and any
credentialed cross-origin policy must be designed together by the owner, including
any necessary future frontend auth adapter. No server secret/provider key belongs
in React or public capability/integration metadata.

## Upload integration point

POST /api/analyses receives multipart/form-data with exactly the established
`metadata` JSON text field and repeated `files` file parts. The metadata model
contains source, url, studyDate, studyDesign, population, uncertainty, context,
claims[], legacy first claim, mode, reviewDepth and optional caseId. The frontend
selects PNG/JPEG/WebP/CSV/JSON/PDF files, checks a 20 MiB per-file limit, and does
not upload anything before server submission. Optional file parts are possible for
an authored local case reference; the backend must resolve permitted references.

No file is accepted, inspected, persisted or made public by this skeleton.
The owner must implement content/MIME and size checks, duplicate handling, source
eligibility, authorization, safe storage/quarantine outside the public web root,
filename handling, access-controlled asset retrieval and cleanup policy. File
extensions, user-declared study design and a source URL do not prove authenticity.
Do not blindly fetch source URLs or trust user filenames. No storage technology
or asset-serving route is selected here.

64 MiB is a request transport budget, not a promise to accept that much evidence;
32 parts includes metadata plus file parts. Tune proxy/server and Flask limits
together with the eventual owner upload policy. Declared oversize bodies are
rejected before stub execution. Flask's stream/multipart limits apply when owner
handlers parse a body; servers/proxies must also bound unknown-length/chunked input.
Unsupported operations never read an unbounded body just to simulate an upload.

## Scientific Core and capabilities handoff

Replace one stub at a time with calls to owner modules under services/. Connect
the Scientific Core there; this skeleton prescribes no scientific architecture,
LLM provider, database or task queue. Keep calculations, provenance decisions,
visual neutralization, Council execution, judging and benchmark scoring out of
HTTP handlers and contract validators.

Creation must return an actual accepted ID. Analysis/benchmark reads must return
exactly the requested ID; comparisons must echo both requested IDs. Use stable
URL-segment-safe IDs when implementing creation, since these are path parameters.
The frontend rejects identity mismatches before using scientific content/actions.
Route parsing is not a database or identifier-generation scheme.

The frontend reads /analyses/{id} while queued/running (normally every five seconds,
with backoff); it does not currently call /status or /events or use SSE. No unused
status/event stream or MCP endpoint was added. Inspection sections have the
existing common SectionResponse DTO; only return fields backed by actual data.
Standalone report preview uses the same section wire format.

Acknowledgement bodies have no currently enforced frontend fields: the
ActionAcknowledgement alias documents a JSON object without imposing an invented
success schema. Deletes can instead return confirmed HTTP 204. Acknowledgements
are not final scientific results; refresh the actual record state. Request timeouts
are 15 seconds for reads, 120 seconds for analysis acceptance and 30 seconds for
benchmark acceptance. Stopping a client wait cannot guarantee job cancellation;
provide owner idempotency/duplicate-submission policy before auto-retry is considered.

All scientific/research flags are explicitly false, available modes/review depths
are empty, providers are empty, activity is false, and job availability is
unavailable. Do not flip a flag because a Blueprint exists. After an operation is
implemented, authorized, schema-validated and tested against real behavior,
update blueprints/system.py to advertise only the corresponding actual support.
If the owner transitions out of skeleton mode, update the health metadata/HealthResponse DTO consistently; status=ok must continue to mean liveness rather than scientific correctness.
List reads may still be attempted by React when flags are false; 501 remains a
truthful unavailable state. Never return fake successful records to hide it.

Case routes are **reserved**: React currently imports local, visibly educational
case inputs and has no HTTP case-catalog adapter. No case-list/detail wire structure
was established by the current frontend. JsonObject is only an explicit pending
contract here; ratify a real Case DTO/frontend consumer before implementing or
enabling these routes. No educational fixture results are served by Flask.

## Endpoint inventory

All paths below are relative to the fixed /api prefix. Every handler's source
contains the owner TODO. Request/response names refer to the contract modules
above; the detailed frontend contract and exported JSON Schemas give the wire
fields. Optional fields remain absent when unknown rather than receiving guesses.

| Blueprint | Method | URL | Python function | Request | Expected success response | Current status |
| --- | --- | --- | --- | --- | --- | --- |
| system | GET | `/api/health` | `health` | No body | HealthResponse | 200 — real infrastructure |
| system | GET | `/api/capabilities` | `capabilities` | No body | CapabilitiesResponse | 200 — real infrastructure |
| system | GET | `/api/activity` | `list_activity` | ActivityQuery | ActivityResponse | 501 — owner TODO |
| analyses | POST | `/api/analyses` | `create_analysis` | multipart metadata: AnalysisCreateMetadata; repeated files parts | AcceptedID | 501 — owner TODO |
| analyses | GET | `/api/analyses` | `list_analyses` | AnalysisListQuery | AnalysisList | 501 — owner TODO |
| analyses | GET | `/api/analyses/<analysis_id>` | `get_analysis` | analysis_id path; no body | Analysis | 501 — owner TODO |
| analyses | DELETE | `/api/analyses/<analysis_id>` | `delete_analysis` | analysis_id path; no body | ActionAcknowledgement or HTTP 204 | 501 — owner TODO |
| analyses | POST | `/api/analyses/<analysis_id>/retry` | `retry_analysis` | analysis_id path; no body | ActionAcknowledgement | 501 — owner TODO |
| analyses | POST | `/api/analyses/<analysis_id>/cancel` | `cancel_analysis` | analysis_id path; no body | ActionAcknowledgement | 501 — owner TODO |
| evidence | GET | `/api/analyses/<analysis_id>/evidence` | `get_analysis_evidence` | analysis_id path; no body | SectionResponse (evidence fields) | 501 — owner TODO |
| evidence | GET | `/api/analyses/<analysis_id>/dataset` | `get_analysis_dataset` | analysis_id path; DatasetQuery | Dataset | 501 — owner TODO |
| visualizations | GET | `/api/analyses/<analysis_id>/visualizations` | `get_analysis_visualizations` | analysis_id path; no body | SectionResponse (visualizations/dataset fields) | 501 — owner TODO |
| council | GET | `/api/analyses/<analysis_id>/council` | `get_analysis_council` | analysis_id path; no body | SectionResponse (reviews/disagreements) | 501 — owner TODO |
| audit | GET | `/api/analyses/<analysis_id>/audit` | `list_analysis_audit` | analysis_id path; no body | SectionResponse (events) | 501 — owner TODO |
| reports | GET | `/api/analyses/<analysis_id>/report` | `get_analysis_report` | analysis_id path; no body | SectionResponse (report/sections) | 501 — owner TODO |
| comparisons | GET | `/api/comparisons` | `compare_analyses` | ComparisonQuery (analysisA/analysisB) | ComparisonResponse | 501 — owner TODO |
| benchmarks | POST | `/api/benchmarks` | `create_benchmark` | JSON BenchmarkCreate | AcceptedID | 501 — owner TODO |
| benchmarks | GET | `/api/benchmarks` | `list_benchmarks` | BenchmarkListQuery | BenchmarkList | 501 — owner TODO |
| benchmarks | GET | `/api/benchmarks/<benchmark_id>` | `get_benchmark` | benchmark_id path; no body | BenchmarkResponse | 501 — owner TODO |
| reports | GET | `/api/reports` | `list_reports` | ReportListQuery | ReportList | 501 — owner TODO |
| reports | GET | `/api/reports/<report_id>` | `get_report` | report_id path; no body | SectionResponse (report/sections) | 501 — owner TODO |
| reports | DELETE | `/api/reports/<report_id>` | `delete_report` | report_id path; no body | ActionAcknowledgement or HTTP 204 | 501 — owner TODO |
| integrations | GET | `/api/integrations` | `list_integrations` | No body | IntegrationList | 501 — owner TODO |
| integrations | POST | `/api/integrations/<integration_id>/test` | `test_integration` | integration_id path; no body | IntegrationTestResponse | 501 — owner TODO |
| cases | GET | `/api/cases` | `list_research_cases` | No body; query contract not yet defined | JsonObject (owner contract pending) | 501 — owner TODO (reserved) |
| cases | GET | `/api/cases/<case_id>` | `get_research_case` | case_id path; no body | JsonObject (owner contract pending) | 501 — owner TODO (reserved) |

## Per-endpoint owner handoff


### GET /api/health

- Blueprint/function: `system.health` in `backend/evidencetwin_backend/blueprints/system.py`.
- Expected input: No body.
- Expected success output: HealthResponse.
- Implementation status: implemented minimal infrastructure; no scientific execution.
- Frontend consumer: api.ts health; ConnectionBadge.
- Owner next step: Infrastructure liveness only.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/capabilities

- Blueprint/function: `system.capabilities` in `backend/evidencetwin_backend/blueprints/system.py`.
- Expected input: No body.
- Expected success output: CapabilitiesResponse.
- Implementation status: implemented minimal infrastructure; no scientific execution.
- Frontend consumer: workspace-api.ts / research hooks.
- Owner next step: Owner service availability mapping.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/activity

- Blueprint/function: `system.list_activity` in `backend/evidencetwin_backend/blueprints/system.py`.
- Expected input: ActivityQuery.
- Expected success output: ActivityResponse.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: workspace-api.ts getActivity.
- Owner next step: services.activity: authorized real activity records.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### POST /api/analyses

- Blueprint/function: `analyses.create_analysis` in `backend/evidencetwin_backend/blueprints/analyses.py`.
- Expected input: multipart metadata: AnalysisCreateMetadata; repeated files parts.
- Expected success output: AcceptedID.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: api.ts createAnalysis; AnalysisBuilder.
- Owner next step: services.analyses: validate supplied metadata/files; authorize storage and invoke owner verification workflow; return ID only after actual acceptance.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses

- Blueprint/function: `analyses.list_analyses` in `backend/evidencetwin_backend/blueprints/analyses.py`.
- Expected input: AnalysisListQuery.
- Expected success output: AnalysisList.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: workspace-api.ts getAnalyses; dashboard/history/compare selectors.
- Owner next step: services.analyses: authorized search/filter/sort and server pagination over real records.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>

- Blueprint/function: `analyses.get_analysis` in `backend/evidencetwin_backend/blueprints/analyses.py`.
- Expected input: analysis_id path; no body.
- Expected success output: Analysis.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readAnalysis; processing polling.
- Owner next step: services.analyses: retrieve authorized record and actual job state; return exactly the requested ID and no synthesized stages.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### DELETE /api/analyses/<analysis_id>

- Blueprint/function: `analyses.delete_analysis` in `backend/evidencetwin_backend/blueprints/analyses.py`.
- Expected input: analysis_id path; no body.
- Expected success output: ActionAcknowledgement or HTTP 204.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: workspace-api.ts deleteAnalysis; history confirmation.
- Owner next step: services.analyses: authorize deletion and owner-defined retention semantics; acknowledge only confirmed deletion.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### POST /api/analyses/<analysis_id>/retry

- Blueprint/function: `analyses.retry_analysis` in `backend/evidencetwin_backend/blueprints/analyses.py`.
- Expected input: analysis_id path; no body.
- Expected success output: ActionAcknowledgement.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: workspace-api.ts retryAnalysis; research-api.ts analysisAction.
- Owner next step: services.analyses: authorize retry, verify state/eligibility and request real owner job restart; return confirmed acknowledgement.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### POST /api/analyses/<analysis_id>/cancel

- Blueprint/function: `analyses.cancel_analysis` in `backend/evidencetwin_backend/blueprints/analyses.py`.
- Expected input: analysis_id path; no body.
- Expected success output: ActionAcknowledgement.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts analysisAction; confirmation dialog.
- Owner next step: services.analyses: authorize cancellation and connect actual job transport; acknowledge request, expose resulting state via record reads.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>/evidence

- Blueprint/function: `evidence.get_analysis_evidence` in `backend/evidencetwin_backend/blueprints/evidence.py`.
- Expected input: analysis_id path; no body.
- Expected success output: SectionResponse (evidence fields).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readAnalysisSection; EvidenceInspector.
- Owner next step: services.evidence: authorize access and map supplied/verified source, file, dataset and evidence-contract records; distinguish computed facts from source authentication.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>/dataset

- Blueprint/function: `evidence.get_analysis_dataset` in `backend/evidencetwin_backend/blueprints/evidence.py`.
- Expected input: analysis_id path; DatasetQuery.
- Expected success output: Dataset.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readDataset; DatasetViewer.
- Owner next step: services.evidence: apply authorized full-dataset search/sort and return the requested 25-row page with matching columns/page metadata; do not impute data.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>/visualizations

- Blueprint/function: `visualizations.get_analysis_visualizations` in `backend/evidencetwin_backend/blueprints/visualizations.py`.
- Expected input: analysis_id path; no body.
- Expected success output: SectionResponse (visualizations/dataset fields).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readAnalysisSection; VisualizationLab/overview.
- Owner next step: services.visualizations: map owner-generated immutable assets, rendering provenance and recorded controlled changes; serve only permitted assets and explicit missing-twin reasons.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>/council

- Blueprint/function: `council.get_analysis_council` in `backend/evidencetwin_backend/blueprints/council.py`.
- Expected input: analysis_id path; no body.
- Expected success output: SectionResponse (reviews/disagreements).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readAnalysisSection; CouncilView.
- Owner next step: services.council: map actual owner independent/cross-review/judge results, citations, execution isolation and unresolved disputes; never infer truth from agreement.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>/audit

- Blueprint/function: `audit.list_analysis_audit` in `backend/evidencetwin_backend/blueprints/audit.py`.
- Expected input: analysis_id path; no body.
- Expected success output: SectionResponse (events).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readAnalysisSection; AuditTrail.
- Owner next step: services.audit: authorize real chronological events with actual timestamps/references; sanitize secrets before any serialization or download.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/analyses/<analysis_id>/report

- Blueprint/function: `reports.get_analysis_report` in `backend/evidencetwin_backend/blueprints/reports.py`.
- Expected input: analysis_id path; no body.
- Expected success output: SectionResponse (report/sections).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: research-api.ts readAnalysisSection; ResearchReport.
- Owner next step: services.reports: retrieve an authorized real report with evidence-linked plain text and genuine references; expose actual JSON permission.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/comparisons

- Blueprint/function: `comparisons.compare_analyses` in `backend/evidencetwin_backend/blueprints/comparisons.py`.
- Expected input: ComparisonQuery (analysisA/analysisB).
- Expected success output: ComparisonResponse.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts readComparison; Comparison.
- Owner next step: services.comparisons: authorize both records and use owner comparability rules to return supplied dimensions/reasons with matching requested IDs; do not invent a winner.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### POST /api/benchmarks

- Blueprint/function: `benchmarks.create_benchmark` in `backend/evidencetwin_backend/blueprints/benchmarks.py`.
- Expected input: JSON BenchmarkCreate.
- Expected success output: AcceptedID.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts createBenchmark; BenchmarkBuilder.
- Owner next step: services.benchmarks: authorize and validate configuration/cases/model/rubric references; enforce owner control protocol and accept a real evaluation run; return its ID.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/benchmarks

- Blueprint/function: `benchmarks.list_benchmarks` in `backend/evidencetwin_backend/blueprints/benchmarks.py`.
- Expected input: BenchmarkListQuery.
- Expected success output: BenchmarkList.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts readBenchmarks; BenchmarkList.
- Owner next step: services.benchmarks: authorized paginated search/filter/sort over actual run metadata; do not produce synthetic metrics or progress.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/benchmarks/<benchmark_id>

- Blueprint/function: `benchmarks.get_benchmark` in `backend/evidencetwin_backend/blueprints/benchmarks.py`.
- Expected input: benchmark_id path; no body.
- Expected success output: BenchmarkResponse.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts readBenchmark; BenchmarkDetail polling.
- Owner next step: services.benchmarks: return the matching real run, configuration, actual measurements/denominators/failures and limitations; preserve unavailable metrics as null.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/reports

- Blueprint/function: `reports.list_reports` in `backend/evidencetwin_backend/blueprints/reports.py`.
- Expected input: ReportListQuery.
- Expected success output: ReportList.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts readReports; Reports library.
- Owner next step: services.reports: authorize search/date/status/mode/sort and pagination over reports that actually exist; report per-record permissions.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/reports/<report_id>

- Blueprint/function: `reports.get_report` in `backend/evidencetwin_backend/blueprints/reports.py`.
- Expected input: report_id path; no body.
- Expected success output: SectionResponse (report/sections).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts readReport; report preview/export.
- Owner next step: services.reports: retrieve the authorized report resource and actual export permission; reconcile report ID to its analysis without leaking another record.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### DELETE /api/reports/<report_id>

- Blueprint/function: `reports.delete_report` in `backend/evidencetwin_backend/blueprints/reports.py`.
- Expected input: report_id path; no body.
- Expected success output: ActionAcknowledgement or HTTP 204.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts deleteReport; Reports confirmation.
- Owner next step: services.reports: authorize and delete only the intended report using owner retention policy; do not assume associated analysis deletion.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/integrations

- Blueprint/function: `integrations.list_integrations` in `backend/evidencetwin_backend/blueprints/integrations.py`.
- Expected input: No body.
- Expected success output: IntegrationList.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts readIntegrations; workspace management.
- Owner next step: services.integrations: return only public, configured/planned availability metadata and real requirements/tool names; never expose keys, signed tokens or invented installation packages.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### POST /api/integrations/<integration_id>/test

- Blueprint/function: `integrations.test_integration` in `backend/evidencetwin_backend/blueprints/integrations.py`.
- Expected input: integration_id path; no body.
- Expected success output: IntegrationTestResponse.
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: features/research/api.ts testIntegration; integration test action.
- Owner next step: services.integrations: authorize a configured connection test and report real reachable/failed status and check timestamp; this is not scientific validation or an MCP server implementation.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/cases

- Blueprint/function: `cases.list_research_cases` in `backend/evidencetwin_backend/blueprints/cases.py`.
- Expected input: No body; query contract not yet defined.
- Expected success output: JsonObject (owner contract pending).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: Reserved: React currently uses content/cases.ts locally.
- Owner next step: services.cases: agree the catalogue DTO with the owner/frontend before implementing authorized real case retrieval; do not copy educational fixtures into fake live results.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.


### GET /api/cases/<case_id>

- Blueprint/function: `cases.get_research_case` in `backend/evidencetwin_backend/blueprints/cases.py`.
- Expected input: case_id path; no body.
- Expected success output: JsonObject (owner contract pending).
- Implementation status: unimplemented, HTTP 501.
- Frontend consumer: Reserved: React currently uses content/cases.ts locally.
- Owner next step: services.cases: agree the case DTO before implementing authorized real source/data/provenance retrieval; retain sample labels and unavailable uncertainty when appropriate.
- Contract reference: `docs/FRONTEND_API_CONTRACT.md`, matching files under `contracts/`, and `catalog.py`.

## Progressive implementation checklist

- [x] `GET /api/health` — `system.health`
- [x] `GET /api/capabilities` — `system.capabilities`
- [ ] `GET /api/activity` — `system.list_activity`
- [ ] `POST /api/analyses` — `analyses.create_analysis`
- [ ] `GET /api/analyses` — `analyses.list_analyses`
- [ ] `GET /api/analyses/<analysis_id>` — `analyses.get_analysis`
- [ ] `DELETE /api/analyses/<analysis_id>` — `analyses.delete_analysis`
- [ ] `POST /api/analyses/<analysis_id>/retry` — `analyses.retry_analysis`
- [ ] `POST /api/analyses/<analysis_id>/cancel` — `analyses.cancel_analysis`
- [ ] `GET /api/analyses/<analysis_id>/evidence` — `evidence.get_analysis_evidence`
- [ ] `GET /api/analyses/<analysis_id>/dataset` — `evidence.get_analysis_dataset`
- [ ] `GET /api/analyses/<analysis_id>/visualizations` — `visualizations.get_analysis_visualizations`
- [ ] `GET /api/analyses/<analysis_id>/council` — `council.get_analysis_council`
- [ ] `GET /api/analyses/<analysis_id>/audit` — `audit.list_analysis_audit`
- [ ] `GET /api/analyses/<analysis_id>/report` — `reports.get_analysis_report`
- [ ] `GET /api/comparisons` — `comparisons.compare_analyses`
- [ ] `POST /api/benchmarks` — `benchmarks.create_benchmark`
- [ ] `GET /api/benchmarks` — `benchmarks.list_benchmarks`
- [ ] `GET /api/benchmarks/<benchmark_id>` — `benchmarks.get_benchmark`
- [ ] `GET /api/reports` — `reports.list_reports`
- [ ] `GET /api/reports/<report_id>` — `reports.get_report`
- [ ] `DELETE /api/reports/<report_id>` — `reports.delete_report`
- [ ] `GET /api/integrations` — `integrations.list_integrations`
- [ ] `POST /api/integrations/<integration_id>/test` — `integrations.test_integration`
- [ ] `GET /api/cases` — `cases.list_research_cases` (ratify case DTO first)
- [ ] `GET /api/cases/<case_id>` — `cases.get_research_case` (ratify case DTO first)

Before checking an owner endpoint as implemented:

- [ ] Parse/validate the declared request; implement real principal/resource authorization.
- [ ] Connect owner services and Scientific Core; define persistence/transport independently as needed.
- [ ] Validate success output, IDs, permissions, source distinctions and unavailable fields.
- [ ] Test real failure paths without returning fake measurements or placeholder reports.
- [ ] Advertise only tested capabilities; keep unfinished operations 501.
- [ ] Verify the corresponding real browser workflow and access-controlled assets.

## Validation record and remaining gaps

Verified results:

- All **131 backend tests pass**. They cover factory/Blueprint registration,
  independently enumerated URLs/methods, every stub's 501 response, truthful health/
  capabilities, JSON errors, HEAD/OPTIONS, transport/parser limits, exact-origin
  CORS, owner-auth hook behavior, DTO constraints, schema export and the unchanged
  frontend-adapter HTTP bridge.
- Editable package installation, `pip check`, Python compilation and Flask CLI
  route enumeration succeed. Python 3.14 / Flask 3.1.3 / Pydantic 2.14.2 /
  Flask-Cors 6.0.5 / pytest 9.2.0 were used; exact versions are locked.
- The unchanged React application was exercised through its actual Vite proxy to
  a live local Flask process. Health/capabilities returned 200, analysis listing
  returned 501, the UI distinguished unavailable records from an empty workspace,
  and no runtime page errors were observed. This was not a mocked Flask response.
  A screenshot is in `frontend/output/playwright/flask-skeleton-live-workspace.png`.
- All 90 existing frontend source/config/asset/test files match their pre-task
  hashes. No frontend code, schema, adapter or dependency modification was needed.
- Temporary smoke-test servers were stopped; existing user preview servers were
  left untouched. Backend/document whitespace checks pass.

Structural and schema tests do not prove scientific implementation. The optional frontend-adapter
bridge starts a temporary WSGI test server and imports the unchanged existing
TypeScript adapters through installed Vite tooling. It checks real HTTP health/
capability parsing and 501 rejection, without mocking the Flask responses. If Node
or frontend dependencies are absent in a backend-only checkout, that bridge is
explicitly skipped; core Flask tests still run independently.

Scientific workflows, persistence, authentication, authorized asset serving,
real report generation, benchmarks, integration connections and deployment remain
owner work. No backend integration completion is claimed from route registration. As each owner operation is implemented, replace its skeleton-only 501/capability assertions with meaningful authorized success and failure tests, update catalog.py and this checklist, and retain guards for unfinished operations. Do not merely delete the unavailable-state checks or enable flags without real implementation.

## Infrastructure references

- [Flask application factories](https://flask.palletsprojects.com/en/stable/patterns/appfactories/).
- [Flask configuration and request limits](https://flask.palletsprojects.com/en/stable/config/).
- [Flask-Cors API configuration](https://flask-cors.readthedocs.io/en/latest/api.html).
- [Pydantic strict validation](https://docs.pydantic.dev/latest/concepts/strict_mode/).
