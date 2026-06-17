# Example: Competitive Landscape Module Tree With Cross-Coverage Backfill

Use this example when the request is a complex analytics/reporting page with several stable page modules, global filters, detail views, export behavior, and data-correctness risk.

## Example Input

```text
请基于 BP3.0 Market Competitive Landscape 页面需求生成详细测试用例并交付 xmind。页面包含全局筛选器、Market Landscape、Trend Analysis、Audience Persona、Competitive Landscape、Creative Insights、Creators Insights 等模块；支持 Market / Brand 视角切换、行业筛选、driverTag 过滤、下钻查看视频或达人详情；部分模块支持导出。请覆盖主流程、模块联动、权限、导出、数据正确性、异常、空态和边界场景。
```

## Target Style

This example intentionally follows a module-tree style:

- Keep stable product modules as top-level groups.
- Backfill permissions, exceptions, empty states, loading behavior, and data correctness into the owning module.
- Put residual global parameter validation or generic page behavior into one compact `其他` bucket.
- Do not create peer top-level buckets such as `数据正确性`, `异常与兜底`, or `页面交互与导航` unless the requirement explicitly asks for them as standalone acceptance themes.
- Combine low-risk filter controls when they share the same state and assertion surface.

## Example Analysis Shape

```text
1. Build primary module tree
   - 全局筛选器
   - Market Landscape
   - Trend Analysis
   - Audience Persona
   - Competitive Landscape
   - Creative Insights
   - Creators Insights
   - 其他

2. Backfill cross-cutting coverage into modules
   - 权限入口 -> 全局筛选器 or 其他
   - 数据正确性 -> owning module, such as Market Landscape or Trend Analysis
   - 导出一致性 -> module that owns the export
   - 空态 / loading / 接口失败 -> owning module when clear, otherwise 其他

3. Tighten granularity
   - combine related filter widgets into one filter-behavior case
   - avoid one case per tiny hover/copy/display variation
   - keep concrete exception assertions instead of broad `接口异常展示错误态`
```

## Example XMind Shape

```text
用例集
├── 全局筛选器
│   ├── [P1] 全局筛选器 - 切换行业 - 刷新所有业务模块
│   └── [P1] 全局筛选器 - 切换 Market / Brand 视角 - 保持可用筛选上下文
├── Market Landscape
│   ├── [P0] Market Landscape - Market View 指标 - 与接口返回口径一致
│   ├── [P1] Market Landscape - Brand View 切换 - Driver 保持选中并刷新明细
│   └── [P2] Market Landscape - 上一周期无数据 - 环比增速安全兜底
├── Trend Analysis
│   ├── [P1] Trend Analysis - driverTag 必传校验 - 缺失时阻断错误请求
│   ├── [P1] Trend Analysis - 时间粒度切换 - 趋势图重新聚合
│   └── [P1] Trend Analysis - Brand 未命中 driverTag - 展示空态且不误导
├── Audience Persona
│   └── [P2] Audience Persona - Audience Size 为 TBD - 展示占位且不支持导出
├── Competitive Landscape
│   ├── [P1] Competitive Landscape - 二级行业不可用 - TCC 与 industry 表状态一致
│   └── [P2] Competitive Landscape - 不支持下载 - 下载入口不可见或不可触发
├── Creative Insights
│   ├── [P1] Creative Insights - Top Videos - 列表按当前筛选上下文刷新
│   └── [P1] Creative Insights - Top Videos - 视频详情继承父模块上下文
├── Creators Insights
│   └── [P1] Creators Insights - Industry / Content / Collaboration 筛选组合 - 列表结果一致
└── 其他
    ├── [P1] 全局参数 - secondaryVerticalId 与 subMarket 不能同时为空
    └── [P2] 页面兜底 - 单模块接口失败不影响其他模块展示
```

## Notes

- This style favors a maintainable product module tree over a full horizontal audit outline.
- `其他` is a controlled residual bucket, not a dumping ground.
- Data correctness cases should be specific: name the metric, parameter, source, or fallback rule.
- Exception cases should be executable: name the missing parameter, failed dependency, timeout, or unsupported action.
