---
name: "interaction-testcase-generator"
description: "Creates detailed interaction-focused QA test cases and XMind trees from PRDs, designs, APIs, prototypes, or feature changes. Use for executable validation cases, not checklists, plans, summaries, reviews, debugging, or unit tests."
allowed-tools: Agent Task
---

`interaction-testcase-generator` creates structured detailed QA test cases for interaction validation, usually delivered as `.xmind`.

## Authority Map

- `references/decision-rules.md`: when deciding ask vs assume vs `draft`
- `references/priority-rubric.md`: when `P0/P1/P2/P3` grading is uncertain
- `references/output-rules.md`: artifact terminology, output contract, naming, and XMind hierarchy
- `references/grouping-rules.md`: when module-first structure, `Miscellaneous`, and parent-child lineage matter
- `references/quality-rules.md`: when case granularity, exception coverage, boundary judgment, or thin-case control matters
- `references/multi-candidate-rules.md`: default dual-candidate execution and adjudication requirements
- `references/coverage-ledger-rules.md`: when broad multi-module prompts need stable leaf-case coverage and per-module budgets
- `examples/`: when the domain shape is similar and you need few-shot guidance
- `templates/` and `scripts/xmind_build.py`: only when building the final `.xmind`

Prefer one targeted read over bulk-loading the whole skill folder.

## Default Workflow

1. Read the requirement, technical design, API, prototype, or change summary.
2. Clarify scope, affected systems, roles, and release risk.
3. Decide whether gaps require a follow-up question, an explicit assumption, or a `draft`.
4. Build a compact module-first case tree, then backfill permissions, exceptions, data consistency, and boundary coverage into the owning module or `Miscellaneous`.
5. Always use dual-candidate mode for detailed case generation. Use parallel subtask tools for 2 candidates when available; otherwise create 2 separate internal drafts serially:
   - Candidate A: `coverage-first`
   - Candidate B: `quality-first`
6. Require explicit Candidate A and Candidate B internal drafts, a target top-level module/workflow set, coverage ledger, per-module or per-workflow case budget, and an adjudication table before finalizing.
7. Run exception and boundary scans, then expand only meaningful coverage into detailed QA cases with priorities.
8. Run a second-pass coverage gap scan across scenario families before finalizing; do not deliver the first draft before the gap scan is complete.
9. Self-check with `references/grouping-rules.md`, `references/quality-rules.md`, and `references/coverage-ledger-rules.md`.
10. Keep each case title short, write concise `note`, include `preconditions`, structured `steps`, and expected results, build normalized JSON, and generate the final `.xmind` when file generation is available.
11. In a final-answer-only or runtime evaluation environment, return exactly one fenced ```json block containing the final normalized case tree before any XMind/script fallback. Do not include prose before or after that JSON block.

## Analysis Pattern

For broad or dense material, split only materially independent tracks. Use parallel subtask tools such as `Agent` or `Task` when available; otherwise keep the same decomposition and create separate serial internal drafts.

Preferred rhythm: parallelize independent analysis, consolidate serially, parallelize focused gap checks, then finalize serially.

Each track should return `scope`, `key risks`, coverage/exception/boundary candidates, open questions, and recommended cases.

The final structure should usually be stable modules or workflows, with happy paths, state changes, permissions, exceptions, consistency, and justified boundaries attached to the owning module. Use one compact `Miscellaneous` bucket only for residual cases.

Dual-candidate roles differ on purpose:
- `coverage-first`: completeness, exception expansion, permission/state splits, dependency failures, and regression-sensitive paths
- `quality-first`: one-intent-per-case, clearer expectations, tighter lineage, and weak-case rejection

The adjudicator should keep shared high-value cases, candidate-only cases worth keeping, priority/grouping fixes, and the final normalized case tree; drop duplicates and weak cases.

## Guardrails

- Treat requirement and technical materials as the source of truth; ask only when gaps change scope, workflow meaning, role behavior, expected outcomes, or release risk.
- If only secondary details are missing, continue with explicit assumptions; if critical workflow, role, contract, or dependency facts are missing or contradictory, produce a `draft`.
- `P0` is a highlight label, not a coverage filter.
- Expand plausible exception paths, scan boundaries every time, and output boundary cases only when the source semantics justify them.
- Prefer module-first organization over horizontal audit buckets; attach cross-cutting coverage to owning modules and use one compact `Miscellaneous` bucket only when ownership is unclear.
- Dual-candidate mode is the default generation path. It must produce explicit internal A/B drafts and an adjudication table; do not claim dual-candidate mode was used unless `references/multi-candidate-rules.md` is satisfied.
- In dual-candidate mode, freeze the final top-level module set before expanding leaf cases. The final tree must use the frozen target top-level module set unless source-backed internal notes justify a deviation.
- For broad, dense, or reference-backed prompts, apply `references/coverage-ledger-rules.md`: module budgets are not coverage caps, use a configurable reference coverage floor when a trusted reference exists, and do not reduce meaningful cases just to fit 4-6 cases per module.
- Use source-defined modules, workflows, entities, interfaces, or pages as top-level groups; preserve canonical display names and avoid generic suffix drift unless the source uses that exact name.
- Each case title must include the owning module name or a concrete scenario noun; reject generic repeated titles such as basic module validation, data export validation, data correctness validation, empty-state validation, and module API error handling when they appear under multiple modules.
- Each detailed case must include `preconditions`, `steps`, and expected results. If no setup is needed, set `preconditions` to `No special preconditions`.
- Every step must include an expected result that states the observable outcome, data change, state change, permission result, or error handling result.
- When backend technical documents or API specifications are provided, link business actions with key API verification in the execution steps.
- Before finalizing, run a coverage gap scan across scenario families and fill source-backed gaps; do not add thin cases solely to increase count.
- The final output must be a single adjudicated result. Do not expose raw candidate drafts, A/B comparisons, or internal merge artifacts unless the user explicitly asks for debugging output.
- In final-answer-only or runtime evaluation environment, summaries, coverage lists, statistics, or promises are not valid deliverables. Return the final normalized JSON case tree, not a plan to inspect files or generate cases later.
- do not start the final response with exploration promises; finish internal analysis first, then output the final normalized case tree.
- In final-answer-only or runtime evaluation environment, do not inspect repository files unless the user explicitly asks for codebase analysis; use the provided prompt content and explicit assumptions instead.
- Default output language is Simplified Chinese unless the user asks for English.

## XMind Generation

Use `references/output-rules.md` for the JSON schema and XMind contract.

1. Build a normalized JSON case tree.
2. Write the JSON to an internal build file such as `.test_case_xmind_input.json`.
3. Populate `note` for each case by default. Use it for focus, risk, or business-context supplements, not for repeating the title.
4. Keep `title` short and scannable. Put secondary explanation in `note`.
5. Run:

```bash
python3 scripts/xmind_build.py .test_case_xmind_input.json output.xmind
```

6. Verify `output.xmind` exists and is non-empty before responding.

If `.xmind` generation fails, explain the exact failure and provide a fallback outline only as a failure mode.
