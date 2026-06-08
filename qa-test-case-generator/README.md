# ttms-qa-checklist-generator

TTMS QA 用例生成 Skill。

这个仓库用于维护 TTMS 测试设计相关的 Skill，包括：
- `SKILL.md` 主入口
- `references/` 按需加载的领域与输出规范
- `templates/` 示例模板
- `scripts/` 机械执行脚本
- `evals/` 最小回归测试集

## 接入方式

1. 创建一个代码仓库，并将 Skill 文件上传到主分支。

2. 本地安装 Skill，让 Agent 执行命令：

```bash
npx skills add -y -g https://github.com/MenXiaoHuan/my_skills.git
```

3. 配置自动更新 Hook：

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

4. 后续更新 Skill 仓库主分支。

## 当前目录结构

```text
.
├── SKILL.md
├── evals/
├── references/
├── scripts/
└── templates/
```
