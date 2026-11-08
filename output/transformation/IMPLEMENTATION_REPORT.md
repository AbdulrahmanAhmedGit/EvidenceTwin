# EvidenceTwin Council transformation — 2026-11-07

## Delivered scope

Implemented a working full-stack local research workflow around persisted cases and immutable evidence revisions, with optional invite-only accounts and actual existing exploratory Council/report services. This is an application implementation, not a disconnected visual prototype. It is also **not a completed or deployed hosted scientific-verification pilot**. The 24 scientific/operating gates remain open. Final product acceptance belongs to the owner.

The app is running at **http://127.0.0.1:5202/app**, with Flask on loopback port 5000 and the original private data directory. The temporary fixture server is stopped. No paid provider request, infrastructure purchase or cloud deployment was performed.

## Initial problems

Browser inspection reproduced `Start Investigation → ?prepare=1 → AnalysisBuilder`, a five-step upload-first wizard. Entry only changed browser state; it neither saved a case nor uploaded evidence. XLSX selections stayed outside backend inputs. `/api/cases` held labeled educational examples, not researcher cases. Creation required a configured provider and immediately started review. Shared provider administration and record access lacked built-in account roles/ownership. The navigation overexposed unavailable benchmark and future integration work, settings mixed ordinary preferences with developer controls, and the inherited palette remained green/sage.

Documentation contained contradictory frontend-only/backend-unavailable/auth-unavailable claims and overlapping historical design/acceptance reports. The full inventory and authority/depth record are linked below.

## New research journey

1. **Question:** enter the original question or claim in a compact composer. The primary action stays inside the composer, including on mobile. Files and a source link are optional for saving.
2. **Save:** Start Investigation persists the actual case, metadata and selected original bytes. Only confirmed server acceptance opens the saved workspace. No wizard handoff remains, including old `?prepare=1` URLs.
3. **Evidence and claims:** edit in the same workspace. Save a new full revision with a current-revision precondition. Previous text/files/hashes remain inspectable. Retained originals can be downloaded; image previews and the reused paginated CSV/JSON table work before any AI call. Additional claims and study context use disclosures.
4. **Investigation:** when the operator-configured service is available and evidence is saved, explicitly confirm external processing. Run requests bind a saved revision and UUID receipt; repeat receipt replay returns the accepted analysis instead of creating another run.
5. **Findings:** follow recorded execution, cancellation/retry support, independent model-call records, cross-review, judge contribution and unresolved disagreements. AI interpretations remain distinct from scientific assessment.
6. **Report:** retrieve supplied report sections, inspect evidence references, download actual report JSON or print/save PDF with the browser. No server PDF generator is advertised.

Research home, new investigation, saved cases, Council reviews and reports are the primary destinations. Educational examples remain labeled/read-only and separate. Ordinary researchers do not administer providers. Supported local-draft text and files survive same-tab navigation. Opt-in browser text now restores only for the authenticated account; prior local drafts remain confined to local mode. Late save responses cannot clear another account's draft or cache private results there.

## Visual and frontend changes

The shared semantic palette now uses slate neutrals, cobalt actions, white light surfaces and graphite dark surfaces. Light page/ink/accent are `#f6f7fa` / `#202737` / `#3159bb`; dark equivalents are `#11151c` / `#eef1f7` / `#9ebaff`. Semantic warning/danger colors retain written state labels. Fourteen representative token text/background pairs have contrast ratios of at least 5.57:1; this is a token calculation, not an exhaustive rendered accessibility audit.

Manrope/Alan Sans remain self-hosted. Layout uses flat records, restrained separators, readable text measures and logical properties. The official four SVG hashes still match their supplied originals. No logo recoloring, mirroring, redrawing or new generated artwork occurred. Existing public composition inherits the new shared tokens; a new landing-page composition was not built.

React Router and TanStack Query retain route/data responsibilities. New case/session adapters validate responses; stable external-store subscriptions retain drafts. Research/case/inspection modules stay split by route. Raw inspection JSON moved into secondary reproducibility details; header job IDs were removed. Existing scientific content is not automatically translated. Loading, empty, unavailable and error states reflect actual operations rather than fabricated progress.

