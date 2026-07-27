# Interaction Testcase Generator Guidelines

## Scope

本文件适用于 `skills/interaction-testcase-generator/`。对应 eval 的专项规则位于 `eval/skills/interaction-testcase-generator/AGENTS.md`。

生产脚本与 eval 工具要求 Python >=3.10。

## Source of Truth

- `SKILL.md`：只保留触发边界、Authority Map、五阶段工作流和不可忽略的不变量
- `references/`：生成协议、测试模型、设计方法、质量门禁、风险优先级和输出契约的唯一权威来源
- `templates/`：只描述结构和格式，不解释业务规则
- `examples/`：只展示正交方法，不复制完整规则
- `scripts/`：负责确定性的校验、质量计算和 XMind 构建

同一规则不得在 README、template、example 和多个 reference 中重复定义。

## Change Requirements

- 修改 schema、受控枚举、内部 IR、覆盖算法或输出契约时，同步修改生产测试和对应 eval
- 新增测试维度时，同时更新 `references/test-model.md`、IR fixture、质量报告和回归断言
- API case 必须追溯到对应接口契约及来源
- 数据一致性 case 必须追溯到对应数据不变量
- 覆盖率、目标覆盖和 case 数量必须从 IR 与最终选中 case 计算，禁止自报式 ledger
- example 必须包含来源、IR 摘要、coverage atoms、候选裁决和最终兼容树
- fixture 必须通过 strict case tree validator；非法样本只允许出现在明确的失败测试中
- 删除或重命名文件前，搜索全部运行时引用，不得留下悬空 Authority Map、模板名或脚本路径

## Compatibility

- 最终 case tree 和 XMind 层级必须遵守 `references/output-contract.md`
- 内部 IR、质量报告和候选裁决不得默认泄漏到用户输出
- 构建器不得静默修复非法输入或生成占位 case

## Verification

在仓库根目录运行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_validate_case_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_quality_report.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_xmind_build.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
git diff --check
```

提交前删除全部 `__pycache__/` 与 `*.pyc`。
