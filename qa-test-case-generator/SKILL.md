---
name: "ttms-qa-checklist-generator"
description: "Generates TTMS QA checklists and test cases from requirement and technical docs, explicitly highlights P0 scenarios, and MUST output a real .xmind file (XMind 8 compatible). Invoke for TTMS web QA design when checklist, case design, or release-critical coverage is needed."
---

# TTMS QA Checklist Generator

Generate implementation-aware TTMS web QA test points, detailed test cases, and a real `.xmind` file from requirement documents, technical design materials, APIs, prototypes, or structured feature descriptions.

## Use This Skill When

- The user asks for TTMS-related QA test cases, test design, checklist generation, or coverage analysis.
- The request concerns TTMS B2B web modules such as Nomination Center, Audience, Brand Diagnosis, Brand Perception, Merchandise Mart, Catalog Analytics, or Post Campaign Report.
- The user expects a deliverable that can drive execution, such as prioritized test points, traceable test cases, or an XMind case tree.

## Do Not Use This Skill When

- The user only wants a brief feature summary with no testing deliverable.
- The request is about fixing source code, debugging runtime behavior, or reviewing code quality.
- No requirement context, technical context, or recoverable TTMS business context can be obtained.

## Operating Model

Treat requirement and technical materials as the primary source of truth. Use TTMS business references only when the provided materials do not fully explain TTMS-specific terms, workflow semantics, role definitions, metric meanings, or status logic.

Default output language is Simplified Chinese. Use professional English only when the user explicitly asks for English.

`P0` is a highlight label for release-critical scenarios, not a filter. Always keep full in-scope coverage after identifying `P0`.

## Input Priority

Ask for the following in roughly this order when they are not already available:

1. requirement document or release scope
2. technical design document
3. API specification or interface contract
4. prototype or wireframe
5. acceptance criteria or change summary

If the feature depends on TTMS-specific business semantics that are not clear from those sources, consult the relevant TTMS references selectively.

## Progressive Disclosure

Read additional files only when you need them:

- Read `references/output-contract.md` when you need stricter formatting rules, stable priority wording, response structure, or XMind hierarchy details.
- Read `references/ttms-modules.md` when TTMS domain semantics, playbook links, module-specific risks, or cross-module context are needed.
- Read `templates/xmind_input.template.json` when you want a stable starter shape for the case-tree JSON before generating the `.xmind`.
- Read `templates/response-template.md` when you want a concise default response skeleton after the file is generated.
- Run `scripts/xmind_build.py` when you are ready to turn a normalized case tree into a real `.xmind` file.

Do not load both reference files by default if the task can be completed from primary materials and the core workflow below.

## Examples and Templates

Use examples to anchor structure, not to override the user's actual scope.

- The examples in `references/output-contract.md` are for naming, response shape, and XMind JSON normalization.
- The templates under `templates/` are starter artifacts. Adapt them to the current feature instead of filling them mechanically.
- If the user's materials already define a clearer structure, follow the user's materials over the templates.

## Default Workflow

1. Confirm the testing target. Identify the TTMS feature, module, workflow, release scope, and intended users or roles.
2. Gather and read the primary materials. Extract business objectives, roles, workflows, inputs, outputs, validations, dependencies, status rules, metric definitions, UI interactions, and out-of-scope boundaries.
3. Ask concise follow-up questions only when key information is missing. Typical gaps include module ownership, affected tabs, role differences, status gating, metric/date-range rules, upstream/downstream dependencies, and explicit exclusions.
4. Derive test points before expanding to detailed cases. Organize coverage by module, workflow stage, or quality dimension. Mark release-critical `P0` candidates first, then continue with the remaining `P1/P2/P3` scope.
5. Expand prioritized cases. Keep each case executable, observable, and non-redundant. Prefer one primary scenario per case. State assumptions when the source material is incomplete.
6. Build the XMind deliverable. Convert the final case tree into structured JSON, generate the `.xmind` file, verify it exists, then return the absolute file path first.

## Minimum Coverage

Unless the user explicitly narrows scope, cover the relevant subset of:

- core functional flows
- negative and validation scenarios
- permissions and role-based access
- boundary and data conditions
- integration dependencies
- regression-sensitive paths
- empty, loading, partial-data, and no-data behavior
- metric, chart, table, and drill-down consistency where applicable

Keep the case set balanced and avoid trivial reworded duplicates.

## Output Rules

The primary deliverable is a real `.xmind` file on disk.

Always:
- return the absolute file path first
- keep supporting narration brief unless the user asks for more
- explicitly mark `P0` cases when justified
- state `本次范围未识别出 P0 场景` when no case truly qualifies
- preserve full agreed coverage beyond `P0`
- treat intermediate JSON as internal build data and do not present it as a user-facing output unless the user explicitly asks for debugging artifacts

Only provide markdown tables or outline previews when the user asks for them or they materially improve traceability.

For stricter formatting, table templates, response sections, and XMind hierarchy details, read `references/output-contract.md`.
For starter artifacts, use the files under `templates/`.

## XMind Generation

When generating the final file:

1. Build a normalized JSON case tree with:
   - `root_title`
   - `groups[]`
   - `cases[]`
   - `priority`
   - `note`
   - `preconditions`
   - `description`
   - `steps[] { action, expected }`
2. Write that JSON to an internal build file such as `.ttms_xmind_input.json` in the current working directory.
3. Run:

```bash
python3 scripts/xmind_build.py .ttms_xmind_input.json output.xmind
```

4. Verify `output.xmind` exists and is non-empty before responding.

Return only the final `.xmind` file path by default. Do not surface `.ttms_xmind_input.json` unless the user explicitly asks for the intermediate artifact.

Use `root_title = 用例集` unless the user explicitly requests another root title.

## Failure Handling

If the source materials conflict:
- identify the conflict explicitly
- keep affected cases marked as assumptions or open questions

If the source materials are thin:
- produce a draft only if the user still wants one
- label assumptions and missing confirmations clearly

If `.xmind` generation fails:
- explain the exact failure
- provide a fallback outline only as a failure mode
- do not present the main deliverable as successful

## Example Opening

`Please share the requirement document link, technical design document link, API documentation, prototype, or any other relevant references for the feature first. I will generate the test cases primarily from those materials and output a real .xmind file by default. If TTMS-specific business semantics are not fully described in the provided materials, I may also consult the relevant TTMS references as supplementary context.`
