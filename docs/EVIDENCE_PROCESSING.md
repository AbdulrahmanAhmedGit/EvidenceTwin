# Evidence processing and descriptive findings

Implemented 2026-11-08. This guide describes `descriptive-evidence/1` in the local HTTP runtime. The approved baseline and all scientific enablement gates retain their authority. These operations do not close the gates or enable a scientifically validated verification service.

## The observed failure

The preserved diabetes CSV contains 455 records. The former `Runtime.build_record` retained the complete parsed table but copied only `rows[:200]` into the Council packet. Egypt's 2024 observation was in CSV record row 124. The United States observation was in row 434 and therefore absent from agent context. Its original file still matches its stored SHA-256. The data were present.

`OllamaProvider.chat` and `RestProvider.chat` additionally told reviewers that browsing never occurred and URLs were metadata. There was no source retrieval implementation. `Workflow.run.finish` always retained `not_evaluated`, and `Workflow.report` repeated static source-access limitations. No Blind Optics implementation was disconnected from the UI. The runtime explicitly marked it unavailable, matching unresolved D07/E04 and the draft Council protocol.

Historical records remain unchanged. Starting a new run uses the new processing version. Retrying a failed/cancelled run preserves the former attempt, packet, prompt snapshots, inputs and processing record in attempt history.

## Complete evidence and bounded context

Original files, filenames, byte hashes and immutable case revisions remain preserved. The complete accepted CSV/JSON table stays in the record. Ingestion still permits one table, at most 5,000 records and 100 columns, within existing upload limits. Larger tables need an explicitly reviewed ingestion extension and are rejected rather than silently shortened.

`science/datasets.py` operates independently of Flask. `query_dataset` applies one to six case-insensitive exact column/value filters over the entire table. A response includes original record row numbers, columns, values, total matches and explicit budget constraints. A query returns up to 100 rows and 64,000 serialized UTF-8 bytes. More matching evidence remains in the retained original. An empty result, unsupported column, budget exclusion and unavailable parser are distinct outcomes.

Automatic preparation currently supports exact Entity, Country or Location names appearing in the original question, and an explicit Year column/year in the question. It does not infer aliases, translate content, guess a year or choose among several measurement columns. It considers at most eight mentioned entities and four explicit years. Missing exact selections are reported. Multi-indicator tables need explicit queries and a future explicit comparison configuration.

`science/processing.py` produces the versioned catalog, selected records, query manifests, calculations, coverage and structured limitations. When no relevant selection is available, a bounded overview is labeled accordingly. Context selection is separate from source-data availability.

Initial specialists can request up to four exact-match queries through `Review.requested_queries`. The backend validates them and invokes that specialist once more with the actual query results. `evidence_id` selects the uploaded table or a parsed `retrieved-source` table. The round is bounded. No arbitrary Python, SQL or model-generated executable code runs. Initial reviewers do not receive other reviewers' outputs or query results. Cross-review and adjudication receive the collected records afterwards.

## Descriptive calculations and plots

A comparison is automatic only when exactly two selected entities each have one record for the same year and the table has one measurement column. Non-numeric, ambiguous, missing or unsupported observations do not produce a comparison.

Values are parsed as Decimal, with at most 28 coefficient digits and exponent/adjusted exponent within ±28. Subtraction uses precision 64. The first/second ratio uses precision 34 and half-even rounding. A zero denominator yields a null ratio. The difference is signed first minus second. Percentage-point labeling requires a `%` indicator header or an explicitly supplied matching variable unit. Other declared units are preserved, and unknown units do not produce a plot. No guessed unit conversion, significance test, confidence interval or causal inference occurs.

The retained record includes values, exact row references, indicator, year, query IDs, file hash, evidence revision and operation settings. The visible plot uses those values and a zero baseline with a domain that includes both observations. Labels and numbers use readable DOM text, and exact tabular observations remain available. A plot is shown only when units are identified. It is a descriptive data display, not a Neutral Twin or a scientific claim of comparability.

The original diabetes evidence yields 22.4 and 13.7 for 2024, a difference of 8.7 percentage points and a first/second ratio of approximately 1.6350. These numbers are derived from the submitted CSV, never hardcoded in production. Age-standardization, methodological compatibility and external authenticity remain separate unanswered checks.

## Public source retrieval

A newly authorized Council run may retrieve its supplied public URL. Saving a case or opening a preview does not make an external request. The updated consent explains retrieval, private retention, readable excerpts, dataset queries and external model sharing. URL-only cases can request review when the provider is available.

`science/sources.py` supports public HTML, UTF-8 plain text, CSV, structured JSON and retained PDF bytes. HTML extraction removes scripts/styles and executes no JavaScript. PDFs are retained with an explicit unavailable text-extraction state. Structured JSON supports `columns` and `rows`, not arbitrary endpoint schemas. Dynamic pages, authenticated content, paywalls and unsupported encodings can remain inaccessible. No universal publisher compatibility is claimed.

Every source and redirect target is DNS-resolved and checked. All returned addresses must be public, excluding local/private/link-local, multicast, reserved and transitional tunnel addresses. Connections pin the validated address, retain the original Host and verify HTTPS certificates against that hostname. Environment proxies, cookies and credentials are not forwarded. Only standard ports are accepted. Each content redirect is checked against its own robots policy before content retrieval. Restricted, redirected or unavailable robots policies fail closed. Crawl-scheduling requirements need a scheduled connector. Extended wildcard/end-anchor robots rules and ambiguous encoded paths are unsupported and fail closed. Conflicting simple rules are handled conservatively, retaining matching disallows.

