# 交互测试用例生成 Skill 内部 IR 重构设计

## 背景

`interaction-testcase-generator` 已具备业务目标提取、模块分组、双候选生成、覆盖账本和 XMind 输出能力，但当前实现仍有以下结构性问题：

- 规则分散在 `SKILL.md`、七份 reference、多个 example 和 template 中，存在重复与冲突
- 覆盖账本依赖人工声明，没有从最终用例反向计算覆盖结果
- 去重只识别完全相同的标题，无法识别验证意图相同的语义重复和薄用例
- 功能交互、接口契约和数据一致性缺少统一建模，生成质量依赖自然语言提示
- 当前 artifact eval 不实际生成 XMind，无法发现构建器和最终产物回归
- 构建器会为不完整输入生成占位节点，而不是拒绝非法 case tree
- 正向 fixture 与规则契约不完全一致，部分质量指标虽然实现但未进入基线门禁

本次重构以“完备但不冗余、规范且不重复、分类具体、证据可追溯”为核心目标

## 目标

- 保持最终标准化 JSON 和 XMind 层级兼容
- 新增内部结构化测试 IR，统一表达业务目标、流程、规则、状态、接口、数据关系和风险
- 从 IR 生成覆盖原子，并由最终用例反向计算覆盖率
- 同时生成有文档依据的交互、接口、数据一致性、权限、异常和边界用例
- 使用确定性归一化、验证意图指纹和覆盖包含关系消除重复
- 使用风险加权的集合覆盖方法得到最小充分用例集
- 生成内部质量报告，并以质量门禁阻止不完整或冗余产物
- 重构并删除重复、冲突和无独立价值的文件
- 增加 `AGENTS.md`，约束 Skill 与 eval 的维护方式
- 建立真实 XMind 端到端评测

## 非目标

- 不改变用户可见 case tree 的必填字段
- 不将内部 IR、候选草稿和裁决过程默认暴露给用户
- 不引入 ACTS、PICT、GraphWalker、向量数据库或第三方 Python 包
- 不执行真实线上接口请求
- 不凭空补充文档未提供的接口、状态和数据规则
- 不建设完整测试管理平台
- 不使用用例数量作为完备性的主要指标

## 总体架构

生成流程分为五个阶段：

```text
证据提取
  → 内部测试 IR
  → 候选用例生成
  → 覆盖与去重裁决
  → 兼容输出与质量报告
```

每个阶段有独立输入、输出和质量门禁。最终输出仍使用现有：

```json
{
  "root_title": "用例集",
  "groups": []
}
```

内部字段不得泄漏到最终 case tree

## 证据模型

所有可测试结论必须关联来源。来源类型包括：

- `requirement`：需求条款、验收标准和业务目标
- `prototype`：页面、控件、弹窗、抽屉和交互路径
- `api`：接口方法、路径、参数、响应、错误码和鉴权
- `technical_design`：状态机、存储、缓存、消息、回调、补偿和依赖
- `data_definition`：指标口径、字段定义、聚合关系和导出规则
- `assumption`：明确标记的次要假设

证据记录使用稳定 ID：

```json
{
  "id": "SRC-API-003",
  "type": "api",
  "title": "创建订单接口",
  "locator": "接口设计/3.2",
  "facts": ["POST /orders", "重复幂等键返回原订单"]
}
```

核心流程、角色权限、状态迁移、接口契约和数据不变量不能只依赖 `assumption`

## 内部测试 IR

内部 IR 使用以下顶层结构：

```json
{
  "version": "1.0",
  "sources": [],
  "business_goals": [],
  "actors": [],
  "modules": [],
  "workflows": [],
  "states": [],
  "business_rules": [],
  "api_contracts": [],
  "data_entities": [],
  "data_invariants": [],
  "dependencies": [],
  "risks": [],
  "coverage_atoms": [],
  "candidate_cases": [],
  "assumptions": [],
  "conflicts": []
}
```

### 工作流

工作流表达：

- 所属模块
- 参与角色
- 起始状态
- 用户或系统动作
- 合法后态
- 关键失败分支
- 终止条件
- 来源

流程型需求以模型驱动测试思想建模：动作对应迁移边，状态与可观察结果对应验证节点

### 业务规则

业务规则表达条件、动作和例外：

