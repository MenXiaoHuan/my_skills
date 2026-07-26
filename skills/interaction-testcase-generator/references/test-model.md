# Test Model

本文件是内部 IR、coverage atom、受控维度和最终业务归属的唯一权威。

## 顶层 IR

内部 IR 版本为 `1.0`，包含：

```text
sources, business_goals, actors, modules, workflows, states,
business_rules, api_contracts, data_entities, data_invariants,
dependencies, risks, coverage_atoms, candidate_cases,
assumptions, conflicts
```

模板见 `templates/internal-ir.template.json`。所有实体使用稳定 ID，引用使用 `*_refs`；引用不得指向不存在的 ID。

## 来源类型

- `requirement`：需求条款、业务目标和验收标准
- `prototype`：页面、控件、弹窗、抽屉与交互路径
- `api`：方法、路径、参数、响应、错误码和鉴权
- `technical_design`：状态、存储、缓存、消息、回调、补偿和依赖
- `data_definition`：字段、指标、聚合、范围和导出规则
- `assumption`：明确隔离的次要假设

## Coverage Atom

coverage atom 是最小可验证事实。字段至少包含：

```json
{
  "id": "ATOM-1",
  "kind": "api_contract",
  "target_ref": "API-1",
  "required": true,
  "risk_weight": 5,
  "source_refs": ["SRC-1"]
}
```

`kind` 只允许：

- `interaction_flow`
- `business_rule`
- `state_transition`
- `permission`
- `api_contract`
- `data_consistency`
- `exception_recovery`
- `boundary`
- `compatibility`

## 候选 Case

候选至少记录 `id`、`title`、`source_refs`、`goal_refs`、`dimensions`、`coverage_atoms`、`path_type`、`preconditions`、`steps` 和 `execution_cost`。API 候选必须有接口来源；数据一致性候选必须有 `invariant_refs`。

`path_type` 使用受控值：

- `positive`
- `critical_failure`
- `negative`
- `recovery`
- `boundary`

验证意图由模块、业务对象、前态、触发动作、条件、断言目标和后态组成。角色、权限、状态、请求契约、恢复行为或业务结果不同，不得只因标题相似而合并。

## 工作流与状态

工作流记录所属模块、角色、起始状态、动作、合法后态、关键失败路径、终止条件和来源。状态迁移 atom 同时引用迁移前态、动作和后态；非法迁移使用独立 atom。

## API 与数据

只有材料存在接口证据时创建 `api_contracts`。数据不变量必须表达对比对象、连接键、范围、一致性类型、允许延迟和来源。异步链路使用最终一致性及明确观察时机，不把即时不一致误判为失败。

## 最终分类

最终树以业务模块和工作流为主。交互、规则、接口、数据、权限、异常等维度作为所属业务节点下的具体分类；不存在真实 case 的分类节点不创建。禁止建立脱离业务上下文的顶层“接口测试”“异常测试”或“数据测试”。无法归属的残余 case 进入单个 `其他`。
