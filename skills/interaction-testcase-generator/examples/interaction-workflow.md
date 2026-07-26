# 交互工作流示例

本示例只突出交互流程和状态迁移。

## 来源片段

`SRC-REQ-1`：采购员从订单草稿页提交订单。库存充足时订单进入“已创建”；库存不足时停留在草稿并提示缺货，不产生订单编号。

## IR 摘要

- 目标 `GOAL-1`：可靠提交订单，风险为 high
- 工作流 `WF-1`：草稿 → 提交 → 已创建
- 失败分支：库存不足，状态保持草稿
- 来源：`SRC-REQ-1`

## Coverage Atoms

| ID | Kind | 可验证事实 | 权重 |
| --- | --- | --- | --- |
| `ATOM-FLOW-1` | `interaction_flow` | 有效草稿提交后进入已创建 | 5 |
| `ATOM-STATE-1` | `state_transition` | 库存不足时保持草稿 | 5 |
| `ATOM-RECOVERY-1` | `exception_recovery` | 缺货提示可观察且不生成订单编号 | 4 |

## 候选裁决

`coverage-first` 将库存不足拆为“状态不变”和“无订单编号”两个候选；`quality-first` 指出二者共享同一触发、状态和断言面。裁决后合并为一个关键失败 case，保留成功 case。两个 path type 不合并。

## 最终兼容 Case Tree 摘要

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "订单 - 创建流程",
      "cases": [
        {
          "title": "[P0] 订单 - 有效草稿提交成功",
          "priority": "P0",
          "preconditions": "采购员已登录且库存充足",
          "steps": [{"action": "提交有效订单草稿", "expected": "订单进入已创建并生成订单编号"}]
        },
        {
          "title": "[P0] 订单 - 库存不足阻止提交",
          "priority": "P0",
          "preconditions": "采购员已登录且商品库存不足",
          "steps": [{"action": "提交订单草稿", "expected": "页面提示缺货，订单保持草稿且不生成订单编号"}]
        }
      ]
    }
  ]
}
```
