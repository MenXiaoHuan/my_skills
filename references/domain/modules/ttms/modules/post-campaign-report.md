# TTMS Module: Post Campaign Report

Use this file only when the change touches campaign closeout reporting, final export packaging, or consistency between the in-product recap and the report delivered to downstream stakeholders.

## Use This Module For

- campaign-end recap flows where the user needs a final readout instead of an in-flight monitoring view
- consistency between on-screen post-campaign sections, packaged exports, and externally delivered report outputs
- campaign/date scope selection that determines which campaign results are included in the closeout
- delivery-readiness semantics such as draft, still-refreshing, or ready-to-share final reporting
- validation of client-facing or stakeholder-facing reporting artifacts after campaign completion

## Business Semantics

### Core Workflow
- open a post-campaign report for a completed or closing campaign where the purpose is recap, handoff, or external sharing
- confirm the campaign scope, reporting window, and any filters that define what belongs in the final readout
- review the summary sections, KPI blocks, and detailed report components that will be used for post-campaign interpretation
- verify that the report is in a delivery-ready state rather than still reflecting partial backfill or draft-only output
- export or deliver the final report package that external or downstream stakeholders will consume

### Important Branches
- single-campaign closeout vs broader filtered recap across more than one campaign scope
- internal QA or draft review vs externally delivered final report
- on-screen recap view vs exported report package or shared artifact
- final data lock vs partial, backfilling, or still-refreshing reporting state

### Status and Visibility Rules
- campaign scope, filters, and date ranges must stay consistent across all report sections so that the delivered recap describes the same campaign window throughout
- delivery-readiness messaging must distinguish between draft, still-refreshing, and ready-to-share reporting states; visible data alone does not mean the report is safe to send
- exported or delivered reports should preserve the same campaign identity, reporting window, and section composition that the user approved on screen
- if partial backfill exists, the report must surface that caveat in a way that prevents a draft recap from being mistaken for the final external deliverable

## Testing Prompts

Prioritize:
- campaign closeout selection and reporting-window correctness
- consistency between final KPI sections, detailed recap sections, and exported report artifacts
- delivery-readiness and freshness semantics for closeout reporting
- on-screen recap vs externally delivered report validation
- handling of draft, partial-backfill, and ready-to-share states

High-risk failure patterns:
- the report is generated from a different campaign scope or date window than the one approved on screen
- the exported or delivered recap omits sections, KPIs, or caveats that were part of the reviewed in-product report
- the UI signals that a report is ready to send even though campaign results are still backfilling or the final window is not locked

Typical P0 candidates:
- exported or externally delivered post-campaign report is materially wrong for the campaign being closed out
- users send a campaign recap to external stakeholders with the wrong campaign scope, wrong reporting window, or missing delivery caveats

## Source Links

- `Post Campaign Report`: `https://bytedance.sg.larkoffice.com/docx/RhHIdMos0oe8I5xxSXOlMn99gTc`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- Read this module as campaign closeout and external-deliverable semantics, not as a generic export page.
- Prioritize questions about finality, delivery readiness, and stakeholder-facing report integrity over generic filtering language.
- If this file materially shaped the answer, mention it explicitly.
