# interaction-testcase-generator eval

评测覆盖 strict schema、IR 驱动质量指标和真实 XMind artifact。

运行 eval 测试与 benchmark 工具需要 Python >=3.10。

## 目录

- `cases/`：通过生产 strict validator 的标准 case tree
- `ir/`：交互、API、审批和数据一致性代表性 IR
- `baseline.json`：fixture 引用、selected case IDs 与阈值
- `.tools/check_case_tree_quality.py`：复用生产 validator 和质量报告的指标适配器
- `.tools/test_check_case_tree_quality.py`：schema 与 quality regression
- `.tools/test_xmind_artifact_e2e.py`：真实构建、ZIP 与 XML 层级检查
- `.tools/validate_benchmark.py`：运行全部 baseline 与 artifact suite

不提交 `expected.xmind`。artifact 测试在系统临时目录构建，测试结束后自动清理。

## 验证命令

```bash
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
```

## 维护规则

- case fixture 与 IR fixture 必须在 `baseline.json` 被引用。
- 覆盖率由 IR 的 coverage atoms 和 `selected_case_ids` 计算，不使用 `_evaluation` 或自报 coverage ledger。
- schema、枚举或质量算法变化时同步修改生产工具、单元测试、fixture 和阈值。
- benchmark 的 artifact suite 必须执行真实 XMind 构建并解析 `content.xml`，不得退化为搜索输入 JSON 字符串。
