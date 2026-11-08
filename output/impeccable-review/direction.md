# Research dossier — frontend redesign brief

Scope: all existing frontend routes. Workspace mode: Operate. Documentation and reports: Read. Public pages retain their content and functioning demonstrations, with shared-system refinement. No new public surface or generated art is required. Existing comp-first preference remains unchanged for future landing-page builds.

The user's detailed brief establishes audience, outcome, visual constraints and permission to implement without another proposal-only stop. Product context was confirmed in the preceding init. No product decision is reopened.

## Incumbent system capture

Before redesign: warm paper #f6f5f0, forest #22352f, green #286b59; Manrope, Alan Sans, Newsreader, IBM Plex Mono. Layered App/observatory/refinement/precision/workspace/feature CSS; repeated boxed controls, three-column educational summaries, and prose assigned to monospace caption roles. Official logos remain authoritative. Original source archived in frontend-before-redesign.tar.gz; docs/DESIGN_SYSTEM.md retains the detailed incumbent record until final documentation.

## Direction exploration

Grounded systems, ordered: journal article, conference proceedings, library finding aid, peer-review matrix, standards annex, systematic review, critical edition. The roll assigned seventh (seed:5aff4d5b551031ea). The brief pins restrained editorial precision; take the critical edition's source gutter, aligned commentary and explicit provenance into familiar web controls, never into ornamental manuscript styling.

Challengers: catalog sleeve declined (coded navigation weakens clarity; keep disciplined indexing); orienteering declined (map navigation misrepresents linear research; keep separation of evidence and interpretation); design annual competitive on editorial identity, loses operational clarity (keep consistent alignment); type specimen declined (display overwhelms research; keep coherent scale); botanical folio competitive on comparison, loses category clarity (keep fixed-scale source comparison); emission rail declined (instrument costume and too little type hierarchy; keep non-color status cues). No challenger beats the pinned brief on audience identification and product clarity.

## Direction contract

THESIS: Research reads as a traceable dossier. Remove redundant framing, keep claims distinct from findings, and make reviewer comparison scannable.

OWN-WORLD: Cool paper, forest ink, sage navigation, flat separators. Manrope interface and Alan Sans Arabic; monospace only for technical content and measurements. Small square controls, clear active navigation, no gradients or decorative dashboards.

STORY: Locate an investigation, inspect its claim, follow a source, compare independent assessments, then read the recorded conclusion with its limits.

FIRST VIEWPORT: Familiar side navigation and a compact utility header; page title and primary action above aligned records. Secondary operational information recedes. Claims lead analysis inspection; references sit beside the reading column. On mobile, content stays full-width and navigation remains reachable without compressing scientific text.

FORM: Critical edition, candidate 7; seed:5aff4d5b551031ea. Signature: aligned reviewer-role gutter with evidence-linked assessments. App and reading work use code-first as required by their modes. Public composition stays incumbent; refine its shared typography, spacing and capability language.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Engineering and verification

Preserve routes, scientific semantics, API adapters, authentication, backend code and data. No runtime mock fallback. Test English/Arabic, both themes, mobile/tablet/desktop, reduced motion, keyboard/forms/dialogs, loading/error/empty states, long content and production fixture exclusion. Real browser tests use authored request fixtures only where needed, with that boundary reported.

Questions skipped: user already specified complete scope, visual direction, priorities, boundaries and instruction to proceed without a proposal-only stop.

## Prompt-first entry amendment

The user's subsequent request replaces the initial upload-first entry with a centered question composer on the existing /app/analyses/new route. Mode: Operate; code-first. The visual reference is the interaction pattern of modern research composers, not chatbot branding. No supplied screenshot files were present in this turn.

THESIS: The scientific question leads; evidence and settings are secondary, optional local draft inputs.
OWN-WORLD: Retain the reviewed paper/forest/sage identity, official logos and shared type; one restrained composer surface, no chat bubbles or decorative metrics.
STORY: Describe a claim, optionally select evidence or a source link, review local selections, then open existing preparation. No network mutation occurs at entry.
FIRST VIEWPORT: Centered heading and large multiline composer, attachments below text, plus menu and optional review settings in the lower toolbar, Start Investigation as the only primary action. On mobile text leads and the toolbar wraps without compressing the input.
FORM: Prompt-first research drafting within the existing world, superseding upload-first entry only; seed:5aff4d5b551031ea retained from the parent redesign.
FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

Existing educational-case links still open preparation directly. The original preparation flow remains on the same route with prepare=1. Existing supported files and one source URL use the unchanged draft model; planned XLSX stays in tab memory outside current API files. No backend code, endpoint, schema, auth, queue or provider behavior changes.
