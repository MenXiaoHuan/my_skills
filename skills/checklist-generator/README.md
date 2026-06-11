# Skill 说明：checklist-generator

## Skill 介绍

`checklist-generator` 是一个用于生成测试点、详细测试用例和真实 `.xmind` 交付物的 Skill。

它的目标不是输出泛泛而谈的测试建议，而是基于需求文档、技术方案、API 说明、原型、变更说明或结构化功能描述，生成具备实现意识、可执行、可追踪的测试设计结果。

## 适用场景

这个 Skill 适用于以下类型的任务：

- 根据 PRD、技术方案或接口文档生成测试用例
- 为功能迭代补充测试点、回归范围或发布检查项
- 从需求材料中识别 `P0` 场景和高风险路径
- 输出可直接交付 QA 使用的 `.xmind` 测试用例树
- 在材料不完整时生成带 assumptions 或 `draft` 标记的测试设计初稿

它适用于多种测试场景，包括但不限于：

- Web 功能测试
- App 功能测试
- API 接口测试设计
- 后台配置与运营流程测试
- 数据报表与导出类测试
- 跨系统业务流程测试

## 核心能力

这个 Skill 的核心能力包括：

- 从需求和技术材料中提炼测试范围与关键风险
- 生成结构化测试点和详细测试用例
- 识别并标记真正的 `P0` 场景
- 区分 confirmed information 与 assumptions
- 在关键材料缺失或冲突时输出 `draft`
- 生成真实 `.xmind` 文件作为主要交付物

## 工作方式

这个 Skill 默认遵循以下原则：

- 优先以需求文档和技术材料作为事实来源
- 仅在主材料不足以解释业务术语、接口语义或系统依赖时，按知识缺口补充相关参考知识
- 只有在信息缺口会影响测试范围、主流程、角色行为或预期结果时，才进一步追问
- 若缺失信息只影响次要细节，则可带 assumptions 继续生成
- 若关键材料缺失或相互冲突，则输出 `draft`，而不是伪装成正式测试设计

## 目录结构

```text
skills/checklist-generator/
├── SKILL.md
├── README.md
├── examples/
├── references/
├── scripts/
└── templates/
```

各目录职责如下：

- `SKILL.md`：主 skill 定义，包含触发条件、工作原则、默认流程和输出契约
- `README.md`：面向维护者和使用者的目录入口说明
- `examples/`：示例输入与输出风格参考，用于 few-shot 风格对齐
- `references/`：补充规则和按需读取的决策说明
- `scripts/`：生成真实 `.xmind` 文件的脚本
- `templates/`：中间结构和响应模板

## 相关文件说明

- `references/output-rules.md`
  - 定义输出约束、标题规范、`P0` 表达要求等
- `references/decision-rules.md`
  - 定义何时补知识、何时追问、何时使用 assumptions、何时输出 `draft`
- `templates/xmind_input.template.json`
  - 定义生成 XMind 所需的标准化输入结构
- `templates/response-template.md`
  - 定义面向用户的标准响应格式
- `scripts/xmind_build.py`
  - 将结构化 JSON 转换为真实 `.xmind` 文件
