# EvidenceTwin frontend redesign and prompt-first research entry

## Delivered experience

The existing `/app/analyses/new` route opens a centered research composer. A scientific claim or question leads the screen, with attachments and review preferences in a secondary toolbar. English and Arabic have authored copy, self-hosted typography and semantic document direction; entered research text uses automatic paragraph direction and technical URLs remain LTR. Light and dark themes use the same semantic roles.

The `+` menu exposes CSV/XLSX data, PNG/JPG images and a source URL. Local selections have compact removable items. Keyboard menu navigation supports arrows, Home/End and Escape with focus restoration. Empty questions and invalid URLs receive field-associated errors. File type, 20MB and duplicate validation preserve existing inputs. Ctrl/Cmd+Enter opens preparation without treating ordinary Enter as submission. Loading reflects actual route transition rather than simulated analysis progress.

`Start Investigation` opens existing preparation with `?prepare=1`. Existing educational `?case=` links still open preparation. Existing supported files, claims, source URL, mode and depth use the existing draft store and unchanged contracts. Changing an educational case stays in preparation. No prompt-entry action creates a case, uploads evidence, calls an AI provider or executes Council work.

## Frontend-only boundaries

- XLSX selections are explicitly labeled frontend-only, retained in tab memory, shown at handoff, and excluded from the existing API file list. Parsing and backend XLSX integration remain later work.
- A source link is stored locally without retrieval or authenticity claims. The existing single-source-URL draft contract is preserved.
- Local file objects do not survive browser refresh. Existing explicit opt-in text persistence remains in force; no new automatic research persistence was introduced.
- Existing final preparation/submission behavior remains capability-gated. The new entry does not bypass it or fabricate successful acceptance.
- Backend Python and API adapter fingerprints were checked against the pre-change baseline and remain unchanged. Dependency manifests also remain unchanged from that baseline.

## Shared design improvements

The preceding full-frontend review and redesign established a research-dossier language: cool paper, forest ink, sage navigation, clear 4px controls and flat records. Monospace is reserved for code/data rather than explanatory prose. Council roles align beside evidence-linked assessments; disagreement, source status, arithmetic and claim assessment stay distinct. The evidence inspector has a desktop source index and mobile select. Repeated unavailable dashboard summaries and duplicate connection labels were reduced. The five-step preparation flow has an explicit current-step/total label on mobile, early submission availability, and preserved validation/focus behavior.

All route families were reviewed. Public composition and useful educational chart demonstrations were preserved while typography, capability language and intermediate-width reflow were corrected. Official brand artwork is unchanged. `DESIGN.md` and `.impeccable/design.json` document the current implemented tokens/components; the older `docs/DESIGN_SYSTEM.md` remains a historical reference.

## Impeccable workflow and evidence

- Init context was confirmed with the user before this work; no product facts were invented or reopened.
- Independent critique A and detector/browser assessment B were completed. Baseline design review: 24/40. The initial technical audit found no sampled P0/P1 accessibility blockers, but identified touch-target and secondary-control-boundary improvements.
- Shape/new-work established the direction contract in `.impeccable/surfaces/frontend-src-app-tsx.md`. The user's detailed scope and instruction to proceed supplied the implementation direction; no redundant approval stop was inserted.
- Operate/Read surfaces were code-first per Impeccable. The existing public composition was refined; no new marketing comp or artwork was created. The stored comp-first preference for future landing-page builds remains unchanged.
- Layout, typeset, distill and craft-floor guidance informed implementation. Polish/technical review addressed actual findings. The native browser host returned unavailable; real Chromium through Playwright supplied live rendered iteration. Detector overlays were captured headlessly, never represented as a user-visible live-picker session.
- Final source detector: one known false positive in the unchanged FilePreview object-URL effect; no remaining accent-border findings.
- Independent finish review identified the preparation case-selector route regression and a docs pre-heading label. Both were corrected and received targeted verification.

## Verification

