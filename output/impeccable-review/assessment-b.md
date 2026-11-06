# Assessment B — independent detector and technical audit

Target: `frontend/src` in Evidence Twin; rendered product verified at `http://127.0.0.1:5194/`. Assessment B did not read or request Assessment A. Source and application state were not edited. Output artifacts only were added.

## Evidence boundary

Native CUA fresh-tab creation returned `The browser access host is unavailable`. Used a fresh Chromium browser/context/page through the project's installed Playwright package as requested. Initial 5173 title probe identified an unrelated Cortex app; no assessment of it was used. The correct 5194 server title and content were verified.

All API requests during inspection were intercepted. Non-GET requests were denied. Generic API reads deliberately returned 503 to inspect honest disconnected states. Analysis `inspection-1` used the repository's authored educational request fixtures, with original/neutral local SVG assets. These are interface evidence, not live scientific/backend execution. No AI provider was invoked, and no data was submitted/deleted.

10 routes: `/`, `/docs/api`, `/app`, `/app/analyses/new`, `/app/library`, `/app/settings`, plus evidence, visualizations, council and report under `/app/analyses/inspection-1/`.

40 desktop axe scans: all 10 routes × English/Arabic × light/dark, using WCAG 2 A/AA, 2.1 AA and 2.2 AA tags. 40 mobile/tablet layout observations across English/Arabic light mode at 360/768 CSS px. An additional 24 clean observations cover `/`, wizard and visualization in English/Arabic at desktop and 320/360/768, without injected overlays.

## Deterministic source detector — separate from confirmed defects

`impeccable detect --json frontend/src` completed; raw results in `detector-raw.json`. **8 warnings: 7 side-tab accent-border matches, 1 broken-image match. No detector errors.**

| Rule | Locations | Context verification |
|---|---|---|
| side-tab | `App.css:4`, `App.css:31`, `features/inspection/inspection.css:2`, `styles/observatory.css:86`, `styles/observatory.css:149`, `styles/workspace.css:72`, `styles/workspace.css:75` | Source pattern matches exist. They primarily signal warnings, selected references or interpreted evidence; these are not seven independent usability/accessibility defects. Several matches share densely minified lines. The detector does not establish whether an accent border is justified by its meaning. |
| broken-image | `features/analyses/FilePreview.tsx:2` | **False positive**: supported uploaded images receive an object URL through the image ref in an effect; cleanup revokes it. Unsupported types render no image. Missing static `src` is not evidence of a shipped broken image. Existing `workspace.spec.ts` specifically exercises the image preview; no test was rerun solely to duplicate that implementation check. |

## Live detector visualization

Mutable preflight succeeded on the correct app: changed title and appended/ran an inline script in the disposable page. Started the bundled live server at localhost:8400, injected `detect.js` and waited 2.6 seconds on three representative views. Console group summaries:

- Homepage: **6 anti-patterns**.
- New Analysis: **3 anti-patterns**.
- Visualization: **4 anti-patterns**.

These are DOM heuristic instances (13 across three pages), not 13 confirmed defects. Screenshots saved as `overlay-_.png`, `overlay-_app_analyses_new.png`, `overlay-_app_analyses_inspection-1_visualizations.png`. Visible labels include eyebrow, wide tracking, nested cards and accent borders. Their relevance is a design judgment; none independently proves an accessibility failure.

There is **no user-visible [Human] browser tab**. Overlay screenshots were captured headlessly. The helper was stopped successfully with `live-server stop --keep-inject`; no HTML injection/removal command was used. The root-owned app dev server was left running. Chromium browsers/contexts were closed.

Injected yellow labels themselves produced two apparent layout overflows in early mobile observations. Those are **tool artifacts**, not product findings. Clean reloads without detector injection at 320/360/768 all passed on the affected pages. `browser-b-clean-mobile.json` supersedes the initial homepage/wizard/visualization mobile records; their 360px screenshots were overwritten with clean captures.

## Audit health

| Dimension | Score | Evidence |
|---|---:|---|
| Accessibility | 3/4 | Zero axe violations in 40 desktop scans; functional skip link and menu focus return. Some compact touch targets, manual SR/high-contrast coverage incomplete. |
| Performance | 3/4 | Research route components and site motion are lazy loaded. Motion is optional and dynamically skipped for reduced motion. No runtime performance profiling or production network budget was performed. |
| Theming | 3/4 | Semantic foreground/surface/control tokens and light/dark parity pass measured text checks. Quiet button borders still use separator tokens. |
| Responsive | 3/4 | Clean reflow at tested widths and RTL; scrollable tabs preserve route access. Secondary links/header controls remain smaller than 44px comfort targets. Physical touch gestures not tested. |
| Implementation integrity | 4/4 | Consistent product-specific evidence language, explicit unavailable states, authored fixture boundaries, honest arithmetic/source-verification distinction. Detector warning count does not undermine this by itself. |
| **Total** | **16/20 — Good** | No confirmed P0 or P1 technical blocker in this sample. |