```json
{
  "id": "RULE-004",
  "conditions": ["订单未关闭", "库存充足"],
  "outcome": "允许提交",
  "exceptions": ["库存校验超时"],
  "source_refs": ["SRC-REQ-008"]
}
```

包含多个独立条件时使用决策表生成有效组合，不穷举无业务意义的笛卡尔积

### 接口契约

仅当材料中存在接口证据时创建：

```json
{
  "id": "API-003",
  "method": "POST",
  "path": "/orders",
  "auth": [],
  "parameters": [],
  "responses": [],
  "error_codes": [],
  "side_effects": [],
  "idempotency": null,
  "dependencies": [],
  "source_refs": []
}
```

接口 case 可覆盖：

- 方法、路径和鉴权
- 必填、可选、类型、枚举和边界参数
- 状态码、业务错误码和响应字段
- 幂等、重复请求和并发竞争
- 超时、重试、限流和依赖失败
- 写库、缓存、消息、回调和回滚
- 版本兼容和字段兼容

未被材料支持的项目不生成独立 case，而是在质量报告中记录信息缺口

### 数据不变量

数据一致性通过不变量建模：

```json
{
  "id": "INV-002",
  "scope": "当前筛选和同一数据快照",
  "left": "导出记录集合",
  "relation": "equals",
  "right": "列表命中记录集合",
  "join_keys": ["order_id"],
  "consistency": "strong",
  "allowed_delay": null,
  "source_refs": ["SRC-REQ-021", "SRC-API-009"]
}
```

支持：

- UI、API、详情和导出一致
- 状态机终态、数据库和下游状态一致
- 成功数加失败数等于总数
- 重复请求不生成重复记录和消息
- 筛选、排序、分页和导出使用一致范围
- 异步链路在允许延迟后达到最终一致

每个数据一致性 case 必须包含对比对象、对比键、数据范围、一致性时机和可观察断言

## 覆盖原子

覆盖原子是最小可验证事实：

```json
{
  "id": "ATOM-API-003-409",
  "kind": "api_contract",
  "target_ref": "API-003",
  "condition": "相同幂等键和不同请求体",
  "expected": "返回冲突且不创建第二个订单",
  "risk_weight": 5,
  "source_refs": ["SRC-API-003"]
}
```

受控分类：

- `interaction_flow`
- `business_rule`
- `state_transition`
- `permission`
- `api_contract`
- `data_consistency`
- `exception_recovery`
- `boundary`
- `compatibility`

覆盖率必须由最终用例关联的 coverage atom 反向计算，禁止手工填写 `covered_dimensions` 或 `final_case_counts`

## 候选生成

候选生成采用不同视角，但不强制所有请求都进行成本相同的双候选：

- 简单、低风险、单模块输入：单轮生成后执行独立 gap scan
- 多模块、高风险、包含接口或跨系统链路：双候选生成与裁决
- 信息不足或冲突：生成 `draft`，不伪造完整覆盖

候选视角：

- `coverage-first`：覆盖目标、规则、状态、接口、数据不变量和失败路径
- `quality-first`：保证单一验证意图、可执行步骤、可观察断言和低重复

候选 case 内部记录：

```json
{
  "id": "CC-018",
  "module_ref": "MOD-ORDER",
  "title": "订单提交 - 重复幂等键返回原订单",
  "source_refs": [],
  "goal_refs": [],
  "risk_refs": [],
  "dimensions": [],
  "coverage_atoms": [],
  "path_type": "critical_failure",
  "preconditions": "",
  "steps": [],
  "execution_cost": 2
}
```

## 组合测试

多个独立参数存在组合风险时：

- 先划分等价类和边界值
- 业务条件使用决策表
- 状态行为使用状态迁移
- 独立参数默认使用 pairwise
- 高风险交互使用风险驱动 `t-way`
- 文档明确禁止的组合不进入候选
- 单变量行为优先由单变量 case 覆盖

本次仅在提示协议和内部 IR 中表达组合模型，不集成外部组合生成工具

## 去重与最小充分集

### 归一化

生成规范化文本：

- 去除优先级前缀
- 统一中英文空格和末尾标点
- 统一模块、角色、动作、状态和实体的 canonical name
- 统一同义结构，例如“点击提交按钮”和“提交订单”

### 验证意图指纹

指纹字段：

```text
模块 + 业务对象 + 前态 + 触发动作 + 条件 + 断言目标 + 后态
```

确定性指纹一致时合并。以下差异必须保留独立 case：

