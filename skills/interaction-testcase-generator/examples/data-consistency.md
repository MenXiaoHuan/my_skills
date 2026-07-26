# 数据一致性示例

本示例只突出数据范围、连接键、快照和一致性时机。

## 来源片段

`SRC-REQ-1`：订单列表与导出使用相同筛选条件和数据快照，以 `order_id` 对齐。导出任务完成后，导出记录集合必须等于列表命中集合。

## IR 摘要

- 不变量 `INV-1`
- 左侧：当前筛选下的导出记录
- 右侧：创建导出任务时的列表命中记录
- 连接键：`order_id`
- 一致性：导出任务完成后的强一致
- 来源：`SRC-REQ-1`

## Coverage Atoms

| ID | Kind | 可验证事实 | 权重 |
| --- | --- | --- | --- |
| `ATOM-DATA-1` | `data_consistency` | 导出与列表使用相同筛选范围 | 4 |
| `ATOM-DATA-2` | `data_consistency` | 两侧 `order_id` 集合相等 | 5 |
| `ATOM-DATA-3` | `data_consistency` | 导出基于任务创建时快照 | 4 |

## 候选裁决

筛选范围、集合相等和快照时机属于同一导出验证意图，且可在一次构造中观察，合并为一个 case。只检查“导出成功”的薄候选被删除，因为它不增加 coverage atom。

## 最终兼容 Case Tree 摘要

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "订单 - 筛选与导出",
      "cases": [
        {
          "title": "[P1] 订单导出 - 与筛选列表快照一致",
          "priority": "P1",
          "preconditions": "订单列表存在跨状态数据且用户有导出权限",
          "steps": [
            {"action": "筛选已创建订单并记录列表命中的 order_id 后创建导出任务", "expected": "导出任务记录当前筛选条件和创建时数据快照"},
            {"action": "任务完成后下载文件并提取 order_id", "expected": "导出 order_id 集合与任务创建时列表命中集合相等"}
          ]
        }
      ]
    }
  ]
}
```
