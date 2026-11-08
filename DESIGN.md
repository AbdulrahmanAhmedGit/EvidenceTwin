---
name: EvidenceTwin Council
description: An annotated seminar review with preserved scientific evidence
colors:
  bg-page: "#fafbfc"
  bg-surface: "#ffffff"
  bg-secondary: "#f1f3f6"
  bg-navigation: "#f1f3f6"
  text-primary: "#202737"
  text-secondary: "#596478"
  border-separator: "#dce1e9"
  border-control: "#8793a6"
  accent-solid: "#3159bb"
  accent-solid-hover: "#244596"
  accent-subtle: "#e5ebfb"
  accent-text: "#2a50ad"
  text-on-accent: "#ffffff"
  warning-text: "#80560f"
  danger-text: "#b3383b"
  data-series-a: "#416cbb"
  data-series-b: "#667a99"
  focus-ring: "#4e6ba6"
  dark-focus-ring: "#4e6ba6"
  dark-bg-page: "#11151c"
  dark-bg-surface: "#181e28"
  dark-bg-secondary: "#202836"
  dark-bg-navigation: "#151b25"
  dark-text-primary: "#eef1f7"
  dark-text-secondary: "#abb7ca"
  dark-border-separator: "#343f52"
  dark-border-control: "#6f809b"
  dark-accent-solid: "#9ebaff"
  dark-accent-solid-hover: "#c2d3ff"
  dark-accent-subtle: "#273650"
  dark-accent-text: "#b4caff"
  dark-text-on-accent: "#15244a"
  dark-warning-text: "#efc47a"
  dark-danger-text: "#ffb0b4"
  dark-data-series-a: "#9ebaff"
  dark-data-series-b: "#b1bfd5"
  investigation-health: "#7554b8"
  investigation-environment: "#287b64"
  investigation-medicine: "#95631b"
  dark-investigation-health: "#ba93f1"
  dark-investigation-environment: "#65c4a5"
  dark-investigation-medicine: "#e7b65f"
typography:
  investigation-heading:
    fontFamily: "Manrope, 'Alan Sans Variable', sans-serif"
    fontSize: "clamp(1.75rem, 2.55vw, 2.625rem)"
    fontWeight: 750
    lineHeight: 1.3
    letterSpacing: "-.035em"
  headline:
    fontFamily: "Manrope, 'Alan Sans Variable', sans-serif"
    fontSize: "1.625rem"
    fontWeight: 650
    lineHeight: 1.4
    letterSpacing: "-.025em"
  body:
    fontFamily: "Manrope, 'Alan Sans Variable', sans-serif"
    fontSize: "1rem"
    lineHeight: 1.65
  interface:
    fontSize: ".875rem"
  caption:
    fontSize: ".8125rem"
  label:
    fontSize: ".75rem"
  question:
    fontFamily: "Manrope, 'Alan Sans Variable', sans-serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.75
  data:
    fontFamily: "'IBM Plex Mono', monospace"
rounded:
  control: "7px"
  navigation: "4px"
  surface: "8px"
  review: "10px"
  dialog: "12px"
  attachment: "8px"
  composer: "12px"
  investigation-composer: "22px"
  investigation-tool: "13px"
  investigation-action: "14px"
  investigation-prompt: "16px"
spacing:
  space-1: "4px"
  space-2: "8px"
  space-3: "12px"
  space-4: "16px"
  space-6: "24px"
  space-8: "32px"
  space-12: "48px"
components:
  button-primary:
    backgroundColor: "{colors.accent-solid}"
    textColor: "{colors.text-on-accent}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  button-primary-hover:
    backgroundColor: "{colors.accent-solid-hover}"
  button-secondary:
    backgroundColor: "{colors.bg-surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  navigation:
    backgroundColor: "{colors.bg-navigation}"
    rounded: "{rounded.navigation}"
    padding: "11px 12px"
  status:
    textColor: "{colors.accent-text}"
    padding: "0"
  case-record:
    textColor: "{colors.text-primary}"
    padding: "20px 24px"
  field:
    backgroundColor: "{colors.bg-surface}"
    rounded: "{rounded.control}"
    padding: "11px 12px"
  composer:
    backgroundColor: "{colors.bg-surface}"
    rounded: "{rounded.composer}"
    padding: "0"
  investigation-composer:
    rounded: "{rounded.investigation-composer}"
  investigation-tool:
    rounded: "{rounded.investigation-tool}"
    padding: "9px 13px"
  investigation-action:
    backgroundColor: "{colors.accent-solid}"
    textColor: "{colors.text-on-accent}"
    rounded: "{rounded.investigation-action}"
    padding: "11px 20px"
  investigation-prompt:
    backgroundColor: "{colors.bg-surface}"
    rounded: "{rounded.investigation-prompt}"
    padding: "17px 16px"
