# 交互测试用例生成 Skill 优化实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 统一移除前置条件、步骤动作和步骤预期末尾的中文句号，并让 Skill 与轻量评测强制关注业务目标、风险和可观察断言

**Architecture:** 生成规则负责源头约束，XMind 构建器提供确定性渲染兜底，轻量评测负责防止格式和业务质量回退。保持现有 case tree schema 与 XMind 层级不变，业务目标评测通过 fixture 中可选的 `_evaluation` 元数据启用

**Tech Stack:** Markdown、JSON、Python 标准库、`unittest`

---

## 文件结构

- 修改 `skills/interaction-testcase-generator/SKILL.md`：加入业务目标推导和字段标点约束
- 修改 `skills/interaction-testcase-generator/references/output-rules.md`：定义输出字段标点契约
- 修改 `skills/interaction-testcase-generator/references/quality-rules.md`：定义业务目标到断言的质量链路
- 修改 `skills/interaction-testcase-generator/references/coverage-ledger-rules.md`：定义目标与风险覆盖要求
- 修改 `skills/interaction-testcase-generator/templates/xmind_input.template.json`：提供符合规则的模板
- 修改 `skills/interaction-testcase-generator/scripts/xmind_build.py`：在渲染层清理目标字段
- 修改 `skills/interaction-testcase-generator/scripts/test_xmind_build.py`：覆盖清理边界和非目标字段
- 修改 `eval/skills/interaction-testcase-generator/.tools/check_case_tree_quality.py`：增加格式与业务质量指标
- 修改 `eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py`：校验新增配置
- 修改 `eval/skills/interaction-testcase-generator/baseline.json`：为代表性 fixture 设置质量阈值
- 修改部分 `eval/skills/interaction-testcase-generator/cases/*.json`：增加可选 `_evaluation` 元数据
- 修改 `eval/skills/interaction-testcase-generator/README.md`：记录新增指标和维护规则

### Task 1: 固化生成规则

**Files:**
- Modify: `skills/interaction-testcase-generator/SKILL.md`
- Modify: `skills/interaction-testcase-generator/references/output-rules.md`
- Modify: `skills/interaction-testcase-generator/references/quality-rules.md`
- Modify: `skills/interaction-testcase-generator/references/coverage-ledger-rules.md`
- Modify: `skills/interaction-testcase-generator/templates/xmind_input.template.json`

- [ ] **Step 1: 在主工作流加入业务推导链**

将默认工作流调整为先提取：

```text
业务目标 → 核心流程 → 失败风险 → 验证意图 → 可观察断言
```

并明确每个核心目标至少映射一个用例，每个高风险目标至少映射一个正向用例和一个关键失败用例

- [ ] **Step 2: 在质量规则加入执行级约束**

加入以下明确规则：

```text
前置条件只包含角色、权限、数据、状态和环境准备
前置条件不能依赖其他用例执行结果
步骤包含明确入口、操作对象、关键输入和触发动作
预期结果包含验证对象、状态或数据变化
异常预期验证错误反馈、数据不变性、补偿或恢复路径
```

- [ ] **Step 3: 在输出契约加入标点规则**

明确以下字段不得以一个或多个中文句号结尾：

```text
case.preconditions
case.steps[].action
case.steps[].expected
```

同时明确保留字段内部中文句号、英文句号和其他标点，不影响标题、分组、说明和备注

- [ ] **Step 4: 更新模板示例**

将模板中三个目标字段的示例值改为无末尾中文句号文本，并增加 `_comment_punctuation`：

```json
"_comment_punctuation": "preconditions、steps[].action、steps[].expected 末尾不使用中文句号。"
```

- [ ] **Step 5: 检查规则一致性**

运行：

```bash
git diff --check
```

Expected: 退出码为 `0`，无空白错误

- [ ] **Step 6: 提交规则修改**

```bash
git add skills/interaction-testcase-generator
git commit -m "Improve testcase generation business rules"
```

### Task 2: 为 XMind 增加确定性标点清理

**Files:**
- Modify: `skills/interaction-testcase-generator/scripts/test_xmind_build.py`
- Modify: `skills/interaction-testcase-generator/scripts/xmind_build.py`

- [ ] **Step 1: 编写失败测试**

