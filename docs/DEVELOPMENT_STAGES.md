# Development stages and experience quality

The master frontend brief remains the acceptance baseline. Navigation, accessibility and purposeful motion are requirements throughout all five phases. All five frontend implementation stages are delivered. Backend integration and deployment remain owner work; frontend acceptance does not imply functioning scientific services. See PHASE_5_ACCEPTANCE.md for verification scope and remaining limits.

## Mandatory rule for every phase

Navigation must remain complete and keyboard accessible. Accessibility must be addressed during implementation, including focus, labels, status feedback, RTL and responsive behavior. Motion must clarify interaction, stay restrained, and respect both system and application reduced-motion settings. Each phase must test these requirements before acceptance; none may defer them entirely to final polish.

## Phase 1 — Foundation and shared navigation

Maintain semantic landmarks, localized navigation labels, current-page indicators, breadcrumbs, skip navigation, visible focus, and route focus management. Mobile menus must support keyboard access, Escape, outside dismissal, and access to all destinations. The desktop sidebar supports collapse without losing labels.

Define short motion tokens and honor both system reduced motion and the explicit workspace setting. Prefer CSS transitions for simple effects; introduce a motion library only where interaction complexity justifies it.

Gate: keyboard journeys, mobile navigation, direction switching, theme switching and reduced-motion browser checks.

## Phase 2 — Public website and documentation

Complete authored bilingual content. Make documentation navigation, search, anchor links and contents accessible. Use subtle menu/page transitions and meaningful original/neutral chart transitions. Keep all data values and accessible explanations available without animation.

Gate: public route/deep-link checks, mobile layouts, heading structure, contrast review, keyboard-only documentation journey and reduced-motion parity.

## Phase 3 — Workspace and analysis submission

Complete management workflows and field behavior. Wizard steps announce the active step and move focus to the step heading. Connect errors to inputs, preserve user data, and announce async feedback. Use short step transitions without delaying input or hiding validation.

Gate: accessible upload, keyboard-complete submission, error recovery, input preservation, touch targets, and focus after each step.

## Phase 4 — Analysis inspection and scientific tools

Complete data/evidence inspection, chart controls, Council, disagreements, audit and reporting. Provide keyboard equivalents for visual controls, chart data alternatives, clear status announcements, and accessible drawers with focus restoration. Use panel transitions and genuine processing-state changes only; never animate invented scientific progress.

Gate: keyboard and screen-reader checks of analysis flows, reduced-motion alternatives, printable reports, responsive inspectors and accurate evidence/status distinctions.

## Phase 5 — Research tools and final validation

Complete comparisons, benchmarks, reports, integrations and remaining API adapters. Inspect every primary interaction, loading/error/empty state, and responsive breakpoint in both languages and themes. Review animation timing, focus behavior, motion preferences and layout stability across routes.

Gate: full acceptance matrix, meaningful unit/E2E coverage, manual accessibility review, visual screenshots, build/lint success, and explicit record of backend-dependent gaps. Passing a small test subset does not complete this phase.

## Implemented shared improvements

- Menu Escape/outside/focus dismissal and focus restoration on Escape.
- Current page styling, workspace breadcrumbs and focus movement to new route content.
- Mobile Settings access and collapsible desktop sidebar.
- Wizard current-step semantics, step-heading focus and claim-error association.
- Page, step, menu, chart and hover transitions with reduced-motion suppression.
- Persisted motion preference applied immediately; initial document language/direction match the selected locale.

## Current work

Phase 2 is complete. See PHASE_2_ACCEPTANCE.md for delivered public routes, bilingual/light-dark accessibility checks, responsive checks and visual review evidence. Phase 3 is complete for its frontend routes and workflows. See PHASE_3_ACCEPTANCE.md for submission, drafts, settings, cases, history and validation evidence. Backend-dependent workflows were tested with request mocks; no live scientific service is claimed. Phase 4 is complete; see PHASE_4_ACCEPTANCE.md for inspection, visualization, Council, audit, report, preview-isolation and regression evidence. Phase 5 frontend work is complete. See PHASE_5_ACCEPTANCE.md for comparison, benchmarks, reports management, integration management, production fixture exclusion and the final verification record. Specialist assistive-technology/cross-browser review and live Flask validation are not claimed.

## November 3 stabilization

The audit identity-validation and comparison-preselection defects have been corrected. Report filters now restore from the URL without losing rapid edits, and native controls follow the selected theme. See FRONTEND_STABILIZATION.md for the final 33-unit/92-browser test results, development-preview checks, unchanged backend ownership and remaining real-service integration gaps.