---

# Design System: EvidenceTwin Council

## Overview

**Creative North Star: "The annotated seminar review"**

Neutral paper and charcoal surfaces, restrained cobalt actions and readable contributions give research a calm working environment. Questions, supplied evidence and individual interpretations stay distinct. Interface language supports English and Arabic while research retains its supplied wording and direction.

This system records the authorized application reconstruction and its unified results/report extension and approved chart-investigation entry through 2026-11-08. Runtime authority is `frontend/src/styles/{precision,workspace,observatory}.css`, `features/analyses/research-entry.css`, `features/analyses/investigation-reference.css`, and the inspection, evidence findings, results overview and report reader styles under `frontend/src/features/inspection/`. The chart-first priority follows the owner’s product-focus decision. The approved entry reference extends the same semantic system with a broad composer and subtle mathematical atmosphere. Public showcase composition remains separate. Scientific validation and hosted-pilot readiness require their own evidence.

**Key Characteristics:**

- Bounded headings and generous scientific reading measures.
- Paper reading surfaces, contextual controls and disclosed detail.
- Semantic light/dark themes and logical RTL layout.
- Original-chart inspection with recorded AI concerns and supporting evidence kept distinct.

## Colors

### Primary

Restrained cobalt marks primary actions, links, focus and selected controls. Accent text and solid-action fill remain separate semantic roles. Dark mode supplies its own lighter cobalt and on-accent text.

### Secondary

The investigation prompt categories use scoped health violet, public-health green and medicine ochre, each with its own light/dark value in frontmatter. Their icon backgrounds mix the category color at 13% with transparency. These accents identify educational prompt categories.

### Neutral

Paper, secondary surfaces and navigation separate reading material from chrome. Charcoal and muted text distinguish content from metadata. Separator and control borders are separate roles. Exact light/dark values are in frontmatter; legacy aliases resolve to the semantic CSS variables.

Warning and danger colors supplement written states. Data-series colors encode charts; they do not establish claim outcomes. The shared focus-ring declaration overrides the earlier light-only value; frontmatter records the effective token.

The approved entry surface aliases its composer top to paper and its bottom to accent-subtle in light mode and secondary surface in dark mode. Its border uses the control-border token, waves use data-series-a, and example surfaces use paper with an accent-subtle or secondary hover. The dark navy/slate ground comes from the existing dark semantic palette. These aliases are scoped to the entry route.

**The Semantic Surface Rule.** Resolve surfaces, text and controls through the active theme's semantic variables.

## Typography

Manrope (variable 200–800) supplies the interface and scientific prose; Alan Sans Variable supplies Arabic. IBM Plex Mono supplies code, identifiers and numerical data with tabular figures. The optional Newsreader direction was not implemented and is not a font token.

Application page headings use the frontmatter headline role (26px), falling to 24px at the mobile breakpoint. Analysis headings use the same size with 1.45 leading; the home creation invitation is 28px on desktop and 24px on mobile. The approved investigation entry uses its own frontmatter heading role, reaching 42px, with a 20px subtitle. At 760px it uses a 30px heading and 16px subtitle. Arabic uses an untracked 32–44px heading with 1.5 leading, becoming 32px/1.6 at 760px. Shared section headings are 20px/1.4; tertiary headings are 16px/1.5. Shared weight is 650 with -.025em tracking; Arabic removes negative tracking. Component-specific heading leading follows its reading context.

Body text is 16px/1.65; scientific contributions use 16px/1.85 with a 72ch maximum measure. Saved questions use 17px/1.85. The unified report uses 16px/1.9 prose and a 70ch measure. Reviewer summaries use 15px/1.8. The earlier report base retains 17px/1.95 for other reading contexts. The composer uses its question role, becoming 16px on mobile. Arabic root leading is 1.85; source-directed scientific paragraphs keep their own typography and `dir="auto"`.

**The Source Wording Rule.** Compact display titles use a bounded verbatim excerpt. Results and reports prefer a quoted claim or remove a recognized English or Arabic instruction wrapper before truncation. Full scientific wording remains available in the original-question disclosure and preserved report records.

## Layout

The desktop shell has a 224px sidebar (76px collapsed) and 56px header. General application pages are centered within 1200px with 28px 36px 64px padding. Existing compact creation contexts use a 920px outer region and 760px content column. The approved investigation entry has a 1124px maximum content region with 56px 44px 64px desktop padding and centered introduction. The empty chart-first composer was captured at 1124×228px. Its height grows with real inputs. At 1200px padding becomes 44px 28px 60px, then 30px 20px 44px at 760px. Educational prompts use four columns, two at 1200px and one at 520px. Above 1500px their group extends 60px beyond each content edge. Saved cases use a flexible reading column and 240px provenance rail separated by 40px; the rail stacks below 1100px.

