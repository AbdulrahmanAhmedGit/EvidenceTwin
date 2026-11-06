No Blocker findings. The concept is understandable and preserves the essential distinction between scientific checks and AI interpretation. The findings below are design requirements for the hosted pilot, not claims that its unfinished features are already-built defects.

1. **Major — UX & Developer Ergonomics: define the evidence-request and resubmission journey.**  
   **Scope:** FeatureConcept “Metadata required as applicable” lines 108–118, “Required fields for every claim” lines 184–192, and primary experience line 23. Existing `contracts/analyses.py:18–31` accepts creation metadata; `runtime.py:196–205` retries the existing packet rather than accepting new evidence.  
   **Friction and consequence:** The concept requires requesting missing metadata, but does not establish how researchers supply it after analysis acceptance. “Retry” could mean repeat an identical failed execution, evaluate amended evidence, or resume unfinished checks. Those operations have different scientific and cost consequences.  
   **Ergonomic requirement:** Define a visible evidence-request workflow tied to a claim/check: requested item, reason, acceptable format, supplied response and resulting analysis revision. Separate retrying the same immutable inputs from submitting revised inputs. Preserve previous conclusions and make clear which revision each report assesses.

2. **Major — UX & Developer Ergonomics: introduce an explicit claim-to-evidence/check plan before execution.**  
   **Scope:** FeatureConcept claim identification lines 65–69, input rules lines 99–118, acceptance lines 129–133. Existing `runtime.py:159–164` assigns claim IDs but places evidence in a shared packet; `contracts/analyses.py:20–28` provides predominantly submission-level metadata.  
   **Friction and consequence:** Multiple claims, sheets, charts, denominators and time periods can coexist in one submission. A researcher cannot reliably correct or understand an assessment unless they can see which data columns, rows, sheets, source passages and assumptions were associated with each assertion. The concept correctly rejects invented assumptions, but does not define how extracted or ambiguous associations are confirmed.  
   **Ergonomic requirement:** Present the normalized assertion and its evidence bindings with provenance, distinguish user-supplied from extracted values, and flag ambiguity before a check relies on it. Define how conflicting metadata is resolved. Record required/applicable checks per claim and make any unresolved essential association an explicit insufficiency.

3. **Major — UX & Developer Ergonomics: make scientific coverage legible across the existing UI and API.**  
   **Scope:** FeatureConcept report requirements lines 73–83, source statuses lines 148–155, assessment lines 174–192, and open taxonomy decision line 205. Existing `contracts/common.py:22–25` separates job status, verdict, mode and source status, but lacks a `contradicted` verdict; `contracts/analyses.py:59–78` exposes submission-level assessment; `contracts/inspection.py:119–133` has no dedicated claim/check assessment structure.  
   **Friction and consequence:** Researchers will otherwise need to reconcile “completed,” “Verified,” a claim verdict and AI judgments across separate panels. A mixed submission might contain one reproduced contradiction, another unsupported inference and an inaccessible source. A single badge cannot explain that result safely.  
   **Ergonomic requirement:** Define claim-level and check-level response shapes and a consistent display hierarchy: execution state, provenance result, check coverage, claim assessment and AI interpretation. Include explicit failed/unperformed/inapplicable check semantics. Define legacy verdict/source-enum mappings and report-list/filter behavior without using “unsupported” as an unexplained synonym for contradiction.

4. **Major — UX & Developer Ergonomics: provide actionable, bounded errors instead of asking researchers to diagnose infrastructure.**  
   **Scope:** FeatureConcept hosted experience line 23, operator-only configuration line 47, actual execution states line 34. Existing `workflow.py:132–140` collapses provider/structured-response failures into one message; `workflow.py:188–190` advises checking provider configuration; `runtime.py:94–105` and `:134–146` raise generic validation exceptions for numerous distinct input failures.  
   **Friction and consequence:** Ordinary hosted researchers cannot repair operator credentials, model availability or malformed provider output. Conversely, a malformed CSV or missing denominator needs a specific correction. A generic failure encourages repeated submissions and unnecessary provider charges.  
   **Ergonomic requirement:** Specify safe error codes and user actions for input correction, missing evidence, unsupported procedure, access restriction, quota exhaustion, temporary infrastructure failure and invalid AI response. Attach input errors to the relevant file/sheet/column/claim when possible. Explain whether an attempt ran, whether retry changes anything, and what the operator must resolve without exposing private upstream responses.

