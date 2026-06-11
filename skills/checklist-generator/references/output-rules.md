# Output Rules

Read this file only when you need stricter behavior constraints, priority wording, or XMind generation rules beyond the default workflow in `SKILL.md`.

Use `templates/` for fixed output formats.

Use `examples/` for few-shot examples of good input and output patterns.

## Deliverable Rules

Default output is a real `.xmind` file generated on disk.

Always:
- return the absolute file path first
- keep supporting narration short unless the user asks for more detail
- treat the `.xmind` file as the primary deliverable
- generate a complete in-scope case set, not only `P0`
- mark `P0` cases explicitly when justified
- state assumptions when source material is incomplete
- call out document conflicts instead of silently merging contradictions

Do not:
- expose the intermediate JSON build file unless the user explicitly asks for debugging artifacts
- return only a prose summary when the user expects test cases
- invent domain-specific business rules without a clear source or an explicit assumption label
- use `P0` as a filter that suppresses `P1/P2/P3`

If generation fails, explain the exact failure and provide a fallback outline only as a failure mode.

## Naming Rules

Use concise, implementation-aware case names.

Recommended patterns:

- Test point: `[Module] - [Business Rule or Verification Focus]`
- Test case: `[Module] - [Action] - [Condition or Expected Behavior]`

Title hygiene:

- do not prefix group titles or test case titles with Markdown list markers such as `+`, `-`, `*`, or numbered bullets
- output clean topic titles only, for example use `任务创建 - 历史参考节点设置`, not `+任务创建 - 历史参考节点设置`
- keep priority labels like `[P0]` only when they are part of the actual case title

## Priority Model

- `P0`: Release-critical path, launch blocker, or severe failure on a core workflow
- `P1`: High-value or high-risk behavior with strong business or operational impact
- `P2`: Important but non-blocking scenario with moderate impact or fallback
- `P3`: Low-risk, low-frequency, cosmetic, or optional coverage

If no case truly qualifies, explicitly state:

`本次范围未识别出 P0 场景`

## XMind Contract

Preferred hierarchy:
- Root topic: `用例集`
- Group node: a short module or workflow label
- Test case node: one topic per case
- Detail node under case: `前置条件` preferred, `文本描述` allowed when setup is not needed
- Step nodes under detail branch
- Expected result node under each step

Priority mapping:
- `P0` -> `priority-1`
- `P1` -> `priority-2`
- `P2` -> `priority-3`
- `P3` -> `priority-4`

Use a normalized case tree before generating the final file.

Write the JSON to an internal build file such as `.test_case_xmind_input.json`.

For the JSON skeleton, use `templates/xmind_input.template.json`.

For the response layout, use `templates/response-template.md`.

For table output, follow the field conventions in this skill and generate a concise Markdown table directly when the user explicitly asks for table-form deliverables.
