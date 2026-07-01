# Coverage Ledger Rules

Read this file for stabilizing leaf-case coverage, module budgets, and coverage-vs-quality tradeoffs.

## Purpose

A coverage ledger stabilizes the final case tree before detailed cases are written. It is not user-facing by default.

Use it to lock three things:

- target top-level modules, workflows, entities, interfaces, or pages
- required coverage dimensions per target group
- expected case budget per target group

The goal is stable, high-value coverage, not an exact global case count.

## Required Ledger

Before expanding leaf cases, create an internal table with:

- module, workflow, entity, interface, or page name
- required dimensions: `core`, `data_correctness`, `exception`, `empty_state`
- conditional dimensions: `permission`, `export`, `state_transition`, `dependency_failure`, `boundary`, `multi_view`
- planned case budget: `[min, max]`
- notes for dimensions intentionally skipped

## Budget Rules

- For broad multi-module prompts, define a target total case count range before expanding cases.
- Default sparse-prompt starting range: 4-6 cases per top-level module; complex modules may significantly exceed the sparse starting range when source-backed scenario families require it.
- A module budget is not a coverage cap. Treat it as an initial planning range and stability guard, not a reason to drop meaningful cases.
- When the user provides a standard case set, expected leaf count, reference case tree, or dense requirement coverage list, use a configurable reference coverage floor; the suggested default is `0.9`, but the user-provided target or project convention wins.
- use source-defined modules, workflows, entities, interfaces, or pages as top-level groups unless the source explicitly defines another stable grouping.
- set a target top-level group count range from the source-defined modules, workflows, entities, interfaces, or pages before expanding cases.
- freeze canonical top-level module display names before expanding cases; do not append generic suffixes such as 模块, 功能, 页面, or 测试 unless the source uses that exact name.
- do not promote cross-cutting dimensions to top-level groups; cross-cutting dimensions include permissions, export, data correctness, exceptions, empty states, multi-view, and linkage.
- do not create nested subgroups solely to expand case count; nested groups are allowed only for real source-backed hierarchy.
- attach permissions, export, data correctness, exceptions, empty states, and linkage cases to owning modules before considering separate top-level audit buckets.
- Use a range, not a fixed number. A range allows valid consolidation without hiding large drift.
- Keep final module case counts inside the planned range unless the source material introduces a concrete new workflow.
- If the final count is outside budget, record a budget variance note before finalizing.
- Do not add thin cases just to hit the upper bound.
- Do not drop meaningful exception, data correctness, or empty-state coverage just to hit the lower bound.
- You must not reduce meaningful cases just to fit 4-6 cases per module.
- A budget is not a coverage target by itself. When a trusted reference or prior high-quality case set exists, set a configurable reference coverage floor before finalizing.
- If a generated result is far below a known standard case count, treat it as under-covered even when every module has some cases.
- If the final count is near the lower budget bound, re-check missing scenario families before accepting the result.

## Reference Coverage Floor

When a trusted reference case set is available:

- record the reference case id and reference leaf count internally
- set `min_reference_coverage_ratio`; the suggested default is `0.9` for broad multi-module product pages, unless the user or project convention provides another target
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
- require each case title to include the owning module name or a concrete scenario noun; generic repeated titles such as 模块基础功能验证, 数据导出功能验证, 数据正确性验证, 模块空态测试, and 模块接口异常处理 must be rewritten before finalizing

## Coverage Gap Scan

Run a second-pass coverage gap scan after the first adjudicated draft and before final delivery.

Check scenario families that apply to the source material:

- core path
- role or permission
- state transition
- exception and dependency failure
- data correctness
- empty state
- boundary
- export or download
- linkage
- notification
- audit or logging
- compatibility

Fill source-backed missing families before finalizing; do not deliver the first draft before the gap scan is complete, and do not add thin cases solely to increase count.

## Final Sweep

Before writing `.xmind`, check:

- every target module has a final case count within budget or a variance note
- every required dimension is covered or intentionally skipped with a reason
- every case has `preconditions`, `steps`, and expected results; use `No special preconditions` when no setup is needed
- `其他` contains only residual checks and does not hide major module behavior
- total leaf count drift is explainable by budgeted module decisions, not random split/merge behavior
