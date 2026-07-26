# Skill Maintenance

- `SKILL.md` 只保留触发边界、Authority Map、五阶段工作流和不可忽略的不变量。
- 每类规则只能有一份权威 reference；README 与 example 不复制规则。
- 修改 schema、受控枚举、覆盖算法或输出契约时，同步修改生产测试、eval 测试、fixture 和 baseline。
- 新增维度时，同时更新 `test-model.md`、IR fixture、质量报告和回归断言。
- 覆盖率、目标覆盖和 case 数量由工具从 IR 与选中 case 计算，禁止提交自报式 ledger。
- example 必须展示独立设计方法，并包含来源、IR 摘要、coverage atoms、候选裁决和最终兼容树。
- 删除文件前搜索全部运行时引用；不得保留悬空 Authority Map、模板名或脚本路径。
- fixture 必须通过 strict case tree validator；非法样本只放在测试代码的明确失败用例中。
- 提交前运行 `scripts/tests/`、eval quality regression、XMind artifact E2E、benchmark validator 和 `git diff --check`，并删除 `__pycache__/` 与 `*.pyc`。
