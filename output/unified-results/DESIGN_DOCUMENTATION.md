# Unified results design documentation

Recorded on 2026-11-08 from the implemented extension and supplied captures.

## System continuity

The DESIGN.md frontmatter is byte-for-byte unchanged by this documentation pass. Existing light/dark slate and cobalt colors, Manrope and Alan Sans typography, IBM Plex Mono data role, spacing and shared component tokens remain intact. The extension uses existing semantic variables. Its local 14px results corners and 12px report corners remain composition-specific guidance.

DESIGN.md now records the results split, responsive semantic reading order, answer-first report, evidence switching, exact-value plots, compact contribution and limitation disclosures, labeled translation fallback and complete print expansion. The sidecar keeps its existing primitives and component snippets. Its overview and source-wording rule match the updated prose, and its breakpoint metadata includes the implemented 900px results stack.

## Evidence examined

Source inspection covered ResultsOverview.tsx, results-overview.css, ResearchReport.tsx, report-reader.css, evidence-processing.ts, EvidenceFindings.tsx, ReportTranslationControls.tsx, research-title.ts and precision.css. The approved brief, PRODUCT.md, direction contract, finish review and final verdict supplied the scope and capability boundaries.

Visual inspection covered diabetes-en-light-viewport.png, diabetes-ar-dark-mobile.png, report-en-light-viewport.png and report-en-light-mobile.png. These show a visible assessment beside actual evidence on desktop, the assessment → evidence → narrative order on mobile, an executive finding within the report opening and original English scientific wording within the Arabic interface. Other required captures remain listed by the finish review and verdict.

The final verdict resolves four scoped reviewer fixes and records ship for that batch. Its PDF evidence reports preservation of the original claim, evidence filename, observations, method and reproducibility records. This documentation pass inspected the print handlers and did not independently rerun printing or keyboard traversal. The parent task owns the separate live translation and execution checks.

## Boundary

This records the shipped visual extension and the supplied review outcome. Scientific verification, hosted readiness and independent accessibility acceptance require separate evidence. No pre-existing drift was repaired or promoted into new tokens. The original finish review and verdict remain unchanged.