## Human-confirmed findings

**Counts: P0 0; P1 0; P2 2; P3 0.** The P2s are measured ergonomic/visual-system opportunities, not claimed WCAG AA violations.

### P2 — Compact navigation targets reduce touch comfort

Location: `App.tsx` header actions and public footer; `PublicPages.tsx` documentation on-page navigation; `styles/precision.css`/header action sizing.

At 360px, mobile header language/theme/menu hit boxes measure **40×42px**. API documentation section links measure **280×21.44px**, vertically separated by roughly 18px. Footer links on the homepage measure roughly 18px tall. These are usable and axe did not flag target-spacing failures, but they fall below the 44px ergonomic target and require more precise taps. Native checkbox visuals are 13px wide, but enclosing labels enlarge their actionable area; do not count those visuals as independent AA failures. Inline links also have applicable exceptions.

Recommendation: expand the three header buttons to 44×44 and give standalone documentation/footer links generous block padding while preserving spacing and reading density. `$impeccable adapt`, then `$impeccable polish`.

### P2 — Quiet button boundaries use separator contrast

Location: `App.css:4` baseline `button,.button` rule; `styles/precision.css` semantic control tokens and input-only override.

Computed style in the wizard: Discard draft has border **#d7ddd3**, surface **#fffefa** and surrounding page **#f6f5f0**. Border contrast is **1.37:1** against the surface and **1.27:1** against the page. The educational-case select correctly uses **#58665d**, measuring **5.99:1** against its surface. The primary Continue button measures **6.23:1** for its text/background pair. Thus inputs and quiet buttons apply different boundary strengths despite an existing control-border token.

Recommendation: decide whether outlined secondary buttons need an explicit stronger control boundary; if so, apply `--color-border-control` to those controls, reserving separator contrast for structural rules. This is a visual affordance issue. **Do not declare SC 1.4.11 failed merely from a low decorative button border where its text already identifies the control.** `$impeccable colorize`, then `$impeccable polish`.

## Verified positives and checks

- **Zero axe violations** across the stated 40 combinations; no pageerror events. Results in `browser-b-results.json`.
- All clean inspected pages reflow without document overflow at specified widths. Visually reviewed clean English/Arabic mobile screenshots; Arabic shell mirrors while chart canvas remains intentionally LTR, and source data is not silently translated/fabricated.
- First Tab on docs focuses `Skip to content` with a visible **3px #286b59 outline**; Enter focuses `#main`.
- Opening mobile navigation focuses Overview; Escape closes it (`aria-expanded=false`) and returns focus to the toggle. Results in `manual-b-results.json`.
- Inputs have explicit labels and strong control-border contrast. Primary buttons and dark/light text passed automated checks.
- Real reduced-motion implementation skips optional GSAP loading, cleans up active motion, and keeps static content available; not a 0.01ms timing hack.
- Dataset semantics include caption, scoped headers, sorting state, focusable overflow region and missing-data labels. Native range comparison also supplies increment/decrement buttons, avoiding a drag-only task.
- Disconnected dashboard states remain distinct from an empty dataset, with retry actions and no fabricated statistics.

## Limits and interpretation

No full manual screen-reader session, physical phone gesture test, browser zoom sweep, performance trace, non-Chromium run, high-contrast emulation or live populated production dataset was performed. Axe desktop passes do not certify WCAG conformance. Short link heights are not automatically AA violations because spacing/inline exceptions apply. Fixture English source text inside Arabic views is authored backend content; shell localization was verified, not translation quality for arbitrary records.

The observed 484KB main JS/104KB CSS artifacts in existing `dist` are merely existing on-disk sizes, not a freshly verified build or performance defect; no severity was assigned from them.

## Run notes

Assessment independence preserved. Ignore file was absent. Raw detector reused without parent rerun requirement. Fresh disposable browser context used; native host fallback recorded. Overlay injection succeeded only in headless capture. Helper stopped with `--keep-inject`; app server preserved. Artifact scripts/JSON/screenshots intentionally retained as reproducible evidence; no source temp files were created. No prior critique reports or Assessment A findings consulted. Questions skipped: Assessment B is delegated evidence collection; parent owns critique synthesis and user questions.
