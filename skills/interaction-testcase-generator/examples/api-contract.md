# API 契约示例

本示例只突出来源支持的接口契约、幂等和副作用。

## 来源片段

`SRC-API-1`：`POST /orders` 要求 `Idempotency-Key`。首次成功返回 201；相同键和相同请求体返回原订单；相同键和不同请求体返回 409，且不得创建第二条订单或发送第二条消息。

## IR 摘要

- 接口 `API-1`：`POST /orders`
- 鉴权：采购员
- 幂等规则：键与请求体共同裁决
- 副作用：写入订单并发送 `OrderCreated`
- 来源：`SRC-API-1`

## Coverage Atoms

| ID | Kind | 可验证事实 | 权重 |
| --- | --- | --- | --- |
| `ATOM-API-1` | `api_contract` | 首次请求返回 201 | 4 |
| `ATOM-API-2` | `api_contract` | 相同键和请求体返回原订单 | 5 |
| `ATOM-API-3` | `api_contract` | 相同键和不同请求体返回 409 | 5 |
| `ATOM-DATA-1` | `data_consistency` | 冲突不产生重复订单和消息 | 5 |

## 候选裁决

首次创建和相同请求重放的响应语义不同，保留独立 case。409 响应与“无重复副作用”共享同一请求和失败意图，合并为一个 case。该 case 同时引用 `API-1` 和副作用不变量。

## 最终兼容 Case Tree 摘要

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "订单 - 创建接口",
      "cases": [
        {
          "title": "[P0] 订单接口 - 相同幂等键重放原订单",
          "priority": "P0",
          "preconditions": "已使用幂等键 K 成功创建订单 A",
          "steps": [{"action": "使用幂等键 K 和相同请求体再次调用 POST /orders", "expected": "接口返回订单 A 且不新增订单和 OrderCreated 消息"}]
        },
        {
          "title": "[P0] 订单接口 - 幂等键请求体冲突",
          "priority": "P0",
          "preconditions": "已使用幂等键 K 成功创建订单 A",
          "steps": [{"action": "使用幂等键 K 和不同请求体调用 POST /orders", "expected": "接口返回 409，订单和 OrderCreated 消息数量不变"}]
        }
      ]
    }
  ]
}
```
