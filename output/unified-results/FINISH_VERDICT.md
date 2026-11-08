## verdict

1. Resolved — The recaptured report places the executive finding within the opening viewport at about 530px on desktop and 642px on mobile. Translation and metadata are compact disclosures, and mobile contents follow the finding.
2. Resolved — The recaptured mobile Results preserve the assessment → evidence → narrative sequence. ResultsOverview.tsx now places introduction, evidence and narrative in that DOM order. Desktop grid areas retain the split composition. This resolution uses captures and source inspection, with live keyboard traversal outside this review.
3. Resolved — The supplied default-state PDF contains the full original claim, evidence filename, exact observations, precision-64 calculation method and reproducibility records. The print handlers open every document disclosure and restore its saved state after printing. print-check.json records all four content checks as true.
4. Resolved — Results and Report now lead with a subject-bearing diabetes excerpt, removing the generic instruction wrapper. The document avoids repeating the title in its normal reading view. The full original research request remains in its disclosure and appears in the printed original-claims section.

## remaining

Clear. No material regression from this fix batch is visible in the seven recaptured files. This ship verdict covers the four scored fixes only.

disposition: ship
