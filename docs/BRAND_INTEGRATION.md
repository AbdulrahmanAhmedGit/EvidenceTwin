# Official EvidenceTwin brand integration

The four owner-supplied SVGs are the sole logo artwork. This integration preserves their original bytes, paths, shapes, colors, dimensions and viewBoxes. No SVG optimization, redrawing, recoloring, mirroring or background injection was performed.

## Added files

- `frontend/public/brand/evidencetwin-logo.svg` and `evidencetwin-logo-dark.svg`: supplied full logos, viewBox `0 0 1277 298`.
- `frontend/public/brand/evidencetwin-icon.svg` and `evidencetwin-icon-dark.svg`: supplied symbols, viewBox `0 0 317 339`.
- `frontend/public/brand/favicon-16.png`, `favicon-16-dark.png`, `favicon-32.png`, `favicon-32-dark.png`: padded square raster derivatives of the corresponding official symbol.
- `frontend/public/brand/apple-touch-icon.png`: 180 × 180, official light symbol centered on the existing warm paper color with 18-pixel clear padding.
- `frontend/src/components/brand/BrandLogo.tsx`, `assets.ts`, `brand.css`, `BrandLogo.test.tsx`: reusable accessible rendering, central asset paths, sizing/theme rules and component tests.
- `frontend/scripts/generate-brand-icons.mjs`: reproducible browser SVG-to-PNG rendering with existing Playwright tooling. It measures artwork bounds and centers them without stretching or changing source artwork. No new dependency is required.
- `frontend/e2e/brand.spec.ts`: theme, browser-icon, layout, accessibility, asset and print regressions.

## Updated components and placement

- `App.tsx`: public navigation/footer and all routes using that shell; sidebar full/icon states; narrow mobile header; theme-aware browser favicons. On desktop workspace routes, branding sits in the sidebar and the global header retains a quiet Research Workspace link, avoiding a duplicate prominent logo. On mobile the sidebar logo is hidden and the header provides branding. Header/sidebar brand links retain access to the public home page; the existing Overview link retains workspace navigation.
- `App.css`: obsolete temporary wordmark/symbol styling removed; established page typography, palette, grid and navigation behavior preserved.
- `AppErrorBoundary.tsx`: application-level recovery view now identifies EvidenceTwin with the official artwork.
- `ResearchReport.tsx`: report masthead uses the official logo. Auto artwork switches to the supplied light version under print styles, matching the existing white print layout.
- `index.html`: official SVG and PNG favicon references and Apple touch icon.

The homepage uses its existing header/footer branding positions. No extra hero logos, decorative illustrations or repeated body logos were introduced. Public articles, documentation, policies and not-found pages share the global shell. Scientific content, analysis adapters, Council behavior and Flask endpoints were not changed.

## BrandLogo API

```tsx
<BrandLogo />
<BrandLogo variant="icon" theme="auto" size="md" />
<BrandLogo theme="light" width={176} label="EvidenceTwin" />
<Link to="/" aria-label="EvidenceTwin home"><BrandLogo decorative /></Link>
```

- variant: full (default) / icon.
- theme: auto (default) / light / dark. Auto follows the existing `.root.dark` application surface through CSS, not an independent OS media query. Existing theme preferences decide whether the app follows the OS. Explicit variants support fixed-color surfaces.
- size: sm / md (default) / lg. Full-logo widths: 144 / 176 / 208 pixels. Symbol widths: 28 / 32 / 40 pixels.
- width: optional numeric CSS width override; height follows the supplied aspect ratio, with a maximum width of the parent container.
- label: accessible name, default EvidenceTwin. Use decorative when a parent link or adjacent visible text already identifies the brand. Internal images have empty alt text and are hidden from assistive technology to prevent duplicate announcements.
- className: optional placement class. The component does not introduce navigation; links remain the parent's responsibility.

## Usage rules

- Use the full horizontal logo where it fits, and the symbol in the collapsed sidebar or at header widths of 380 pixels and below. Wider mobile headers retain the full logo.
- Full logos should render at least 144 pixels wide in ordinary UI; symbols at least 28 pixels. Browser icons are intentionally separate 16/32-pixel assets.
- Preserve at least 8 pixels of clear space, or one quarter of the rendered symbol height where larger. Existing header/footer/document padding and centered sidebar spacing provide this without changing the global spacing system.
- Link hit areas remain at least 44 pixels high. Brand links have contextual accessible names, existing focus outlines, and a sidebar title for the collapsed state.
- Never use CSS inversion, artwork transforms, arbitrary colors, stretching or overflow clipping. SVG width/height attributes reserve the supplied proportions and prevent image-load shifts.
- The artwork is isolated LTR with `dir="ltr"` and `translate="no"`; RTL layout may reposition its container but never reverses the mark.
- Auto instances use the light artwork for the existing light print surface, including when the on-screen application is dark.

