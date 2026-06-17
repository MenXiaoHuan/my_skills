---
name: "checklist-generator"
description: "Use when the user wants detailed QA test cases or an XMind case tree derived from requirements, PRDs, technical designs, API specs, prototypes, change logs, or feature descriptions for web, app, API, backend workflow, reporting, export, or cross-system changes. Do not use for loose test points, test plans, requirement summaries, implementation proposals, code review, debugging, or unit and automation test generation."
allowed-tools: Agent Task
---

`checklist` is retained only as the skill name. The actual artifact is a structured detailed QA test case set, usually delivered as `.xmind`.

## Authority Map

- `references/decision-rules.md`: when deciding ask vs assume vs `draft`
- `references/priority-rubric.md`: when `P0/P1/P2/P3` grading is uncertain
- `references/output-rules.md`: artifact terminology, output contract, naming, quality, and XMind hierarchy
- `examples/`: when the domain shape is similar and you need few-shot guidance
- `templates/` and `scripts/xmind_build.py`: only when building the final `.xmind`

Prefer one targeted read over bulk-loading the whole skill folder.

## Default Workflow

1. Read the requirement, technical design, API, prototype, or change summary.
2. Clarify scope, affected systems, roles, and release risk.
3. Decide whether gaps require a follow-up question, an explicit assumption, or a `draft`.
4. Split coverage by workflow, validation, permissions, state transitions, integrations, and consistency.
5. Use `spawn` only when there are materially independent analysis tracks worth splitting.
6. Expand coverage slices into detailed QA cases and grade priorities with the rubric.
7. Keep each case topic title short, then write a concise `note` as the subtitle-like supplement shown under the title in XMind.
8. Generate and deliver the final `.xmind` file.

## Analysis Pattern

When the request is broad or the material is dense, explicitly use the word `spawn` for independent analysis tracks.

Preferred rhythm: `先并行, 再串行, 再并行, 再串行`.

Only split materially independent tracks. If `Agent` or `Task` is available, actually `spawn` them. Otherwise keep the same decomposition and execute serially. After each wave, merge findings before writing cases.

Each track should return:
- `scope`
- `key risks`
- `coverage candidates`
- `open questions`
- `recommended cases`

## Guardrails

- Treat requirement and technical materials as the source of truth.
- Ask follow-up questions only when the gap changes scope, workflow meaning, role behavior, expected outcomes, or release risk.
- If only secondary details are missing, continue with explicit assumptions.
- If critical workflow, role, contract, or dependency facts are missing or contradictory, produce a `draft` instead of a final case set.
- `P0` is a highlight label, not a coverage filter.
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
