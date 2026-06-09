这个仓库用于维护个人技能和参考资料技能。

目录约定：

- `skills/`
  放可安装的技能包。
- `references/`
  放独立维护的参考资料技能，按 `apis/`、`architecture/`、`domain/` 分类组织；每类包含 `SKILL.md` 和 `modules/`。
- `tests/`
  仅作为本地临时验证目录使用，不作为长期维护内容；验证完成后应清理。

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
