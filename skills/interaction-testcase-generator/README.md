# interaction-testcase-generator

本 skill 用于把需求文档、PRD、技术方案、API 说明、原型描述等材料，转成**面向交互验证的详细测试用例**。
默认交付物不是松散的测试点或 checklist，而是一份可执行、可展开、可直接交给 QA 使用的 `interaction-focused QA test cases`，通常落成真实 `.xmind` 文件。

## 适用范围

适合处理下面这类请求：

- “根据需求文档帮我设计测试用例”
- “根据接口设计整理详细 QA cases，并输出 xmind”
- “根据审批/导出/报表/权限需求，给出完整测试覆盖”

不适合处理下面这类请求：

- 只要测试点，不要详细 case
- 只要测试计划或回归范围，不要具体用例
- 代码 review、debug、修 bug、写单测

一句话理解：

> 该 skill 的定位是把需求材料转成交互验证详细用例树，而不是泛化测试顾问、checklist 工具或代码工具箱。

## 工作方式

默认流程可以简化理解为四步：

1. 读材料，搞清楚范围、角色、状态和风险
2. 先拆 coverage，再补异常、边界、权限、状态、依赖失败
3. 组织成结构化 case tree
4. 最后生成真实 `.xmind`

如果需求很长、跨多个模块，或者单次生成波动较大，还可以切到更稳的模式：

- 并行生成两个候选版本
- 一个偏 coverage-first
- 一个偏 quality-first
- 再做裁决合并，给出最终版

## 渐进式披露

这里的“渐进式披露”指的是：**先读最关键的文件，不一次把整个 skill 文件夹全塞进上下文。**

推荐按这个顺序读取：

1. 先看 `SKILL.md`
   - 判断这个 skill 该不该触发
   - 看默认流程怎么跑
2. 遇到具体问题，再按需看 `references/`
   - 追问还是假设：看 `decision-rules.md`
   - 输出格式和 XMind 结构：看 `output-rules.md`
   - 优先级不确定：看 `priority-rubric.md`
3. 只有场景接近时，再挑一个 `examples/` 看
4. 真要生成 `.xmind` 时，再看 `templates/` 和 `scripts/`

这样做的目的很直接：

- 减少无关上下文
- 提高触发和输出稳定性
- 避免规则在多个文件里重复、冲突

## 并行操作

这里的“并行”不是把所有步骤一起做，而是只在**可以独立分析**的部分才拆开并行。

典型并行方式包括：

- 权限分析一条线
- 主流程 / 状态流转一条线
- 异常 / 超时 / 回退一条线
- 数据一致性 / 导出一致性一条线

先并行拿到各自的风险和候选 case，再串行汇总，最后统一生成结果。

详细用例生成默认进入双候选模式：

- Candidate A：coverage-first
- Candidate B：quality-first
- 最后裁决合并成一个最终版

重点是：**并行的目的在于补漏和降低波动，而不是制造多份用户可见结果。**

## Single Source Map

- `SKILL.md`：主 skill 定义，决定何时触发、默认流程、并行节奏、多候选模式
- `references/decision-rules.md`：何时追问、何时假设、何时降级为 `draft`
- `references/output-rules.md`：输出契约、命名、XMind 层级
- `references/grouping-rules.md`：模块优先、横切回填、`其他`、父子归属
- `references/quality-rules.md`：case 粒度、异常覆盖、边界判断、薄 case 控制
- `references/multi-candidate-rules.md`：默认双候选流程与裁决合并
- `references/priority-rubric.md`：`P0/P1/P2/P3` 判级标准

## 目录结构

```text
skills/interaction-testcase-generator/
├── SKILL.md
├── README.md
├── examples/
├── references/
├── scripts/
└── templates/
```

各目录职责如下：

- `SKILL.md`：主 skill 定义，只保留触发与流程
- `README.md`：维护入口与文件地图
- `examples/`：按场景选择的 few-shot 参考
- `references/`：唯一权威规则，按触发、分组、质量、多候选、优先级分文件维护
- `scripts/`：生成真实 `.xmind` 文件的脚本
- `templates/`：中间结构、响应模板、双候选内部裁决模板

## Example Routing

| 需求类型 | 推荐 example | 典型信号 |
| --- | --- | --- |
| 登录、鉴权、账号状态、MFA、锁定 | `examples/web-login.md` | 账号密码、验证码、锁定窗口、登录成功/失败 |
| API 合约、幂等、冲突、重试、并发 | `examples/order-api-idempotency.md` | `Idempotency-Key`、409、202、重复请求、处理中 |
| 复杂分析页、Competitive Landscape、模块树与横切回填 | `examples/competitive-landscape-module-tree.md` | Market Landscape、Trend、Persona、Creative/Creator、模块多且横切风险多 |
| 报表分析、维度切换、筛选联动、数据一致性、下载 | `examples/trend-analysis-reporting.md` | 视角切换、时间粒度、driverTag、图表/下载一致性、Fun Facts |
| 权限控制、后台报表、导出成功/超时/失败回退、下载中心 | `examples/permission-report-export.md` | 角色差异、导出按钮、下载中心、超时回退、筛选保留 |
| 高风险长需求、跨模块流程、单次输出波动较大 | `examples/multi-candidate-adjudication.md` | 审批+导出+同步+通知、覆盖与结构易摇摆、需要更稳的最终版 |

## 维护原则

- 规则只放在 `references/`，不要把规则复制回 `README.md`
- `README.md` 负责讲清楚用途、入口和文件地图，不负责承载细规则
- 新 example 只在新增了稳定失败模式或新领域覆盖时加入
- 新 benchmark 先补到 `eval/`，再决定是否需要新 example
