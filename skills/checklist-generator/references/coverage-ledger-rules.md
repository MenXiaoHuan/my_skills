# Coverage Ledger Rules

Read this file for stabilizing leaf-case coverage, module budgets, and coverage-vs-quality tradeoffs.

## Purpose

A coverage ledger stabilizes the final case tree before detailed cases are written. It is not user-facing by default.

Use it to lock three things:

- target top-level modules
- required coverage dimensions per module
- expected case budget per module

The goal is stable, high-value coverage, not an exact global case count.

## Required Ledger

Before expanding leaf cases, create an internal table with:

- module name
- required dimensions: `core`, `data_correctness`, `exception`, `empty_state`
- conditional dimensions: `permission`, `export`, `state_transition`, `dependency_failure`, `boundary`, `multi_view`
- planned case budget: `[min, max]`
- notes for dimensions intentionally skipped

## Budget Rules

- Use a range, not a fixed number. A range allows valid consolidation without hiding large drift.
- Keep final module case counts inside the planned range unless the source material introduces a concrete new workflow.
- If the final count is outside budget, record a budget variance note before finalizing.
- Do not add thin cases just to hit the upper bound.
- Do not drop meaningful exception, data correctness, or empty-state coverage just to hit the lower bound.
- A budget is not a coverage target by itself. When a trusted reference or prior high-quality case set exists, set a reference coverage floor before finalizing.
- If the final count is near the lower budget bound, re-check missing scenario families before accepting the result.

## Reference Coverage Floor

When a trusted reference case set is available:

- record the reference case id and reference leaf count internally
- set `min_reference_coverage_ratio`, usually `0.85` for broad multi-module product pages
- compare the final leaf count against `reference_leaf_count * min_reference_coverage_ratio`
- if the final count is below the floor, return to coverage expansion instead of finalizing
- prefer adding missing scenario families over splitting thin display checks

Do not hardcode product names, reference ids, or reference counts into the generic workflow. They belong in eval fixtures, examples, or user-provided context.

## Merge Rules

When adjudicating candidates:

- map both candidates into the same ledger before comparing leaf cases
- compare missing dimensions first, then compare duplicate or thin cases
- keep candidate-only cases when they fill a ledger gap
- drop candidate-only cases when their dimension is already covered by a stronger case
- reject module-name drift before comparing leaf counts

## Final Sweep

Before writing `.xmind`, check:

- every target module has a final case count within budget or a variance note
- every required dimension is covered or intentionally skipped with a reason
- `其他` contains only residual checks and does not hide major module behavior
- total leaf count drift is explainable by budgeted module decisions, not random split/merge behavior
