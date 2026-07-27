# Interaction Testcase Generator Evaluation Guidelines

## Scope

本文件适用于 `eval/skills/interaction-testcase-generator/`，用于验证生产目录 `skills/interaction-testcase-generator/` 的 schema、质量算法和 XMind 输出契约。

生产脚本与 eval 工具要求 Python >=3.10。

## Evaluation Layers

- Schema regression：验证 case tree 字段、类型、优先级、步骤和标点
- Quality regression：验证覆盖、来源追踪、重复裁决和最小充分集
- Artifact E2E：真实生成 XMind，并解析 ZIP 与 XML 校验完整输出
- Benchmark validator：验证 fixture 引用、阈值配置和全部质量门禁

## Fixture Rules

- 标准 case fixture 必须通过生产 strict validator
- 非法样本只允许放在明确断言失败的测试代码中
- IR fixture 必须与对应 case fixture 属于同一业务场景
- 最终 case tree 的 `case_id` 必须与 IR 中选中的 case 集合一致
- 覆盖率只能从 IR、coverage atoms 和最终选中 case 计算
- 禁止自报式 coverage ledger、手工 `final_case_counts` 或手工覆盖结论
- API case 必须关联对应接口契约和来源
- 数据一致性 case 必须关联对应 data invariant
- baseline 遇到未知字段、未消费阈值或未知 fixture 必须失败

## Artifact Requirements

- Artifact 测试必须实际调用生产 XMind 构建器
- 必须验证 ZIP 成员和 XML 可解析性
- 必须完整比较输入输出的分组、case、前置条件、步骤、预期和 note
- 必须校验 `P0/P1/P2/P3` 与 marker 的正确映射
- 临时 XMind 只能写入临时目录，测试结束后删除

## Change Requirements

- 修改 baseline、fixture、质量阈值或 artifact 契约时，必须反向核对生产 Skill
- 不得在 eval 中复制生产 validator、覆盖算法或输出规则，应直接复用生产实现
- 新增质量指标时，必须同时增加正向、失败和防假阳性的回归用例

## Verification

在仓库根目录运行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
git diff --check
```

提交前删除全部 `__pycache__/` 与 `*.pyc`。
