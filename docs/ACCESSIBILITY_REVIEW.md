# EvidenceTwin accessibility improvements

Date: 2026-11-06. Applied the `better-accessibility` skill to user journeys, not only developer diagnostics. Existing branding, scientific meanings, backend contracts and Alan Sans Arabic remain unchanged.

## Resize and reflow

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| HIGH — fixed | `frontend/src/styles/accessibility.css:20` | With the expanded sidebar and 200% text, the header extended beyond a 768px viewport; narrow dashboard columns also overflowed. | Text-size-aware responsive rules hide the duplicate header documentation link, retain sidebar/mobile documentation navigation, and stack research summaries/cases where necessary. Sidebar items no longer shrink into overlapping rows; long navigation text wraps and the sidebar scrolls vertically. | WCAG 1.4.4 / 1.4.10: low-vision readers must retain content and functionality without page-level horizontal scrolling. The regression caught this before the fix. |

## Forms and focus order

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| MEDIUM — fixed | `frontend/src/features/analyses/AnalysisBuilder.tsx:17`, `:31`, `:34` | Validation moved focus only to the error summary. The evidence error link targeted the upload container rather than its usable file picker, and date errors lacked their field association. | Focus the first invalid control, connect errors with `aria-describedby` and `aria-invalid`, and make error-summary links focus their actual controls. Scroll the focused field into view. | WCAG 3.3.1 and 2.4.3; keyboard and screen-reader users can act directly on the correction rather than searching for the field. |
| MEDIUM — fixed | `frontend/src/features/analyses/AnalysisBuilder.tsx:18`, `:35` | Adding/removing a claim did not explicitly preserve a useful editing position. | Move focus to the new claim or the nearest remaining claim. | Focus-order principle / concrete editing task: users can continue entering claims without traversing the page again. |
| MEDIUM — fixed | `frontend/src/WorkspaceHome.tsx:11` | Deleting a record could remove the control that opened its confirmation dialog. | After a completed deletion, move focus to the surviving Analysis history heading; failed deletion keeps the dialog available. | WCAG 2.4.3: deletion must not leave keyboard users without an understandable continuation point. |
| LOW — recommendation implemented | `frontend/src/styles/accessibility.css:2`, `:4`, `:12`, `:14` | Sticky chrome and a visually hidden native file input could make the picker focus indicator difficult to see. | Reserve scroll space, center the upload label on validation, retain its wrapper ring and use system focus colors in forced-colors mode. | WCAG 2.4.7 / 2.4.11 focus visibility and non-obscuration. The picker rectangle was visually checked clear of the mobile header after the fix. |
| LOW — recommendation implemented | `frontend/src/features/analyses/AnalysisBuilder.tsx:40` | Native disabling during submission could remove focus from the active submit button. | Keep pending submission focusable with `aria-disabled`; the existing synchronous submission guard blocks repeated activation. Unavailable backend capabilities still use native disabled controls. | Stable keyboard interaction while waiting. No validation rule or scientific capability was relaxed. |

## Understandable feedback and alternatives

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |
| MEDIUM — fixed | `frontend/src/WorkspaceHome.tsx:11`, `frontend/src/features/analyses/AnalysisBuilder.tsx:41` | Some polite status regions were inserted together with their message; history result counts had no dedicated stable announcement. | Keep feedback/draft status regions mounted and update their text; announce history loading and matching result totals without moving focus. | WCAG 4.1.3: assistive technology must receive action outcomes without requiring users to find them visually. Browser DOM/accessibility semantics checked; spoken delivery still requires real screen-reader testing. |
| MEDIUM — fixed | `frontend/src/features/workspace/AnalysisRecords.tsx:15`, `frontend/src/WorkspaceHome.tsx:11` | Retry unavailability relied on a disabled button's hover title; deletion guidance used implementation language. | Show the retry explanation and next action as ordinary text; explain unavailable deletion in workspace language. | Disabled controls cannot expose hover-only explanations to keyboard/touch users. This makes the same information available without developer knowledge. |
| LOW — recommendation implemented | `frontend/src/features/inspection/VisualizationLab.tsx:17` | Chart comparison offered a native range control with keyboard support, but no explicit incremental pointer controls. | Add “Show less neutral” / “Show more neutral” buttons, the current percentage, and short instructions. Preserve the native slider and its accessible value text. | Additional motor-access alternative consistent with the intent of WCAG 2.5.7. The native range was not classified as a proven failure; this is an enhancement. No source data changes. |

## Verification and limits

- Keyboard-only browser walk: first Tab reaches Skip to content; Enter focuses main; Tab/Enter reach wizard controls and switch steps; confirmation opens on Keep draft; Escape closes it and returns focus to Discard draft.
- Browser accessibility tree: inspected form control names, roles, selected/disabled state, headings and native field groups. Invalid input description assertions are included in the form regression.
- Reflow: checked nine public/research routes at 320px. Added a bilingual regression for dashboard, history, builder, settings and docs at 320px and at 200% text size on a 768px viewport. The initial failure identified the real zoom overflow; targeted tests passed after correction.
- Forced-colors emulation: inspected the native upload control's visible wrapper outline and captured its focused position. Browser emulation is not physical Windows high-contrast testing.
- Existing browser regressions cover dark/light themes, Arabic/English, responsive views, reduced motion, dialogs, research inspection, charts, report printing and network failures. Mocked scientific records prove frontend behavior only.
- No new runtime dependencies, backend changes, capability enablement or paid provider calls.
- **Not verified:** actual NVDA, JAWS, VoiceOver, TalkBack or Orca spoken output; real switch/voice-control devices; physical mobile screen readers; physical Windows high-contrast mode. Browser accessibility-tree checks and axe do not substitute for those tests.
- **Not verified in this pass:** a fresh comprehensive contrast measurement of every rendered color pair. The established palette was preserved; forced-colors support and existing contrast regressions were retained.

Final command results are recorded below after completion. Approval is limited to the inspected browser scope, not a blanket WCAG certification.

## Final validation results

- Lint: passed.
- Strict TypeScript / production build: passed.
- Unit/component tests: 49 passed across 10 files.
- Full browser regression suite: 109 passed. This includes the new bilingual 320px / 200% text regression, modified form focus/error-description checks, chart button alternatives and post-deletion focus.
- After the final sidebar wrapping and upload-description refinements: 13 affected browser regressions passed, including branding, keyboard sidebar access, reflow, form validation and file selection.
- Additional pending-submission regression: 1 passed. It confirms focus remains on the pending button and repeated Enter does not submit a second request. This brings the distinct browser checks exercised in this pass to 110; they were not all run as one final 110-test invocation.
- Production fixture exclusion: passed.
- `git diff --check`: passed.
- Backend tracked/untracked checks: no backend modifications.

Local screenshots under ignored `frontend/output/playwright/` include high-contrast upload focus, enlarged-text dashboard and history, and the corrected sidebar. No deployment, production migration or scientific capability enablement was performed.

No confirmed HIGH accessibility issue remains in the inspected browser scope. Actual assistive-technology speech/device coverage remains explicitly Not verified above. Approval does not certify untested combinations or the full WCAG standard.

Approve