在 `XMindBuildTests` 增加测试，输入包含：

```python
{
    "title": "标题保留。",
    "priority": "P1",
    "note": "备注保留。",
    "preconditions": "用户已登录。。 ",
    "steps": [
        {
            "action": "打开订单。确认状态。。 ",
            "expected": "展示订单。状态为待支付。",
            "note": "步骤备注保留。",
        },
        {
            "action": "调用 API v2.",
            "expected": "返回 HTTP 200.",
        },
    ],
}
```

断言所有标题包含：

```python
self.assertIn("用户已登录", titles)
self.assertIn("步骤 1: 打开订单。确认状态", titles)
self.assertIn("预期 1: 展示订单。状态为待支付", titles)
self.assertIn("步骤 2: 调用 API v2.", titles)
self.assertIn("预期 2: 返回 HTTP 200.", titles)
self.assertIn("[P1] 标题保留。", titles)
self.assertIn("备注保留。", _all_notes(root))
```

- [ ] **Step 2: 运行测试并确认失败**

Run:

```bash
python3 -m unittest skills/interaction-testcase-generator/scripts/test_xmind_build.py
```

Expected: 新测试因目标字段仍保留末尾中文句号而失败

- [ ] **Step 3: 实现最小清理函数**

在 `xmind_build.py` 增加：

```python
def _strip_trailing_chinese_periods(value):
    text = str(value or "").strip()
    return re.sub(r"。+$", "", text).rstrip()
```

仅在 `_render_case` 中处理：

```python
preconditions = _strip_trailing_chinese_periods(case.get("preconditions"))
action = _strip_trailing_chinese_periods(step.get("action"))
expected = _strip_trailing_chinese_periods(step.get("expected"))
```

- [ ] **Step 4: 运行单元测试并确认通过**

Run:

```bash
python3 -m unittest skills/interaction-testcase-generator/scripts/test_xmind_build.py
```

Expected: 所有测试通过

- [ ] **Step 5: 提交构建器修改**

```bash
git add skills/interaction-testcase-generator/scripts
git commit -m "Normalize testcase XMind punctuation"
```

### Task 3: 增加轻量质量指标

**Files:**
- Modify: `eval/skills/interaction-testcase-generator/.tools/check_case_tree_quality.py`
- Create: `eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py`

- [ ] **Step 1: 编写格式与业务指标失败测试**

新增 `unittest`，构造带 `_evaluation` 元数据的 case tree：

```python
"_evaluation": {
    "business_goals": [
        {"id": "G1", "risk": "high", "required_paths": ["positive", "critical_failure"]},
        {"id": "G2", "risk": "medium", "required_paths": ["positive"]}
    ],
    "case_traceability": {
        "支付成功": {"goals": ["G1"], "path": "positive"},
        "重复支付": {"goals": ["G1"], "path": "critical_failure"}
    }
}
```

断言指标包含：

```python
self.assertEqual(metrics["trailing_chinese_period_count"], 3)
self.assertEqual(metrics["business_goal_coverage_rate"], 0.5)
self.assertEqual(metrics["high_risk_goal_path_coverage_rate"], 1.0)
self.assertEqual(metrics["precondition_action_leak_count"], 1)
self.assertEqual(metrics["unobservable_expectation_count"], 1)
self.assertEqual(metrics["priority_distribution"], {"P0": 0, "P1": 1, "P2": 1, "P3": 0})
```

- [ ] **Step 2: 运行新测试并确认失败**

Run:

```bash
python3 -m unittest eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
```

Expected: 因新增指标尚不存在而失败

- [ ] **Step 3: 实现字段扫描**

增加中文句号和前置条件动作扫描：

```python
TRAILING_CHINESE_PERIOD_RE = re.compile(r"。+\s*$")
PRECONDITION_ACTION_PATTERNS = ["点击", "输入", "选择", "提交", "调用", "校验", "打开"]
UNOBSERVABLE_EXPECTATION_PATTERNS = WEAK_EXPECTATION_PATTERNS + ["处理成功", "操作成功", "符合预期"]
```

`trailing_chinese_period_count` 只扫描 `preconditions`、`action`、`expected`

- [ ] **Step 4: 实现可选目标覆盖计算**

