# Output Rules

Read this file only when you need stricter behavior constraints, priority wording, or XMind generation rules beyond the default workflow in `SKILL.md`.

Use `templates/` for fixed output formats.

Use `examples/` for few-shot examples of good input and output patterns.

## Artifact Terminology

- `checklist-generator` is only the skill name and trigger term
- call the actual artifact `detailed QA test cases`
- do not describe the final artifact as loose `test points`, a high-level `test plan`, or a generic `checklist` unless the user explicitly asks for that coarser deliverable

## Deliverable Rules

Default output is a real `.xmind` file that is generated and delivered to the user.

Always:
- deliver the generated `.xmind` file as the primary user-facing artifact
- keep supporting narration short unless the user asks for more detail
- treat the `.xmind` file as the primary deliverable
- generate a complete in-scope test case set, not only `P0`
- mark `P0` cases explicitly when justified
- state assumptions when source material is incomplete
- call out document conflicts instead of silently merging contradictions

Do not:
- expose a local or workspace absolute path as the main user-facing result
- expose the intermediate JSON build file unless the user explicitly asks for debugging artifacts
- return only a prose summary when the user expects test cases
- invent domain-specific business rules without a clear source or an explicit assumption label
- use `P0` as a filter that suppresses `P1/P2/P3`

If generation fails, explain the exact failure and provide a fallback outline only as a failure mode.

## Naming Rules

Use concise, implementation-aware case names.

Recommended patterns:

- Test case: `[Module] - [Action] - [Condition or Expected Behavior]`

Title hygiene:

- do not prefix group titles or test case titles with Markdown list markers such as `+`, `-`, `*`, or numbered bullets
- output clean topic titles only, for example use `任务创建 - 历史参考节点设置`, not `+任务创建 - 历史参考节点设置`
- include `[P0]`, `[P1]`, `[P2]`, or `[P3]` in case titles as a compatibility fallback for platforms that do not parse XMind priority markers
- keep the title prefix aligned with the `priority` field; they must not disagree
- use the `priority` field and XMind marker rendering as the structured source of truth
- prefer short topic titles; move secondary explanation, risk reminder, or observation point into `note` instead of overloading the title

## Quality Rules

Always:
- keep one case focused on one verification intent
- keep `前置条件` limited to setup, data state, role state, or environment state
- put actions only in `步骤`
- make expected results observable, concrete, and verifiable
- split cases when role, state, request contract, or expected outcome changes
- cover single-variable behavior first, then add high-risk combinations or pairwise interactions
- write a concise `note` for each case topic by default so XMind can show a subtitle-like supplement under the title
- keep `note` short and explanatory, usually one sentence or one clause, such as the business intent, focus point, or key risk being verified

Avoid:
- merged mega-cases with multiple unrelated assertions
- vague expectations such as `展示正常` or `返回正确结果`
- putting steps or expectations inside `前置条件`
- repeating the full title verbatim inside `note`

## Priority Model

- `P0`: Release-critical path, launch blocker, or severe failure on a core workflow
- `P1`: High-value or high-risk behavior with strong business or operational impact
- `P2`: Important but non-blocking scenario with moderate impact or fallback
- `P3`: Low-risk, low-frequency, cosmetic, or optional coverage

Rating rules:
- use `P0` when failure blocks launch, blocks a core money path, breaks a core reporting truth source, causes irreversible data loss, creates severe permission leakage, or makes a primary workflow unavailable
- use `P1` when failure does not block launch but materially harms a high-value workflow, core operator efficiency, or major downstream correctness
- use `P2` when failure is important but recoverable, bounded in scope, or has a reasonable workaround
- use `P3` when failure is low-risk, low-frequency, cosmetic, or affects non-critical convenience behavior

Quick heuristics:
- ask whether the release should be stopped if this case fails
- ask whether the failure affects a core workflow, core role, core metric, or externally visible correctness
- ask whether the failure spreads to other systems, exports, notifications, or downstream decisions
- downgrade when the issue is recoverable, scoped, and does not mislead users or operators in a critical path

If no case truly qualifies, explicitly state:

`本次范围未识别出 P0 场景`

## XMind Contract

Preferred hierarchy:
- Root topic: `用例集`
- Group node: a short module or workflow label
- Test case node: one topic per case, with `note` populated by default
- Optional detail node under case: `前置条件` when setup is needed
- Optional detail node under case: `文本描述` when narrative context is needed and setup is not needed
- Step nodes directly under the case as a sibling branch to `前置条件` or `文本描述`
- Expected result node under each step

Normalized JSON fields:
- root: `root_title`, optional `note`
- group: `title`, optional `note`, `cases`
- case: `title`, `priority`, recommended `note`, optional `preconditions`, optional `description`, `steps`
- step: `action`, `expected`, optional `note`

Priority mapping:
- `P0` -> `priority-1`
- `P1` -> `priority-2`
- `P2` -> `priority-3`
- `P3` -> `priority-4`

Priority rendering should use both:
- marker mapping above for platforms that parse XMind priority markers
- `[P0]` text prefixes in case titles as a compatibility fallback for platforms that do not

Use a normalized case tree before generating the final file.

Write the JSON to an internal build file such as `.test_case_xmind_input.json`.

For the JSON skeleton, use `templates/xmind_input.template.json`.

For the response layout, use `templates/response-template.md`.

For table output, follow the field conventions in this skill and generate a concise Markdown table directly when the user explicitly asks for table-form deliverables.
