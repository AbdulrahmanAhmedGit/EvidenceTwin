# Frontend redesign — November 6, 2026

This report records the initial scientific-folio pass. The subsequent [motion refinement](FRONTEND_MOTION_REFINEMENT.md) supersedes its motion-stack and icon-dependency notes.

## Scope and audit

Applied the `redesign-existing-projects` workflow to the existing React/TypeScript/Vite frontend. Kept vanilla CSS, routing, adapters, form workflows, English/Arabic support, theme preferences, official brand assets and scientific content boundaries.

The audit identified repetitive panel compositions, small text, weak differentiation between controls and surfaces, and public navigation competing with workspace navigation. The chosen direction is a scientific folio: warm paper, graphite text, restrained teal, editorial headlines and fine instrument rules.

## Implemented changes

- Shared theme tokens, Manrope interface typography, deliberate radii, readable surfaces, focus/hover/pressed states and restrained motion.
- Paired homepage instrument showing identical values under two baselines; both frames retain labels, caveats and data tables. Narrow layouts stack the charts.
- Editorial public-page and documentation layouts, content-width limits, sticky desktop contents/navigation and anchor clearance.
- Dedicated workspace toolbar, icon-assisted collapsible sidebar and four-destination mobile bottom navigation. All secondary destinations remain in the keyboard-accessible header menu.
- Dashboard status rail, catalog-style case library, analysis records and explicit loading/empty/error treatments.
- Consistent styling across analysis creation, overview, evidence, Visualization Laboratory, Council, audit, report, comparison, benchmarks, report library, integrations, settings and AI-provider configuration.
- Shared accessible route-loading skeletons. Existing native dialogs, navigation focus, form validation, query lifecycles and capability checks remain intact.
- Application theme colors also update browser chrome. Official light/dark logos and favicons remain unchanged.
- Fixed development-only fixture SVG imports to use Vite's `no-inline` asset form. This preserves the existing credential-free URL policy instead of weakening validation to accept data URLs.

No backend, endpoint, scientific policy, gate register, provider configuration or official SVG changes form part of this redesign. No scientific capability was enabled and no analysis/provider execution was initiated for visual review.

## Review and verification

Visual review includes the homepage and workspace in light/dark themes; expanded/collapsed navigation; Arabic RTL; mobile navigation; analysis creation; source/evidence inspection; chart comparison; Council; reporting; and documentation. Responsive checks use 360, 390, 768, 1024, 1440 and 1920-pixel widths through the existing browser suite.

Screenshots are local inspection artifacts under `frontend/output/playwright/`, excluded from Git. Live workspace screenshots may contain existing local research records and are not published. Inspection success states use explicitly authored development fixtures or request mocks, not invented production results.

The first browser pass identified new contrast failures in sidebar numbers and sample bars, plus transient low contrast from a route fade. These were corrected. The route transition now uses movement only. Existing browser assertions were adjusted for the intentional mobile Settings menu path and the new browser theme colors; scientific and authorization assertions were retained.

Final verification:

| Check | Result |
| --- | --- |
| `npm run lint` | Passed |
| `npm test` | 8 files / 42 tests passed |
| `npm run build` | Passed with TypeScript strict checking |
| `npm run verify:fixtures` | Production artifacts exclude development scientific fixtures |
| `npm run test:e2e` | All 103 existing main browser tests passed |
| `npm run test:preview` | All 3 development-preview browser tests passed, including chart asset loading and no Flask requests |
| Focused creation/navigation rerun after step-ledger refinement | 17 tests passed |
| Print regression | Dark-screen report prints on white paper with the light official artwork |
| `git diff --check` | Passed |

The main browser suite includes axe checks in English/Arabic and light/dark themes, responsive overflow assertions, native theme behavior, keyboard navigation, scientific display boundaries, identity-mismatch recovery, report permissions and API failure recovery. These assertions passed; they are not a blanket WCAG conformance claim.

React review retained route-level lazy imports and existing Query caching/cancellation. No new API requests or query waterfalls were introduced. New iconography uses the existing Lucide dependency; Manrope is the only added runtime package. Official brand asset checks continue to pass.

The print review additionally caught a theme-specific CSS precedence issue. Print variables now override both light and dark screen themes; the existing report-brand test also asserts a white print surface.

## Remaining integration boundaries

The redesign does not establish that hosted authentication, the new PostgreSQL execution infrastructure, scientific source verification, statistical procedures, benchmarks, or MCP are integrated or enabled. Existing API/capability behavior remains authoritative. All 24 scientific/technical gates remain open.

Browser mocks validate frontend behavior and error recovery only. They do not prove real Flask scientific execution, scientific validity, hosted capacity or production accessibility certification. The current API migration, identity-provider selection and capability-specific acceptance work remain separate from this visual change.
