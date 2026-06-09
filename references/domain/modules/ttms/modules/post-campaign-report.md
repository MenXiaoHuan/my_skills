# TTMS Module: Post Campaign Report

Use this file only when the change touches post-campaign reporting, export, or delivered-report consistency.

## Use This Module For

- post-campaign reporting workflows
- reporting output and export correctness
- data freshness semantics
- filter and date-range consistency
- externally delivered report validation

## Business Semantics

### Core Workflow
- open post-campaign reporting views
- apply filters and date ranges
- compare on-screen report sections and summary components
- export or deliver the final report

### Important Branches
- filtered vs unfiltered reporting
- on-screen report vs exported or delivered report
- full-data vs partial-data reporting

### Status and Visibility Rules
- filters and date ranges must stay consistent across report sections
- freshness messaging must reflect delivery readiness and data completeness

## Testing Prompts

Prioritize:
- post-campaign reporting workflows
- reporting output and export correctness
- data freshness semantics
- filter and date-range consistency
- externally delivered report validation

High-risk failure patterns:
- filters affect one component but not another
- delivered report does not match on-screen selection
- freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered report is materially wrong
- a release breaks the main post-campaign reporting workflow

## Source Links

- `Post Campaign Report`: `https://bytedance.sg.larkoffice.com/docx/RhHIdMos0oe8I5xxSXOlMn99gTc`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
