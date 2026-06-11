---
name: "checklist-generator"
description: "Use when the user needs structured test points, detailed test cases, coverage analysis, regression scope, or a real .xmind deliverable from requirement docs, technical designs, API specs, prototypes, change logs, or feature descriptions."
---

# Checklist Generator

Generate implementation-aware test points, detailed test cases, and a real `.xmind` file from requirement documents, technical designs, APIs, prototypes, change summaries, or structured feature descriptions.

This skill is cross-domain. It is not limited to web features. Use it for web, app, API, backend configuration, data reporting, and cross-system workflow testing.

## Use This Skill When

- The user asks for test cases, test points, QA checklist generation, coverage analysis, regression scope, or release-critical scenario identification.
- The user wants a deliverable that can drive execution, such as prioritized cases, a traceable checklist, or an XMind case tree.
- The user wants a testing output derived from requirement materials rather than a short prose summary.

## Do Not Use This Skill When

- The user only wants a short feature summary without a testing deliverable.
- The request is mainly about fixing code, debugging runtime behavior, or reviewing implementation quality.
- The user wants implementation code rather than a test design artifact.

## Operating Model

Treat requirement and technical materials as the primary source of truth.

Use supplementary reference skills only when those materials do not fully explain business terms, workflow semantics, role definitions, metric meanings, status logic, API contracts, or architecture dependencies.

Choose the relevant reference skill based on the knowledge gap:
- use a domain-oriented reference skill for business concepts, workflows, roles, status semantics, and metric meaning
- use an API-oriented reference skill for request and response contracts, field meaning, validation rules, and integration behavior
- use an architecture-oriented reference skill for cross-system dependencies, component boundaries, data flow, and upstream or downstream coupling

Do not use supplementary reference skills as a substitute for clear requirement or technical documents when those documents already answer the question.

Decision order:
1. Read requirement and technical materials first.
2. If core business, API, or architecture semantics are unclear, use the relevant reference skill.
3. If the remaining gap still affects scope, core workflow, user roles, expected behavior, or release risk, ask follow-up questions.
4. If only secondary details are missing, continue with explicit assumptions.
5. If critical source material is missing or contradictory, produce a draft instead of a final test design.

Default output language is Simplified Chinese. Use English only when the user explicitly asks for English.

`P0` is a highlight label for release-critical scenarios, not a filter.

## Progressive Disclosure

Read additional files only when needed:

- `references/decision-rules.md`
- `references/output-rules.md`
- `templates/xmind_input.template.json`
- `templates/response-template.md`
- `examples/web-login.md`
- `examples/order-api-idempotency.md`
- `scripts/xmind_build.py`

## Default Workflow

1. Identify the feature, affected systems, release scope, users, and main risks.
2. Read the requirement, technical design, API, prototype, and change summary.
3. Check whether any unresolved gap affects scope, workflow meaning, role behavior, contract semantics, or system boundaries.
4. If needed, use the relevant supplementary reference skill to close that knowledge gap.
5. Use `references/decision-rules.md` only when you need to decide whether to ask follow-up questions, proceed with assumptions, or produce a draft.
6. Derive test points, then expand them into detailed cases.
7. Mark `P0` scenarios when justified, but keep full in-scope coverage.
8. Generate a real `.xmind` file and return its absolute path first.

## Decision Rules

Use `references/decision-rules.md` only when you need finer guidance for:
- ask vs assume decisions
- draft vs final output decisions
- thin or conflicting source material

## Minimum Coverage

Unless the user explicitly narrows scope, cover the relevant subset of:

- core functional flows
- negative and validation scenarios
- permissions and role-based access
- boundary and data conditions
- state transitions and workflow gating
- integration dependencies
- regression-sensitive paths
- empty, loading, partial-data, and no-data behavior
- data accuracy, reporting consistency, export correctness, and cross-view consistency where applicable

## Output Rules

The primary deliverable is a real `.xmind` file on disk.

Always:
- return the absolute file path first
- keep supporting narration brief unless the user asks for more
- explicitly mark `P0` cases when justified
- state `本次范围未识别出 P0 场景` when no case truly qualifies
- preserve full agreed coverage beyond `P0`
- treat intermediate JSON as internal build data and do not present it as a user-facing output unless the user explicitly asks for debugging artifacts
- keep group and case titles free of Markdown bullet prefixes such as `+`, `-`, `*`, or numbered list markers
- separate confirmed information from assumptions when assumptions are used

## XMind Generation

1. Build a normalized JSON case tree with `root_title`, `groups`, `cases`, `priority`, `note`, `preconditions`, `description`, and `steps`.
2. Write that JSON to an internal build file such as `.test_case_xmind_input.json`.
3. Run:

```bash
python3 scripts/xmind_build.py .test_case_xmind_input.json output.xmind
```

4. Verify `output.xmind` exists and is non-empty before responding.

## Failure Handling

If the source materials conflict, identify the conflict explicitly instead of silently merging them.

If the source materials are thin, use `references/decision-rules.md` only when the next action is not obvious.

If `.xmind` generation fails, explain the exact failure and provide a fallback outline only as a failure mode.
