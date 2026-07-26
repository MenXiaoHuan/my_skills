# 交互测试用例生成 Skill 内部 IR 重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在保持最终 JSON/XMind 兼容的前提下，以内部测试 IR、可计算覆盖、语义去重和质量报告重构测试用例生成 Skill

**Architecture:** `SKILL.md` 只保留入口与强制工作流，六份 reference 分别作为生成协议、测试模型、测试设计、质量门禁、风险优先级和输出契约的唯一权威。Python 工具负责严格 schema 校验、内部质量报告、覆盖计算、重复裁决检查和 XMind 端到端验证

**Tech Stack:** Markdown、JSON、Python 标准库、`unittest`、XML、ZIP

---

## 目标文件结构

```text
skills/interaction-testcase-generator/
├── AGENTS.md
├── README.md
├── SKILL.md
├── examples/
│   ├── api-contract.md
│   ├── data-consistency.md
│   └── interaction-workflow.md
├── references/
│   ├── generation-protocol.md
│   ├── output-contract.md
│   ├── quality-gates.md
│   ├── risk-priority.md
│   ├── test-design-methods.md
│   └── test-model.md
├── scripts/
│   ├── quality_report.py
│   ├── validate_case_tree.py
│   ├── xmind_build.py
│   └── tests/
│       ├── test_quality_report.py
│       ├── test_validate_case_tree.py
│       └── test_xmind_build.py
└── templates/
    ├── internal-ir.template.json
    ├── quality-report.template.json
    └── xmind-input.template.json
```

## Task 1：严格 case tree validator

**Files:**
- Create: `skills/interaction-testcase-generator/scripts/validate_case_tree.py`
- Create: `skills/interaction-testcase-generator/scripts/tests/test_validate_case_tree.py`
- Modify: `skills/interaction-testcase-generator/scripts/xmind_build.py`
- Move: `skills/interaction-testcase-generator/scripts/test_xmind_build.py` to `skills/interaction-testcase-generator/scripts/tests/test_xmind_build.py`

- [ ] **Step 1：编写 validator 失败测试**

覆盖以下非法输入：

```python
INVALID_CASES = [
    {"title": "", "priority": "P1", "preconditions": "无特殊前置条件", "steps": []},
    {"title": "[P1] 示例", "priority": "P4", "preconditions": "无特殊前置条件", "steps": [{"action": "执行", "expected": "成功"}]},
    {"title": "[P2] 示例", "priority": "P1", "preconditions": "无特殊前置条件", "steps": [{"action": "执行", "expected": "成功"}]},
    {"title": "[P1] 示例", "priority": "P1", "preconditions": [], "steps": [{"action": "执行", "expected": "成功"}]},
    {"title": "[P1] 示例", "priority": "P1", "preconditions": "无特殊前置条件", "steps": [{"action": "", "expected": "成功"}]},
    {"title": "[P1] 示例", "priority": "P1", "preconditions": "无特殊前置条件", "steps": [{"action": "执行", "expected": ""}]}
]
```

有效树必须返回原数据，非法树必须抛出包含 JSON 路径的 `ValidationError`

- [ ] **Step 2：运行测试确认 RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_validate_case_tree.py
```

Expected: 因 `validate_case_tree.py` 不存在而失败

- [ ] **Step 3：实现 validator**

公开接口：

```python
class ValidationError(ValueError):
    pass

def validate_case_tree(data: dict) -> dict:
    ...
```

约束：

- 顶层必须为 object，`groups` 必须为非空 list
- group title 非空，`groups` 与 `cases` 必须为 list
- case title、priority、preconditions 和 steps 必填
- priority 仅允许 `P0/P1/P2/P3`
- 标题前缀必须与 priority 一致
- preconditions 必须为非空 string
- steps 必须为非空 list
- 每个 action 和 expected 必须为非空 string
- 错误消息包含 `groups[0].cases[0].steps[0].action` 形式的路径

- [ ] **Step 4：接入 XMind 构建器**

`xmind_build.py` 在 `build_content_xml` 和 CLI 写文件前调用 `validate_case_tree(data)`。删除：

```python
case.get("title") or "用例标题"
group.get("title") or "分组"
if not steps:
    _topic(steps_attached, "步骤 1")
```

- [ ] **Step 5：运行 validator 与构建器测试**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_validate_case_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_xmind_build.py
```

