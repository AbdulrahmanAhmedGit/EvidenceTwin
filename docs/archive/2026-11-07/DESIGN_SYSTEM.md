# EvidenceTwin design system

## Scientific folio

The November 6 frontend redesign uses an editorial public website and a compact research instrument workspace. Paired chart frames, explicit baselines, fine rules, and technical labels establish the identity. Original scientific assets retain their colors, proportions and data. A1/A2/A3 remain explicitly educational examples.

The existing React/Vite application and vanilla CSS remain in place. `frontend/src/styles/observatory.css` defines the shared visual layer over the existing structural and feature styles. Scope new visual selectors beneath `.root` so route-loaded feature styles cannot accidentally replace the theme. Functional data and adapters belong outside this layer.

## Tokens

| Purpose | Light | Dark |
| --- | --- | --- |
| Background | `#f6f5f0` | `#14221f` |
| Paper | `#fffefa` | `#1b2c27` |
| Secondary surface | `#eeeee6` | `#20352d` |
| Primary text | `#22352f` | `#edf0e7` |
| Secondary text | `#58665d` | `#afc0b4` |
| Separator | `#d7ddd3` | `#354b3e` |
| Interaction | `#286b59` | `#a3cbb1` |
| Accent surface | `#e4ede4` | `#283f32` |
| Text on accent | `#fffefa` | `#14291d` |
| Uncertainty | `#92621d` | `#e3be79` |
| Error | `#9d4036` | `#f0afa0` |

Amber and red accompany explicit status text. Color alone never indicates scientific correctness. Chart series may use cobalt and teal independently of interaction colors. Never recolor a supplied original chart to fit the application theme.

The base spacing rhythm is 4/8/12/16/24/32/48 pixels. Controls have a 6-pixel radius; document and instrument surfaces use tighter 3–5-pixel corners. Shadows are subtle and reserved for the hero instrument, document and dialog surfaces.

## Typography

- Manrope: interface text and workspace headings, with medium and semibold hierarchy.
- Newsreader: selected public headlines, editorial callouts and reviewer titles.
- IBM Plex Mono: identifiers, statistical values and computational details.
- Alan Sans: Arabic shaping and headings; Arabic receives its own line-height and tracking rules.

Fonts are self-hosted through existing Fontsource conventions. License texts, including Manrope's OFL, are in `docs/font-licenses/`. Unused Inter and Noto packages have been removed; the shared English interface uses Manrope and Arabic uses Alan Sans. Data uses tabular numerals. Paragraphs have bounded reading widths, and headings use balanced wrapping.

## Layout and navigation

Public pages use a restrained header, editorial content grid and compact footer. The homepage compares the same supplied 42% and 40% values under two baselines. Selecting a presentation highlights its frame without changing the values. On narrow screens, the charts stack for legibility. Figure data remains available as accessible tables.

The desktop workspace has a fixed 244-pixel sidebar (218 at intermediate widths), an 82-pixel collapsed state, and a dedicated workspace toolbar. Expanded navigation uses the official full logo; collapsed navigation uses the official symbol and retains accessible link names. Public product navigation does not compete with research navigation.

At 760 pixels and below, four primary destinations move to a safe-area-aware bottom rail. The header menu contains every workspace destination, including Settings and Documentation. Escape restores menu-toggle focus, route navigation closes the menu, and the main landmark receives focus. The service inventory stacks or uses two compact columns as space permits.

Case lists use a catalog composition: figure, scientific context, source limitations, then action. Forms use grouped paper panels and a clear step ledger. Evidence uses inspectable ledgers; Council reviewers use parallel instruments without avatars or consensus scores. Comparison preserves A/B labels and comparability warnings. Reports use a publication surface with an on-page index.

## Interaction and accessibility

Controls retain native semantics and visible 3-pixel focus outlines. Primary controls target at least 44 pixels; smaller secondary controls retain appropriate spacing. Pressed controls move one pixel. Native dialogs preserve Escape and focus restoration. Source and status labels remain textual.

Route entry uses a short vertical transform without fading essential text. Skeletons represent loading structure only; they contain no fabricated research records. The existing operating-system and application reduced-motion preferences suppress animation and transitions. Anchored sections have clearance for the sticky header.

Use logical inline/block properties for layout. Brand artwork remains LTR and is never mirrored. Scientific canvases and sliders retain the direction needed to preserve chart geometry, while surrounding controls follow document direction. Backend narratives retain their original language.

## Scientific display boundaries

Arithmetic, source authentication, model interpretation, missing evidence and unresolved disagreement remain separate. Frontend view controls never produce a scientific verdict or a verified Neutral Twin. Missing assets receive explicit error states. Capability-dependent actions continue to depend on the existing backend contracts.

Printing removes navigation and controls, uses a white document surface, and selects the light official artwork. Browser printing remains distinct from a server-generated PDF export.

## Official artwork

Use `components/brand/BrandLogo` and the four supplied SVGs unchanged. Sizing, accessible labels, decorative use, theme selection and icon generation are documented in [BRAND_INTEGRATION.md](../../BRAND_INTEGRATION.md). Application theme selects the artwork through `.root.dark`; operating-system preference alone does not override an explicit theme.

For redesign scope and verification evidence, see [FRONTEND_REDESIGN.md](../../FRONTEND_REDESIGN.md).

## Motion refinement

The subsequent `build-awwwards-quality-sites` pass adds the [Evidence in motion system](../../FRONTEND_MOTION_REFINEMENT.md): optional GSAP choreography, one Lenis instance on public reading pages, and native scrolling throughout research workspaces. Initial content remains readable; scientific values and chart geometry do not animate. Split headings preserve a single accessible name. Live system/application reduced-motion changes tear down the runtime.

Interface symbols now use individually bundled Solar data through Iconify's offline component, replacing the former Lucide dependency. Public attribution is available from the footer. Official brand artwork is unchanged. A JavaScript-disabled English reading fallback supplies a useful introduction and sample data without pretending that interactive research functions are available.

## Color and type precision

The [measured color and typography review](../../FRONTEND_COLOR_TYPOGRAPHY_REVIEW.md) records the current semantic token layer in `styles/precision.css`, rem-based reading roles, independent control boundaries, and self-hosted Alan Sans for Arabic. Existing palette values and official artwork remain unchanged. Actual contrast values and verification limits are documented in that review.

## Workspace composition (November 2026)

Use `WorkspacePrimitives` for page headings, actions, buttons and state panels. Prefer children composition and explicit dashboard/history components. Preserve backend mutations in the page controller, with controlled record views and pagination.

The workspace uses 6px control and 10px grouped-surface radii, 16/24/32px primary spacing, subtle separators, and the existing semantic color roles. Dashboard summaries form one ledger rather than separate decorative cards. Secondary service information follows the main research content on narrow screens. History preserves full titles and becomes a stacked record layout below 900px; search/filter controls adapt independently. All workflow graphics include text equivalents and explicit scope. Never use execution completion as scientific verification.
