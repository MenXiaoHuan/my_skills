# Grouping Rules

Read this file when the difficult part is case tree structure, module ownership, parent-child lineage, or whether a cross-cutting concern should become a top-level group.

## Module-First Structure

- Top-level groups should usually map to stable product modules, workflows, tabs, or child pages that match how users and reviewers understand the feature.
- Keep the main reading path close to the product information architecture rather than turning the output into a horizontal audit checklist.
- Keep the top-level group count compact; prefer a small stable module set plus, if needed, one `其他` bucket over many peer audit buckets.

## Cross-Cutting Coverage Placement

Attach permissions, exceptions, empty-state behavior, loading behavior, and data consistency checks to the owning module whenever the owner is clear.

Create a standalone top-level group for a cross-cutting concern only when it truly spans multiple modules and is independently reviewable as one acceptance theme.

When ownership is unclear but the concern is still local or residual, place it under `其他` instead of creating new top-level groups such as:

- `页面交互与导航`
- `数据正确性`
- `异常与兜底`

Use `其他` as a controlled sink for residual page interaction, global parameter validation, minor layout checks, or global error handling that do not clearly belong to a single module.

## Parent-Child Lineage

Preserve parent-child lineage in group titles when a child page, drawer, modal, tab, or sub-flow is entered from a parent module.

Prefer:

- `Top10 Videos - 视频详情`
- `审批中心 - 活动详情`

Avoid detached top-level groups such as:

- `视频详情`
- `活动详情`

Only let a child page become a top-level group when the source material clearly describes it as an independent module with its own stable entry, ownership boundary, or release scope.