Expected: 全部通过

- [ ] **Step 6：提交**

```bash
git add skills/interaction-testcase-generator/scripts
git commit -m "Add strict testcase tree validation"
```

## Task 2：内部 IR 与质量报告

**Files:**
- Create: `skills/interaction-testcase-generator/templates/internal-ir.template.json`
- Create: `skills/interaction-testcase-generator/templates/quality-report.template.json`
- Create: `skills/interaction-testcase-generator/scripts/quality_report.py`
- Create: `skills/interaction-testcase-generator/scripts/tests/test_quality_report.py`

- [ ] **Step 1：编写质量报告失败测试**

最小 IR 包含：

```json
{
  "version": "1.0",
  "sources": [{"id": "SRC-1", "type": "api"}],
  "business_goals": [{"id": "G-1", "risk": "high", "required_paths": ["positive", "critical_failure"]}],
  "api_contracts": [{"id": "API-1", "source_refs": ["SRC-1"]}],
  "data_invariants": [{"id": "INV-1", "source_refs": ["SRC-1"]}],
  "coverage_atoms": [
    {"id": "A-1", "kind": "api_contract", "target_ref": "API-1", "required": true, "risk_weight": 5},
    {"id": "A-2", "kind": "data_consistency", "target_ref": "INV-1", "required": true, "risk_weight": 4}
  ],
  "candidate_cases": [
    {"id": "C-1", "title": "创建订单", "goal_refs": ["G-1"], "path_type": "positive", "coverage_atoms": ["A-1"]},
    {"id": "C-2", "title": "重复请求", "goal_refs": ["G-1"], "path_type": "critical_failure", "coverage_atoms": ["A-1"]},
    {"id": "C-3", "title": "订单数据一致", "goal_refs": ["G-1"], "path_type": "positive", "coverage_atoms": ["A-2"]}
  ]
}
```

断言：

- 必选 atom 覆盖率为 `1.0`
- API 覆盖率为 `1.0`
- 数据不变量覆盖率为 `1.0`
- 高风险路径覆盖率为 `1.0`
- 相同 coverage atom 的候选被列为重复裁决候选，但不同 `path_type` 不自动合并
- 缺少 source 的 API case 进入阻断门禁

- [ ] **Step 2：运行测试确认 RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_quality_report.py
```

Expected: 因 `quality_report.py` 不存在而失败

- [ ] **Step 3：实现质量报告**

公开接口：

```python
def normalize_case_title(title: str) -> str:
    ...

def verification_fingerprint(case: dict) -> tuple:
    ...

def select_minimum_sufficient_cases(ir: dict) -> list[str]:
    ...

def build_quality_report(ir: dict, selected_case_ids: list[str] | None = None) -> dict:
    ...
```

最小充分集按以下稳定排序选取：

```text
score = 新增 atom 风险权重 + 高风险路径奖励 - execution_cost - 重叠数
```

同分时按 `candidate_cases` 原顺序选择

- [ ] **Step 4：增加模板**

`internal-ir.template.json` 包含设计文档中的全部顶层数组和一个交互、接口、数据一致性示例

`quality-report.template.json` 包含：

```json
{
  "source_coverage": {},
  "goal_coverage": {},
  "risk_coverage": {},
  "dimension_coverage": {},
  "api_coverage": {},
  "data_invariant_coverage": {},
  "state_transition_coverage": {},
  "duplicate_clusters": [],
  "merged_cases": [],
  "uncovered_atoms": [],
  "assumptions": [],
  "conflicts": [],
  "quality_gates": {}
}
```

- [ ] **Step 5：运行测试**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_quality_report.py
```

Expected: 全部通过

- [ ] **Step 6：提交**

```bash
git add skills/interaction-testcase-generator/scripts skills/interaction-testcase-generator/templates
git commit -m "Add testcase IR quality reporting"
```

## Task 3：重构 Skill 规则和文档

**Files:**
- Create: `AGENTS.md`
- Create: `skills/interaction-testcase-generator/AGENTS.md`
- Modify: `skills/interaction-testcase-generator/SKILL.md`
- Modify: `skills/interaction-testcase-generator/README.md`
- Create: `skills/interaction-testcase-generator/references/generation-protocol.md`
- Create: `skills/interaction-testcase-generator/references/test-model.md`
- Create: `skills/interaction-testcase-generator/references/test-design-methods.md`
- Create: `skills/interaction-testcase-generator/references/quality-gates.md`
- Create: `skills/interaction-testcase-generator/references/risk-priority.md`
- Create: `skills/interaction-testcase-generator/references/output-contract.md`

