# Proposed frontend API contract

These are frontend wire contracts. A Flask integration skeleton now registers the 24 operations currently consumed by React, plus two reserved case-catalog routes. Only health and disabled-capability metadata are implemented; business/scientific operations return consistent HTTP 501 JSON errors. See [BACKEND_IMPLEMENTATION_GUIDE.md](../BACKEND_IMPLEMENTATION_GUIDE.md) for exact status, Python functions and owner TODOs. Earlier phase descriptions below preserve the original proposed-contract context; they do not imply scientific functionality is operational.

## Implemented frontend calls

- `GET /api/health`: JSON object; non-JSON responses are rejected to detect accidental SPA fallback.
- `POST /api/analyses`: multipart form with `metadata` JSON and repeated `files` entries. Metadata currently includes claim, source, URL, verification mode, optional case ID. Returns `{ "id": "analysis-id" }` after server acceptance. All source/study/date/review-depth fields are now wired; see the Phase 3 update below.
- `GET /api/analyses/:id`: fields `id`, `title`, `status`, `mode`, `createdAt`, `claim`, `limitations[]`, `findings[]`; optional `stage`, `assessment`.
- `GET /api/analyses/:id/{evidence|visualizations|council|audit|report}`: section payloads described below.

Analysis status: draft, awaiting_evidence, queued, running, completed, completed_with_limitations, failed, cancelled. Mode: verified or exploratory. Assessment: supported, unsupported, partially_supported, insufficient_evidence, unresolved, not_evaluated.

Findings contain `kind` (calculation, source_backed, interpretation, unverified), `text`, `citations[]`.

## Section payloads

- Evidence: `sources[]` with id/title/status/checked/optional URL; `dataset` with columns and row arrays; optional `contract` JSON object.
- Visualizations: `visualizations` with original/neutral asset URLs, compatible boolean, changes array, provenance, optional unavailableReason. Alignment compatibility is a backend assertion; the frontend never guesses a neutral twin.
- Council: `reviews[]` with id, role, phase (independent, cross-review, judge), status, summary, optional model, findings and citations. `disagreements[]` contains claim, positions, optional resolution.
- Audit: `events[]` with id, timestamp, component, type, status. Do not send private credentials in event payloads.
- Report: `sections[]` with id, title, body, optional references (title and URL).

The executable section schemas are in `frontend/src/research-api.ts`. Missing section fields are currently optional; owners should agree on required section shapes before deployment.

## Remaining proposed interfaces

Frontend adapters for capabilities, analysis actions, paginated datasets, research comparisons, benchmarks, reports management and integration diagnostics are implemented in the Phase 3–5 sections below. All endpoints still require owner implementation or mapping to actual Flask routes. Authentication/session, additional export formats and a backend-authored case catalog remain optional future adapters. No UI state should advertise backend execution as available until positively confirmed.

Errors should use meaningful HTTP status codes. 401 means authorization required; network failures must not become empty datasets. Mutations must not be automatically retried without idempotency support.

## Phase 3 list and capability adapters

`GET /api/analyses` accepts `search`, `status`, `mode`, `verdict`, `sort`, `page`, `pageSize` as query parameters. Empty filters mean unrestricted. Sort values are `createdAt:desc`, `createdAt:asc`, `title:asc`, `status:asc`. Filtering and pagination are server responsibilities; the UI does not imply searching only a downloaded page.

Response: `{items: AnalysisRecord[], total: number, page: number, pageSize: number}`. Each record has `id`, `title`, ISO timestamp `createdAt`, `status`, `mode`, optional `source`, `assessment`, `summary`, and `reportAvailable` (defaults false). Status/assessment enums match the detail contract. Response validation rejects incompatible records and invalid dates.

`GET /api/capabilities` proposed response: `{analyses: {create: boolean, delete: boolean, retry: boolean}, services: [{name: string, status: "available" | "unavailable" | "not_configured"}]}`. Missing action flags default false. List retrieval and capability retrieval are independent: a capability failure must not hide successfully retrieved records.

`DELETE /api/analyses/{id}` accepts JSON success or HTTP 204. `POST /api/analyses/{id}/retry` requires JSON success. Neither is automatically retried. Bulk deletion invokes the confirmed endpoint once per selected record; after partial failure already deleted IDs are removed from the pending selection and the list is refreshed.

## Phase 3 creation and settings update