Limits include three redirects, 2 MiB source bodies, 128 KiB robots bodies, no content decompression, bounded socket operations and an interrupt timer within a 45-second retrieval budget. DNS resolution uses the host resolver. Content types are allowlisted. Retrieval uses a dedicated user agent. It neither bypasses access controls nor establishes rights for redistribution. Operator review remains necessary before hosted deployment.

Snapshots are private content-addressed files, with URL, final URL, time, media type, size, hash, extraction status and outcome. Retries never overwrite an earlier source artifact with different bytes. Complete snapshots remain downloadable through an ownership-authorized attachment endpoint. Prompt excerpts are explicitly selected by lexical overlap, with line numbers and excerpt bounds. External text is always evidence data, never instructions.

Retrieval, provenance, authenticity, content verification and claim assessment remain separate. A successful download does not authenticate the source or validate its science.

## Council, outcomes and reports

The versioned evidence-access supplement is appended to preserved role prompts. It directs roles to inspect available records, cite exact evidence/query/calculation IDs, state findings first, avoid invented numbers, and request only applicable checks. All original role files remain preserved. Actual prompt snapshots/hashes are pinned per accepted attempt. Successful raw outputs, structured outputs, usage, per-role packets and query request/response records remain inspectable.

Optional structured `limitation_records` distinguish processing failures, evidence gaps, method limits, verification gaps and unavailable capabilities. They group by category, affected check and evidence references, preserve each role's original explanation/cause, and order blocking issues first. Reviewer causes remain identified as AI concerns. Legacy string limitations stay in original outputs and detailed records. Grouping does not prove that the reviewers correctly diagnosed a cause.

Execution status remains separate from the scoped descriptive result and scientific coverage. The existing full scientific assessment stays `not_evaluated`. A visible comparison can still establish the ordering of reported submitted values without implying source verification or an approved scientific verdict. Council agreement cannot promote it into proof.

Results lead with actual descriptive findings, calculations and coverage. The visualization laboratory also exposes the same recorded descriptive plots separately from original-image controls. Original prompts and the detailed AI record disclose separately. Council views use structured finding titles and claim positions with explanations on demand, while retaining legacy output support. Reports include a concise executive finding, real calculation/chart, source outcome, coverage, observations, limitations and reproducibility. Original inputs and technical records remain accessible in document disclosures and JSON. Browser printing is the supported PDF route.

Blind Optics remains unavailable. Exact blinding disclosures, chart/data binding, rendering templates, paired ordering and scientific acceptance are unresolved. The descriptive plot is not substituted for the intended blinded reconstruction.

## New read APIs

- GET `/api/research-cases/{caseId}/revisions/{revisionId}/processing` computes a read-only preview from that immutable revision, with no network request or historical analysis rewrite.
- GET `/api/analyses/{id}/processing` returns the processing actually used for that run. Pre-version runs return `historical: true` and no invented retrospective findings. The response omits full source text and parsed source table bodies, which remain in the private evidence record.
- GET `/api/analyses/{id}/dataset-query?filters={...}&limit=25` queries the complete uploaded table. Filters use exact column names and scalar values. Source-table queries are currently available to Council roles, not this uploaded-table endpoint.
- GET `/api/analyses/{id}/source-snapshot` downloads a retained source artifact as an attachment. No source HTML is executed or served as an application page.

All routes apply existing session and ownership checks before reading evidence. No schema migration or account reassignment is required. The existing JSON record store carries additive fields. See the deployment guide for coordinated backup/rollback. Existing historical analyses are not automatically reprocessed.

## Owner acceptance

Start the application using DEVELOPMENT.md. Open the saved diabetes investigation, inspect its new complete-table preview, then explicitly request a new review. Inspect the exact country/year rows and calculations, source status/snapshot, independent perspectives and any follow-up queries. Confirm the old analyses retain their original packet and report. Try missing/ambiguous rows and blocked URLs. Inspect English/light, Arabic/dark, mobile, the composer expansion/menus, report contents, browser printing and JSON exports.

Focused engineering checks and isolated browser diagnostics are recorded under `output/evidence-processing/`. The isolated visual diagnostic uses copied original evidence and real source retrieval, carries an engineering label and draft status, and performs no Council calls. Synthetic providers exist only in isolated tests. No paid-provider, hosted, scientific, screen-reader or cross-browser acceptance is claimed. Final acceptance belongs to the owner.

## Multiple links, public captions and report translation

The current source-discovery pass finds HTTP(S) links in the explicit source field, original questions and research notes without changing those inputs. It records up to ten unique references and retrieves up to three, prioritizing the explicit field. Every source has a distinct evidence reference and access outcome. New reviews use processing version `descriptive-evidence/2`. Older runs retain their original records.

HTML extraction uses Scrapling over the existing bounded pinned-IP downloader. Public YouTube video links use `youtube-transcript-api` through a restricted transport. Captions retain original language, timestamps, generated/manual status and hashes. Access restrictions and missing captions produce unavailable outcomes. PDF download does not imply PDF text extraction. Source access does not establish authenticity.

Report translation is a separately labeled machine-generated derivative supplied by operator-managed LibreTranslate. The original report is preserved. Jobs are owner-scoped, tied to the original report hash, bounded and retryable. Numeric observations and references are checked for preservation. Scientific terminology requires human review. See [setup](DEVELOPMENT.md) and the [dated integration record](../output/source-connectors/IMPLEMENTATION.md).

The protected report translation client retains original passages when numeric/reference integrity cannot be confirmed, labels the derivative partial and records retained block locations. Transport/service failures still fail the translation job. This safety fallback does not validate translation semantics.
