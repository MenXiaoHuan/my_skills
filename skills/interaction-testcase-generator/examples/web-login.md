# Example: Web Login With MFA And Lockout

Use this example when the request is a feature requirement and the expected output is a structured testing deliverable plus a real `.xmind` file.

## Example Input

```text
请基于以下 Web 登录需求设计测试用例，并默认输出真实 .xmind 文件。需求：用户输入正确账号密码后，如果账号开启了 MFA，则必须先完成短信验证码校验才能进入控制台；连续输错密码 5 次后账号锁定 15 分钟；已锁定账号在锁定期内使用正确密码也不能登录。请覆盖正常流程、MFA、锁定、边界和异常场景，并标记 release-critical 场景。
```

## Example Output Shape

```text
### P0 Scenario Summary
- `Authentication - Account lock remains effective during the lock window even with the correct password`

### Source Summary
- user-provided requirement text

### Full Case Coverage Summary
- login success without MFA
- MFA challenge and verification
- failed verification and retry behavior
- wrong-password lockout threshold
- lock-window restrictions
- boundary and abnormal input scenarios

### Risks and Open Questions
- need confirmation on SMS code expiration and resend throttling if those rules affect this release
```

## Example XMind Shape

The final user-facing answer should deliver the generated `.xmind` file as the primary artifact, without exposing a local absolute path, and the generated file itself should follow an XMind-oriented case tree similar to:

```text
用例集
└── Authentication
    ├── [P1] Authentication - Login succeeds without MFA
    │   └── 步骤
    │       └── 步骤 1: 输入正确账号和密码
    │           └── 预期 1: 进入控制台首页
    ├── [P0] Authentication - Require MFA after valid password submission
    │   ├── 前置条件
    │   │   └── 账号已开启 MFA
    │   └── 步骤
    │       ├── 步骤 1: 输入正确账号和密码
    │       │   └── 预期 1: 展示短信验证码校验步骤
    │       └── 步骤 2: 输入正确短信验证码
    │           └── 预期 2: 登录成功并进入控制台
    ├── [P0] Authentication - Account remains locked during the lock window
    │   ├── 前置条件
    │   │   └── 连续输错密码 5 次导致账号锁定
    │   └── 步骤
    │       └── 步骤 1: 锁定期内输入正确密码并尝试登录
    │           └── 预期 1: 账号仍不可登录
    └── [P2] Authentication - Boundary and abnormal input handling
        ├── 文本描述
        │   └── 空密码、错误验证码、过期验证码、重复提交
        └── 步骤
            └── 步骤 1: 分别提交异常输入
                └── 预期 1: 系统给出正确拦截和提示
```

## Example Builder Input Shape

When the skill needs to build the actual `.xmind` file, the normalized JSON should be close to:

```json
{
  "root_title": "用例集",
  "groups": [
    {
      "title": "Authentication",
      "cases": [
        {
          "title": "[P0] Authentication - Require MFA after valid password submission",
          "priority": "P0",
          "preconditions": "账号已开启 MFA",
          "description": "",
          "steps": [
            {
              "action": "输入正确账号和密码",
              "expected": "展示短信验证码校验步骤"
            },
            {
              "action": "输入正确短信验证码",
              "expected": "登录成功并进入控制台"
            }
          ]
        }
      ]
    }
  ]
}
```

## Notes

- Deliver the generated XMind file as the main user-facing artifact.
- Keep the response brief after the delivery.
- Cover the full scope, not only `P0`.
- Keep the `[P0]` or `[P1]` title prefix aligned with the `priority` field and XMind marker.
- The few-shot signal should teach both the final response shape and the XMind hierarchy actually written to disk.
