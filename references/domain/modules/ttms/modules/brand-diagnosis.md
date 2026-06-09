# TTMS Module: Brand Diagnosis

Use this file only when the feature affects funnel metrics, benchmark logic, or reporting consistency.

## Use This Module For

- funnel grouping semantics
- metric glossary correctness
- campaign mapping logic
- benchmark-dependent behavior
- cross-view reporting consistency

## Business Semantics

### Core Workflow
- interpret premium reach, massive reach, consideration, and conversion
- apply benchmark-dependent metric logic
- compare summary and detail reporting views

### Important Branches
- with benchmark vs without benchmark
- summary cards vs detail tables and charts

### Status and Visibility Rules
- glossary and displayed metric values must stay aligned
- benchmark changes must not silently alter downstream meaning

## Testing Prompts

Prioritize:
- funnel grouping correctness
- glossary and tooltip consistency
- campaign mapping classification
- benchmark-dependent metric behavior
- cross-card, chart, and glossary consistency

High-risk failure patterns:
- metric definitions differ across views
- benchmark changes silently alter downstream values
- glossary text and displayed calculations drift apart

Typical P0 candidates:
- core reporting metrics become materially incorrect for decision-making
- summary and detail views disagree on key business numbers

## Source Links

- `Brand Diagnosis`: `https://bytedance.sg.larkoffice.com/docx/TEFzdBzFYofX7hxRakxlE4Qvgzf`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