- [ ] **Step 1：重写 `SKILL.md` 入口**

保留：

- description 与触发边界
- Authority Map
- 五阶段工作流
- 简单请求单候选加 gap scan
- 高风险、多模块、接口或跨系统场景双候选
- 内部 IR 与质量报告不得默认暴露
- 最终 JSON/XMind 兼容契约

删除与 reference 重复的细节

- [ ] **Step 2：建立六份唯一权威 reference**

职责：

- `generation-protocol.md`：ask/assume/draft、候选模式、覆盖与裁决流程
- `test-model.md`：IR、coverage atom、受控维度和分类
- `test-design-methods.md`：交互、决策表、状态、API、数据一致性、组合与异常设计
- `quality-gates.md`：阻断门禁、警告门禁、去重和最小充分集
- `risk-priority.md`：风险权重和 `P0/P1/P2/P3`
- `output-contract.md`：最终 JSON、XMind、标点和失败回退

- [ ] **Step 3：增加 `AGENTS.md`**

根 `AGENTS.md` 只约束 Skill 与 eval 同步修改、测试和缓存清理

Skill 子树 `AGENTS.md` 约束单一权威、受控枚举、fixture、删除引用检查和提交前命令

- [ ] **Step 4：更新 README**

README 只描述目录职责、维护入口和验证命令，不复制生成规则

- [ ] **Step 5：静态检查**

```bash
git diff --check
```

Expected: 通过

- [ ] **Step 6：提交**

```bash
git add AGENTS.md skills/interaction-testcase-generator
git commit -m "Refactor testcase skill around internal IR"
```

## Task 4：重构示例、模板与冗余文件

**Files:**
- Create: `skills/interaction-testcase-generator/examples/interaction-workflow.md`
- Create: `skills/interaction-testcase-generator/examples/api-contract.md`
- Create: `skills/interaction-testcase-generator/examples/data-consistency.md`
- Rename: `skills/interaction-testcase-generator/templates/xmind_input.template.json` to `skills/interaction-testcase-generator/templates/xmind-input.template.json`
- Delete old references after migration
- Delete `skills/interaction-testcase-generator/examples/multi-candidate-adjudication.md`
- Delete `skills/interaction-testcase-generator/templates/response-template.md`
- Delete `skills/interaction-testcase-generator/templates/multi_candidate_adjudication.template.md`
- Delete old examples not retained by the new Authority Map

- [ ] **Step 1：创建三个正交示例**

每个示例包含：

- 来源片段
- IR 摘要
- coverage atoms
- 候选裁决
- 最终兼容 case tree 摘要

三个示例分别只突出交互工作流、接口契约和数据一致性

- [ ] **Step 2：迁移 XMind 模板**

新文件保持兼容 schema，示例内容符合严格 validator，并保留标点规则注释

- [ ] **Step 3：引用扫描**

```bash
rg "decision-rules|priority-rubric|output-rules|grouping-rules|quality-rules|multi-candidate-rules|coverage-ledger-rules|multi-candidate-adjudication|response-template|multi_candidate_adjudication|xmind_input" .
```

Expected: 只出现计划或历史设计文档中的描述，不出现运行时引用

- [ ] **Step 4：删除旧文件**

使用文件删除工具删除已迁移且无引用的旧 reference、example 和 template

- [ ] **Step 5：提交**

```bash
git add -A skills/interaction-testcase-generator
git commit -m "Consolidate testcase skill references"
```

## Task 5：重构 eval 为 schema 与 quality regression

**Files:**
- Refactor: `eval/skills/interaction-testcase-generator/.tools/check_case_tree_quality.py`
- Refactor: `eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py`
- Refactor: `eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py`
- Modify: `eval/skills/interaction-testcase-generator/baseline.json`
- Modify: existing standard case fixtures
- Delete: self-reported coverage ledger fixtures
- Create: `eval/skills/interaction-testcase-generator/ir/` representative IR fixtures

