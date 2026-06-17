# Example: Trend Analysis Reporting

Use this example when the request is analytics-focused and the expected output is structured detailed QA test cases plus a real `.xmind` file.

## Example Input

```text
请基于以下趋势分析页面需求设计测试用例，并默认输出真实 .xmind 文件。需求：页面支持切换 Market/Brand 两种分析视角，支持 DAY/WEEK/MONTH 时间粒度切换，支持 driverTag 过滤，支持下载当前趋势分析数据；趋势图需要展示指定 metric 的时间序列变化；若品牌未命中当前 driverTag，则需要展示空状态提示；页面还会展示 Fun Facts 洞察卡片。请覆盖正常流程、维度切换、筛选联动、数据准确性、空态、下载、异常和边界场景，并标记 release-critical 场景。
```

## Example Analysis Plan Shape

For broad analytics features, the skill should explicitly use `spawn` for independent tracks before synthesizing final cases:

```text
1. spawn single-variable analysis
   - 视角切换
   - 时间粒度切换
   - driverTag 筛选

2. 串行汇总第一波结果
   - 合并单变量发现
   - 识别共享歧义与缺失前置条件
   - 确定需要继续展开的高风险组合

3. spawn dual-variable analysis
   - 视角 × driverTag
   - 时间粒度 × 下载结果

4. spawn data quality checks
   - 趋势图点位与聚合口径
   - 空数据/缺失数据/延迟数据
   - 页面图表与下载文件一致性

5. spawn fun facts validation
   - 洞察卡片展示条件
   - 洞察文案与主图数据一致性

6. 串行汇总第二波结果
   - 去重、补齐前置条件、统一优先级
7. 再生成最终详细测试用例
```

## Example Output Shape

```text
### P0 Scenario Summary
- `Trend Analysis - DriverTag filter updates the trend chart with the correct scoped data`
- `Trend Analysis - Downloaded report matches the current page filters and visible chart data`

### Source Summary
- user-provided analytics requirement text

### Full Case Coverage Summary
- perspective switching
- time-grain switching
- driverTag filtering
- chart data accuracy and aggregation consistency
- empty state and unsupported brand handling
- download and cross-view consistency
- fun facts visibility and insight correctness

### Risks and Open Questions
- need confirmation on the exact aggregation formula and rounding rule for each metric
- need confirmation on whether Fun Facts should disappear or downgrade when source data is incomplete
```

## Example XMind Shape

The final user-facing answer should deliver the generated `.xmind` file as the primary artifact, without exposing a local absolute path, and the generated file itself should follow an XMind-oriented case tree similar to:

```text
用例集
└── Trend Analysis
    ├── [P1] Trend Analysis - Switch analysis perspective between Market and Brand
    │   └── 步骤
    │       ├── 步骤 1: 在页面中切换到 Brand 视角
    │       │   └── 预期 1: 页面展示 Brand 维度趋势图与相关筛选项
    │       └── 步骤 2: 再切回 Market 视角
    │           └── 预期 2: 页面恢复 Market 维度趋势图且数据范围正确
    ├── [P0] Trend Analysis - Update trend chart after selecting driverTag
    │   ├── 前置条件
    │   │   └── 已命中有效 driverTag 且页面已有趋势数据
    │   └── 步骤
    │       └── 步骤 1: 选择某个 driverTag
    │           └── 预期 1: 趋势图仅展示该 driverTag 范围内的数据
    ├── [P1] Trend Analysis - Show empty state when Brand does not match current driverTag
    │   ├── 前置条件
    │   │   └── 当前 Brand 不在所选 driverTag 的支持范围内
    │   └── 步骤
    │       └── 步骤 1: 保持 Brand 视角并应用该 driverTag
    │           └── 预期 1: 页面展示空状态提示且无误导性趋势数据
    ├── [P0] Trend Analysis - Downloaded file matches current filters and chart data
    │   ├── 前置条件
    │   │   └── 页面已按目标视角、时间粒度与 driverTag 完成筛选
    │   └── 步骤
    │       └── 步骤 1: 点击下载
    │           └── 预期 1: 下载文件中的维度、筛选条件与核心数值与页面一致
    └── [P2] Trend Analysis - Fun Facts cards stay consistent with source metrics
        ├── 前置条件
        │   └── 页面已返回 Fun Facts 洞察卡片数据
        └── 步骤
            └── 步骤 1: 校验洞察卡片文案与主趋势图、筛选范围
                └── 预期 1: 洞察描述、数值和适用范围一致
```

## Example Builder Input Shape

When the skill needs to build the actual `.xmind` file, the normalized JSON should be close to:

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "Trend Analysis",
      "cases": [
        {
          "title": "[P0] Trend Analysis - Downloaded file matches current filters and chart data",
          "priority": "P0",
          "preconditions": "页面已按目标视角、时间粒度与 driverTag 完成筛选",
          "description": "",
          "steps": [
            {
              "action": "点击下载",
              "expected": "下载文件中的维度、筛选条件与核心数值与页面一致"
            }
          ]
        }
      ]
    }
  ]
}
```

## Notes

- Use `spawn` explicitly when the feature contains several independent analytics dimensions.
- If sub-task capability is unavailable, keep the same branch split but execute the branches serially before merging.
- Cover single-variable behavior first, then add high-risk combinations and consistency checks.
- Treat data quality, download consistency, and fun facts correctness as first-class QA tracks for analytics features.
- Keep the `[P0]` or `[P1]` title prefix aligned with the `priority` field and XMind marker.
