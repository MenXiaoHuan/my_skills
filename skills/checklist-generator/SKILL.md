---
name: "checklist-generator"
description: "Use when the user wants detailed QA test cases or an XMind case tree derived from requirements, PRDs, technical designs, API specs, prototypes, change logs, or feature descriptions for web, app, API, backend workflow, reporting, export, or cross-system changes. Do not use for loose test points, test plans, requirement summaries, implementation proposals, code review, debugging, or unit and automation test generation."
allowed-tools: Agent Task
---

`checklist` is retained only as the skill name. The actual artifact is a structured detailed QA test case set, usually delivered as `.xmind`.

## Authority Map

- `references/decision-rules.md`: when deciding ask vs assume vs `draft`
- `references/priority-rubric.md`: when `P0/P1/P2/P3` grading is uncertain
- `references/output-rules.md`: artifact terminology, output contract, naming, and XMind hierarchy
- `references/grouping-rules.md`: when module-first structure, `其他`, and parent-child lineage matter
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
4. Build a compact module-first case tree, then backfill permissions, exceptions, data consistency, and boundary coverage into the owning module or `其他`.
5. Always use dual-candidate mode for detailed case generation. Explicitly `spawn` 2 candidates in parallel when `Agent` or `Task` is available:
   - Candidate A: `coverage-first`
   - Candidate B: `quality-first`
6. Require explicit Candidate A and Candidate B internal drafts, a target top-level module set, coverage ledger, per-module case budget, and an adjudication table before finalizing.
7. Run exception and boundary scans, then expand only meaningful coverage into detailed QA cases with priorities.
8. Self-check with `references/grouping-rules.md`, `references/quality-rules.md`, and `references/coverage-ledger-rules.md`.
9. Keep each case title short, write concise `note`, build normalized JSON, and generate the final `.xmind`.

## Analysis Pattern

When the request is broad or the material is dense, explicitly use the word `spawn` for independent analysis tracks.

Preferred rhythm: `先并行, 再串行, 再并行, 再串行`.

Only split materially independent tracks. If `Agent` or `Task` is available, actually `spawn` them. Otherwise keep the same decomposition and execute serially. After each wave, merge findings before writing cases.

Each track should return:
- `scope`
- `key risks`
- `coverage candidates`
- `exception candidates`
- `boundary candidates`
- `open questions`
- `recommended cases`

The final structure should usually look like:
- top level: stable modules or workflows
- inside each module: happy path, state changes, permissions, exceptions, consistency, and justified boundaries
- optional `其他`: only one compact catch-all bucket when residual cases do not clearly belong to one module
- cross-cutting top-level groups: only when the topic truly spans multiple modules and would be awkward or misleading if forced into one owner

Dual-candidate roles differ on purpose:
- `coverage-first`: more aggressive on completeness, exception expansion, permission and state splits, dependency failures, and regression-sensitive paths
- `quality-first`: more conservative on case count, stricter on one-intent-per-case, clearer expectations, tighter lineage, and weaker-boundary rejection

The adjudicator should return:
- `shared high-value cases`
- `candidate-only cases worth keeping`
- `duplicates or weak cases to drop`
- `priority conflicts to resolve`
- `grouping or lineage fixes`
- `final normalized case tree`

## Guardrails

- Treat requirement and technical materials as the source of truth.
- Ask follow-up questions only when the gap changes scope, workflow meaning, role behavior, expected outcomes, or release risk.
- If only secondary details are missing, continue with explicit assumptions.
- If critical workflow, role, contract, or dependency facts are missing or contradictory, produce a `draft` instead of a final case set.
- `P0` is a highlight label, not a coverage filter.
- Exception paths should be expanded by default when they are plausible within the described workflow, dependency chain, or user interaction.
- Boundary cases are conditional: scan for them every time, but only output them when the requirement, contract, state model, timing rule, limit, or data semantics suggests a meaningful edge.
- If no standalone boundary case is justified, keep the coverage focused and make that a deliberate outcome rather than manufacturing weak cases.
- Prefer module-first organization over horizontal audit buckets. A structure that follows the product’s real modules is usually easier to read, review, and maintain.
- Cross-cutting coverage such as permissions, exceptions, empty states, loading behavior, and data consistency should usually be attached to the relevant module rather than promoted to a parallel top-level branch.
- When ownership is unclear, prefer one compact `其他` bucket over creating multiple new peer branches such as `页面交互与导航`, `数据正确性`, or `异常与兜底`.
- Do not let the output drift into too many top-level groups. A compact, stable module tree is usually more maintainable than a fully unpacked audit outline.
- Group naming should preserve navigation and ownership semantics. A child page, detail page, or modal flow should inherit the parent module label unless the source material clearly treats it as an independent module.
- Dual-candidate mode is the default generation path for this skill. Producing only one draft is a workflow mistake, not a style preference.
- Dual-candidate mode must produce explicit internal A/B drafts and an adjudication table before finalization. A single blended draft, or a claim that two perspectives were considered, is still single-pass.
- Do not claim dual-candidate mode was used unless the internal artifacts satisfy `references/multi-candidate-rules.md`.
- In dual-candidate mode, freeze the final top-level module set before expanding leaf cases, then reject naming drift unless the source material justifies a new stable module.
- For broad prompts with prior leaf-count drift, use `references/coverage-ledger-rules.md` to stabilize required coverage dimensions and per-module case budgets before writing detailed cases.
- When a trusted reference case set exists, per-module budget cannot override the reference coverage floor; a stable but materially smaller case tree is still under-covered.
- The final output must be a single adjudicated result. Do not expose raw candidate drafts, A/B comparisons, or internal merge artifacts to the user unless the user explicitly asks for debugging output.
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
