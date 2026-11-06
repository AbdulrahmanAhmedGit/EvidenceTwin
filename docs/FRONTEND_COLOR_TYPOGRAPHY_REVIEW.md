# Color and typography refinement

Applied `better-colors` and `better-typography` to the existing EvidenceTwin frontend. The palette and English font families are preserved. At the owner's request, Arabic now uses self-hosted **Alan Sans**, including its Arabic subset and variable weights 300–900, through `@fontsource-variable/alan-sans@5.3.1`. The package's OFL text is retained in `docs/font-licenses/alan-sans.txt`; the [upstream project](https://github.com/alan-eu/Alan-Sans) is the source.

## Color principles

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| HIGH, resolved | `frontend/src/styles/precision.css:13`, `frontend/src/styles/precision.css:50` | Form boundaries borrowed decorative separator colors: **1.37:1 light**, **1.55:1 dark** against the actual field surface | Dedicated control-border role using an existing neutral: **5.99:1 light**, **7.67:1 dark** | Role separation: interactive boundaries meet the project's 3:1 non-text target without darkening every decorative separator. |
| MEDIUM, resolved | `frontend/src/styles/precision.css:3`, `frontend/src/styles/precision.css:11`, `frontend/src/styles/precision.css:24` | Theme literals and short aliases did not expose primitive/semantic tiers | Existing hex values organized as consumed neutral/accent/status/data primitives, semantic roles and compatibility aliases | Name values by hue and semantics by job; independently theme surfaces, secondary text, controls and accent text/fills. No new palette ramp or hue migration was needed. |
| LOW, resolved | `frontend/src/App.tsx:34`, `frontend/src/styles/precision.css:17` | Authored case chart series used inline color literals | Same colors through `--color-data-series-a/b` | Preserve categorical data encoding while centralizing its role. Supplied scientific image assets remain unchanged. |

Measured sampled text pairs did not fail the project's 4.5:1 normal-text target. No palette hue was changed to obtain a different aesthetic. Decorative separators intentionally remain lighter than control borders. Compatibility aliases remain for established feature styles; original brand SVG colors and backend-supplied image/legend colors are not application-theme tokens.

### Rendered measurements

The browser resolved each foreground and ancestor background, composited alpha where present, and calculated WCAG 2 relative luminance with the sRGB transfer function. These are actual sampled pairs, not values estimated by eye. Text samples are opaque; the field surface is the nearest painted background.

| Sample | Light | Dark |
| --- | ---: | ---: |
| Primary text on page | 11.89:1 | 14.25:1 |
| Secondary text on page | 5.54:1 | 8.62:1 |
| Chart caption on paper | 5.99:1 | 7.67:1 |
| Primary action label on its fill | 6.23:1 | 8.60:1 |
| Field text on field surface | 12.86:1 | 12.69:1 |
| Field border on field surface, after | 5.99:1 | 7.67:1 |

Local measurement artifacts: `frontend/output/playwright/color-type-before.json` and `color-type-after.json`. They cover the homepage, methodology and analysis builder in both languages and appearances at 390 CSS pixels. These figures must not be generalized to every unmeasured pair. The existing axe page matrices provide additional automated coverage of both themes.

## Typography principles

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| MEDIUM, resolved | `frontend/src/styles/precision.css:72` | Mobile fields computed to 14px | Natural 1rem fields: 16px at the default root, 32px at 200% text scaling | Avoid undersized mobile editing text without scaling transforms or shrinking hit areas. This is the recommended routine implementation choice under the owner's standing decision instructions. |
| MEDIUM, resolved | `frontend/src/styles/precision.css:20`, `frontend/src/styles/precision.css:39`, `frontend/src/styles/precision.css:41` | Numerous pixel sizes; sampled captions as small as 10px and eyebrows at 9px | Rem-based dimensions and explicit body/interface/caption/label roles; long-form text 1rem with a 68ch cap; technical labels 0.75rem and supporting captions 0.8125rem | Type roles, browser font preferences and readable small text. Dense professional interface text remains smaller than long-form reading text by design. |
| MEDIUM, resolved | `frontend/src/styles/precision.css:37`, `frontend/src/styles/precision.css:60` | Analysis titles could wrap with tight leading; report H2 could exceed its enclosing analysis H1 | Analysis title leading 1.4; report title H2 2.25rem; Arabic heading leading 1.6 | Heading hierarchy and sufficient leading for wrapped scientific titles. |
| LOW, resolved | `frontend/src/App.css:3`, `frontend/src/styles/precision.css:86` | Static mono regular bytes incorrectly declared a 400–500 range | Correct 400 declaration plus an actual 600 WOFF2 face for semibold technical values | Load the weights actually used rather than mislabeling a static face. |
| LOW, resolved | `frontend/src/styles/precision.css:22`, `frontend/src/styles/precision.css:58` | Tabular digits inherited throughout prose | Proportional prose; tabular values on tables, statistics, timestamps, pagination and changing metadata | Numeric stability where it matters without imposing table typography on prose. |
| LOW, owner-directed | `frontend/src/main.tsx:8`, `frontend/src/styles/precision.css:68` | Noto Sans Arabic; redundant historical Inter font payload | Alan Sans Arabic; Manrope/Newsreader/IBM Plex Mono retained for their existing English/data roles | Requested Arabic family, with the unused Inter and Noto font packages removed. No English typeface was substituted. |

Tracking is now relative, text remains selectable, underlines use font metrics, and document language/direction and mixed-direction value handling remain intact. Original visualization SVG coordinate text and immutable uploaded assets are outside UI type-unit conversion.

## Browser verification and limits

- Browser font inspection reports a **custom Alan Sans** font supplying Arabic heading glyphs; computed heading and field families use `Alan Sans Variable`. The variable file's base PostScript name includes `Light`; this is not a claim that all text renders at weight 300. Computed weights and the package's variable range govern selection.
- Thirty reflow checks passed without document overflow: English/Arabic × homepage, methodology, API docs, builder and settings × 320px, 640px with 200% text scaling, and 1440px.
- Mobile documentation, builder and settings controls computed to 16px in both languages. The new regression checks both theme contrasts, the Arabic family and 200% field scaling.
- Screenshot inspected: `frontend/output/playwright/alan-arabic-mobile.png`. Existing automated screenshot matrices additionally cover the public and research routes at 360/390/768/1024/1440/1920px, both themes and both languages.
- **Not verified:** physical iOS Safari auto-zoom behavior, real assistive-technology reading, and every operating-system fallback font. The mobile font-size prerequisite is verified; this is not a Safari-device test or blanket accessibility certification.
- Native control menus and scientific image contents are not recolored or re-typeset by this pass. No backend, scientific policy, capability gate or official logo artwork changed.

Final validation:

| Check | Result |
| --- | --- |
| Lint | Passed without warnings |
| Production build / TypeScript | Passed |
| Unit/component tests | 9 files, 45 tests passed |
| Full browser suite | 106 tests passed |
| Focused brand/journey rerun, including the new Alan Sans/control-contrast/text-scaling regression | 23 tests passed |
| Development-preview suite | 3 tests passed |
| Production fixture exclusion | Passed |
| Diff whitespace validation | Passed |

The focused run includes the new regression not present when the full suite began, for 107 distinct browser tests covered overall. Repeated tests are not additional distinct cases. Both theme/language axe matrices and all existing scientific-boundary assertions passed. These are frontend checks, not proof of backend execution or scientific verification.

**Approve — for the inspected color roles and typography; no HIGH finding remains in that inspected coverage.**
