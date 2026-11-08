# EvidenceTwin live demonstration

This is an explicitly educational visual-encoding example using real observations from your previously submitted diabetes CSV. The application has not generated or validated these demo charts.

## Files to upload

1. Upload `01-upload-chart.png` as the original chart for this demonstration.
2. Add `02-upload-data.csv` through Add evidence → Add dataset.
3. Copy `04-paste-this-prompt.txt` into the composer. It includes the source reference.
4. Create the investigation, then request a Visual review and confirm consent when you are ready to send the evidence to the configured provider.

Use only files 01 and 02 as evidence for this demo. File 03 is a presenter-prepared descriptive reference to discuss afterwards. It is not an EvidenceTwin reconstruction.

## What the team can examine

The supplied CSV reports Egypt 22.4% and United States 13.7% for the 2024 indicator. Their arithmetic difference is 8.7 percentage points. The educational chart displays the same values with a vertical axis starting at 10%. Ask how that choice affects perceived bar lengths and whether it is defensible in context.

A useful review should examine the actual axis and labels, cite available evidence, distinguish suspected interpretation risks from established chart properties, and preserve uncertainty. The test does not require a predetermined AI verdict. A non-zero axis alone does not establish misleading presentation.

Current Blind Optics reconstruction remains unavailable. The app should explain that limitation. Source access failures should remain explicit, and missing evidence must not become contradiction or a fabricated scientific outcome.

## Provenance

The 455-row CSV is byte-for-byte identical to the previously submitted `diabetes-prevalence.csv`, recovered from the restorable reset backup. The selected records and original SHA-256 are in `source-provenance.json`. The chart uses the column's supplied unit, percent of the population aged 20 to 79.

The source page credits the International Diabetes Federation via the World Bank, processed by Our World in Data. Its indicator documentation is available on the [data page](https://ourworldindata.org/grapher/diabetes-prevalence).

The data-page reference was checked on 8 November 2026. A fresh direct CSV request returned HTTP 403, so this package uses your preserved supplied CSV and makes no fresh-download identity or independent source-authentication claim.

## Short presenter script

“For the live demo, I will upload an educational bar chart and its actual dataset. The chart starts its vertical axis at ten percent. We will examine how that affects interpretation, check the recorded numbers, and confirm that the app reports its reconstruction limitations honestly.”
