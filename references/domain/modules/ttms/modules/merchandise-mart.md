# TTMS Module: Merchandise Mart

Use this file only when the change touches merchandise insight browsing, reporting, export, or content synchronization across Merchandise Mart views.

## Use This Module For

- merchandise insight browsing
- filter and segmentation behavior
- table and chart synchronization
- data freshness messaging
- export and reporting correctness

## Business Semantics

### Core Workflow
- open merchandise insight views
- apply filters and segmentation dimensions
- compare synchronized table and chart output
- export or report selected merchandise insight results

### Important Branches
- filter combinations
- segmented vs unsegmented views
- on-screen browsing vs exported output

### Status and Visibility Rules
- filters must affect all linked components consistently
- freshness and empty-state messaging must reflect real data completeness

## Testing Prompts

Prioritize:
- merchandise insight browsing
- filter and segmentation behavior
- table and chart synchronization
- data freshness messaging
- export and reporting correctness

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered report is materially wrong
- the main merchandise insight workflow is broken for customer-facing usage

## Source Links

- `Merchandise Mart`: `https://bytedance.sg.larkoffice.com/docx/Rr4AdFQN9o6rKxxj9JSlLCSrg5f`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
