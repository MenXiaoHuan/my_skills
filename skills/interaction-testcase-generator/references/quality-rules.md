# Quality Rules

Read this file when the hard part is case granularity, exception coverage, boundary judgment, or avoiding thin/duplicated cases.

## Case Quality

Always:

- establish `business goal → core flow → failure risk → verification intent → observable assertion` before expanding detailed cases
- map every core business goal to at least one case and every high-risk goal to both a positive case and a critical-failure case
- keep one case focused on one verification intent
- keep `前置条件` limited to role, permission, data, state, and environment setup
- make every case independently constructible; never depend on another case's execution result
- put actions only in `步骤`
- make key steps state the entry, operation target, necessary input, and trigger action
- make expected results observable, concrete, and verifiable
- make expected results identify the verification target and state or data change
- make exception expectations verify error feedback, data invariance, and applicable compensation or recovery behavior
- split cases when role, state, request contract, or expected outcome changes
- cover single-variable behavior first, then add high-risk combinations or pairwise interactions
- write a concise `note` for each case topic by default; use it for focus, risk, or business context, not a title repeat

When backend technical documents or API specifications are part of the source material:

- link business actions with key API verification instead of describing only frontend or business gestures
- make request parameters, response fields, status codes or error codes, and data side effects visible when they are necessary to verify the scenario
- keep API checks tied to the case intent; do not turn every case into a pure API test

Avoid:

- merged mega-cases with unrelated assertions
- vague expectations such as `展示正常` or `返回正确结果`
- putting steps or expectations inside `前置条件`
- preconditions containing actions such as click, input, select, submit, invoke, verify, or open
- unobservable expectations such as `处理成功`, `操作成功`, or `符合预期` without a concrete verification target
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
- does every core goal have a mapped case and every high-risk goal have positive plus critical-failure coverage
- do priorities match goal risk, impact scope, and recoverability rather than general visibility
- are `preconditions`, `action`, and `expected` free of trailing Chinese full stops while preserving internal and non-Chinese punctuation