Council separates a 210px reviewer navigation column from the reading surface with a 32px gap; below 1150px it becomes 180px with a 20px gap. The unified report pairs an up-to-860px document with a 150–200px contents column and 36px gap. At 1150px and below, contents become a disclosure after the executive finding. Document padding is 36px 42px, falling to 28px at 1150px and 22px 4px at 600px.

At 760px the sidebar becomes four-destination bottom navigation, general page padding becomes 24px 20px 40px, creation padding becomes 28px 20px 40px, field pairs stack and actions wrap. Main content reserves 96px plus safe-area clearance. Tables and chart stages retain intentional local scrolling. Use logical properties and wrap long filenames and scientific text.

The unified results surface extends to 1480px and pairs a 1.35fr reading column with a minimum-330px evidence column across a 40px gap. At 1100px it uses a minimum-300px rail and 24px gap. At 900px and below, introduction, evidence and narrative stack in their DOM order. The visual assessment, original question and section links precede the evidence workspace. Narrative sections follow it.

## Elevation & Depth

Paper fills, one-pixel separators and alignment carry hierarchy. Reading containers have restrained borders and rounded corners; ordinary controls have no shadow. Dialogs use `0 20px 80px #11182730`, with `#11182780` backdrop and no blur. Composer focus changes its outer border. Keyboard focus also outlines the writing input; forced colors adds a Highlight outline.

The approved investigation entry adds a low-contrast radial cobalt atmosphere and a diagonal paper-to-secondary composer blend. Dotted mathematical curves sit behind content, remain pointer-inert and hidden from assistive technology, and encode no measurements. Wave opacity is .3 in light mode and .55 in dark mode. Mobile light mode uses .25. Composer elevation is `0 16px 38px #03091a0b`, with `#03091426` in dark mode. This treatment belongs to the approved entry surface.

Controls transition background, border and color over 150ms ease. System reduced motion and the explicit reduced-motion preference disable transitions, animation and smooth scrolling.

## Shapes

Shared buttons and fields use the control radius in frontmatter. Navigation retains its smaller radius. Evidence rows, case surfaces and reports use the surface radius; review records and Council reading surfaces use the review radius. Dialogs use the dialog radius and the composer its larger radius. Circular status marks accompany written labels. The unified results assessment and evidence rail use 14px corners, while report documents and executive findings use 12px corners. The approved entry uses a 22px composer, 13px tool buttons, 14px primary action, 16px prompt cards and 12px prompt icons. At 760px tools become 10px, the action 11px and prompt icons 10px. These are local surface treatments. Shape varies with the component's purpose.

## Components

### Buttons and fields

Primary buttons use accent fill and on-accent text; hover uses the theme's hover accent. Shared buttons use 10px 16px padding and minimum 44px height. Contextual actions may use explicit compact variants (36–40px). Disabled controls use .6 opacity. Keyboard focus uses a 3px accent outline offset by 3px.

Fields use surface fill, one-pixel control borders and 11px 12px padding. Focus changes the border to accent. Errors remain written and associated with inputs. The borderless composer textarea auto-sizes from a 56px CSS minimum. Its default height cap is min(340px, 40vh), becoming min(340px, 30vh) below 600px. Questions longer than 240 characters expose an explicit expansion control with a 65vh cap. The source handler updates height as the question and viewport change. The complete investigation request shares one compact composer surface. Its default action row contains an add control, the selected review mode and Create investigation. A shared top-layer popover presents the add menu, review choices and focused source, claim or study editors. Opening a tool never adds a configuration panel to the document flow. Source and claim chips and file previews appear only for actual inputs. Attachment thumbnails sit above the question in a locally scrolling row. Images preview the selected local file or saved original. CSV thumbnails show the first complete records from a bounded local read, with up to six records and four displayed columns. Their local-preview label and selected/saved state preserve the distinction from submitted processing and the complete original file. The popover is anchored and constrained to the visual viewport by `ComposerPopover.tsx`, with Escape/outside dismissal and native invoker focus order. [Popover API reference](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/showPopover).


### Chart-investigation entry

The approved composition pairs the official artwork and existing navigation with a centered chart-investigation invitation, one composer and four educational chart prompts. The sidebar review destination reads Chart reviews. The reference-approved contextual badge remains specific to this surface.

The original-chart upload invitation appears inside the composer before optional question/context text. With an image attached, an empty written question uses the visible standard presentation-inspection request. Saving preserves the chart and context first. AI review follows the existing consent step. The five-step intended journey appears beside an explicit current-availability boundary, including unavailable blind reconstruction.

