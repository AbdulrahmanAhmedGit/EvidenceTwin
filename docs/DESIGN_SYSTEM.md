# EvidenceTwin design system

Identity: paired chart frames, explicit baselines, restrained editorial headings and precise mono labels. Chart marks always encode supplied values. A1/A2/A3 are educational examples, not live analysis results.

Light tokens: background #f7f7f1, paper #fffef9, ink #182d35, muted #626f70, teal #286c64. Dark counterparts are declared in App.css. Cobalt distinguishes data series; amber denotes missing information. Status text accompanies color.

Fonts: Newsreader, Inter, IBM Plex Mono and Noto Sans Arabic. Fonts are self-hosted through Fontsource packages; license copies are included in docs/font-licenses.

Controls have visible focus outlines; layouts use logical inline properties. Mobile shells replace side navigation with a scrollable navigation strip. Charts expose SVG labels and source values in case tables. Full screen-reader, contrast and Arabic typography review remains outstanding.

Print CSS removes navigation and controls. Browser printing is distinct from a server PDF export.

## Phase 2 refinements

Fonts now ship as local WOFF2 assets through Fontsource packages. Their license texts are retained in `docs/font-licenses/`. No external font request is needed. Public chart figures include expandable data tables. Hero, walkthrough, example audit and integration flow use authored educational inputs, with no executed AI results implied.

The page/step entrance uses a five-pixel transform without lowering text opacity. The problem-band helper text uses #566365 for sufficient contrast. Public footer links wrap on tablet widths. All motion still honors system and application reduced-motion settings.

## Phase 4 research instruments

Analysis views use shared identity/source/status lines and a collapsible evidence-context band. Evidence facts use ledger rows and explicit category selection. Numeric findings use tabular mono text with source-authentication status kept separate. The Laboratory preserves original image colors, geometry and text direction; theme changes affect the frame, not the scientific asset. Overlay requires explicit compatibility and matching loaded dimensions.

Council roles are parallel instruments with hairline separators, not avatars or consensus gauges. A disagreement ledger keeps the claim, positions and evidence visible together. Audit events use chronological rules and readable status text. Reports switch to an editorial document surface and remove navigation/controls for print.

Native controls and dialogs provide keyboard behavior and focus restoration. Slider coordinates remain LTR with the chart canvas while Arabic labels and surrounding layout are RTL. Backend narrative text uses automatic direction and retains its language. Motion is brief and functional, with no opacity reduction for essential text and no synthetic scientific progress.

## Phase 5 research instruments

Comparison uses paired A/B selection frames followed by an evidence ledger. Comparability precedes dimensional differences; missing values remain text, and neither column receives a winner treatment. Mobile stacks each pair while retaining A/B labels.

Benchmark results use a measurement ledger rather than promotional metric cards: condition, supplied value, definition, denominator and limitations remain adjacent. Missing metrics read Unavailable. Reports use a document index with a focused native-dialog preview and a separate destructive confirmation. Integration status comes from configuration and remains separate from the outcome of a connection test.

All new forms have labels, semantic groups and related error text. Native dialogs restore focus and support Escape. Controls remain keyboard operable and document direction uses logical spacing/borders. Disclosure motion lasts 160ms and is suppressed by either reduced-motion setting. Responsive filters wrap; measurement definitions move below values on small screens. The palette and local fonts are shared with the established workspace.

## Official brand artwork

Use `components/brand/BrandLogo` rather than rebuilding a wordmark from text or substituting a UI icon. Four supplied SVGs live unchanged under `public/brand/`; their shared proportions, sizing tokens, clear space, RTL/decorative accessibility rules and theme/print behavior are defined in [BRAND_INTEGRATION.md](BRAND_INTEGRATION.md). Auto selects through the active application's `.root.dark` class. Public navigation/footer, workspace sidebar/mobile header, recovery view and report masthead use this component. No palette, typography or scientific-graphic redesign accompanies the brand integration.
