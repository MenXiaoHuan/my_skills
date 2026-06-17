# Example: Dual-Candidate Adjudication For A High-Risk Workflow

Use this example when the request is long, high-risk, cross-module, or historically unstable enough that a single-pass result is likely to drift in coverage or structure.

## When To Use

- approval workflow + export + notification + external sync
- reporting or operational features with multiple dependent branches
- prompts that are known to oscillate between over-coverage and under-coverage
- cases where one run usually has better coverage while another has cleaner grouping and stronger case quality

This mode is not optional for requests of this shape. A request with multiple stable modules plus approval, export, notification, or external-sync risk should not stay in single-pass mode.

## Goal

Generate two internal candidate case trees in parallel, then adjudicate them into one final normalized case tree.

- Candidate A: `coverage-first`
- Candidate B: `quality-first`

The user should only receive the final adjudicated `.xmind` result, not the raw candidate drafts.

Do not respond with “single-pass is enough” for this class of request. The whole point of this workflow is to reduce drift in coverage, grouping, and priority decisions across runs.

An implicit mental comparison is not enough. The workflow must create explicit internal Candidate A and Candidate B drafts before adjudication. The drafts are internal and should not be shown to the user by default.

## Example Input

```text
请基于以下审批中心需求设计详细测试用例，并默认输出真实 .xmind 文件。需求：运营提交促销审批后进入一级审核，一级通过后自动触发预算校验；预算通过后进入二级审核；任一级驳回都退回草稿并保留驳回原因；全部审核通过后同步营销平台创建活动，失败时需要记录可追踪状态并通知运营；页面支持按活动类型、审批状态、预算结果筛选并导出。请覆盖主流程、异常、权限、状态流转、预算校验、营销平台同步、通知和导出一致性，并标记 release-critical 场景。
```

## Candidate Role Split

### Candidate A: coverage-first

Focus on completeness first:

- expand approval branches, reject branches, rollback, and retry paths
- expand budget-check pass/fail/timeout behavior
- expand sync failure and notification behavior
- expand filter, export, and status-consistency checks
- tolerate some overlap that the adjudicator can prune later

### Candidate B: quality-first

Focus on precision first:

- keep one intent per case
- keep expectations concrete and observable
- reject weak boundary cases without a real business edge
- keep child pages, detail views, and exported artifacts under the correct parent lineage
- prefer tighter, cleaner grouping

## Example Adjudication Output Shape

The internal artifacts should follow this shape:

```text
Candidate A: coverage-first
- module tree outline: 审批主流程 / 预算校验 / 营销平台同步 / 筛选与导出 / 其他
- recommended cases: 主流程推进、一级/二级驳回、预算失败、预算超时、同步失败、导出一致性
- known weakness: may over-split rejection and notification cases

Candidate B: quality-first
- module tree outline: 审批中心 / 审批中心 - 活动详情 / 其他
- recommended cases: one-intent approval cases, concrete sync failure cases, cleaner grouping
- known weakness: may under-cover budget retry and notification fallback

Shared high-value cases
- 审批主流程成功推进
- 任一级驳回后退回草稿并保留原因
- 营销平台同步失败后状态可追踪且通知运营
- 导出结果与当前筛选一致

Candidate-only cases worth keeping
- 候选 A 的“预算校验超时后阻断进入二级审核”
- 候选 B 的“活动详情页继承审批列表上下文，不单独漂成一级模块”

Cases to drop
- 候选 A 中重复表达审批驳回提示的弱重复 case
- 候选 B 中过薄的样式类空态 case

Priority conflicts to resolve
- 营销平台同步失败应从 P1 提升为 P0
- 预算校验重试入口维持 P2

Final grouping fixes
- `审批中心 - 活动详情`
- `审批中心 - 导出结果`

Execution gate
- Candidate A draft exists: yes
- Candidate B draft exists: yes
- candidate roles are materially different: yes
- adjudication table exists: yes
- final tree is based on explicit merge decisions: yes
- raw candidate drafts are hidden from user-facing response: yes
```

## Example Final Output Shape

The final user-facing structure should still be a single XMind-oriented case tree, for example:

```text
用例集
└── 审批中心
    ├── 审批主流程
    │   ├── [P0] 审批中心 - 推进审批到终态 - 预算校验通过后进入二级审核
    │   └── [P1] 审批中心 - 驳回后退回草稿 - 保留驳回原因并允许修订
    ├── 预算校验
    │   ├── [P1] 审批中心 - 预算校验失败 - 阻断进入二级审核
    │   └── [P1] 审批中心 - 预算校验超时 - 保持可追踪状态并提示后续动作
    ├── 营销平台同步
    │   └── [P0] 审批中心 - 同步失败 - 记录可追踪状态并通知运营
    ├── 筛选与导出
    │   └── [P1] 审批中心 - 导出结果 - 与当前筛选条件保持一致
    └── 审批中心 - 活动详情
        └── [P2] 审批中心 - 活动详情 - 继承来源列表的上下文与状态信息
```

## Notes

- Use dual-candidate mode only when stability gain is worth the extra cost.
- The adjudicator should merge and prune; it should not blindly concatenate candidates.
- Candidate provenance is internal. The final artifact should look like one coherent case tree, not an A/B comparison report.