- [ ] **Step 1：编写失败测试**

新增测试验证：

- 空 action 不算 schema complete
- 非法 priority 被识别
- 标题前缀不一致被识别
- 归一化重复标题被识别
- verification fingerprint 重复被识别
- API case 无 source 失败
- 数据一致性 case 无 invariant 失败
- coverage 数据由 IR 和 selected case 计算

- [ ] **Step 2：运行确认 RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
```

Expected: 新指标不存在或断言失败

- [ ] **Step 3：复用生产工具**

eval 通过 import 复用：

```python
validate_case_tree
build_quality_report
```

不复制 schema 和覆盖算法

- [ ] **Step 4：迁移 fixture**

- 标准 case tree 全部满足 strict schema
- 删除 `case_002`、`case_003`、`case_004` 自报 ledger
- 代表性交互、API、审批和数据一致性 IR 放入 `ir/`
- baseline 只保存阈值和 fixture 引用，不重复 target modules 与 dimensions

- [ ] **Step 5：运行 schema 与 quality baseline**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
```

Expected: 全部通过

- [ ] **Step 6：提交**

```bash
git add -A eval/skills/interaction-testcase-generator
git commit -m "Rebuild testcase quality regression suite"
```

## Task 6：真实 XMind Artifact E2E

**Files:**
- Create: `eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py`
- Modify: `eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py`
- Modify: `eval/skills/interaction-testcase-generator/README.md`

- [ ] **Step 1：编写 E2E 失败测试**

测试应：

1. 从标准 fixture 调用 `xmind_build.py`
2. 输出到 `tempfile.TemporaryDirectory`
3. 验证 ZIP 成员：

```text
content.xml
meta.xml
styles.xml
META-INF/manifest.xml
```

4. 解析 `content.xml`
5. 验证根、分组、用例、前置条件、步骤和预期层级
6. 验证 priority marker、note、父级合并和末尾句号清理

- [ ] **Step 2：运行确认 RED**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py
```

Expected: 当前 eval 尚未满足新的 E2E 入口或 fixture 要求

- [ ] **Step 3：接入 benchmark validator**

`validate_benchmark.py` 的 artifact suite 必须执行真实构建和 XML 检查，不再只搜索输入 JSON 字符串

- [ ] **Step 4：运行全部测试**

```bash
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_validate_case_tree.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_quality_report.py
PYTHONDONTWRITEBYTECODE=1 python3 skills/interaction-testcase-generator/scripts/tests/test_xmind_build.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_check_case_tree_quality.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/test_xmind_artifact_e2e.py
PYTHONDONTWRITEBYTECODE=1 python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py
```

Expected: 全部通过

- [ ] **Step 5：提交**

```bash
git add eval/skills/interaction-testcase-generator
git commit -m "Add testcase XMind artifact regression"
```

## Task 7：旧文档、缓存与最终验证

**Files:**
- Delete: `docs/superpowers/plans/2026-07-22-interaction-testcase-generator-optimization.md`
- Delete: `docs/superpowers/specs/2026-07-22-interaction-testcase-generator-optimization-design.md`
- Keep: `docs/superpowers/specs/2026-07-26-interaction-testcase-generator-ir-refactor-design.md`
- Keep: `docs/superpowers/plans/2026-07-26-interaction-testcase-generator-ir-refactor.md`

- [ ] **Step 1：确认新设计已吸收旧决策**

检查兼容、标点、业务目标、质量门禁和评测决策均存在于新设计与新 reference

- [ ] **Step 2：正式提交旧文档删除**

```bash
git add -u docs/superpowers
git add docs/superpowers/plans/2026-07-26-interaction-testcase-generator-ir-refactor.md
git commit -m "Retire superseded testcase design docs"
```

- [ ] **Step 3：清理缓存**

删除所有：

```text
__pycache__/
*.pyc
```

- [ ] **Step 4：运行最终验证**

重复 Task 6 的全部测试，并运行：

```bash
git diff --check
git status --short --branch
git log -10 --oneline
```

Expected:

- 所有测试通过
- 无缓存和临时文件
- 工作区干净
- `main` 仅领先远端，未落后

- [ ] **Step 5：推送前报告**

汇总改动、删除文件、测试结果、提交列表和剩余风险。只有用户明确要求推送时才执行：

```bash
git push origin main
```