5. **Major — UX & Developer Ergonomics: expose processing scope and limits before submission.**  
   **Scope:** FeatureConcept input formats lines 97–106 and workload limits line 232. Existing guide lines 176–189 limits files, datasets and model context; `runtime.py:167–170` sends only the first 200 dataset rows to reviewers while preserving the complete accepted dataset.  
   **Friction and consequence:** “Dataset uploaded” can be mistaken for “all observations examined by every reviewer.” Adding XLSX also makes silent first-sheet or first-range selection particularly difficult to interpret. General limitations buried in a report do not explain which portion each computation or reviewer actually used.  
   **Ergonomic requirement:** Show accepted input limits and analysis scope before launch. Record the exact dataset version, sheet/range, row selection, exclusions and transformations used by each deterministic check and AI reviewer. Surface truncation beside affected contributions. Define how researchers select or correct scope without treating sampled AI review as full-data verification.

6. **Major — UX & Developer Ergonomics: explain external processing of private evidence at the point of use.**  
   **Scope:** FeatureConcept access/privacy lines 38–47 and controlled audience line 23. Existing `workflow.py:145–161` passes evidence packets and images to provider calls; provider settings are presently explained in `AIProviderSettings.tsx:32–41`.  
   **Friction and consequence:** Hosted researchers will no longer configure their own models, so they also lose the current contextual cue that uploaded research is processed by a selected provider. Private storage and account isolation alone do not explain that processing boundary.  
   **Ergonomic requirement:** Define researcher-facing disclosure of which evidence categories leave the service for AI review, which provider configuration applies, and applicable handling/retention constraints. Place this information in onboarding or submission and retain the relevant processing configuration in the audit record. Define the supported path when particular evidence cannot be sent to the configured provider. This is a design requirement, not an assertion that any particular consent mechanism is already approved.

7. **Nit — UX & Developer Ergonomics: disambiguate research cases from illustrative cases.**  
   **Scope:** FeatureConcept primary experience line 23 versus existing `runtime.py:33–37`, `:317–323`, and `contracts/analyses.py:31`.  
   **Friction and consequence:** The proposed user-owned “research cases” share terminology with `/api/cases`, which currently serves three authored educational examples. Implementers could accidentally reuse the catalog interface or `caseId` semantics for private case ownership.  
   **Ergonomic requirement:** Define case, analysis attempt, evidence revision and educational example as separate concepts, including their identifiers and relationships. Document any route/field changes and preserve explicit sample labeling.

**Read coverage:** Fully read the immutable `review_input.md` (255 lines), the Comprehension persona (69 lines), and Heilmeier standard (30 lines). Fully read every required public project file:

- `BACKEND_IMPLEMENTATION_GUIDE.md` — 318 lines.
- `docs/FRONTEND_API_CONTRACT.md` — 252 lines.
- `backend/evidencetwin_backend/__init__.py` — 69 lines.
- `backend/evidencetwin_backend/services/runtime.py` — 380 lines.
- `backend/evidencetwin_backend/services/workflow.py` — 213 lines.
- `backend/evidencetwin_backend/services/store.py` — 75 lines.
- `backend/evidencetwin_backend/contracts/analyses.py` — 90 lines.
- `backend/evidencetwin_backend/contracts/inspection.py` — 133 lines.
- `backend/evidencetwin_backend/contracts/common.py` — 69 lines.
- `frontend/src/features/settings/AIProviderSettings.tsx` — 48 lines.

No required file was inaccessible. Truncated tool output was covered by subsequent targeted reads. No writes, tests, provider calls, private configuration, databases, uploads, memory or session-history reads were performed. Parent-turn isolation was requested; exclusion of inherited host instructions was not independently verifiable.
