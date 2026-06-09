# TTMS Module: Brand Perception

Use this file only when the change touches insight browsing, reporting, export, or content synchronization across Brand Perception views.

## Use This Module For

- filter combinations and segmentation dimensions
- table and chart synchronization
- metric explanation correctness
- data freshness and partial-data behavior
- export workflow correctness

## Business Semantics

### Core Workflow
- select a perception sub-view such as Brand Insights, Search Insights, Vertical Insights, or Tentpole Strategy
- apply filters and segmentation dimensions
- compare synchronized table and chart output
- export or report selected insight results

### Important Branches
- Brand Insights
- Search Insights
- Vertical Insights
- Tentpole Strategy

### Status and Visibility Rules
- filters must affect all linked components consistently
- freshness messaging must reflect real data completeness

## Testing Prompts

Prioritize:
- filter combinations and segmentation dimensions
- table and chart synchronization
- metric explanation correctness
- data freshness and partial-data behavior
- export workflow correctness

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered report is materially wrong
- a release breaks the main customer-facing insight workflow

## Source Links

- `Brand Insights`: `https://bytedance.sg.larkoffice.com/docx/L6O0drMbmo6d1vxFcAKcS4SPn1c`
- `Search Insights`: `https://bytedance.sg.larkoffice.com/docx/OLRKdWFEzoeYtAxWeuZlwEGygVe`
- `Vertical Insights`: `https://bytedance.sg.larkoffice.com/docx/Nm6kdyVjboyC6yxS1VvlEEejgG7`
- `Tentpole Strategy`: `https://bytedance.sg.larkoffice.com/docx/CUUednSAPo4Vyaxne7dlmbCbgZe`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
