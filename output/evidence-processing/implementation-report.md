# EvidenceTwin evidence-processing and composer increment

Implemented and inspected 2026-11-08. The local application is running at [the workspace](http://127.0.0.1:5202/app). Final product and scientific acceptance belong to the owner.

## Root causes confirmed

The preserved real diabetes CSV has 455 records and matches SHA-256 `896799a79e97b433101f5ea005bbd5b921c42f1bc6b939af2d712eb354d15c98`.

- `Runtime.build_record` retained the complete parsed dataset but formerly supplied `rows[:200]` to the Council. Egypt's 2024 record is row 124. The United States record is row 434. The excerpt excluded that observation.
- `OllamaProvider.chat` and `RestProvider.chat` explicitly instructed reviewers that browsing never occurred. The backend had no source-ingestion operation. Source URLs were metadata.
- `Workflow.run.finish` always retained the full scientific assessment as `not_evaluated`. Its static limitations and the old report repeated unavailable-source and calculation wording. This protected scientific scope but obscured useful bounded descriptive answers.
- Runtime packet construction explicitly set Blind Optics and Neutral Twin to unavailable. Repository/runtime/snippet searches found no operational reconstruction implementation. The Council draft and D07/E04 leave disclosure, data binding, rendering and paired-review acceptance unresolved.

Relevant implementations are in `backend/evidencetwin_backend/services/{runtime,workflow,provider,transports,research_cases}.py` and the new Flask-independent `science/` package. The [change manifest](change-manifest.json) enumerates this increment's files separately from earlier dirty-worktree changes.

## Implemented evidence operations

Original files and complete accepted tables remain retained. New attempts prepare selected records from the complete table, with row numbers, exact values, evidence IDs, hashes and revision references. Column/value queries use exact equality and explicit bounded results. Reviewers can request a single follow-up round with up to four queries. Initial specialist inputs remain isolated from other reviews, followed by collected cross-review and adjudication inputs.

The automatic descriptive method requires exact entity/year mentions, one measurement column, and one observation for each of two entities. It computes signed/absolute differences and an appropriate first/second numerical ratio. Decimal input bounds, precision and rounding are recorded. Scientific comparability stays unresolved unless established separately. General multi-indicator selection, joins, aliases and arbitrary statistical procedures remain outside this automatic method.

The actual submitted CSV yields Egypt 22.4% and United States 13.7% for 2024, an 8.7 percentage-point difference and a ratio of approximately 1.6350. The application derives those observations and values from data. The [real-data diagnostic](real-data-diagnostic.json) records the inputs, calculations and source outcome. Age-standardization and broader methodological/source claims remain unverified.

Comparison records include a versioned linear, zero-baseline rendering specification, original observations, units and identity transformation. Descriptive plots appear in results, saved-case previews, reports and the visualization laboratory. They retain an exact-value table and provenance disclosure. Blind reconstruction remains unavailable.

## Source ingestion and security

Newly consented runs can retrieve permitted public HTML, UTF-8 text, CSV, structured JSON and PDF bytes. Readable HTML/text and supported tables become available to Council packets. PDF text extraction, dynamic JavaScript pages, arbitrary JSON schemas and restricted publications remain unsupported.

Network protections include public-address validation, mixed public/private DNS rejection, address pinning, HTTPS hostname verification, standard ports, per-redirect policy checks, robots restrictions, conservative handling of conflicting rules, fail-closed unsupported robots patterns, socket/overall budgets, response-size/type limits, no decompression, no environment proxies/cookies/credentials, and attachment-only source downloads. DNS uses the host resolver. This bounded implementation still needs hosted security/operating acceptance.

A real OWID HTML response was retrieved successfully with preserved bytes, extraction status, timestamp and hash. Source access, provenance, authenticity, scientific content verification and claim assessment have separate states. External content is evidence data, and the model receives no arbitrary executable tool.

## Council and result semantics

The new evidence-access supplement uses actual packet availability and instructs roles to examine records and calculations before reporting material caveats. Original role prompt files remain retained. Prompt snapshots/hashes are pinned to each attempt. Successful raw text, validated structured output, per-role inputs, query requests/results and received text preceding invalid/unconfirmed reviews remain available in authorized inspection records. Transport bodies and provider credentials stay outside public error messages.

Structured limitation records group by stable category/check/evidence references, preserve role-specific variants, distinguish AI-reported causes, and prioritize blocking issues. Legacy string limitations and original reviewer outputs remain inspectable.

Execution state, descriptive result and scientific verification coverage stay separate. The global scientific assessment remains `not_evaluated` under the unresolved scientific acceptance baseline. Actual ordering/difference findings remain visible. A Council-supported position is labeled as an AI view.

## UI and report changes

The composer retains one add menu, review selector and Create action. Actual image and CSV previews sit above the question. Long input auto-grows, has a compact viewport-dependent cap and offers explicit expansion. Menus remain outside layout flow. Local selection and persisted evidence remain distinguishable, with full accessible filenames and removal controls. Image decoding/object URLs clean up through their resource lifecycle. The image hook finding was fixed without suppression.

Results lead with the descriptive answer, readable values/bars, arithmetic, coverage, source outcome and prioritized limits. The original question and detailed AI record disclose separately. Council views use structured finding titles and claim positions with legacy fallback. Reports preserve original inputs and technical details in disclosures, bound display titles, render real comparisons and support JSON plus browser printing. Existing uploads, revisions, run consent, provider administration, ownership and cancellation/recovery paths remain connected.

Visual evidence uses copied real evidence in an explicitly titled, draft-status engineering diagnostic inside a temporary private workspace. No Council request was made for these screenshots.

- [Desktop composer](composer-desktop-dark.png)
- [Floating menu](composer-menu.png)
- [Arabic mobile composer](composer-mobile-ar-dark.png)
- [Desktop findings](results-desktop-light.png)
- [Arabic mobile findings](results-mobile-ar-dark.png)
- [Readable mobile comparison](comparison-mobile-detail.png)
- [Arabic mobile report](report-mobile-ar-dark.png)
- [Visualization laboratory](laboratory-mobile-ar-dark.png)

The independent Impeccable review initially returned `fix`. Its two issues were mobile SVG text scaling and structured-only Council counts/disclosure defaults. Both were corrected. The final [scoped verdict](finish-verdict.md) is `ship` for those two fixes. Mobile label readability was inspected in captures, and Council counts/disclosure were reviewed in source. This verdict does not establish whole-product or scientific acceptance.

## Tools and checks actually used

Impeccable context, craft floor, automatic design hooks, independent finish reviewer and documenter were used. Installed Vercel React Best Practices and Web Design Guidelines guided hooks, semantic controls, focus, responsive reflow and progressive disclosure. Current guidelines were fetched from their official repository.

At the owner's authorization, Context7 4.5.1, Playwright MCP 0.0.84 and Chrome DevTools MCP 1.12.0 were installed in the user tool directory and registered with Codex. They were invoked through a local stdio MCP client. Context7 supplied Pydantic 2.14.1 documentation for the installed 2.14.2 patch family. Playwright supplied actual rendered captures and geometry. DevTools inspected live case/processing requests and reported no warning/error console messages. Browsers used isolated Chromium. The earlier unavailable-tool limitation has been resolved for this environment. Tool packages remain outside application dependencies.

Focused results are frontend build/lint, 53 existing frontend tests, production-fixture exclusion, 66 relevant backend tests and whitespace/diff checks. Regression checks cover records beyond the former excerpt, exact arithmetic, role query flow, source target/redirect/robots boundaries, extraction/retrieval distinction and ownership of new endpoints. The explicitly excluded frontend-parser subprocess scenario was outside this focused run. Synthetic providers are confined to isolated tests.

Browser diagnostics confirmed unchanged composer height while opening its menu, no horizontal overflow in the mobile composer/results/report, and an accessible action row in the inspected viewport. No paid-provider generation, scientific validation, hosted deployment, screen-reader acceptance or cross-browser campaign was performed.

## Data and rollback

There are no database/schema migrations or ownership assignments. New records carry additive versioned fields. The running backend preserves the prior environment and account mode. Activation occurred with zero active jobs and a coordinated private backup at `backend/instance/backups/2026-11-08-before-evidence-processing/`.

All 13 pre-existing record bodies retained their hashes and all 20 original file references matched their stored hashes. Historical processing remains explicitly legacy. The real saved diabetes case now has a complete-table preview with 455 rows and one derived comparison. See [preservation evidence](data-preservation.json). No restore drill was performed. Preserve later work separately before any restoration, following the canonical rollback guide.

## Documentation review and cleanup

The [documentation inventory](documentation-review.json) lists 142 discovered Markdown/MDX paths, authority treatment and review depth. Relevant canonical guides, the approved brief, product/design context, runtime prompts, scientific applicability, Council/blinding and gate sections were directly reviewed. Historical reports were retained under the existing documentation map. The inventory distinguishes direct review from discovery and makes no line-by-line recertification claim for every historical file.

The new canonical `docs/EVIDENCE_PROCESSING.md` describes supported operations, algorithms, limits and scientific boundaries. Architecture, API, workflow, scientific scope, development, deployment/rollback, documentation map, AGENTS.md, DESIGN.md and its sidecar were updated. Outdated active statements about un-fetched URLs and first-200-row consent were replaced. Dated reports, approval/gate records, scientific drafts, brand provenance and earlier rollback materials remain preserved.

No documents were merged, archived or removed during this increment. Remaining documentation decisions concern hosted source policy/security acceptance, scientific comparability/verification procedures, Blind Optics and the existing open gate register.

## Owner manual acceptance

1. Open the running workspace and the saved diabetes investigation. Inspect its complete-table preview and source filename/row references.
2. Save a new revision if needed, then explicitly authorize a new multi-perspective review. Check the new consent, actual stages, selected data, reviewer query records and real provider response.
3. Confirm the 2024 observations, 8.7-point difference, ratio, source retrieval outcome and downloadable retained snapshot. Inspect scientific coverage separately.
4. Read Council positions and disagreements, original outputs, row/hash/revision provenance, report sections, JSON and browser printing.
5. Confirm the older analyses retain their original packets/reports. Try an absent row, ambiguous selection, invalid query and blocked source URL.
6. Exercise long input, attachments, source/claim/settings popovers, keyboard dismissal, both themes and Arabic/English at desktop/mobile widths.

For a fresh local launch, use `docs/DEVELOPMENT.md`. Backend uses its existing `.venv` and Flask on loopback port 5000. Frontend uses `FLASK_DEV_ORIGIN=http://127.0.0.1:5000 VITE_API_BASE_URL=/api npm run dev -- --host 127.0.0.1 --port 5202 --strictPort` from `frontend/`. Keep provider credentials server-side. Current services are already running.
