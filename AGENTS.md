# Repository Maintenance

`interaction-testcase-generator` 生产脚本与 eval 工具要求 Python >=3.10。

修改 `skills/interaction-testcase-generator/` 的 schema、规则、质量算法或输出契约时，必须同步检查 `eval/skills/interaction-testcase-generator/` 的测试、fixture 和阈值。反向修改 eval 契约时也必须核对生产 Skill。

提交前运行 Skill 单元测试、eval schema/quality regression、真实 XMind artifact E2E 和 benchmark validator。删除全部 `__pycache__/` 与 `*.pyc`，并运行 `git diff --check`。覆盖率只能由 IR 和最终选中 case 计算，不提交手工覆盖账本。
