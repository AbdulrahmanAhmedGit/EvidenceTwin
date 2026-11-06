# Landing page redesign

## Design read and audit

Reading this as a research SaaS landing page for evidence-conscious researchers, with a precise, calm visual language. This is a visual redesign that preserves the forest-green identity, supplied logo artwork, public navigation labels, routes, English/Arabic behavior, saved theme preferences, and scientific limitations.

Dials: DESIGN_VARIANCE 7, MOTION_INTENSITY 5, VISUAL_DENSITY 4. The foundation is the project's existing React, native CSS, self-hosted Manrope/Alan Sans fonts, Solar icons and scoped GSAP runtime. No additional runtime dependency was introduced.

Before: oversized serif hero, additional text below the main action, controls below the initial desktop viewport, repeated eyebrows and numbered labels, repeated boxed explanatory diagrams. Existing metadata: EvidenceTwin Council title, evidence-inspection description, branded favicons, no structured data or OG image. No ranking or analytics service is connected, so rankings and tracking were not inferred.

After: asymmetric hero with a generated optical study, a standalone interactive educational chart, a compact principles band, a sticky research-process introduction, a four-perspective review composition, case-library links, integrations guidance and a final workspace action. Shared workspace screens retain their existing layouts.

## Assets

`frontend/public/evidence-optics.webp` and `evidence-optics-600.webp` are responsive exports of one generated conceptual illustration. The image is not an experiment, scientific measurement, customer endorsement or product screenshot. Its prompt and source attribution are recorded in `frontend/public/asset-credits.txt`. The built-in image generation tool was used. The chart is the existing accessible chart component with the supplied educational values, not a simulated product screenshot.

The image is preloaded with matching responsive sizes and stays visible while the hero enters. Landing chart colors use the existing green accent. Controls and media use a 6px radius. Theme tokens apply to the whole page. Two eyebrows appear across eight sections. CTA labels remain consistent by intent. No customer claims or fabricated metrics were added.

## Verification

- Production TypeScript/Vite build and oxlint pass.
- All 49 existing unit tests pass across 10 files.
- `git diff --check` passes.
- Browser inspected at 1440x900, 1280x720, 390x844 and 320x740. No horizontal overflow in measured desktop, mobile or Arabic layouts; the main hero action remains visible in the initial viewport.
- English light/dark and Arabic dark screenshots inspected. Arabic desktop also captured.
- Neutral-baseline control changes the chart from truncated-axis to zero-baseline presentation, retains the supplied 42%/40% values, updates pressed state and explanatory text.
- Mobile menu opens, Escape closes it and restores focus to the menu button.
- Start an Analysis navigates to `/app/analyses/new`, displaying the existing analysis builder.
- Reduced-motion emulation disables the GSAP runtime and leaves headings visible.
- Final Lighthouse production-preview mobile run: performance 97, accessibility 100, best practices 100, SEO 100. LCP 2.6s, CLS 0, total blocking time 80ms. These are local synthetic results, not deployed Core Web Vitals or real-user INP. LCP remains slightly above the skill's 2.5s target.

Artifacts: `output/playwright/landing-before.png`, `landing-desktop-full.png`, `landing-dark.png`, `landing-mobile-dark.png`, `landing-arabic-dark.png`, `landing-arabic-desktop.png`, and `lighthouse-landing.json`.

Scope notes: no form or asynchronous result flow was added to the landing page, so loading/error/empty-result states remain owned by existing product routes. No live scientific backend run was performed. Existing legal pages, URL structure, logo files and primary navigation labels were preserved. Existing unrelated uncommitted work was retained.
