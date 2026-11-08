# Capture validity

Inspected all eight current `.impeccable/review` captures: desktop/mobile default, attachment menu, empty-question validation and attached draft. These show the actual prompt-first page at desktop English/light and mobile Arabic/dark, including realistic multiline and mixed-direction draft content. Also inspected the four supplied broader captures: desktop Council, evidence, API documentation and mobile Arabic Council. No clipping, broken brand artwork or horizontal overflow is visible in these captures. Code-first Operate mode requires no image composition. The full-page mobile Council capture includes fixed navigation in its stitched image; this is not evidence of a navigation placement defect. Captures are sufficient for this review; no recapture is required before the identified source fixes.

# Direction and craft

The composer expresses the amended direction: a centered scientific question with a single paper surface, restrained forest action, quiet optional tools and compact removable evidence. It borrows a familiar composing interaction without chatbot branding. Mobile Arabic keeps the question prominent, attaches files as full-width rows and retains readable mixed-direction content. The broader dossier has a coherent source rail and reviewer-role gutter, flat separators and suitable reading rhythm. Shared type, control shapes, official logos and palette remain consistent. The documentation provenance eyebrow remains an explicit craft-floor violation and should move below the heading.

# Product/engineering/accessibility

Read PRODUCT.md, DESIGN.md, the complete surface brief including prompt-first amendment and craft-floor.md. Inspected ResearchEntry.tsx, composer-evidence.ts, research-entry.css, App.tsx, existing draft-store/AnalysisBuilder and shared precision/observatory CSS. Entry validation, accessible textarea label and error association, live attachment feedback, menu arrow/Home/End/Escape handling, focus restoration, local file removal, source URL validation and reduced-motion styling are present. Shared browser details include selection, caret, focus outlines, scrollbar color and tabular numerals.

The exact English placeholder is present. Question and existing settings write through the existing draft model. Start Investigation only navigates to preparation. XLSX is isolated in tab memory and excluded from the API file list, with explicit labels both in the composer and preparation handoff. The single URL contract is retained and source retrieval is not claimed. Existing case links enter preparation directly. No new API calls appear in the composer. Parent-reported unchanged backend/API hashes support the frontend-only boundary; this review did not independently recompute them.

The supplied browser-b-results.json records the reported 40 axe scans and 80 layout observations; its checked observations contain no reported violations/overflow. Detector output has one FilePreview image warning; actual code assigns a real object URL in an effect and revokes it, so this warning is a false positive. Full final E2E execution remains in progress at review time and must be reported by its final result, not assumed passed. This evidence is browser/fixture verification, not independent scientific validation or screen-reader certification.

# Prioritized findings

1. **P1 — Case selection unexpectedly exits preparation.** `frontend/src/features/analyses/AnalysisBuilder.tsx:33` still calls `navigate('/app/analyses/new',{replace:true})` from the educational-case selector. With the new wrapper that URL renders the composer. Selecting, changing or removing a case therefore unmounts the wizard instead of leaving the researcher in preparation. Change this internal navigation to `/app/analyses/new?prepare=1`, retaining the selected draft case; verify both choosing and clearing a case remain in the preparation step and Continue still works. Discard navigation to the bare route is intentional and should remain.

2. **P2 — Documentation retains a banned eyebrow above its title.** `frontend/src/PublicPages.tsx:12` renders `v0.1 / PROPOSED CONTRACTS` before the documentation h1; it is visible in the supplied API capture. The craft floor explicitly bans kickers/eyebrows above headings. Keep the meaningful proposed-contract qualification as ordinary provenance below the title or alongside the introductory copy, without losing that scientific/product boundary.

No additional material visual, accessibility or product-boundary issues were established by the reviewed evidence.

# Disposition

fix

The direction is sound and does not need rebuilding. Resolve the preparation route regression and documentation heading treatment, run focused regression verification, then finish with the completed full E2E result.
