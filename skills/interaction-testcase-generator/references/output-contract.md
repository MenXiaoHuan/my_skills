# Output Contract

本文件是最终 JSON、XMind、标点、命名和失败回退的唯一权威。

## 用户可见产物

默认交付真实 `.xmind`，称为详细 QA 测试用例。内部 IR、质量报告、候选草稿、裁决表和构建 JSON 不默认暴露。

仅文本或 runtime eval 环境必须返回一个 fenced `json` 代码块，代码块前后不得有说明。JSON 是最终规范化 case tree，不得用摘要、统计、脚本或生成承诺替代。

## JSON Schema

```json
{
  "root_title": "用例集",
  "note": "可选",
  "groups": [
    {
      "title": "业务模块",
      "note": "可选",
      "groups": [],
      "cases": [
        {
          "case_id": "CASE-ORDER-CREATE",
          "title": "[P1] 订单 - 创建成功",
          "priority": "P1",
          "preconditions": "用户已登录",
          "note": "可选",
          "steps": [
            {"action": "提交有效订单", "expected": "订单状态为已创建"}
          ]
        }
      ]
    }
  ]
}
```

顶层必须是 object，`groups` 是非空 list。group title 非空，`groups` 与 `cases` 为 list。case 的 `case_id` 绑定内部 IR 中最终选中的候选 ID；eval 中最终树的 ID 集合必须与 `selected_case_ids` 完全一致。case 的 title、priority、preconditions、steps 必填；priority 必须是 string 且只允许精确值 `P0/P1/P2/P3`，标题前缀必须匹配。preconditions 是非空 string；steps 是非空 list；action 和 expected 是非空 string。顶层、group、case 和 step 的可选 note 必须是 string。

## 命名和标点

- 标题简短并包含业务对象或具体场景，禁止跨模块复用“基础功能验证”“数据正确性验证”等通用标题。
- group 和 case title 不含 Markdown 列表符。
- `preconditions`、`action`、`expected` 去除周围空格和末尾一个或多个中文句号 `。`。
- 保留字段内部中文句号、英文句点和其他标点。
- 标题、描述、note 与 step note 不执行末尾句号清理。

## XMind 层级

```text
用例集
  业务模块或工作流
    可选子组
      [P1] 用例标题
        前置条件
          前置文本
        步骤
          步骤 1: 动作
            预期 1: 结果
```

case 默认可写简短 note。priority marker 映射为：

- `P0` → `priority-1`
- `P1` → `priority-2`
- `P2` → `priority-3`
- `P3` → `priority-4`

平级 group 中至少两个标题匹配 `共同业务父级 - 子模块` 时，构建器可以合并真实业务父级；`页面`、`模块`、`列表`、`详情`、`流程`、`功能`、`场景` 等通用词不得作为自动合并父级。

## 构建

使用 `templates/xmind-input.template.json` 创建输入，运行：

```bash
python3 scripts/xmind_build.py input.json output.xmind
```

构建前必须通过严格 validator。构建器不生成“用例标题”“分组”或空步骤占位节点。生成后验证文件非空、ZIP 成员完整且 `content.xml` 可解析。

## 失败回退

构建失败时报告具体 schema 路径或产物错误。只有无法附加 `.xmind` 时才回退到规范化 JSON；不得把内部 IR 或未裁决候选作为回退产物。