读取 `_evaluation.business_goals` 和 `_evaluation.case_traceability`。未提供元数据时两个覆盖率返回 `None`；提供元数据时按 goal id 和 required path 计算，未知 case title 不计入覆盖

- [ ] **Step 5: 实现配置校验**

在 `validate_against_config` 支持：

```text
max_trailing_chinese_periods
max_precondition_action_leaks
max_unobservable_expectations
min_business_goal_coverage_rate
min_high_risk_goal_path_coverage_rate
```

覆盖率为 `None` 且基线配置要求最小值时必须失败，避免配置形同虚设

- [ ] **Step 6: 运行新旧质量测试**

Run:

```bash
python3 -m unittest eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
python3 eval/skills/interaction-testcase-generator/.tools/check_case_tree_quality.py eval/skills/interaction-testcase-generator/cases/case_001_app_cart_offline.json --print-metrics
```

Expected: 单元测试通过，现有 fixture 可正常输出新增指标

- [ ] **Step 7: 提交质量检查修改**

```bash
git add eval/skills/interaction-testcase-generator/.tools
git commit -m "Add testcase business quality metrics"
```

### Task 4: 接入代表性业务基线

**Files:**
- Modify: `eval/skills/interaction-testcase-generator/baseline.json`
- Modify: `eval/skills/interaction-testcase-generator/cases/case_001_app_cart_offline.json`
- Modify: `eval/skills/interaction-testcase-generator/cases/case_005_crm_import_review_center.json`
- Modify: `eval/skills/interaction-testcase-generator/cases/case_007_order_api_idempotency_draft.json`
- Modify: `eval/skills/interaction-testcase-generator/cases/case_008_supplier_settlement_approval.json`
- Modify: `eval/skills/interaction-testcase-generator/README.md`

- [ ] **Step 1: 为四类代表性场景增加评测元数据**

分别覆盖：

```text
case_001：离线与恢复
case_005：导入审核与数据一致性
case_007：接口幂等与冲突
case_008：审批状态与权限
```

每个 fixture 增加 `_evaluation.business_goals` 和 `_evaluation.case_traceability`，引用已有用例标题，不修改用户可见 groups 内容

- [ ] **Step 2: 为所有结构质量案例启用标点约束**

在 `baseline.json` 的 `structure_quality_suite` 各项增加：

```json
"max_trailing_chinese_periods": 0
```

为四个代表性 fixture 增加：

```json
"min_business_goal_coverage_rate": 1.0,
"min_high_risk_goal_path_coverage_rate": 1.0
```

- [ ] **Step 3: 更新评测维护文档**

说明 `_evaluation` 只服务本地评测，不属于最终 case tree schema；新增 fixture 若声明业务目标，必须同步维护可追溯映射和基线阈值

- [ ] **Step 4: 运行基线并修正数据问题**

Run:

```bash
python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
```

Expected: 输出 `lightweight baseline validation passed`

- [ ] **Step 5: 提交基线修改**

```bash
git add eval/skills/interaction-testcase-generator
git commit -m "Add business goal testcase baselines"
```

### Task 5: 全量验证与清理

**Files:**
- Verify: `skills/interaction-testcase-generator/`
- Verify: `eval/skills/interaction-testcase-generator/`

- [ ] **Step 1: 运行构建器测试**

```bash
python3 -m unittest skills/interaction-testcase-generator/scripts/test_xmind_build.py
```

Expected: 所有测试通过

- [ ] **Step 2: 运行评测工具测试**

```bash
python3 -m unittest eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
```

Expected: 所有测试通过

- [ ] **Step 3: 运行完整轻量基线**

```bash
python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
```

Expected: 输出 `lightweight baseline validation passed`

- [ ] **Step 4: 检查格式和临时文件**

```bash
git diff --check
git status --short
```

确认没有 `__pycache__`、`.pyc`、临时 JSON 或临时 XMind。若测试产生缓存，删除后再继续

- [ ] **Step 5: 检查提交历史与最终差异**

```bash
git log -5 --oneline
git status --short
```

Expected: 实施提交清晰，工作区仅包含实施计划文档或为空

- [ ] **Step 6: 提交实施计划与必要收尾**

```bash
git add docs/superpowers/plans/2026-07-22-interaction-testcase-generator-optimization.md
git commit -m "Add testcase skill implementation plan"
```
