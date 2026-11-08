disposition: fix

Missing inputs — standalone five-block direction contract, seed reference and QUALITY BAR card were not supplied. Reviewed this code-first extension against incumbent DESIGN.md, PRODUCT.md, the calling brief and craft floor. No approved raster comp applies.

## persistence

Pass. PRODUCT.md and incumbent DESIGN.md exist. The additions retain the annotated seminar reading surface, semantic themes, supplied scientific language and disclosed provenance. All seven named captures exist and show the claimed surfaces. No comp-led state or comp-diff obligation applies.

## fidelity

| Element | Assessment |
| --- | --- |
| TYPE | Contradicted on mobile comparison labels and values. Fixed SVG coordinates shrink the data typography below a comfortable reading size. |
| MATERIAL | Match. Paper/charcoal reading surfaces and geometric data bars fit the incumbent system. |
| GROUND | Match. Light neutral paper and dark charcoal remain consistent across supplied captures. |
| Composer | Match. Real attachment previews lead, the question remains prominent, add/review/create controls stay compact and Arabic chrome preserves English source wording. |
| Evidence hierarchy | Match. Actual reported values and arithmetic precede provenance, coverage and detailed records. |
| Scientific scope | Match. Draft status, unverified methodology/authenticity and unavailable reconstruction remain explicit. |
| Council detail disclosure | Contradicted for structured-only reviewer findings. The full explanation opens using the legacy findings array alone. |

## ceiling

The native device left unresolved is readable mobile data labeling. Desktop evidence comparison and compact question composition otherwise retain the incumbent working-surface character.

## material_fixes

1. Make comparison labels and exact values readable at mobile widths. `frontend/src/features/inspection/EvidenceFindings.tsx:37` fixes the chart at a 540-unit viewBox and `frontend/src/features/inspection/evidence-findings.css:10` scales its entire text into the narrow figure. The Arabic mobile result and report captures visibly reduce labels/values to approximately 6–8px. Use responsive text outside the scaled plot or a mobile-specific chart layout that retains normal-size labels and values. Keep the underlying observations available without requiring the exact-method disclosure.
2. Honor structured findings when deciding whether to open the full AI explanation. `frontend/src/features/inspection/CouncilView.tsx:26` renders `structured.data.findings`, while line 27 opens the long explanation whenever `selected.findings` is empty. For a structured-only response this defeats the requested concise-first disclosure. Compute the available findings from the selected structured or legacy representation and base the default-open condition on it. The same representation should supply the recorded-findings count at line 24.

## keep

Preserve actual dataset values, inspectable row/hash/revision provenance, explicit unavailable checks, restrained semantic themes, rich top attachments and independent direction for original scientific wording.
