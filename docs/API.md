# Current HTTP API

Current local runtime contracts, 2026-11-08. API prefix is `/api`; the planned `/api/v1/` Scientific Core contract is not this runtime. Existing typed DTOs live in `backend/evidencetwin_backend/contracts/`, browser schemas in the domain adapters. Every private resource is server-authorized; inaccessible resources return 404, unauthenticated requests 401, operator violations 403. Errors use the common API error envelope. Responses are `no-store`; downloads use `nosniff`. Use a same-origin browser deployment for account sessions.

## Sessions

| Method and path | Contract |
| --- | --- |
| GET `/api/session` | `{accountsEnabled, authenticated, operator, name, workspaceId}`; identity fields are nullable before login. `workspaceId` is the opaque principal ID used to scope browser drafts. |
| POST `/api/session/login` | JSON exactly `{name,password}`; returns session metadata and session cookie. No public registration. Accounts-disabled login is forbidden. |
| POST `/api/session/logout` | Clears the session; 204. |

Login throttling persists per hashed remote address (ten failures per 15-minute window); do not treat this local bound as a reviewed hosted abuse-control policy. Operators provision/disable accounts through the standalone `python -m evidencetwin_backend.accounts` CLI without stopping the service; see [setup](DEVELOPMENT.md).

## Revisioned cases

| Method and path | Behavior |
| --- | --- |
| GET `/api/research-cases?search=&page=1` | Current principal's title search; `{items,total,page,pageSize:20}`. Summaries contain `id,title,createdAt,updatedAt,currentRevision,revisionCount,analysisCount`. |
| POST `/api/research-cases` | Multipart full metadata and optional files; saves a case independently of a provider; 201 detail. |
| GET `/api/research-cases/{caseId}` | Current summary plus `metadata,files,revisions,analyses,limitations`. |
| POST `/api/research-cases/{caseId}/revisions` | Multipart full replacement metadata, retained file IDs and new files; requires `If-Match` equal to `currentRevision`; 201 detail. |
| GET `/api/research-cases/{caseId}/revisions/{revisionId}` | Immutable `{id,metadata,files,createdAt}`. |
| GET `/api/research-cases/{caseId}/revisions/{revisionId}/files/{fileId}` | Authorized original bytes/download filename. `?preview=1` permits inline images only. |
| GET `/api/research-cases/{caseId}/revisions/{revisionId}/dataset` | Existing dataset DTO for table inspection; parsing is not scientific validation. |
| POST `/api/research-cases/{caseId}/analyses` | JSON exactly `{revisionId,requestId,consent:true}`; UUID request ID required; 202 `{id}`. |

Multipart has one `metadata` JSON string, repeated `files` parts and optional `retainedFiles` JSON array. Metadata requires `source,url,studyDate,studyDesign,population,uncertainty,context,claims,claim,mode,reviewDepth`; `claim` must equal the first unique nonblank `claims` entry. `mode` must be `exploratory`; depth is `focused` or `council`. Empty optional text values are supplied as strings. Date is empty or `YYYY-MM-DD`. The typed contract defines bounded lengths and study-design values; the browser's optional educational `caseId` is not an actual persisted case ID.

Revisions are full snapshots. Retained IDs must belong to the current revision; omitting an old file removes it only from the new revision. Old bytes and revisions remain. Invalid/stale preconditions yield 409; do not silently overwrite or automatically retry. File metadata is `{id,name,size,mediaType,sha256}`.

Run acceptance requires the current saved revision, evidence, a configured provider and no active run for that case. Same UUID/same revision replays the accepted `{id}` with 200; same UUID/different revision yields 409. Receipt and analysis acceptance are atomic. The browser does not automatically retry external processing. A transport failure may leave acceptance uncertain: reconcile using the saved case/run history or replay the same request identity, never create a replacement run blindly. Missing provider gives 503; malformed metadata/consent/evidence 422; unsupported media 415; request-size rejection 413.

## Input and processing limits

Accept UTF-8 (optional BOM) CSV or structured JSON `{columns,rows,variables?,notes?}`, PNG/JPEG/WebP and PDF attachment bytes. XLSX is unavailable. Maximum ten files, five images, one table, 20 MiB per file and 64 MiB retained bytes per revision; default HTTP request cap is also 64 MiB including multipart overhead. CSV has at most 5,000 data rows, 100 uniquely named nonblank columns and consistent row widths; cell text is bounded at 10,000 characters. Images are verified for format and bounded to 16 million pixels. Duplicate content hashes within a revision are rejected. PDF signature checking is not extraction; PDF contents are not sent to the model. Newly authorized reviews can retrieve supported public source URLs under the bounded access policy in [Evidence processing](EVIDENCE_PROCESSING.md). Case saving and revision previews do not fetch them.

Explicit run consent covers the saved research metadata, supplied images, selected complete-table records, descriptive calculations and readable public-source excerpts shared with the operator-configured provider. Reviewers can request bounded exact-match table queries. The retained table and selected model context have separate limits. Read [Evidence processing](EVIDENCE_PROCESSING.md) for budgets and [Scientific scope](SCIENTIFIC_SCOPE.md) for interpretation limits.

## Retained analysis and operator API

Legacy `/api/analyses` creation/list/detail and per-analysis `cancel`, `retry`, `evidence`, `dataset`, `visualizations`, `council`, `audit`, `report` and `files/{fileId}` remain. Case-linked run/report deletion is forbidden; legacy standalone deletion remains permission-aware. `/api/reports` supports real report list/detail/JSON and legacy authorized deletion. Reports print in the browser; no server PDF generator is claimed. `/api/comparisons`, `/api/activity`, `/api/integrations`, `/api/health`, `/api/capabilities` retain their existing adapters and capability boundaries. `/api/cases` remains the educational catalogue, separate from persisted `/api/research-cases`. Benchmark scoring and verified-mode creation remain unavailable.

`/api/settings/ai` configuration and its provider/model operations require an operator server-side. Stored keys are never returned. Exact retained wire shapes remain in typed contracts/adapters; the [archived API chronology](archive/2026-11-07/FRONTEND_API_CONTRACT.md) documents their evolution, not a replacement for current source. The [preserved backend guide](../BACKEND_IMPLEMENTATION_GUIDE.md) holds detailed legacy route evidence.

## Evidence-processing extension

See [the processing guide](EVIDENCE_PROCESSING.md#new-read-apis) for revision previews, recorded run processing, complete-table queries and retained source downloads. These ownership-authorized read APIs are additive. New runs record `descriptive-evidence/2`, selected rows/calculations, source retrieval status, coverage and structured limits. Historical runs return an explicit legacy response. Original scientific assessment and existing wire status taxonomy remain separate. URL-only saved cases can now request source-based review with consent and an available provider.

## Source snapshots and report translations

Analysis processing includes `sources[]` with per-source evidence identifiers and outcomes. The original `source` alias remains supported. `GET /api/analyses/{id}/source-snapshot?sourceId={evidenceId}` returns that analysis's authorized retained bytes. Optional `raw=1` selects retained raw captions when available.

`GET /api/analyses/{id}/report-translations` returns actual LibreTranslate availability and current-owner derivatives for the current report hash. `POST` accepts only `{"targetLanguage":"ar"}` or `"en"` and returns the accepted or cached job. `GET /api/analyses/{id}/report-translations/{translationId}` returns the authorized matching job. Translations preserve original report records. Credentials remain server-side.
