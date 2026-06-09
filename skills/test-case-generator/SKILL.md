---
name: "test-case-generator"
description: "Generate structured test points, detailed test cases, and real .xmind deliverables from requirement docs, technical designs, API specs, prototypes, change logs, or feature descriptions. Use for web, app, API, backend, data, reporting, or workflow testing whenever the user asks for QA design, coverage analysis, checklist generation, regression scope, or release-critical scenarios."
---

# Test Case Generator

Generate implementation-aware test points, detailed test cases, and a real `.xmind` file from requirement documents, technical designs, APIs, prototypes, change summaries, or structured feature descriptions.

This skill is cross-domain. It is not limited to web features. Use it for web, app, API, backend configuration, data reporting, and cross-system workflow testing.

## Use This Skill When

- The user asks for test cases, test points, QA checklist generation, coverage analysis, regression scope, or release-critical scenario identification.
- The user wants a deliverable that can drive execution, such as prioritized cases, a traceable checklist, or an XMind case tree.

## Do Not Use This Skill When

- The user only wants a short feature summary without a testing deliverable.
- The request is mainly about fixing code, debugging runtime behavior, or reviewing implementation quality.

## Operating Model

Treat requirement and technical materials as the primary source of truth.

Use supplementary reference skills only when those materials do not fully explain business terms, workflow semantics, role definitions, metric meanings, status logic, API contracts, or architecture dependencies. When that happens, use the matching reference skill such as `domain-reference-retriever`, `api-reference-retriever`, or `architecture-reference-retriever`.

Default output language is Simplified Chinese. Use English only when the user explicitly asks for English.

`P0` is a highlight label for release-critical scenarios, not a filter.

## Progressive Disclosure

Read additional files only when needed:

- `references/output-rules.md`
- `templates/xmind_input.template.json`
- `templates/response-template.md`
- `examples/web-login.md`
- `examples/order-api-idempotency.md`
- `scripts/xmind_build.py`

## Default Workflow

1. Identify the feature, affected systems, release scope, users, and main risks.
2. Read the requirement, technical design, API, prototype, and change summary.
3. Ask concise follow-up questions only when key information is missing.
4. Derive test points, then expand them into detailed cases.
5. Mark `P0` scenarios when justified, but keep full in-scope coverage.
6. Generate a real `.xmind` file and return its absolute path first.

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

## XMind Generation

1. Build a normalized JSON case tree with `root_title`, `groups`, `cases`, `priority`, `note`, `preconditions`, `description`, and `steps`.
2. Write that JSON to an internal build file such as `.test_case_xmind_input.json`.
3. Run:

```bash
python3 scripts/xmind_build.py .test_case_xmind_input.json output.xmind
```

4. Verify `output.xmind` exists and is non-empty before responding.

## Failure Handling

If the source materials conflict, identify the conflict explicitly.

If the source materials are thin, produce a draft only if the user still wants one and label assumptions clearly.

If `.xmind` generation fails, explain the exact failure and provide a fallback outline only as a failure mode.
