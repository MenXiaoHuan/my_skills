# Example: Permissioned Report Export With Fallback

Use this example when the request mixes permissions, reporting views, export behavior, and failure fallback in one backend feature.

## Example Input

```text
请基于以下后台报表页需求设计测试用例，并默认输出真实 .xmind 文件。需求：报表页仅管理员和分析师可访问完整报表页；运营角色不可进入完整报表页，但可在概览首页查看摘要卡片；完整报表页支持按组织、日期范围、报表类型筛选；图表和表格展示的数据必须保持一致；点击导出后若导出服务正常，则生成报表文件并提示下载成功；若导出服务超时，则页面提示“导出任务已提交，请稍后在下载中心查看”；若接口失败，则保留当前筛选条件并给出失败提示。请覆盖权限、筛选联动、数据一致性、导出成功、超时回退、失败回退、空态、异常和边界场景，并标记 release-critical 场景。
```

## Example Analysis Plan Shape

For mixed backend reporting features, the skill should split the analysis into independent tracks and merge twice:

```text
1. parallel track: permission analysis
   - 管理员 / 分析师 / 运营 三类角色
   - 页面入口、概览卡片、明细表、导出按钮可见性

2. parallel track: single-variable filter analysis
   - 组织筛选
   - 日期范围筛选
   - 报表类型筛选

3. 串行汇总第一波结果
   - 统一角色边界
   - 识别必须继续展开的数据一致性和导出路径

4. parallel track: report consistency analysis
   - 概览卡片与明细表一致性
   - 页面筛选条件与导出内容一致性

5. parallel track: export and fallback analysis
   - 导出成功
   - 导出超时转下载中心
   - 导出失败后保留筛选条件
   - 下载中心中的任务与导出范围一致
   - 下载中心中的权限与源页面导出权限一致

6. 串行汇总第二波结果
   - 去重、补齐前置条件、统一优先级
7. 生成最终详细测试用例
```

## Example Output Shape

```text
### P0 Scenario Summary
- `Permissioned Report - Only authorized roles can access details and export`
- `Permissioned Report - Export fallback keeps current filters and routes the user correctly when the export service times out`

### Source Summary
- user-provided backend reporting requirement text

### Full Case Coverage Summary
- role-based access and visibility
- single-filter and combined-filter behavior
- chart, card, table, and export consistency
- export success, timeout fallback, and failure fallback
- empty state and abnormal response coverage
- boundary cases only when the source material implies a real limit, threshold, timing window, or other meaningful edge

### Risks and Open Questions
- need confirmation on whether analysts and admins see the same export columns
- need confirmation on download center polling or refresh behavior after export timeout
```

## Example XMind Shape

The final user-facing answer should deliver the generated `.xmind` file as the primary artifact, without exposing a local absolute path, and the generated file itself should follow an XMind-oriented case tree similar to:

```text
用例集
└── Permissioned Report
    ├── [P1] Permissioned Report - Block operator from entering the full report page
    │   ├── 前置条件
    │   │   └── 当前账号角色为运营
    │   └── 步骤
    │       └── 步骤 1: 尝试进入完整报表页
    │           └── 预期 1: 无法进入完整报表页，但可在概览首页查看摘要卡片
    ├── [P1] Permissioned Report - Update report content after changing report type filter
    │   └── 步骤
    │       └── 步骤 1: 切换报表类型筛选
    │           └── 预期 1: 图表、概览卡片和明细表同步刷新且筛选条件一致
    ├── [P1] Permissioned Report - Keep chart, summary cards, and detail table consistent
    │   ├── 前置条件
    │   │   └── 页面已按目标组织、日期范围和报表类型完成筛选
    │   └── 步骤
    │       └── 步骤 1: 核对概览卡片、图表和明细表中的核心数值
    │           └── 预期 1: 各视图展示的统计口径和结果一致
    ├── [P0] Permissioned Report - Export file matches current filters on success
    │   ├── 前置条件
    │   │   └── 当前账号角色有导出权限且页面已完成筛选
    │   └── 步骤
    │       └── 步骤 1: 点击导出并等待成功返回
    │           └── 预期 1: 成功生成报表文件，文件内容与当前页面筛选条件一致
    ├── [P1] Permissioned Report - Keep filters and show failure message on export error
    │   ├── 前置条件
    │   │   └── 当前账号角色有导出权限且导出接口返回失败
    │   └── 步骤
    │       └── 步骤 1: 点击导出
    │           └── 预期 1: 页面保留当前筛选条件并给出失败提示
    ├── [P0] Permissioned Report - Create a correct download-center task after export timeout
    │   ├── 前置条件
    │   │   └── 当前账号角色有导出权限且导出服务超时
    │   └── 步骤
    │       └── 步骤 1: 点击导出后前往下载中心查看任务
    │           └── 预期 1: 下载中心生成与当前筛选范围一致的导出任务
    ├── [P0] Permissioned Report - Enforce the same export permission in download center
    │   ├── 前置条件
    │   │   └── 导出任务已进入下载中心
    │   └── 步骤
    │       └── 步骤 1: 使用不同角色查看或下载该导出任务
    │           └── 预期 1: 仅具备导出权限的角色可查看或下载对应文件
    └── [P0] Permissioned Report - Route user to download center on export timeout
        ├── 前置条件
        │   └── 当前账号角色有导出权限且导出服务超时
        └── 步骤
            └── 步骤 1: 点击导出
                └── 预期 1: 页面提示任务已提交，并引导用户稍后前往下载中心查看
```

## Example Builder Input Shape

When the skill needs to build the actual `.xmind` file, the normalized JSON should be close to:

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "Permissioned Report",
      "cases": [
        {
          "title": "[P0] Permissioned Report - Route user to download center on export timeout",
          "priority": "P0",
          "note": "聚焦超时降级后的用户引导与任务留痕是否完整，属于发布关键路径。",
          "preconditions": "当前账号角色有导出权限且导出服务超时",
          "description": "",
          "steps": [
            {
              "action": "点击导出",
              "expected": "页面提示任务已提交，并引导用户稍后前往下载中心查看",
              "note": "同时观察筛选条件是否被保留，以及提示文案是否明确指向下载中心。"
            }
          ]
        }
      ]
    }
  ]
}
```

## Notes

- Use parallel subtask tools to separate permission, filter, consistency, and export-fallback analysis when the environment supports them; otherwise run the same tracks serially before merging.
- Treat role visibility, data consistency, and timeout fallback as distinct verification intents rather than one merged case.
- When fallback behavior exists, verify both user messaging and state retention, such as preserved filters and preserved page context.
- In this example, exception coverage is mandatory because export success, timeout, and failure are explicit requirement branches.
- Boundary coverage should be scanned, but only promoted to standalone cases if the requirement or contract actually defines meaningful edges such as export size limits, date-range limits, retry windows, or polling thresholds.
- Keep the `[P0]` or `[P1]` title prefix aligned with the `priority` field and XMind marker.
- Keep the case `title` scannable and move explanatory context into `note` so the XMind topic can show a subtitle-like supplement.
