## verdict

- Resolved. Mobile comparison labels and exact values now appear as readable native text above proportional bars in `results-mobile-ar-dark.png` and `comparison-mobile-detail.png`. Implemented at `frontend/src/features/inspection/EvidenceFindings.tsx:35` and `frontend/src/features/inspection/evidence-findings.css:11`.
- Resolved. `frontend/src/features/inspection/CouncilView.tsx:21` derives findings availability from the rendered structured or legacy representation. Line 29 uses that result for the default explanation disclosure, and lines 22/26 use the matching representation for counts. This resolution was inspected in source. The supplied diagnostic does not execute Council reviews.

## remaining

Clear for the two scored fixes. This ship verdict covers those fixes only.

disposition: ship
