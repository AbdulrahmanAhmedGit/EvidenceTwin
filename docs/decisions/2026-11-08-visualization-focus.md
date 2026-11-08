# EvidenceTwin Council — Correct the Core Product Focus

## Important Product Clarification

I want to clarify the central purpose of EvidenceTwin Council.

**EvidenceTwin is primarily a scientific platform for detecting, explaining, and correcting misleading data visualizations (misleading plots), with an initial focus on healthcare, medical research, and public-health data.**

It is not intended to be merely a general-purpose AI research assistant or a scientific claim-checking chatbot.

Scientific claim assessment is important, but it supports the platform's main goal: understanding whether the way data are visualized could mislead researchers, healthcare professionals, or readers.

## 1. The Core User Journey

Simplify the application around five steps:

**Upload → Analyze → Detect → Reconstruct → Compare**

A user should be able to:

1. Upload a scientific chart or medical visualization.
2. Optionally provide the underlying dataset (CSV/XLSX), source URL, and research context.
3. Have the system inspect the original visualization.
4. Identify potential misleading visual-design choices.
5. Generate an independent, evidence-grounded reconstruction when the underlying data and supported methods permit it.
6. Compare the original and reconstructed plots.
7. Receive a clear explanation of what changed, why it matters, and whether the original presentation is potentially misleading.

Additional scientific claim analysis should support this workflow rather than dominate it.

## 2. Make Misleading Plot Detection the Main Capability

Prioritize examination of:

- Truncated or inappropriate axes.
- Misleading scales or baselines.
- Distorted proportions.
- Cherry-picked observations or time ranges.
- Misleading color encoding.
- Inappropriate chart types.
- Missing units or labels.
- Missing or improperly represented uncertainty.
- Misleading comparisons between groups.
- Visual exaggeration of effects.
- Confusion between absolute and relative risk.
- Missing denominators or relevant context.

Use scientifically appropriate evaluation rules.

Do not automatically label a chart misleading because it uses a non-zero baseline, logarithmic scale, or unconventional presentation.

Explain the specific visual issue, its supporting evidence, and how it could affect interpretation.

Distinguish confirmed presentation problems from suspected problems and insufficient evidence.

## 3. Blind Optics Expert — Core Product Component

The Blind Optics Expert should be a central component of EvidenceTwin's scientific workflow, not a hidden optional feature.

Its intended responsibility is to independently reconstruct visualizations from the underlying data without being influenced by other agents' interpretations or the original visual framing, according to a documented blind-review protocol.

When reconstruction is supported:

- Use real underlying observations.
- Preserve units and scientific definitions.
- Choose defensible visual encodings.
- Document axes, scales, transformations, and assumptions.
- Generate a reproducible visualization.
- Compare it with the original plot after the independent reconstruction.

Never invent data to complete a reconstruction.

If the original dataset is unavailable or the reconstruction method is not yet implemented or validated, clearly report that limitation.

Inspect the repository and approved scientific specifications before changing this expert's implementation.

## 4. Redesign the Results Around Visual Comparison

The most important result should not be a wall of AI-generated text.

The Results page should prioritize:

**A. Visual assessment**

Is the original plot potentially misleading? Explain the judgment clearly and with appropriate uncertainty.

**B. Original vs. reconstructed plot**

Show the original and independently reconstructed visualizations side by side when reconstruction was actually performed.

**C. Detected issues**

Clearly explain which visualization choices may distort interpretation and why.

**D. Scientific implications**

Explain whether the visual presentation could affect the interpretation of the medical or health-related findings.

**E. Council review**

Show concise specialist findings, supporting evidence, disagreements, and important limitations.

**F. Methodology and provenance**

Make the underlying dataset, transformations, calculations, and source information inspectable.

Avoid fabricated accuracy percentages, confidence scores, or misleading-detection metrics.

## 5. Simplify the Whole Product

The current application has become too complicated.

I want researchers and students to understand its purpose immediately:

**"Upload a scientific chart, discover potentially misleading visualizations, and compare it with an evidence-grounded reconstruction."**

Make this the central message of the application.

Simplify:

- Navigation.
- New Investigation.
- Evidence submission.
- Council presentation.
- Results.
- Reports.
- Technical settings.

Do not force ordinary users to understand agent orchestration, internal jobs, provider configuration, or complicated verification terminology.

Use simple language and progressive disclosure.

Keep advanced scientific details available for researchers who need them.

The user interface should be as intuitive as a modern AI workspace, but the product must retain its own identity and scientific purpose.

## 6. Preserve Real Scientific Functionality

Do not remove valuable existing capabilities such as:

- Claim assessment.
- Source ingestion.
- Deterministic calculations.
- Evidence provenance.
- Independent Council reviews.
- Reports and audit records.

Instead, organize them around the central misleading-visualization investigation workflow.

The existing frontend, backend, and Scientific Core should remain integrated.

Do not fabricate:

- Medical observations.
- Scientific conclusions.
- Reconstructed plots.
- Verification outcomes.
- Statistical certainty.
- Scientific accuracy scores.

Never present a visual reconstruction as independently validated unless its method and acceptance criteria justify that claim.

## 7. Product Priority

From now on, prioritize the product in this order:

1. Reliable inspection of original scientific visualizations.
2. Detection and explanation of potentially misleading visual choices.
3. Independent visualization reconstruction using original numerical data.
4. Clear original-versus-reconstructed visual comparison.
5. Evidence-grounded interpretation and Council review.
6. Supporting scientific claim assessment and reporting.

These priorities describe the intended product direction, not a claim that every capability has already been implemented or validated.

Follow `concepts_brief.md` as the approved requirements baseline. If this clarification conflicts with an approved requirement or unresolved scientific decision, identify the conflict rather than silently changing the specification.

## Final Direction

**EvidenceTwin is not simply an AI system that answers scientific questions.**

It is an evidence-driven tool designed to help researchers identify potentially misleading scientific visualizations, understand why they may be misleading, and construct more defensible representations of the same underlying data.

Initially, focus on healthcare, medicine, and public-health research.

Make the product simpler, more visual, more scientifically rigorous, and easier to understand.

Do not rebuild everything unnecessarily. Refocus the existing application around this primary mission while preserving working functionality and scientific integrity.