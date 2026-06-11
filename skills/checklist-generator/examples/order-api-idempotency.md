# Example: Order API Idempotency

Use this example when the request is API-focused and the expected output is a structured test design plus a real `.xmind` file.

## Example Input

```text
请基于以下订单创建 API 需求设计测试用例，并默认输出真实 .xmind 文件。需求：客户端调用创建订单接口时必须带 `Idempotency-Key`；同一个 key 在 24 小时内重复请求且请求体完全一致时，服务端返回首次成功创建的订单结果；如果同一个 key 对应的请求体不一致，则返回 409；如果首次请求仍在处理中，重复请求返回 202 并提示稍后重试。请覆盖正常流程、冲突、并发、异常和边界场景，并标记 release-critical 场景。
```

## Example Output Shape

```text
### P0 Scenario Summary
- `Order API - Repeated request with the same idempotency key and same payload returns the original successful result`
- `Order API - Repeated request with the same idempotency key and different payload returns 409 conflict`

### Source Summary
- user-provided API requirement text

### Full Case Coverage Summary
- mandatory key validation
- first successful order creation
- same-key same-payload replay behavior
- same-key different-payload conflict behavior
- in-progress duplicate request handling
- concurrency, timeout, and boundary scenarios

### Risks and Open Questions
- need confirmation on whether the 24-hour idempotency window is based on request arrival time or order creation time
```

## Example XMind Shape

The final user-facing answer should return the `.xmind` file path first, but the generated file itself should follow an XMind-oriented case tree similar to:

```text
用例集
└── Order API
    ├── [P1] Order API - Reject request without idempotency key
    │   └── 文本描述
    │       ├── 缺少 `Idempotency-Key`
    │       │   └── 返回参数校验错误
    ├── [P0] Order API - Return original order result for same key and same payload
    │   └── 前置条件
    │       ├── 首次请求已成功创建订单
    │       │   └── 重复请求返回同一订单结果
    ├── [P0] Order API - Return 409 for same key and different payload
    │   └── 前置条件
    │       ├── 首次请求已记录该 key
    │       │   └── 重复请求 payload 不一致时返回 409
    └── [P1] Order API - Return 202 when first request is still in progress
        └── 前置条件
            ├── 首次请求仍在处理中
            │   └── 重复请求返回 202 并提示稍后重试
```

## Example Builder Input Shape

When the skill needs to build the actual `.xmind` file, the normalized JSON should be close to:

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "Order API",
      "cases": [
        {
          "title": "[P0] Order API - Return original order result for same key and same payload",
          "priority": "P0",
          "preconditions": "首次请求已成功创建订单",
          "description": "",
          "steps": [
            {
              "action": "使用相同 Idempotency-Key 和相同 payload 重复请求",
              "expected": "返回首次成功创建的订单结果"
            }
          ]
        }
      ]
    }
  ]
}
```

## Notes

- Prefer API-oriented naming for groups and cases.
- Explicitly cover duplicate, conflict, and in-progress branches.
- Mark `P0` only for truly launch-blocking flows.
- The few-shot signal should teach both the final response shape and the XMind hierarchy actually written to disk.
