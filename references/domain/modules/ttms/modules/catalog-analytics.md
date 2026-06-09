# TTMS Module: Catalog Analytics

Use this file only when the change touches catalog reporting, export, or content synchronization across Catalog Analytics views.

## Use This Module For

- catalog reporting workflows
- export consistency
- metric explanation correctness
- data freshness and partial-data behavior
- filter-driven cross-view consistency

## Business Semantics

### Core Workflow
- open catalog reporting views
- apply filters and dimensions
- compare synchronized table and chart output
- export or report selected catalog metrics

### Important Branches
- filtered vs unfiltered reporting
- on-screen analysis vs exported output
- full-data vs partial-data scenarios

### Status and Visibility Rules
- filters must affect all linked reporting components consistently
- freshness messaging must reflect partial-data and stale-data states honestly

## Testing Prompts

Prioritize:
- catalog reporting workflows
- export consistency
- metric explanation correctness
- data freshness and partial-data behavior
- filter-driven cross-view consistency

High-risk failure patterns:
- filters affect one component but not another
- export output does not match on-screen selection
- data freshness messaging is absent or misleading

Typical P0 candidates:
- exported or externally delivered catalog report is materially wrong
- a release breaks the main catalog analysis workflow

## Source Links

- `Catalog Analytics`: `https://bytedance.larkoffice.com/wiki/BwruwhM4Yif2W1kaYTEcHaREn6f`

## Notes For Agent Usage

- Prefer explicit requirement and technical docs first.
- Use this file only to fill TTMS-specific semantic gaps.
- If this file materially shaped the answer, mention it explicitly.
