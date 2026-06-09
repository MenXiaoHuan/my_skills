# TTMS Module: Audience

Use this file only when the feature affects ACC journeys, transition analysis, or model-driven audience behavior.

## Use This Module For

- ACC stage definitions and transitions
- diagram and table toggle semantics
- drill-down flows
- touchpoint, creator, and video insight sections
- model-specific audience analysis

## Business Semantics

### Core Workflow
- select an ACC model
- inspect journey and transition stages
- switch between visual and tabular views
- drill into downstream audience details

### Important Branches
- Web Payment
- Web Payment and Registration
- App Payment
- Ticketing
- past 7, 15, and 30 day windows

### Status and Visibility Rules
- selected stage or journey must propagate to downstream views
- selected model and time window must stay consistent across related components

## Testing Prompts

Prioritize:
- ACC stage definitions and transition logic
- transition tiles and diagram or table toggle behavior
- drill-down flows
- touchpoint, creator, and video insight sections
- time-window and model-specific behavior

High-risk failure patterns:
- selected stage or journey does not propagate to downstream views
- time-window switching causes inconsistent metrics or segmentation
- drill-down results do not match summary tiles

Typical P0 candidates:
- core transition analysis cannot be completed end to end
- selected model or time window produces materially wrong audience results

## Source Links

- `Audience`: `https://bytedance.sg.larkoffice.com/docx/K5azdNO98oWMqYxTuHLlHLrkgbf`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
