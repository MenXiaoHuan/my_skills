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
- if multi-candidate generation is used internally, merge and adjudicate before responding so the user sees one final deliverable rather than multiple competing drafts

Do not:
- expose a local or workspace absolute path as the main user-facing result
- expose the intermediate JSON build file unless the user explicitly asks for debugging artifacts
- return only a prose summary when the user expects test cases
- invent domain-specific business rules without a clear source or an explicit assumption label
- use `P0` as a filter that suppresses `P1/P2/P3`
- expose raw candidate A/B outputs, internal compare notes, or merge scratchpads unless the user explicitly asks for them

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
- preserve parent-child lineage in group titles when the child page, drawer, modal, tab, or sub-flow is entered from a parent module; prefer `Top10 Videos - 视频详情` over a detached top-level group like `视频详情`
- only let a child page become a top-level group when the source material clearly describes it as an independent module with its own stable entry, ownership boundary, or release scope

## Related Rule Files

- Use `grouping-rules.md` when deciding module-first structure, `其他`, top-level groups, or parent-child lineage.
- Use `quality-rules.md` when deciding case granularity, exception coverage, boundary judgment, or thin-case control.
- Use `multi-candidate-rules.md` when dual-candidate mode is mandatory or candidate adjudication is needed.
- Use `priority-rubric.md` when priority grading is uncertain.

## Quality Rules

Default case-quality guidance lives in `quality-rules.md`. Keep this file focused on the final artifact contract.

## Priority Model

Use `priority-rubric.md` when priority grading is uncertain.

If no case truly qualifies as `P0`, explicitly state `本次范围未识别出 P0 场景`.

## XMind Contract

Preferred hierarchy:
- Root topic: `用例集`
- Group node: a short module or workflow label
- Optional subgroup node: use when multiple sibling modules clearly belong to the same business parent
- Test case node: one topic per case, with `note` populated by default
- Optional detail node under case: `前置条件` when setup is needed
- Optional detail node under case: `文本描述` when narrative context is needed and setup is not needed
- Step nodes directly under the case as a sibling branch to `前置条件` or `文本描述`
- Expected result node under each step

Normalized JSON fields:
- root: `root_title`, optional `note`
- group: `title`, optional `note`, optional `groups`, optional `cases`
- case: `title`, `priority`, recommended `note`, optional `preconditions`, optional `description`, `steps`
- step: `action`, `expected`, optional `note`

Shared parent grouping rules:
- prefer flat group titles by default when generating normalized JSON; let the builder auto-merge a shared parent during XMind rendering
- use explicit nested `groups` only when the source material already contains a clear business hierarchy that must be preserved as-is
- when input is still flat, the builder may auto-merge sibling groups into a shared parent if at least 2 group titles match `共同父节点 - 子模块`
- auto-merge only when the shared prefix is a real business domain label, not a generic word such as `页面`, `模块`, `列表`, `功能`, or similar placeholders
- after auto-merge, the shared parent is only a structure node; the original child groups keep their own `cases`, `note`, and nested `groups`
- if the shared prefix is ambiguous or appears only once, keep the original flat structure
- if a detail page or subordinate view belongs to a parent workflow, encode that relationship in the group title before rendering so the builder can preserve the intended hierarchy instead of treating it as a separate top-level module

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
