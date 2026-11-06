# Proposed first acceptance case: Ember global clean electricity, 2025

**Status:** User-selected case with an agreed primary-historical/separate-current evaluation policy. Manual reference-data investigation was performed on 2026-11-05. This is a planning/research artifact; EvidenceTwin's scientific backend has not executed or passed the case. Exact publication-time dataset/methodology binding and original-chart access remain incomplete.

## Claim under test

Low-carbon sources, defined here using Ember's grouping of renewables plus nuclear, generated approximately 43% of global electricity in calendar year 2025.

Keep the geography, period, numerator definition and denominator explicit. This is a descriptive electricity-generation share, not a statistical-significance, causal, energy-consumption or emissions claim. A reproduced publisher aggregate is not an independent census of all underlying national observations.

## Publisher references

- [Report landing page](https://ember-energy.org/latest-insights/global-electricity-review-2026/) lists 21 April 2026 and report authors.
- [2025 in Review](https://ember-energy.org/latest-insights/global-electricity-review-2026/2025-in-review/) provides the originally requested chapter.
- [Chapter 3, Supply overview](https://ember-energy.org/latest-insights/global-electricity-review-2026/electricity-demand-and-supply-trends/) provides the directly relevant low-carbon share: 42.6%.
- [Supporting materials and publication methodology](https://ember-energy.org/latest-insights/global-electricity-review-2026/supporting-materials/) links the report-associated CSV and describes the report's 2025 estimates and revision limitations.
- [Yearly Electricity Data portal](https://ember-energy.org/data/yearly-electricity-data/) links a separately updated global dataset and notes its July 2026 schema change.
- [Currently linked full methodology](https://files.ember-energy.org/public-downloads/ember_electricity_data_methodology.pdf) was also preserved. Do not assume its present contents equal the report's publication-time methodology.
- [Report-associated CSV](https://ember-energy.org/app/uploads/2026/04/Global-Electricity-Review-2026-%E2%80%93-Report-dataset.csv).
- [Current global yearly CSV](https://files.ember-energy.org/public-downloads/generation/outputs/release_generation_yearly_global.csv).

Retrieved documents establish observed publisher records, not completion of every proposed authenticity, correction/retraction, integrity and provenance check. In particular, no complete independent publication-notice search or upstream national-data audit was performed.

## Preserved evidence

[Retrieval manifest](20261105T112019Z/retrieval_manifest.json) records requested/resolved URLs, UTC retrieval times, response status/type, available Last-Modified/ETag headers, byte sizes and SHA-256 hashes. Exact downloaded bytes are retained in the same directory. Publisher material is attributed to Ember; its site states CC BY 4.0.

| Artifact | Bytes | SHA-256 |
| --- | --- | --- |
| Current global yearly CSV | 16,120,810 | 08932763076fa781634371dd1b75d8156f76592710c7e984836ed56a663d5688 |
| Report-associated CSV | 22,468,542 | 3e6f5793d8fd7aca3b1f444c1cc1e86d6fa125f47af281dace001e3ce6e0b84f |

Both were retrieved on 2026-11-05, beginning at 11:20:19 UTC. Returned Last-Modified headers were 2026-11-03 for the current CSV and 2026-04-22 for the report-associated CSV. These are observed server headers, not proof of immutable publication versions. The report-associated file must not be described as independently proven identical to the file on the report's 21 April publication date.

The snapshot also retains the report landing/chapter/supporting pages, data portal, current methodology PDF and text extraction. The text extraction is a derivative, not the hashed PDF original.

## Reference extraction and calculation

Machine-readable selected records and calculation outputs are in [world_2025_reference.json](20261105T112019Z/world_2025_reference.json). CSV record numbers include the header as record 1 and identify parsed records, not guaranteed physical line numbers.

### Report-associated dataset

Filter Area=World, Year=2025, Category=Electricity generation, then bind Variable and Unit explicitly. Do not select an identically named emissions row.

| Variable | Unit | Value | CSV record |
| --- | --- | --- | --- |
| Clean | TWh | 13,541.66 | 261144 |
| Renewables | TWh | 10,729.52 | 261150 |
| Nuclear | TWh | 2,812.14 | 261162 |
| Total generation | TWh | 31,779.37 | 261171 |
| Clean | % | 42.61 | 261143 |

The component sum is 10,729.52 + 2,812.14 = 13,541.66 TWh.

100 × 13,541.66 / 31,779.37 = 42.61148034086264139282811459132135092672%.

Using explicit decimal half-up rounding, that is 42.61% at two decimal places, 42.6% at one, and 43% at whole-percent precision. The ratio uses already rounded published generation values. Any bound derived from their decimal precision is a numerical rounding bound, not a confidence interval or quantified uncertainty about estimated generation.

The full file failed strict UTF-8 decoding. The research extraction used a reversible cp1252 fallback; this is not a publisher-confirmed encoding declaration. All selected World/2025 record contents are ASCII, so their numeric values do not depend on that fallback. A production ingestion/encoding policy must be explicit and must retain the original bytes rather than silently replace invalid characters.

### Current yearly dataset

The currently downloaded schema uses metric columns and Electricity source labels rather than the report-associated Category/Variable/Unit/Value layout. Filter Area=World and Year=2025.

| Electricity source | Generation (TWh) | Published share (%) | CSV record |
| --- | --- | --- | --- |
| Renewables | 10,702.271 | 33.523 | 102978 |
| Nuclear | 2,805.03 | 8.786 | 102972 |
| Clean | 13,507.301 | 42.309 | 102979 |
| Total generation | 31,925.357 | 100.0 | 102981 |

100 × 13,507.301 / 31,925.357 = 42.30900534643982211381379384418473378387%.

This matches its published share at three decimal places. Under nearest-whole-percent rounding it gives 42%, not 43%. The word approximately must therefore have an explicit precision/tolerance policy; do not broaden tolerance retrospectively to force a pass.

Do not mix one snapshot's numerator with another snapshot's denominator, sum aggregate rows alongside components, substitute capacity or emissions, or silently treat electricity demand as interchangeable with generation merely because a particular World row has the same value.

## Acceptance requirements

1. Preserve the exact submitted claim and define the numeric interpretation of approximately before judging it.
2. Establish publisher identity, canonical report/data relationships, observed publication metadata and version information under a documented source policy.
3. Record correction/retraction/notice checks as performed, failed, unavailable or not applicable with justification; do not invent a passed notice check.
4. Bind the clean grouping to renewables plus nuclear using the relevant source version and record classification caveats, including the publisher's treatment of bioenergy.
5. Validate schema, encoding, unique row selection, area, year, category, units, aggregation flags, numeric values and a nonzero denominator.
6. Reproduce the arithmetic deterministically from one pinned dataset; compare the selected aggregate with its components and its published share using declared rounding.
7. Use total electricity generation as the denominator. A denominator with a different concept must fail the binding check even if it happens to yield the same value.
8. Make historical verification primary, but require established publication-time input/methodology identity before assigning historical support. Run current verification separately; retain both results and revision provenance without rewriting historical reports.
9. Disclose the report methodology's use of 2025 estimates and possible revisions. Do not invent uncertainty intervals, or assume every latest-vintage record has the same estimate status as the earlier report.
10. Audit an actual pinned original visualization when available and bind any neutral rendering to documented transformations. Preserve the original bytes and provenance; do not invent visual defects or claim a missing chart was inspected.
11. Run the configured isolated Council roles against the same versioned evidence contract. Keep interpretations separate from deterministic findings; record actual failures and disagreements.
12. Generate a claim-level report with check coverage, supporting/conflicting/missing evidence, concise assessment, version-specific limitations and next steps. Scientific status must be gated by completed applicable checks, not by the expected number or agent agreement.

## Coverage limitations of this first case

This arithmetic case does not itself validate significance tests, p-values, causal identification or XLSX parsing. Those need separate acceptance cases. All reviewers agreeing on an arithmetic fact does not exercise disagreement resolution; use separately labeled controlled disagreements and actual unresolved conflicts to test that path.

No original chart was supplied by the user. A publisher-linked relevant visualization thumbnail is at https://public.flourish.studio/visualisation/27864750/thumbnail; the web retrieval tool received HTTP 403 during research. Its visual content was not inspected or archived, so visualization auditing and Neutral Twin comparison have not passed. Select and preserve an accessible publisher figure or an attributable original screenshot before that part of the acceptance case can run.

No live Council, source-verification backend, hosted authorization, job recovery or report export was tested by this manual investigation.

## Historical/current policy established by the user

Historical verification is primary and must use the dataset, methodology, assumptions and precision available at publication. Current verification is separate, uses the latest identified version, examines available revision history and never overwrites historical results.

Keep Historically Supported, Historically Supported — Later Revised, Historically Contradicted, Historical Verification Incomplete and Current Data Disagrees distinct. Model them as historical assessment plus revision information plus current assessment; a source's authenticity status remains separate from all three. An unestablished historical dataset cannot be replaced by a later file just because its rounded result matches.

The Ember historical check remains incomplete in this manual investigation. The report-associated CSV reproduces the printed number, but its exact publication-day identity and applicable methodology have not been independently established. Report the reproducible arithmetic as such, without assigning a fully verified historical verdict.

The [reference comparison record](20261105T112019Z/reference_revision_comparison.json) preserves the distinction. Current minus report-associated share is approximately -0.302475 percentage points, an absolute magnitude of 0.302475 percentage points and a relative change of -0.709844% using the report-associated share as the base. The authenticated historical recomputation field is null, with a reason; it is not silently filled with the report-associated reference value. The cause of the revision is unestablished.

The eventual revision report must include dataset versions and relevant publication/revision dates, reported value, historical/current recomputations, differences with units and explicit relative base, documented revision reason and effect on interpretation. Record unknown dates/reasons as unknown. Retrieval times and Last-Modified headers are evidence metadata, not automatically authoritative revision or publication dates. Numerical changes should be evaluated at the claim's declared precision rather than automatically treated as changed scientific support.

Companion controlled cases should test wrong denominators, omitted nuclear generation, duplicate aggregates, mixed snapshots, changed claims, missing provenance, unavailable chart assets and actual/controlled reviewer disagreement. Altered test inputs must remain visibly labeled and must not be attributed to Ember as published errors.
