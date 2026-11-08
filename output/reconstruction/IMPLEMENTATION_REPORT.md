# EvidenceTwin visual reconstruction — 2026-11-07

This reconstruction changes application composition and frontend presentation while preserving the existing persistence, evidence revision, authorization, Council, and report APIs. It does not enable new scientific methods. The owner performs final acceptance.

## What changed

- Home: saved investigations and recent real Council reviews, with an explicit starting point and short workflow explanation.
- Composer: one writing surface with contextual file/source controls, attachment previews, optional claims/context, existing validation and draft ownership protection.
- Library: compact research records, bounded titles, revision/review metadata and labeled continuation actions.
- History: responsive review records rather than a dense table; status/search lead, other filters disclose; permissions, selection, retry and deletion remain.
- Reports library: document records, restrained metadata, on-demand filters, actual report preview and existing exports.
- Saved investigation: read first, explicit question/evidence editor, original question preserved, downloadable evidence, saved dataset exploration, Council next action and immutable revision history.
- Inspection: bounded headings, original claim in a reading surface, technical/reproducibility details placed after research content.
- Evidence: supplied source/file/check counts, clear categories, identifiers behind disclosure, explicit absent-check boundary.
- Visualization: original chart stage, essential zoom/reset controls, contextual pan and image operations; recorded generation limitations and provenance remain accessible. No Neutral Twin is synthesized.
- Council: phase selection, reviewer navigation, individually recorded findings, uncertainty, full explanation, evidence references, original report and provenance. No agreement score or inferred scientific summary.
- Audit: readable event names, chronological timestamps, advanced identifiers/payloads and existing filtered export.
- Report reader: document measure, paragraph boundaries, contents navigation, metadata separated from scientific text, browser printing with flowing long sections.

`researchTitle` produces only a whitespace-normalized bounded prefix of supplied text with ellipsis. It never infers a research topic. `ResearchText` renders original wording with supplied paragraph boundaries. No original stored scientific content is rewritten or translated.

Shared design foundations use Manrope and Alan Sans, white/charcoal paper, restrained blue, fixed comfortable hierarchy, limited separators and differentiated reading/operating surfaces. Replaced the old application sections of `observatory.css`, `workspace.css`, `research-entry.css` and `inspection.css`; removed roughly26KB of competing shared CSS from the built bundle. Public articles retain their existing composition.

## Preservation and scope

No backend/API/database/migration changes in this reconstruction. No production research mutations, new model executions, user-data cleanup or new fixture records. Existing source snapshots and private research-data backups remain available. This task's source snapshot is `before-source.tar.gz`; it is not a database backup and should not replace the preserved data directory. Official brand assets are unchanged.

## Evidence and limitations

See `build.log`, `lint.log`, `unit-tests.log`, `capture-metrics.json`, `detector.json`, and the independent review records. Screenshot files live in `../playwright/reconstruction/`. Captures use existing local records, not new synthetic research. Browser checks are implementation feedback, not end-to-end/scientific validation. Existing unit checks are not new acceptance coverage. No screen reader or device hardware acceptance was performed.

Playwright MCP, Context7 MCP, and Chrome DevTools MCP are not exposed in this environment. The installed Playwright CLI skill with Brave provides real rendered inspection. Used installed Impeccable direction, craft floor, detector, independent finish review/documentation, Vercel React Best Practices and Web Interface Guidelines. No new version-sensitive framework APIs or dependencies were introduced.

Source/statistical verification, validated Neutral Twin generation and benchmark scoring remain unavailable. Browser print can create a local PDF; server PDF generation remains unconfigured. Long reviewer/source content remains in its original language.

## Launch

The existing local workspace is running at http://127.0.0.1:5202/app, proxying Flask on5000. For a fresh launch follow `../../docs/DEVELOPMENT.md`: run the backend with its existing `.venv`, then Vite with `FLASK_DEV_ORIGIN=http://127.0.0.1:5000` on5202. Keep the listeners on loopback and use the existing data root; do not start a second backend against the same root.

## Owner acceptance checklist

1. Create a question with source/file attachments, save, reopen and edit; confirm an immutable new revision and original downloads.
2. Resume a saved investigation, inspect its exact question, dataset and evidence hashes.
3. Request a real Council review only if desired and authorized to share its inputs; check status/cancellation/recovery and actual results.
4. Switch review phases/perspectives, read findings, uncertainty, originals and evidence references.
5. Inspect original charts, zoom/reset/fullscreen, available image downloads and missing-method explanation.
6. Search/filter library, review history, reports and audit; inspect advanced provenance.
7. Read/preview/export a report and inspect browser PDF pagination.
8. Repeat key flows in Arabic/English, light/dark, mobile, keyboard and zoomed text. Check account/operator permission boundaries if enabled.

Independent review disposition and any unresolved findings are recorded separately; this report does not imply owner approval.

## Final review and documentation outcome

The independent Impeccable review requested five material corrections: retained-label collision in history; Arabic audit event/status labels; print skip-link/repeated title; mobile report contents; and unnecessary eyebrows/thick side accents. These were corrected in one batch and all48screen captures regenerated at the same paths. The reviewer scored all five resolved, disposition `ship` at that fix-list scope. This is not whole-product acceptance. See `../../.impeccable/review/reconstruction/finish-review.md` and `finish-verdict.md`.

Final engineering checks: TypeScript/Vite build, lint,53existingfrontendtests, production fixture exclusion and `git diff --check` pass. Final48capture measurements show zero document-level horizontal overflow; that alone cannot establish accessibility or absence of every local collision. Official SVG hashes match the saved baseline. An actual browser PDF was generated and its first page inspected after correcting print artifacts.

Canonical documentation updated from shipped source: `../../DESIGN.md`, `../../.impeccable/design.json`, `../../docs/PRODUCT_WORKFLOWS.md`. `AGENTS.md` remains concise and applicable with links to these references. No documentation was merged, archived or removed during this visual reconstruction; earlier scientific/history/approval records remain intact. No new product/scientific decision was approved by the visual review.

See [visual review and screenshot index](VISUAL_REVIEW.md), [desktop contact sheet](desktop-overview.png), [Arabic mobile contact sheet](mobile-ar-overview.png) and [documentation outcome](design-documentation.md). The isolated inspection servers on5001/5203 were stopped; the main workspace on5202 and its backend on5000 remain running. No research data directory was deleted or migrated.