## Backend/API, storage and security

- Added `/api/session` and login/logout, optional invited accounts, signed HttpOnly/SameSite/API-scoped sessions, persisted login throttling and account revocation. Account administration has a standalone CLI that does not contend with the running worker lock.
- Added `/api/research-cases`, immutable revisions, authorized original files/table reads and explicit-consent review submission. Case/run acceptance and replay receipts persist atomically through `Store.put_many`.
- Centralized record ownership checks cover lists, counts, cases/revisions, analyses, files, reports, audit/activity, comparisons and actions. Operator authorization is enforced server-side for provider configuration and operational integrations.
- Retained the actual local provider transports, ingestion, independent-call orchestration, cancellation, failed/interrupted-job recovery, retry histories, reports and isolated PostgreSQL execution package. The HTTP path was not cut over to PostgreSQL.
- Original Unicode filenames are preserved; generated file IDs control storage paths. Format/size/row/image limits, duplicate hashes, credential-free HTTP(S) reference URLs and origin checks remain enforced. Source URLs are not fetched, so no source-retrieval/SSRF capability was added.
- Provider credentials remain server-side private configuration. Researchers authorize external processing of claims/study context, supplied images and up to 200 dataset rows. PDF contents are stored without extraction or model transmission.

No destructive schema migration occurred. New JSON record kinds (`research_case`, `case_revision`, `account`, `login_limit`) coexist with existing rows. Pre-task unassigned records are operator-only under accounts mode. New local-mode rows have `ownerId=local`; they are not silently imported into an account. Team/supervisor sharing and reviewed ownership migration remain unimplemented.

A private rollback copy exists at `backend/instance/backups/2026-11-07-before-transformation/`; original code is preserved in `output/transformation/source-before.tar.gz`. Original workspace analysis count remains 2 and both record bodies match the backup exactly. Diagnostic browser cases were confined to `/tmp/evidencetwin-inspection-jv7s2O`. No restore drill is claimed.

## Removed/consolidated UI and code

Removed the actual `AnalysisBuilder.tsx` wizard, unused old dashboard component and planned-XLSX composer adapter. Replaced the disconnected entry with persisted preparation. Removed unavailable benchmark creation from primary navigation, removed educational-to-production submission controls, removed ordinary settings' dead exports/notification placeholders/verified-mode selection, and separated provider administration. Case-linked reports/reviews are retained rather than exposing deletion that would break provenance. Legitimate backend diagnostics, audit, historical records and execution infrastructure remain.

No synthetic production results or replacement API-success fallback was added. One existing development fixture incorrectly classified missing inputs as contradiction; it now retains them as unresolved missing information, with no fabricated contradicting evidence. Educational and development data remain explicitly labeled and isolated.

## Skills and tools actually used

