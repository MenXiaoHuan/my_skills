---
name: "interaction-testcase-generator"
description: "Creates detailed interaction-focused QA test cases and XMind trees from PRDs, designs, APIs, prototypes, or feature changes. Use for executable validation cases, not checklists, plans, summaries, reviews, debugging, or unit tests."
allowed-tools: Agent Task
---

`interaction-testcase-generator` 将需求、原型、API 和技术设计转为可执行的详细 QA 用例及 `.xmind`。它不生成测试计划、检查项、代码评审或单元测试。

## Authority Map

- `references/generation-protocol.md`：信息缺口、候选模式、覆盖与裁决流程
- `references/test-model.md`：内部 IR、coverage atom、分类与业务归属
- `references/test-design-methods.md`：交互、规则、状态、API、数据与异常设计方法
- `references/quality-gates.md`：覆盖计算、去重、最小充分集和门禁
- `references/risk-priority.md`：风险权重与 `P0/P1/P2/P3`
- `references/output-contract.md`：最终 JSON、XMind、标点和失败回退
- `examples/`：仅在领域形态接近时读取一个示例
- `templates/` 与 `scripts/`：构建和验证产物时使用

优先定向读取一份 reference，不批量加载整个目录。

## 五阶段工作流

1. **证据提取**：识别来源、业务目标、角色、模块、流程、规则、状态、接口、数据关系、依赖和风险。关键事实必须有来源；按 `generation-protocol.md` 决定追问、假设或 `draft`。
2. **内部测试 IR**：按 `test-model.md` 建模，并把最小可验证事实拆成 coverage atoms。禁止手填可由映射推导的覆盖率。
3. **候选生成**：按 `test-design-methods.md` 生成单一验证意图、独立可构造、结果可观察的候选。简单低风险单模块使用单候选并执行独立 gap scan；高风险、多模块、含接口或跨系统链路使用 `coverage-first` 与 `quality-first` 双候选。
4. **覆盖与裁决**：按 `quality-gates.md` 计算覆盖、识别标题和验证指纹重复、裁决覆盖包含关系，并选择风险加权的最小充分集。每个高风险目标必须覆盖正向与关键失败路径。
5. **兼容输出**：按 `risk-priority.md` 定级，转为 `output-contract.md` 规定的 case tree，严格校验后生成 XMind。默认只交付最终结果。

## Guardrails

- 材料是事实来源；不得臆造核心流程、权限、接口、状态或数据规则。
- API case 必须追溯到接口来源；数据一致性 case 必须追溯到数据不变量。
- `P0` 是高亮标签，不是覆盖过滤器。
- 最终结构按业务模块或工作流组织；接口、数据、权限和异常回填所属模块，仅无法归属时使用一个紧凑的 `其他`。
- 每个 case 必须有匹配优先级前缀的标题、`P0/P1/P2/P3`、非空字符串 `preconditions` 及非空 `steps`；每步必须有非空 `action` 和 `expected`。
- `preconditions`、`action` 和 `expected` 不得以中文句号结尾。
- 内部 IR、质量报告、原始候选和裁决草稿默认不向用户暴露。用户明确要求调试信息时可提供质量报告，但不提供原始候选。
- 最终 JSON/XMind 必须保持 `output-contract.md` 的兼容层级。纯文本评测环境只输出一个 fenced JSON case tree，不附加说明。
- 默认使用简体中文，除非用户指定其他语言。