Evidence, source and review controls open compact anchored top-layer menus or editors. Existing choices, input limits, Escape/outside dismissal and focus behavior remain authoritative. Expanded controls use accent-subtle fill and the composer border. At 760px source/evidence text labels yield to accessible icon buttons while the review control stays bounded. Supported limits remain written inside the evidence menu.

Educational choices cover health, public health, medicine and data analysis. Selection fills editable question text and creates no saved research or findings. Replacing nonempty text requires the inline replacement choice. Real attachment previews, draft isolation and the shared save operation retain their existing behavior.

### Navigation and records

Sidebar selection uses paper fill, accent text and weight 700. Inline status labels have a current-color dot and no pill border. Case rows show supplied title prefixes, real revision/review counts and an explicit Continue link. Review/report records keep metadata and relevant actions together; advanced filters disclose beneath primary search/status controls.

### Research reading surfaces

Saved cases open in read mode with the full question, saved evidence and an explicit editor toggle. Provenance and revision history remain accessible in the rail. Council leads with supplied findings, then reviewer perspectives, limitations and disagreements. Structured reviewer findings use expandable titles, observations, significance, recommendations and evidence references. Claim positions are explicitly identified as AI positions. Legacy records retain their supplied finding lists and full explanation fallback. Original output and provenance remain inspectable through disclosure. No generated summary or agreement score is introduced.

Evidence findings use secondary surface fill, accent and muted comparison bars, and separator tokens. Proportional bars sit beneath readable DOM labels and exact reported values. Labels remain outside the bars and retain their text size at narrow widths. Exact observations, source-record rows, arithmetic method and scope disclose beneath each comparison. Dataset hashes and revision references, source retrieval records, and limits remain separately inspectable. Processing coverage is listed apart from scientific claim assessment. Historical runs and unavailable comparisons carry written boundary states. Reports reuse this findings surface and disclose preserved claim, evidence and reproducibility records.

The unified results introduction leads with visual assessment and the first recorded visual finding’s title and observation. The recorded visual summary is the fallback. AI visual review and potential-issue status remain explicit, with independent confirmation limits and full original interpretation available. Loading, missing and unavailable states retain written labels. The adjacent evidence workspace switches among charts, data and sources using pressed-state controls. Original visuals retain their supplied image and caption. Council contributions, disagreements and grouped limitations use compact disclosures. Blind Optics carries an explicit unavailable state with its recorded boundary.

Comparison figures use linear bars from a zero baseline and recorded domain when available. A left-to-right numerical axis remains stable inside RTL layouts. Exact supplied labels and values remain readable DOM text above the bars. Observations, calculation method, precision and plot version remain inspectable. A plot accompanies available quantitative records, while source status and scientific assessment retain separate written states.

The report document brings the recorded visual section into the opening reading viewport. New reports prefer visual_summary. Older reports prefer their existing visual_analyst section, then summary, while retaining the original section content. Original submitted charts precede supporting descriptive plots, with their recorded provenance and image actions. This is reading priority and preserves the stored report. Export actions and a compact translation disclosure sit above it. Metadata discloses beneath the masthead, while the repeated document title appears for print. Mobile contents follow the executive finding when that section exists. Original claim, submitted evidence, calculation and reproducibility records remain inspectable through disclosures. Translation is labeled as a derivative, with original-reading access and a partial-translation notice when protected numbers or references require retained original-language passages. Scientific content preserves its original direction.

Print hides application chrome, controls and contents, preserves the report title and uses 18mm page margins with 11pt/1.7 report text. Before printing, every document disclosure opens, including nested records, methods and reviewer contributions. After printing, each disclosure regains its previous state. The default print path includes the full original claim and preserved records.

See [the implemented workflow](docs/PRODUCT_WORKFLOWS.md) for persistence, consent and input-capability boundaries.

## Do's and Don'ts

- Do resolve surfaces, text, controls and status through semantic CSS variables.
- Do preserve question, evidence revision and real review history as distinct records.
- Do use Manrope/Alan Sans for prose and IBM Plex Mono for code and numerical data.
- Do preserve original content direction with dir="auto", bdi and isolated code.
- Do keep visible focus, reduced motion and honest missing/failed/unavailable states.
- Do preserve official logo bytes, colors, proportions and orientation.

- Don't treat AI agreement, parsing or a completed run as scientific proof.
- Don't recolor or mirror the official artwork.
- Don't spread the approved entry atmosphere into scientific reading surfaces or treat its mathematical curves as data.
- Don't fabricate findings or reconstruct missing scientific imagery.
- Don't present a URL as retrieved, a PDF as extracted or XLSX as supported.