- [Impeccable](../../../../.agents/skills/impeccable/SKILL.md): actual context loader, direction seed, new-work/craft-floor/polish guidance, one detector scan, fresh independent finish reviewer and documenter. The initial review required fixes; its verdict scores all three findings resolved at the fix-list scope. See `finish-review.md` and `finish-verdict.md`.
- Installed Vercel React Best Practices and Web Design Guidelines: component/state/fetching/accessibility review. Current [Web Interface Guidelines](https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md) were fetched. Official [React store guidance](https://react.dev/reference/react/useSyncExternalStore), [Flask security guidance](https://flask.palletsprojects.com/en/stable/web-security/) and [Werkzeug security utilities](https://werkzeug.palletsprojects.com/en/stable/utils/) informed version-sensitive choices.
- Installed Playwright CLI with Brave: reproduced old routing, inspected real Flask saving/upload/revision/reload in disposable storage, and visually inspected English/light desktop plus Arabic/dark mobile and labeled inspection fixtures. It was implementation feedback, not a comprehensive acceptance campaign.
- Dedicated Context7 MCP, Playwright MCP and Chrome DevTools MCP were not exposed. No use is claimed. Native documentation/browser/network tools were used instead. No external messaging or paid infrastructure was used.

## Engineering evidence and limits

Passed: TypeScript/Vite production build, lint, production fixture exclusion,53 frontend unit/component checks, 53 focused backend runtime/provider/case checks. After the standalone account CLI addition, the expanded five-case integrity/CLI checks passed; this brings the distinct focused backend set to 54 checks, **not one final 54-test invocation**. Python compilation, official logo hashes and `git diff --check` passed. The design detector reported no findings on its scanned source targets.

Browser-observed real operations: case save, CSV attachment/revision, refresh restoration, saved-table read and honest no-provider state in disposable storage. Council/evidence/report visual inspection also used labeled development fixtures. Existing original historical records were read/preserved, not newly scientifically revalidated. No live-provider generation, independent scientific verification, large E2E suite, deployment, physical-device, specialist screen-reader or cross-browser acceptance was performed. Older broad E2E specs were preserved rather than disabled; they need deliberate adaptation to the changed journey.

## Documentation deliverables

Read [the documentation map](../../docs/DOCUMENTATION_MAP.md) and [post-implementation audit](documentation-audit.md) for per-family conflicts and review depth. [The inventory](documentation-inventory.json) and [review manifest](documentation-review-manifest.json) list individual documents. Current entry points/source were directly reviewed; older scientific/history families were inspected by status/decision/boundary sampling, not claimed line-by-line revalidated.

Seven canonical guides now cover authority, architecture, development, API, product workflow, scientific scope and deployment/rollback. Root/module READMEs, service README, AGENTS, DESIGN and Impeccable sidecar were updated. Six overlapping guides were merged into those references and archived with pointer files: FRONTEND_ARCHITECTURE, INTEGRATION_GUIDE, DESIGN_SYSTEM, BACKEND_SKELETON_REFERENCE, DEVELOPMENT_STAGES and FRONTEND_API_CONTRACT. See [archive/hash manifest](documentation-archive-manifest.json). No unique historical or scientific documentation was removed outright. Baseline requirements, approval history, dated verification, brand provenance, scientific designs and isolated-infrastructure evidence remain.

Unresolved documentation/product questions: approved scientific methods/status/schema/source policies, historical Ember identity/chart access, account ownership migration, hosted identity/team boundaries, retention/deletion, durable HTTP-worker cutover, spend limits, hosted restore/operations and pilot acceptance.

## Launch and manual acceptance

The app is already running at http://127.0.0.1:5202/app. To restart locally, use two terminals:

```sh
cd '/home/abdulrahman/Desktop/Evidence Twin/backend'
EVIDENCETWIN_CORS_ORIGINS=http://127.0.0.1:5202 .venv/bin/python -m flask --app evidencetwin_backend:create_app run --host 127.0.0.1 --port 5000 --no-debugger --no-reload
```

```sh
cd '/home/abdulrahman/Desktop/Evidence Twin/frontend'
FLASK_DEV_ORIGIN=http://127.0.0.1:5000 npm run dev -- --host 127.0.0.1 --port 5202 --strictPort
```

For account-mode setup and private operator invitations, see [DEVELOPMENT.md](../../docs/DEVELOPMENT.md). Local mode is single-user/loopback; optional accounts do not establish hosted readiness.

Owner checklist:

- Save a question without a provider; refresh and reopen it. Confirm no legacy wizard appears.
- Attach your CSV/chart, inspect the saved table/original download, revise inputs, and inspect both old and new revisions.
- Confirm unavailable Council service is honest. With a deliberately configured real provider, authorize a review, inspect actual status/findings/disagreements, and exercise supported cancellation/retry.
- Retrieve an available real report, inspect references, download JSON and print/save PDF through the browser.
- In account mode, use two researcher accounts: verify case/file/report isolation, separate browser drafts, sign-out/revocation and denial of provider administration.
- Inspect English/Arabic, light/dark, narrow screens, keyboard focus, empty/error states and the distinction between AI interpretation, missing evidence and scientific verification.

Remaining infrastructure/scientific blockers are explicit in [SCIENTIFIC_SCOPE.md](../../docs/SCIENTIFIC_SCOPE.md) and the gate register. No fully verified hosted pilot is claimed.