The complete builder now submits `metadata` containing `source`, `url`, `studyDate` (YYYY-MM-DD or empty), `studyDesign`, `population`, `uncertainty`, `context`, `claims[]`, `mode`, `reviewDepth`, optional `caseId`, and the first claim as `claim` for adapters using a single claim. These replace the initial partial-metadata description above. File objects are repeated multipart `files` fields; source links are not automatically fetched by the frontend.

Acceptance requires a non-empty string `id`. The client returns this ID; the presentation layer controls navigation. HTTP 422 preserves inputs and requests corrections; HTTP 401 requests authentication. Network/timeout failures are unconfirmed, and the interface advises checking history before manual resubmission. No submission mutation is retried automatically.

`capabilities.analyses` additionally accepts `modes` (exploratory/verified), `reviewDepths` (focused/council), and `maxClaims` (1–10). Defaults are exploratory, focused, one claim, respectively. `create` still defaults false. A configuration is submit-enabled only when positively supported. Eligibility of actual evidence, especially Verified Mode, is checked by the backend at acceptance; a supported configuration is not a scientific verification result.

Optional capability fields: `activity` boolean (default false), `jobAvailability` available/unavailable/unknown, `providers[]` with name and configured/not_configured/unavailable status. Absent provider or queue information stays unknown.

`GET /api/activity?limit=10` is queried only when `activity` is advertised. Response: `{items:[{id,timestamp,description,analysisId?}]}` with an ISO timestamp. Events are rendered as received; the frontend does not create activity to populate a dashboard.

Safe preferences, locale/theme, motion and density apply locally. No authentication adapter, server data export or workspace-wide deletion is configured. Those controls must remain unavailable until their corresponding adapters are implemented. Settings diagnostics copy only the public base URL, query states and known capability booleans.

## Phase 4 analysis inspection contracts

All routes remain proposed Flask interfaces. The frontend adapters are implemented; no live Flask implementation or scientific execution was supplied or verified.

### Analysis record and processing

`GET /api/analyses/{id}` retains id, title, status, mode, createdAt, claim, limitations and findings. `createdAt` and optional `startedAt` use ISO timestamps with offsets. Optional additions:

- `claims[]`: the original user-supplied claims.
- `sourceStatus`: verified / partially_verified / unverified / unavailable / unknown; defaults unknown.
- `assessment`: the existing assessment enum; absence remains Not evaluated.
- `stage`: an actual backend-reported description. `stages[]`: id, label, status (pending/running/completed/failed/skipped), optional timestamp and durationMs. Missing stages are not reconstructed.
- `issues[]`, `suggestedInterpretation`, `error`, `reviewSummary[]` (role/status/summary).
- `actions`: retry and cancel booleans; both default false. These should reflect both service support and permission for this analysis.

Findings retain kind, text and citations. Optional id, value (number/string), unit, sourceVerified enrich the view. A calculation label does not imply source verification. The frontend renders the backend assessment; it never votes on findings or derives a scientific verdict.

`POST /api/analyses/{id}/retry` and `/cancel` require advertised support and user confirmation. Success acknowledges the request; displayed status comes from subsequent record retrieval, not an optimistic frontend job state. Neither mutation is automatically retried.

The current transport polls the analysis record while queued/running, normally every five seconds with failure backoff capped at thirty seconds. It stops at terminal states, does not poll static previews, and does not request background interval polling. A reconnect/refresh reads the current record. An SSE implementation can replace the transport in the adapter without introducing frontend stage simulation.

### Common section permissions

Each inspection response may include `permissions` with dataDownload, contractDownload, assetDownload, auditDownload and reportJson. All default false. These flags control affordances; the backend must independently enforce access. Viewing/copying supplied text does not grant public sharing or server-wide export rights.

### Evidence and dataset

`GET /api/analyses/{id}/evidence` may return sources, files, dataset, study, checks, uncertainty and contract.

Sources: id/title/status/checked, optional URL/date/limitations[]/identifiers. Status uses the sourceStatus enum; `checked` states the actual scope of inspection. Files: id/name/size/mediaType/status and optional URL. Images are previewed where supported; documents open only through safe supplied links.

Dataset: columns (ordered strings), rows (ordered arrays of string/finite number/boolean/null), optional variables (name/unit/description/missingCount), notes, serverPaginated, totalRows, page and pageSize. Row widths must match the columns. Null is displayed as missing; the frontend does not impute values or classify arbitrary source strings as missing. Locally supplied snapshots are limited to 5,000 rows and render 25 matching rows at once.

