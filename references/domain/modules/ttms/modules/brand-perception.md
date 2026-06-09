# TTMS Module: Brand Perception

Use this file only when the change touches the Brand Perception parent entry, shared filtering or export semantics, or the decision of which perception sub-view a question belongs to.

## Use This Module For

- deciding whether a perception question should be answered from Brand Insights, Search Insights, Vertical Insights, or Tentpole Strategy
- understanding the parent-level contract shared by those four sub-views: same brand-perception topic, but different evidence lens and downstream usage
- checking which filters, segmentation choices, navigation state, and export context are allowed to stay shared when the user moves across sub-views
- recognizing when this file is enough as an overview and when the question has crossed into source-specific metrics, definitions, or business rules
- validating parent-level freshness and partial-data caveats without flattening the four sub-views into one interchangeable report

## Business Semantics

### Core Workflow
- enter Brand Perception as an overview entry that helps the user choose the right perception lens, not as the final source of truth for every metric
- identify whether the question is about broad brand health, search-origin demand signals, vertical/category context, or tentpole-event planning
- carry only the shared context that should survive sub-view switches, such as selected brand, market, or comparable segmentation where the product supports it
- read the selected sub-view with its own summaries, tables, charts, and export surface while preserving the chosen perception lens
- leave this file and follow the specific source link as soon as the answer depends on sub-view-only metric definitions, cadence, or interpretation rules

### Important Branches
- Shared concern: all four sub-views answer "how is the brand perceived," but they do not use the same evidence source, comparison frame, or action context
- Brand Insights: use when the user needs the broadest brand-level reading and does not need search-specific, vertical-specific, or event-specific framing
- Search Insights: use when the perception story is inferred from search behavior or search-led discovery rather than from a generic brand summary
- Vertical Insights: use when perception must be interpreted inside a vertical or category boundary and should not be read as whole-brand truth
- Tentpole Strategy: use when the user is planning around major moments or campaign windows and needs event-aware interpretation rather than always-on monitoring

### Status and Visibility Rules
- shared filters and segmentation choices should stay coherent when the user moves between the parent entry and a selected sub-view, but only for controls that are truly common across those surfaces
- the parent entry may summarize caveats, yet it must not imply that Brand Insights, Search Insights, Vertical Insights, and Tentpole Strategy are refreshed on the same cadence or are directly comparable metric for metric
- export behavior should preserve the currently selected perception lens and label it clearly instead of silently switching to a different sub-view or a default scope
- when a sub-view has source-specific definitions, the parent entry should hand off to that definition instead of trying to normalize all four into one rule

## Testing Prompts

Prioritize:
- choosing the correct sub-view for questions about broad brand health, search-origin signals, vertical context, or tentpole planning
- handoff correctness from the Brand Perception entry into the selected sub-view without losing the intended perception lens
- shared filter and segmentation behavior that should persist across entry paths versus controls that are intentionally sub-view-specific
- export labeling and content correctness when users share perception findings outside the product
- identifying the boundary where parent-level guidance stops and source-specific documentation is required

High-risk failure patterns:
- a parent-level rule is generalized onto a sub-view whose metrics or interpretation are source-specific
- switching between sub-views keeps stale context and makes Search Insights, Vertical Insights, or Tentpole Strategy look like the same analysis with renamed tabs
- the entry page or export hides which perception lens was actually used, so downstream readers treat incompatible views as comparable

Typical P0 candidates:
- users are routed to the wrong perception lens and make brand decisions from an incompatible evidence source
- exported or externally shared perception output omits the chosen sub-view context and is consumed as authoritative brand guidance

## Source Links

- `Brand Insights`: `https://bytedance.sg.larkoffice.com/docx/L6O0drMbmo6d1vxFcAKcS4SPn1c`
- `Search Insights`: `https://bytedance.sg.larkoffice.com/docx/OLRKdWFEzoeYtAxWeuZlwEGygVe`
- `Vertical Insights`: `https://bytedance.sg.larkoffice.com/docx/Nm6kdyVjboyC6yxS1VvlEEejgG7`
- `Tentpole Strategy`: `https://bytedance.sg.larkoffice.com/docx/CUUednSAPo4Vyaxne7dlmbCbgZe`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- Treat this file as the Brand Perception parent entry for shared semantics and sub-view triage.
- Use this file when the job is to decide "which lens applies" or "what stays shared across lenses."
- If the question depends on a metric, rule, cadence, or workflow unique to one sub-view, go back to that source link instead of treating this parent file as universal truth.
- If this file materially shaped the answer, mention it explicitly.
