# Evidence in motion — frontend refinement

## Direction

Applied `build-awwwards-quality-sites` with the compatible installed `frontend-design` skill to the existing application. The visual thesis remains a research folio: readable paper surfaces, restrained teal interaction, precise data and editorial typography. The signature is the same dataset shown under two framing choices, not unrelated imagery.

Hero focal asset: the existing labeled paired chart, with unchanged values and expandable data tables. Type: Newsreader for selected editorial headings, Manrope for interface hierarchy, IBM Plex Mono for technical details, Noto Sans Arabic for Arabic shaping. Color: paper `#f6f5f0`, ink `#22352f`, accent `#286b59`, secondary surface `#eeeee6`; existing dark counterparts remain.

Section sequence: claim/framing demonstration → evidence workflow → specialized reviewers → scientific limitation principle → illustrative audit → cases → integration concept → final action. Motion follows this sequence. No navigation labels or scientific status imply an award or recognition.

## Stack and decisions

- **GSAP 3.15.1 + ScrollTrigger:** optional route-scoped choreography loaded dynamically after semantic content. A composed hero timeline sequences heading words, the comparison frame, supporting copy and actions. Other major public headings sequence their words and copy. Research headings receive only a short bounded movement.
- **Lenis 1.3.27:** the sole installed and initialized smooth-scroll engine. Public pages use one GSAP ticker callback and forward Lenis scroll events to ScrollTrigger. Locomotive Scroll was evaluated but its additional abstraction/parallax system is unnecessary; its current documentation describes a Lenis-based implementation. It is not installed.
- **Native scrolling in research:** tables, dialogs, chart panes and all workspace routes preserve native scrolling. Touch scrolling remains native (`syncTouch: false`); wheel smoothing applies only in the public environment. No pinned or scrubbed sequence is necessary for this evidence narrative.
- **No Three.js:** shader depth would not help inspect evidence and could distract from data geometry. No canvas, render loop or decorative image generation was added.
- **Solar through offline Iconify:** individual local icon data imports replace Lucide. The offline component removes runtime icon-fetch code and remote icon requests. Existing official EvidenceTwin SVGs are untouched.

Implementation follows the official [Lenis integration guide](https://github.com/darkroomengineering/lenis), [Locomotive documentation](https://scroll.locomotive.ca/docs/) and [GSAP context cleanup documentation](https://gsap.com/docs/v3/GSAP/gsap.context()/).

## Accessibility and lifecycle

Word fragments are decorative; each split heading retains one full accessible name. Words are never hidden by CSS and remain readable in the initial frame. Links and rich inline markup are not automatically split. Arabic words retain their shaping and logical reading order.

Neither scientific numbers nor chart geometry animate. Motion changes presentation wrappers and heading transforms only, without fading essential text. Existing CSS route entrance is disabled so it cannot compete with GSAP.

Both the application Reduced setting and live `prefers-reduced-motion` changes destroy motion contexts and Lenis. Reduced mode does not import the motion runtime. Font completion, media loading, container resizing and restored pages refresh measurements. Route changes cancel pending initialization, remove listeners/observers/ticker callbacks, revert GSAP contexts and destroy Lenis. Printing clears transient transforms and retains the white report surface and official light artwork.

A JavaScript-disabled browser receives a self-contained English reading introduction with the official logo, sample data table and scientific limitations. It explicitly explains that interactive workspace functionality requires JavaScript; this is a fallback document, not server rendering of every application route.

## Asset provenance

Official logos: supplied by the owner, unchanged. Hero/case graphics: existing authored educational data graphics with explicit labels; original scientific assets are not redrawn. No avatars, fictional customers, stock imagery, partner logos or testimonials were introduced.

Solar by **480 Design**, [original collection](https://www.figma.com/community/file/1166831539721848736), distributed by [Iconify](https://github.com/iconify/icon-sets/blob/master/collections.md#solar), **[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)**. Paths are unchanged; theme color and display size vary. A public `asset-credits.txt` file is linked in the footer.

## Validation

Final verification:

| Check | Result |
| --- | --- |
| Production build / TypeScript | Passed; main chunk about 491 kB, motion runtime about 134 kB, separately loaded |
| Lint | Passed without warnings |
| Unit/component suite | 9 files, 45 tests passed |
| Main browser suite | 106 tests passed |
| Explicit development preview suite | 3 tests passed |
| Production fixture exclusion | Passed |
| Scroll-engine inventory | Only `lenis@1.3.27`; no Locomotive Scroll or ScrollSmoother |
| Diff whitespace check | Passed |

The new browser checks cover route ownership cleanup, live reduced-motion transitions, skipped motion loading under Reduced, Arabic accessible heading names, and JavaScript-disabled content. Existing checks cover keyboard menus, focus restoration, chart controls, print artwork and white paper, error recovery, capability gates, identity validation, and responsive layouts at 360/390/768/1024/1440/1920 widths. Existing axe matrices in both themes and languages passed.

Manual browser inspection captured the homepage at desktop/mobile sizes, Arabic dark mode and the JavaScript-disabled mobile document. Local screenshots are in `frontend/output/playwright/` and remain excluded from Git. The inspected public browser session reported no console errors. Browser automation also exercises the workspace and public-route matrices.

These tests use local fixtures and mocked API responses; they do not prove scientific execution or hosted backend readiness. The fallback is an English introduction; full interactive functionality and Arabic application localization require JavaScript. No award, certification or performance guarantee is implied.

## Source inventory

New presentation modules: `src/motion/MotionHeading.tsx`, `useSiteMotion.ts`, `siteMotion.ts`, component tests, `src/components/ui/Icons.tsx`, and `src/styles/refinement.css`. Public fallback/credits live in `public/reading-fallback.css`, `public/asset-credits.txt` and the `index.html` noscript document.

Existing integration points: `App.tsx`, `PublicPages.tsx`, `PublicVisuals.tsx`, `WorkspaceHome.tsx`, `main.tsx`, existing journey tests and dependency manifests. API modules and scientific contracts are unchanged.

Backend code, scientific procedures, API contracts and all 24 open gates remain outside this refinement. No paid provider calls, deployment or scientific capability enablement is part of this work.
