# interaction-testcase-generator

该 Skill 将需求、原型、API 和技术设计转换为详细 QA case tree 与真实 XMind。生成规则从 `SKILL.md` 进入，并按 Authority Map 定向读取唯一权威 reference。

运行生产脚本、测试与 eval 工具需要 Python >=3.10。

## 目录职责

- `SKILL.md`：触发边界、Authority Map、五阶段工作流和强制不变量
- `AGENTS.md`：维护约束和提交前验证要求
- `references/`：生成协议、测试模型、设计方法、质量门禁、风险优先级和输出契约
- `examples/`：交互工作流、API 契约和数据一致性的正交示例
- `templates/`：内部 IR、质量报告和兼容 XMind 输入
- `scripts/`：strict validator、质量报告、XMind 构建器及其单元测试

## 维护入口

规则修改从对应 reference 开始；不要把规则复制到 README 或 example。schema、受控枚举、质量算法或输出契约变化时，同步更新生产测试、`eval/skills/interaction-testcase-generator/` 的 fixture 和 baseline。

## 验证命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/tests/test_validate_case_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/tests/test_quality_report.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/tests/test_xmind_build.py
PYTHONDONTWRITEBYTECODE=1 python3 ../../eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 ../../eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py
PYTHONDONTWRITEBYTECODE=1 python3 ../../eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
```

仓库根目录运行命令时使用完整的 `skills/interaction-testcase-generator/` 和 `eval/skills/interaction-testcase-generator/` 路径。提交前清理 `__pycache__` 与 `*.pyc`，并运行 `git diff --check`。