For larger data, set serverPaginated true and provide totalRows/page/pageSize. `GET /api/analyses/{id}/dataset?page=1&pageSize=25&search=&sort=-1&direction=asc` returns a matching dataset page. `sort` is a zero-based column index; -1 means supplied order. Page/pageSize and column identities must match the requested evidence schema or the frontend refuses to display potentially mislabeled values. Server search/sort must apply to the full permitted dataset.

Study and contract contain structured JSON. Recognized human-readable contract categories are inputFacts, computedFacts, constraints, provenance, unsupportedInferences and missingInformation; other supplied keys remain inspectable without invented classification. Client display/export helpers redact recognized credential keys and common credential strings. They are not unmodified wire captures. **Never send private tokens or provider secrets to these endpoints**; browser-side redaction is a defense in display, not backend data isolation.

### Visualization assets

`GET /api/analyses/{id}/visualizations` returns optional dataset and visualizations:

- original/neutral asset URLs, compatible boolean, changes[] and provenance.
- Optional unavailableReason, originalDescription, neutralDescription, version, parameters, generationStatus (pending/ready/failed/unavailable) and supplied warnings[]. Generation state and uncertainty warnings are not guessed by the frontend.
- Optional legend[] (label and #RRGGBB color), interpretations[] (representation original/neutral, text, kind interpretation/source_backed), interpretationChanged.

Use immutable asset URLs for each visualization version. Compatibility means the backend has confirmed aligned raster/rendered frames; the UI additionally requires identical loaded image dimensions before overlay/slider modes. Missing or incompatible assets remain explicit. Recorded changes, not guessed pixel differences, populate Differences View. Stable or changed interpretations do not establish correctness.

Zoom/pan/legend/data controls are local display operations. Copy selected image creates a PNG from the loaded asset when browser and origin permissions permit. Downloads fetch actual supported image bytes through the API boundary; failed access/CORS/type checks do not report success. Cross-origin asset endpoints need the appropriate CORS policy for downloads; canvas copying may be restricted by browser origin rules. Source assets remain available through explicit open links when permitted.

### Council and disagreements

`GET /api/analyses/{id}/council` returns reviews[] and disagreements[]. Reviews retain id/role/phase/status/summary/findings[]/citations[]. Optional roleKey identifies visual/statistical/scientific/counterfactual; model, provider, independentExecution, claims[], uncertainty[] and report add detail. A phase named independent does not itself assert isolation. Only independentExecution true produces a reported-independence label. Missing reviewers are not shown as executed or completed.

Disagreements contain optional id, claim, positions[], supportingEvidence[], contradictingEvidence[], optional status (resolved/unresolved/not_evaluated), and resolution rationale. A rationale without a status does not cause the frontend to invent a resolved verdict. Cross-review and judge output remain distinct from initial reviews. No consensus accuracy or overall winner is computed.

### Audit and report

`GET /api/analyses/{id}/audit`: events[] with id/timestamp/component/type/status and optional durationMs/inputRef/outputRef/error/metadata. Times display in the browser time zone; structured JSON retains original offsets. Events are ordered chronologically and paginated in groups of 25. Metadata and known credential patterns are redacted before JSON presentation or download. Backend logs must already exclude private data.

`GET /api/analyses/{id}/report`: sections[] with stable id/title/body (plain text) and optional references[] (title/URL). Only supplied, nonempty sections render. Optional report metadata contains title/generatedAt/version/reproducibility. Titles/body retain their supplied language and use automatic text direction. There are no generated citations or inferred report sections. Browser printing is implemented; server PDF export is not configured. reportJson permission enables a local JSON export of the supplied report data.

All source/asset/reference links must use credential-free HTTP(S) URLs or same-origin paths. Executable URL schemes and credential-bearing URLs are rejected. Serve uploads and generated assets with appropriate content types and backend access controls.

## Phase 5 research-tool adapters

The following adapters are now implemented in `frontend/src/features/research/api.ts`. Every endpoint remains **proposed and unverified against Flask**. Scientific comparisons and evaluation measurements are backend responsibilities. An HTTP health response never enables research mutations by itself.

### Capability additions

`GET /api/capabilities` may include:

```json
{
  "research": {
    "comparison": false,
    "benchmarks": { "read": false, "create": false },
    "reports": { "read": false },
    "integrations": { "read": false }
  }
}
```

Missing fields default false. Comparison and benchmark creation require positive support. Read-only lists attempt their real endpoint to distinguish authorization, unavailable services, incompatible data, and an empty result; `read` flags describe service configuration without replacing HTTP authorization. Per-record permissions govern report deletion/export and integration testing.

### Analysis comparison

`GET /api/comparisons?analysisA={id}&analysisB={id}` returns:

- `analysisA`, `analysisB`: exact requested IDs; mismatches are rejected.
- `comparability`: comparable / limited / incompatible / unknown.
- `reasons[]`: explicit comparability limitations, including incompatible populations, metrics or conditions.
- `dimensions[]`: key, label, a (string or null), b (string or null), relation (same / different / not_comparable / unknown), optional note.

Supply dimensions for claims, modes, source validity, numerical findings, verdicts, reviewer findings, sensitivity, uncertainty, configuration and duration only when available. Null means missing, never zero. Labels/narrative retain the backend-supplied language. The frontend does not derive comparability, an overall winner or a scientific accuracy score. Selection uses the existing paginated analyses endpoint and preserves the chosen IDs in `?a=&b=` deep links.

### Benchmark creation

`POST /api/benchmarks` accepts JSON:

```json
{
  "name": "Owner-defined research evaluation",
  "description": "Owner-defined comparison objective and protocol.",
  "caseIds": ["a1"],
  "conditions": ["standard", "council"],
  "modelConfigRef": "owner-defined-model-configuration",
  "rubricRef": "owner-defined-evaluation-rubric",
  "repetitions": 1,
  "seed": "owner-defined-seed",
  "preserveControls": true,
  "outputs": ["summary", "per_case"]
}
```

This is a proposed configuration example, not an executed evaluation. Conditions: standard / evidence_first / deterministic / council. At least one case and two conditions are required. Repetitions are integers from 1 to 100. Output options: summary / per_case / audit. Backend validation must resolve configuration and rubric references, confirm available conditions/models/cases, enforce controls, authorize the run and implement reproducibility; a frontend seed field cannot establish reproducibility. Reference fields must not contain provider keys.

Return `{id: string}` only after accepting the configuration. Reads have 15-second timeouts; benchmark acceptance has a 30-second timeout. No mutation retries are automatic. Stopping the browser wait aborts transport, not server execution. An uncertain submission should be checked in the benchmark list before resubmission.

### Benchmark retrieval

`GET /api/benchmarks` accepts search, status, sort (createdAt:desc / createdAt:asc / name:asc), page and pageSize=10. Return `{items, total, page, pageSize}`. Summary records: id, name, description, createdAt (ISO), status (analysis status enum), caseCount, conditions[], optional availableMetrics[], completedRuns, totalRuns. Do not return invented run progress.

`GET /api/benchmarks/{id}` returns the summary plus:

- `configuration`: the accepted creation shape above.
- `metrics[]`: key, label, definition, value (finite nonnegative number or null), unit (rate / count / milliseconds / currency), condition, optional numerator, denominator, currency, limitations[]. Rates use a fraction from 0 to 1 and require a positive sample denominator when measured. A supplied numerator must not exceed the denominator. Currency-valued costs require currency. Null displays Unavailable.
- `cases[]`: caseId, title, condition, status, outcome (string or null), optional analysisId and failure. Status failed / disagreement supports filtering. The linked analysis must independently authorize access.
- `limitations[]`, optional reproducibility text.
- `permissions: {json: boolean}` (default false): allow the inspection JSON download.

The detail view polls every five seconds only while queued/running and visible. Errors stop interval polling until user retry; terminal states stop polling. Rates and counts remain distinct. The frontend does not declare measured improvement or statistical adequacy. Product evaluation is explicitly separated from the original NYAS student experiment. Large run-result services should supply bounded case collections; the UI renders ten supplied case outcomes at a time.

### Reports management

`GET /api/reports` accepts search, status (assessment enum), mode, from, to (YYYY-MM-DD, inclusive creation-date bounds as interpreted by the backend), sort (createdAt:desc / createdAt:asc / title:asc), page, pageSize=10. Return `{items,total,page,pageSize}`. Each record: id, analysisId, title, createdAt (ISO), status (assessment enum), mode, optional summary, `permissions: {delete, json}` (both default false).

`GET /api/reports/{id}` returns the existing Phase 4 section schema, including supplied report sections and `permissions.reportJson`. Preview export requires **both** record.permissions.json and detail.permissions.reportJson. A report is not inferred merely because an analysis exists. Full report navigation uses the analysis report route. JSON is currently the managed downloadable format; browser printing remains available on the full report. No server PDF export is claimed.

`DELETE /api/reports/{id}` requires record permission and user confirmation; return JSON acknowledgement or HTTP 204 after deletion. HTTP errors preserve the record. The frontend never assumes that deleting a report deletes its analysis. Define retention and associated-resource semantics in the backend policy before deployment.

### Integration management

`GET /api/integrations` returns `{items: Integration[]}`:

- id, name; category: mcp / skill / api / developer.
- status: available / configured / not_configured / planned / unsupported.
- overview; capabilities[], requirements[], instructions[] (backend-authored text).
- optional endpoint: public HTTP(S) URL or same-origin path, without embedded credentials or token/key/secret/password query parameters.
- optional authentication description, invocation trigger; tools[]; documentation: api / mcp / skills / getting-started.
- canTest boolean (default false).

Do not return private keys, signed credential-bearing URLs, session tokens, provider secrets or arbitrary private configuration. The public copy action is built from only category, endpoint and tool names. It is a connection description, not an installation command. Tool/endpoint configuration does not guarantee automatic assistant invocation.

`POST /api/integrations/{id}/test` is invoked only when canTest=true. Return status reachable / failed, message and checkedAt (ISO). A successful HTTP response with status=failed remains a failed test. No connection-success message is fabricated when the request fails. Reachability does not validate scientific results.

### Integration ownership

The frontend contains no Flask code. Authentication/session management, server-side authorization, private configuration, scientific execution, job cancellation semantics, durable storage, real benchmark measurements and integration installation remain backend/deployment concerns. Existing owner routes may replace these proposed paths by editing typed adapters; no Flask architecture changes are required.

## November 3 stabilization clarification

`GET /api/analyses/{id}` must return an exactly matching `id`. The frontend rejects an otherwise schema-valid record whose identity differs. This follows the existing comparison/benchmark identity checks. A mismatch blocks initial dependent reads/actions; a refresh mismatch also withholds cached metadata and stops interval polling until recovery. It is a client integration error, not a generated scientific outcome. No server response fields or new endpoints were added.

The browser comparison route uses `a` / `b`, accepting legacy `analysisA` / `analysisB` links and canonicalizing them. The proposed **API** comparison query remains `analysisA` / `analysisB` as previously documented. Report-list filters are reflected in the browser URL using the existing request field names: search, status, mode, from, to, sort, page. HTTP filtering/permission contracts are unchanged.

## Flask skeleton status

The skeleton does not change the frontend schemas, request paths or clients. `GET /api/health` returns status=ok plus public apiVersion/mode/scientificServices metadata. `GET /api/capabilities` reports all scientific/research flags false, empty mode/review-depth/provider lists and unavailable jobs/services. Every other registered domain operation returns HTTP 501 `{error:{code,message,operation?}}`; unknown routes return JSON 404 and unsupported methods JSON 405. Automatic OPTIONS/HEAD preserve normal HTTP behavior without scientific execution. Case-catalog responses remain an owner contract decision because the current React library uses local educational inputs.

## November 5 runtime implementation update

The Flask backend now implements persistent local exploratory records, upload
handling, actual queued review execution and the existing inspection/report/
comparison/integration/activity read contracts. `EVIDENCETWIN_RUNTIME=0` retains
contract-only skeleton behavior for structural testing; normal runtime defaults on.
Creation requires an explicitly configured server provider/model. The six adapters
follow the owner's snippets without importing interactive evaluation scripts or
credentials. Four initial calls have isolated conversations; all use the selected
provider/model. Cross-review requires four valid initial outputs and judging
requires valid cross-review. Failures remain inspectable.

Verified mode, source/statistical verification, Blind Optics/Neutral Twin,
benchmark scoring and MCP stay unavailable pending scientific specifications.
Model judgment remains in the Judge report, not a verified final verdict badge.
`GET /health.mode` may now be `workspace` as well as `integration_skeleton`; existing
React only consumes status. Original upload assets have a new record-aware GET
`/api/analyses/{id}/files/{file_id}` boundary. No frontend source changed. See the
root Backend Implementation Guide for current endpoint availability and limits;
older skeleton status statements above are historical.

## Workspace AI API configuration

Runtime endpoints GET/POST /api/settings/ai and POST /api/settings/ai/test support
the /app/settings/ai page. See [AI provider configuration](AI_PROVIDER_CONFIGURATION.md).
Only non-secret configuration and key-presence flags are returned. Saving selects
the provider for future jobs without a restart; accepted jobs retain their initial
provider. No scientific capability is enabled by saving this form.
