这个仓库用于维护个人技能和参考资料技能。

## Skill 项目规范

单个 skill 建议按下面的职责分层组织。核心原则是按用途拆分，不要把规则、模板、示例和脚本混在一起。

| 目录 / 文件 | 作用 | 为什么这么设计 |
| --- | --- | --- |
| `SKILL.md` | 主 Prompt / 能力说明（怎么想） | 作为 skill 的入口，定义能力边界、使用场景、流程规则，是模型调用时读取的核心文件。 |
| `references/` | 参考文档（背景知识、规则） | 存放领域知识、业务规则、术语表，让 skill 依赖权威资料而不是靠模型猜测。 |
| `templates/` | 输出模板（格式、填充用） | 存放固定输出格式，如 XMind 用例模板、Markdown 报告模板，保证输出风格统一。 |
| `examples/` | 示例数据（Few-shot 用） | 存放高质量输入输出示例，让模型学习正确结果长什么样，提升稳定性。 |
| `scripts/` | 可执行脚本（真正的手脚） | 存放可落地执行的代码，如生成 XMind、调用 API、转换结构化数据。 |
| `sub-skills/` | 子 Skill（可复用能力单元） | 拆出可复用的原子能力，如领域检索器、API 校验器，实现模块化复用。 |

补充约定：

- `references/` 放规则和知识，不放纯输出骨架。
- `templates/` 放可直接套用的格式，不承载业务规则解释。
- `examples/` 只放少量高质量示例，不要堆大量测试产物。
- `scripts/` 优先承接机械式、可程序化的工作。
- `sub-skills/` 按需引入，不是每个 skill 都必须有。

## 如何使用

1. 本地安装 Skill，让 Agent 执行命令：

```bash
npx skills add -y -g https://github.com/MenXiaoHuan/my_skills.git
```

2. 配置自动更新 Hook：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "type": "command",
        "command": "npx skills update -g -y 2>/dev/null"
      }
    ]
  }
}
```