## Browser and application icons

The HTML offers 16/32-pixel PNG fallbacks followed by the official scalable SVG favicon. The existing application theme effect updates all three favicon references immediately to match the active application preference. The Apple touch icon is a static, padded light-surface raster derived from the official symbol. It contains no full wordmark.

No web app manifest existed, so none was added. No service worker, installability claim or unrelated PWA behavior was introduced; 192/512-pixel PWA icons are not configured. If an actual manifest is introduced separately, use the official symbol and retain clear-space/aspect-ratio rules.

To regenerate committed raster derivatives:

```sh
cd frontend
node scripts/generate-brand-icons.mjs
```

This uses the already-installed Playwright Chromium renderer. The source SVG files remain unchanged. Browser/native Apple icon caching can retain an older icon until the browser or OS refreshes its cache; no cache-clearing feature was added.

## Removed scaffold branding

Removed the old Vite favicon/sprite and unused React/Vite SVGs: `public/favicon.svg`, `public/icons.svg`, `src/assets/react.svg`, `src/assets/vite.svg`. Replaced the temporary `Ⅱ` mark and text-built wordmarks in navigation, footer and report. Ordinary functional Lucide icons and research graphics remain unchanged.

## Original asset integrity

| Copied SVG | SHA-256 |
| --- | --- |
| evidencetwin-logo.svg | 427a29c5c5949bccb77694e9ba8b7ab41df30b5fb8f9ead84adc45b7e8a541dd |
| evidencetwin-logo-dark.svg | 7c3f970eb547bdde44808f890808a2bb65de679c4cedce0983b7fdff0347f397 |
| evidencetwin-icon.svg | 3f279a74322496b224810badbb33603a5951f1c177b165dfba03f5bb907f2478 |
| evidencetwin-icon-dark.svg | a5df61decb61051e0f3d3823c4c7e2c3647144833c71796a6501dd8085f92606 |

These hashes match the supplied originals byte-for-byte.

## Verification and visual review

Verified results:

- Production build and lint pass; production scientific fixture exclusion passes.
- All 36 unit/component tests pass, including BrandLogo labeling, decorative rendering, source selection, dimensions and sizing.
- The full 101-test browser regression passes (3.7 minutes), including nine brand-specific tests and prior navigation, accessibility, theme, scientific inspection and stabilization journeys. After retaining the public-home destination in the sidebar brand link, the focused expanded/collapsed keyboard-navigation check was rerun and passed.
- Brand tests cover 48 page/width/locale/theme combinations across both homepage and workspace at 360, 390, 768, 1024, 1440 and 1920 pixels. Expanded/collapsed states and mobile menu Escape/focus behavior are exercised in both languages and themes. Axe checks on desktop/mobile samples report no violations for the tested rules.
- All three isolated development-preview tests also pass: named fixtures do not call Flask, static processing does not synthesize completion, and unknown IDs retain the real API boundary.
- All nine official/derived assets load with the correct image content types and dimensions. No failed brand-asset requests or runtime page errors were observed in the brand matrix.
- A built-production preview smoke check covered eight homepage/workspace/language/theme states with zero console errors or failed requests. API reads were intercepted for these frontend-only checks. Production SVG bytes also match the original supplied files exactly.
- File-integrity checks confirm dependency manifests, API/scientific adapters and backend/Python files are unchanged; changed-file whitespace checks pass.

 Screenshots are generated under `frontend/output/playwright/brand-*`, including homepage/workspace in both languages/themes at 390/1440 pixels and collapsed sidebar states. The brand matrix also checks 360, 768, 1024 and 1920 pixels, correct intrinsic aspect ratios, and no document overflow.

Manual image review covered desktop/mobile public and workspace examples, light/dark and RTL, collapsed sidebars, and the 16/32/180-pixel derived icons. Artwork remained crisp, correctly oriented and clear against the existing surfaces; no unwanted SVG backgrounds, clipping, distortion or missing details were observed. Brand asset requests and runtime page errors are checked in the browser tests.

The brand integration introduces no scientific or backend capability. Real Flask integration and specialist cross-browser/assistive-technology verification retain the project's existing limits. No outstanding missing logo assets remain.