Final results: **51 unit tests, 132 unique browser tests, and 3 isolated fixture-preview tests passed**. The main browser process reached the tool execution limit after 125 passing checks; a completion batch passed eight checks, covering the seven remaining unique tests plus a repeated targeted regression. No tests remain unverified in the 132-test inventory. These were batched results, not one final uninterrupted 132-test invocation.

Production build, lint, production fixture exclusion and `git diff --check` passed. The final independent browser audit completed 40 axe scans with no detected violations, 80 sampled layout observations with no document overflow, and no page errors. The broader browser matrix covers all 33 listed public/workspace/inspection routes at 320/768/1440 in English/Arabic and light/dark; composer-specific checks additionally cover 390 and 1920 pixels. Both finish-review findings were resolved and independently verified; disposition is ship for that review scope.

All 49 protected backend/API source fingerprints, both dependency manifests and the four original official SVG hashes match their recorded baselines. Scientific and backend integration claims are intentionally excluded: request mocks and authored educational fixtures test frontend behavior only.

## Important files

Composer component: `frontend/src/features/analyses/ResearchEntry.tsx`.
Local planned-evidence boundary: `frontend/src/features/analyses/composer-evidence.ts`.
Composer layout/states: `frontend/src/features/analyses/research-entry.css`.
Route integration: `frontend/src/App.tsx`.
Existing preparation compatibility: `frontend/src/features/analyses/AnalysisBuilder.tsx`.
Shared tokens/components: `frontend/src/styles/precision.css`, `frontend/src/styles/observatory.css`.
New browser suites: `frontend/e2e/research-entry.spec.ts`, `frontend/e2e/dossier.spec.ts`.

All source paths changed or added during this task (compared with the saved pre-change archive):

- `frontend/src/App.tsx`
- `frontend/src/AnalysisWorkspace.tsx`
- `frontend/src/PublicPages.tsx`
- `frontend/src/main.tsx`
- `frontend/src/LandingPage.tsx`
- `frontend/src/App.css`
- `frontend/src/motion/siteMotion.ts`
- `frontend/src/motion/useSiteMotion.ts`
- `frontend/src/styles/precision.css`
- `frontend/src/styles/observatory.css`
- `frontend/src/styles/workspace.css`
- `frontend/src/styles/refinement.css`
- `frontend/src/styles/landing.css`
- `frontend/src/features/analyses/ResearchEntry.tsx`
- `frontend/src/features/analyses/composer-evidence.ts`
- `frontend/src/features/analyses/AnalysisBuilder.tsx`
- `frontend/src/features/analyses/composer-evidence.test.ts`
- `frontend/src/features/analyses/research-entry.css`
- `frontend/src/features/research/Benchmarks.tsx`
- `frontend/src/features/research/Comparison.tsx`
- `frontend/src/features/research/Reports.tsx`
- `frontend/src/features/research/research.css`
- `frontend/src/features/research/Integrations.tsx`
- `frontend/src/features/inspection/VisualizationLab.tsx`
- `frontend/src/features/inspection/CouncilView.tsx`
- `frontend/src/features/inspection/inspection.css`
- `frontend/src/features/inspection/EvidenceInspector.tsx`
- `frontend/src/features/settings/AIProviderSettings.tsx`
- `frontend/src/features/workspace/ResearchDashboard.tsx`
- `frontend/src/components/ui/Icons.tsx`

## Review artifacts and rollback

- `.impeccable/review/`: current desktop/mobile composer, menu, validation, selected-file and corrected-preparation/docs screenshots.
- `output/impeccable-review/`: independent reviews, raw audit JSON, detector output, protected fingerprints and test/build logs.
- `output/impeccable-review/frontend-before-redesign.tar.gz`: exact pre-task source, entry HTML, manifests and previous design-system document. Restore selected files from this archive for rollback; it preserves the worktree state that predated this task. It does not contain private backend data or credentials.

## Limits

No backend deployment, live scientific verification, external source retrieval, physical-device or specialist screen-reader certification was performed. Automated axe and Chromium checks do not certify every accessibility/browser/device combination. Existing backend scientific and hosted-pilot limitations remain unchanged. The prompt-first backend integration is deliberately deferred to the next phase.