- 角色或权限不同
- 前态或后态不同
- 请求契约不同
- 失败恢复行为不同
- 可观察业务结果不同

### 覆盖包含

若候选 B 的 coverage atoms 完全包含于 A，并且：

- A 没有混合多个无关验证意图
- A 的前置条件不更昂贵
- A 的步骤没有显著增加执行成本

则删除 B

只有输入数据不同的候选优先合并成参数化 case。目标、状态或预期不同的候选不得为了减少数量而合并

### 风险加权集合覆盖

最终集合使用确定性贪心选择：

```text
score =
  新增覆盖原子权重
  + 高风险路径奖励
  + 多来源证据奖励
  - 与已选用例重叠度
  - 执行成本
```

选择过程持续到：

- 所有必选 coverage atoms 已覆盖
- 剩余 atom 均有明确跳过理由
- 不再存在仅增加重复覆盖的候选

P0/P1 独立风险、权限泄漏、数据损坏和不可恢复状态不得因集合压缩被删除

## 分类与 XMind 结构

最终 XMind 以业务模块和工作流为主：

```text
业务模块
  └─ 页面或工作流
      ├─ 交互与流程
      ├─ 业务规则
      ├─ 接口契约
      ├─ 数据一致性
      ├─ 权限与安全
      └─ 异常与恢复
```

规则：

- 分类节点仅在存在真实用例时创建
- 分类名称必须保留业务上下文
- 接口和数据一致性用例归属到对应业务模块
- 避免顶层“接口测试”“异常测试”“数据测试”横向桶
- 无法归属的残余用例进入单个紧凑的 `其他`
- 禁止“基础功能验证”“接口异常验证”“数据正确性验证”等重复通用标题

## 内部质量报告

质量报告结构：

```json
{
  "source_coverage": {},
  "goal_coverage": {},
  "risk_coverage": {},
  "dimension_coverage": {},
  "api_coverage": {},
  "data_invariant_coverage": {},
  "state_transition_coverage": {},
  "duplicate_clusters": [],
  "merged_cases": [],
  "uncovered_atoms": [],
  "assumptions": [],
  "conflicts": [],
  "quality_gates": {}
}
```

默认不向用户展示。用户要求调试信息时，可以输出质量报告，但仍不暴露原始候选草稿

## 质量门禁

阻断门禁：

- case tree schema 完整率为 100%
- group、case、action 和 expected 不为空
- priority 仅允许 `P0/P1/P2/P3`
- 标题优先级前缀与 priority 字段一致
- 前置条件、动作和预期末尾中文句号数量为零
- 高风险目标正向与关键失败路径覆盖率为 100%
- 必选 coverage atoms 全部覆盖
- 每个 API case 都能追溯到接口证据
- 每个数据一致性 case 都能追溯到数据不变量
- 所有重复簇已完成保留、合并或删除裁决
- XMind 成功生成、可解压、XML 可解析且层级正确

警告门禁：

- 假设数量异常
- 分类集中度异常
- P0/P1 占比异常
- 平均步骤过少或过多
- `其他` 用例占比过高
- 单个 case 覆盖过多无关 atoms

## 严格 case tree 校验

新增独立 validator，在 XMind 构建前执行：

- 验证顶层和嵌套字段类型
- 拒绝空 group、空 case、空 steps、空 action 和空 expected
- 拒绝非法 priority
- 拒绝优先级前缀不一致
- 拒绝 list 类型的 preconditions
- 不再生成“用例标题”“分组”“步骤 1”等占位节点

构建器只负责渲染，不再静默修复结构错误

## 文件重构

目标结构：

```text
skills/interaction-testcase-generator/
├── SKILL.md
├── AGENTS.md
├── README.md
├── references/
│   ├── generation-protocol.md
│   ├── test-model.md
│   ├── test-design-methods.md
│   ├── quality-gates.md
│   ├── risk-priority.md
│   └── output-contract.md
├── templates/
│   ├── internal-ir.template.json
│   ├── quality-report.template.json
│   └── xmind-input.template.json
├── examples/
│   ├── interaction-workflow.md
│   ├── api-contract.md
│   └── data-consistency.md
└── scripts/
    ├── validate_case_tree.py
    ├── quality_report.py
    ├── xmind_build.py
    └── tests/
```

### 合并映射

