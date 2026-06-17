# Quality Rules

Read this file when the hard part is case granularity, exception coverage, boundary judgment, or avoiding thin/duplicated cases.

## Case Quality

Always:

- keep one case focused on one verification intent
- keep `前置条件` limited to setup, data state, role state, or environment state
- put actions only in `步骤`
- make expected results observable, concrete, and verifiable
- split cases when role, state, request contract, or expected outcome changes
- cover single-variable behavior first, then add high-risk combinations or pairwise interactions
- write a concise `note` for each case topic by default; use it for focus, risk, or business context, not a title repeat

Avoid:

- merged mega-cases with unrelated assertions
- vague expectations such as `展示正常` or `返回正确结果`
- putting steps or expectations inside `前置条件`
- repeating the full title verbatim inside `note`

## Exception And Boundary Coverage

Exception paths are default coverage whenever plausible:

- timeout
- failure
- fallback
- rejection
- empty-state
- partial-data
- dependency-error behavior

Boundary cases are conditional. Scan for thresholds, time windows, state edges, enum edges, empty/extreme data, duplicates, and concurrency every time, but output standalone boundary cases only when a real business or contract edge exists.

If no standalone boundary case is justified, keep the case set focused and do not invent thin boundary cases just to raise the count.

## Thin Case Control

Combine closely related light checks when they share the same user intent, state, and assertion surface, especially for:

- default states
- filter widgets
- low-risk presentation checks
- adjacent hover/copy/display checks

Prefer one stronger case with concrete expectations over several thin sibling cases that only vary by wording or a minor display nuance.

Avoid splitting one filter area into many weak per-control cases when a combined filter-behavior case would be clearer and closer to the product workflow.

## Final Sweep

Before delivering the final case set, quickly ask:

- have core exception paths been expanded beyond the happy path
- have dependency failure, timeout, rollback, or fallback behaviors been considered when the workflow touches external systems
- have empty-state, no-data, and inconsistent-data behaviors been considered when the feature shows lists, reports, cards, charts, or exports
- have real business boundaries been checked for limits, timing windows, state transitions, duplicate operations, or concurrency
- if no boundary case is output, is that because no meaningful edge exists rather than because the scan was skipped