- `decision-rules.md`、`multi-candidate-rules.md` 和 `coverage-ledger-rules.md` 合并为 `generation-protocol.md`
- `grouping-rules.md` 的分组模型并入 `test-model.md`
- `quality-rules.md` 扩展并重构为 `test-design-methods.md`
- `priority-rubric.md` 精简为 `risk-priority.md`
- `output-rules.md` 精简为 `output-contract.md`

### 删除清单

- 删除与强制双候选规则冲突的 `examples/multi-candidate-adjudication.md`
- 删除重复表达输出模式的 `templates/response-template.md`
- 删除不满足新 IR 和质量门禁的旧 example
- 删除静态、自报式 coverage ledger fixture
- 删除旧 reference，确保迁移后没有悬空引用
- 清理 `__pycache__` 和 `.pyc`

删除前必须执行引用搜索。仍有独立教学价值的旧 example 先迁移内容，再删除原文件

## `AGENTS.md`

`skills/interaction-testcase-generator/AGENTS.md` 约束：

- `SKILL.md` 只保留入口、核心工作流和不可忽略的不变量
- 每类规则只能有一个权威 reference
- 修改规则必须同步测试和 fixture
- 覆盖数据必须由工具计算，禁止手填可推导值
- 新增维度必须加入受控枚举和质量报告
- 新增 example 必须覆盖独立方法，不复制规则
- 删除文件前必须检查引用
- 提交前清理缓存并运行全部门禁

由于 Skill 和 eval 位于不同子树，仓库根目录增加简短 `AGENTS.md`，只描述二者共同的同步修改和验证要求；具体生成规则不复制到根文件

## 评测重构

评测分三层：

### Schema regression

验证：

- case tree schema
- priority 和标题前缀
- 前置条件、步骤与预期
- 标点规范
- 非法输入拒绝

### Quality regression

验证：

- coverage atoms 反向计算
- 业务目标和高风险路径覆盖
- 语义指纹重复
- 覆盖包含关系
- 分类规范
- API 证据追踪
- 数据不变量追踪
- 最小充分集选择稳定性

### Artifact E2E

临时生成 XMind 并验证：

- zip 成员完整
- `content.xml` 可解析
- 根节点、分组、用例、前置条件、步骤和预期层级
- priority marker
- note
- 自动父级合并
- 标点清理

临时文件写入系统临时目录，测试结束后删除，不提交二进制产物

## 兼容性

- 最终 case tree schema 不增加必填字段
- XMind 根节点和详细节点层级保持不变
- priority marker 和文本前缀保持不变
- 内部 IR 与质量报告保存在临时工作文件中，不作为默认附件
- 旧标准 case tree 在满足严格 schema 后仍可直接构建 XMind
- 违反原有文档契约但过去被静默接受的输入将改为明确失败

## Git 与旧文档

当前工作区已有两个旧设计和计划文档处于未提交删除状态。本次重构：

- 不恢复旧实施计划
- 将旧设计中的仍有效决策吸收到本设计
- 在实施清理提交中正式删除旧文档
- 设计、计划、规则重构、代码重构和 fixture 重构分别提交
- 完成全部验证后再推送远端

## 验收标准

- 最终 JSON 和 XMind 对现有合规输入保持兼容
- 内部 IR 能表达交互、规则、状态、接口和数据一致性
- 最终覆盖率由 case 与 coverage atom 映射计算
- 无手工 `final_case_counts` 和自报式 `covered_dimensions`
- 语义重复、覆盖包含和薄用例能够被识别并裁决
- 接口 case 均有接口来源
- 数据一致性 case 均有数据不变量来源
- 分类使用业务模块加具体维度，不产生横向通用大桶
- validator 拒绝非法输入，构建器不生成占位节点
- 真实 XMind 端到端测试通过
- 所有规则只有一个权威文件，仓库无悬空引用
- `AGENTS.md` 明确维护约束
- 仓库无 `__pycache__`、`.pyc` 和临时产物
- 全部单元测试、质量基线和 Git 格式检查通过

## 研究依据

- NIST 组合测试项目说明组合方法能够以更小测试集覆盖参数交互，并提供 ACTS 等工程实践：https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software
- OpenAPI Specification 将 HTTP API 能力描述为机器可理解的标准契约：https://spec.openapis.org/oas/v3.1.1.html
- GraphWalker 使用边表达动作或迁移、顶点表达验证或断言，可作为流程与状态建模参考：https://graphwalker.github.io/
