# Skill Eval Directory Standard Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate `test-case-generator` from a skill-local monolithic eval file to the new repository-level `eval/skills/<skill-name>/` structure.

**Architecture:** Keep runtime skill assets in `skills/test-case-generator/` and move evaluation assets into `eval/skills/test-case-generator/`. Split the current `evals.json` into one human-readable `README.md`, one shared `baseline.json`, and three independent case JSON files under `cases/`, then remove the legacy skill-local eval file.

**Tech Stack:** Markdown, JSON, git, shell commands

---

## File Structure

**Create**
- `eval/skills/test-case-generator/README.md`
- `eval/skills/test-case-generator/baseline.json`
- `eval/skills/test-case-generator/cases/case_001.json`
- `eval/skills/test-case-generator/cases/case_002.json`
- `eval/skills/test-case-generator/cases/case_003.json`

**Delete**
- `skills/test-case-generator/evals/evals.json`

**Leave Unchanged**
- `skills/test-case-generator/SKILL.md`
- `skills/test-case-generator/examples/web-login.md`
- `skills/test-case-generator/examples/order-api-idempotency.md`
- `skills/test-case-generator/references/decision-rules.md`
- `skills/test-case-generator/references/output-rules.md`
- `skills/test-case-generator/scripts/xmind_build.py`
- `skills/test-case-generator/templates/response-template.md`
- `skills/test-case-generator/templates/xmind_input.template.json`

### File Responsibilities

- `eval/skills/test-case-generator/README.md`: explains purpose, scope, pass criteria, and maintenance rules for this eval pack
- `eval/skills/test-case-generator/baseline.json`: stores skill-wide shared eval defaults and forbidden behaviors
- `eval/skills/test-case-generator/cases/case_001.json`: web login plus MFA plus account lockout case
- `eval/skills/test-case-generator/cases/case_002.json`: app cart plus stock plus offline retry case
- `eval/skills/test-case-generator/cases/case_003.json`: API idempotency plus sparse-material draft behavior case

### Task 1: Create Eval Pack Skeleton

**Files:**
- Create: `eval/skills/test-case-generator/README.md`
- Create: `eval/skills/test-case-generator/baseline.json`

- [ ] **Step 1: Create the target directory tree**

Run:

```bash
mkdir -p eval/skills/test-case-generator/cases
```

Expected: directory `eval/skills/test-case-generator/cases` exists.

- [ ] **Step 2: Write the eval pack README**

Write `eval/skills/test-case-generator/README.md` with exactly:

```md
# Eval Pack: test-case-generator

## Purpose

Evaluate whether `test-case-generator` produces structured, implementation-aware test design outputs from requirement or technical materials, with correct prioritization, assumptions handling, and real `.xmind` deliverables when required.

## Scope

This eval pack covers:
- trigger fit
- coverage completeness
- P0 labeling quality
- assumptions and draft behavior
- output contract compliance
- XMind deliverable expectations

This eval pack does not cover:
- implementation correctness of product code
- UI rendering quality of the generated XMind viewer
- external system availability

## Pass Criteria

A case passes only when:
- the skill is correctly triggered
- the response follows the expected output contract
- required scope is covered
- forbidden behavior is not present
- draft or assumptions behavior is correct when applicable

## Files

- `baseline.json`: shared evaluation defaults for this skill
- `cases/`: independent eval cases

## Maintenance Rules

- keep one intent per case
- prefer small, composable cases over mega-cases
- add a new case when a bug, regression, or prompt failure is discovered
- update `baseline.json` only for truly shared rules
```

- [ ] **Step 3: Write the shared baseline**

Write `eval/skills/test-case-generator/baseline.json` with exactly:

```json
{
  "skill_name": "test-case-generator",
  "version": 1,
  "default_language": "zh-CN",
  "output_contract": {
    "primary_artifact": "xmind",
    "return_absolute_path_first": true,
    "require_real_xmind_file": true
  },
  "global_expectations": [
    "keep full in-scope coverage instead of outputting only P0 cases",
    "mark P0 only when justified",
    "state no P0 explicitly when none qualifies",
    "separate confirmed information from assumptions when assumptions are used",
    "label output as draft when critical source material is missing or conflicting"
  ],
  "forbidden_behaviors": [
    "returning only prose when a real xmind deliverable is required",
    "treating P0 as a coverage filter",
    "silently inventing critical workflow semantics",
    "using markdown bullet prefixes in xmind group or case titles"
  ],
  "scoring": {
    "mode": "rule-based",
    "pass_threshold": 1.0
  }
}
```

- [ ] **Step 4: Verify the README and baseline exist**

Run:

```bash
ls -R eval/skills/test-case-generator
```

Expected:

```text
README.md
baseline.json
cases
```

- [ ] **Step 5: Commit the skeleton**

Run:

```bash
git add eval/skills/test-case-generator/README.md eval/skills/test-case-generator/baseline.json
git commit -m "docs(eval): add test-case-generator eval pack skeleton"
```

Expected: a commit containing only the new README and baseline files.

### Task 2: Split Monolithic Evals Into Independent Cases

**Files:**
- Create: `eval/skills/test-case-generator/cases/case_001.json`
- Create: `eval/skills/test-case-generator/cases/case_002.json`
- Create: `eval/skills/test-case-generator/cases/case_003.json`
- Modify: `skills/test-case-generator/evals/evals.json` only as migration input reference during this task

- [ ] **Step 1: Write case 001**

Write `eval/skills/test-case-generator/cases/case_001.json` with exactly:

```json
{
  "id": "case_001",
  "title": "Web login with MFA and lockout",
  "type": "core",
  "tags": ["web", "auth", "mfa", "lockout", "p0"],
  "prompt": "请基于以下 Web 登录需求设计测试用例，并默认输出真实 .xmind 文件。需求：用户输入正确账号密码后，如果账号开启了 MFA，则必须先完成短信验证码校验才能进入控制台；连续输错密码 5 次后账号锁定 15 分钟；已锁定账号在锁定期内使用正确密码也不能登录。请覆盖正常流程、MFA、锁定、边界和异常场景，并标记 release-critical 场景。",
  "inputs": {
    "files": []
  },
  "expect": {
    "must": [
      "generate a real .xmind file",
      "return the absolute path first",
      "cover login success flow",
      "cover MFA flow",
      "cover account lockout behavior",
      "cover boundary and negative scenarios"
    ],
    "should": [
      "identify at least one justified P0 scenario"
    ],
    "must_not": [
      "output only P0 cases",
      "omit lockout-with-correct-password behavior"
    ]
  },
  "notes": "Core regression case for auth flow."
}
```

- [ ] **Step 2: Write case 002**

Write `eval/skills/test-case-generator/cases/case_002.json` with exactly:

```json
{
  "id": "case_002",
  "title": "App cart with inventory and offline retry",
  "type": "core",
  "tags": ["app", "cart", "inventory", "offline", "assumptions"],
  "prompt": "请根据以下 App 购物车功能描述生成测试点和测试用例，默认输出 .xmind 文件。功能：用户可在商品详情页加入购物车；同一 SKU 重复加入时数量累加；库存不足时应阻止加入并提示；离线状态下加入购物车请求进入重试队列，网络恢复后自动同步。请标记 release-critical 场景，并在信息不足处写 assumptions。",
  "inputs": {
    "files": []
  },
  "expect": {
    "must": [
      "generate a real .xmind file",
      "return the absolute path first",
      "cover add-to-cart flow",
      "cover repeated add quantity accumulation",
      "cover insufficient stock behavior",
      "cover offline retry and sync consistency",
      "state assumptions when information is missing"
    ],
    "should": [
      "identify justified P0 scenarios without reducing full coverage"
    ],
    "must_not": [
      "output only P0 cases",
      "ignore offline recovery behavior"
    ]
  },
  "notes": "Core app workflow plus assumptions handling."
}
```

- [ ] **Step 3: Write case 003**

Write `eval/skills/test-case-generator/cases/case_003.json` with exactly:

```json
{
  "id": "case_003",
  "title": "Order API idempotency draft case",
  "type": "draft",
  "tags": ["api", "idempotency", "draft", "assumptions"],
  "prompt": "我这里只有一个简短变更说明，没有正式 PRD：订单创建 API 新增幂等键 idempotency_key。同一个 key 的重复请求如果 payload 完全一致，应返回同一个订单结果；如果 payload 不一致，应返回冲突错误；过期 key 允许重新创建订单。请先用现有描述产出一版 draft 测试设计，默认输出真实 .xmind 文件，并明确哪些地方是基于假设。",
  "inputs": {
    "files": []
  },
  "expect": {
    "must": [
      "generate a real .xmind file",
      "return the absolute path first",
      "label the result as draft",
      "cover first request behavior",
      "cover repeated request behavior for identical payload",
      "cover conflict behavior for mismatched payload",
      "cover expired key behavior",
      "separate confirmed information from assumptions"
    ],
    "should": [
      "preserve an execution-oriented test structure despite sparse input"
    ],
    "must_not": [
      "present the result as a final test design",
      "silently invent missing contract rules as confirmed facts"
    ]
  },
  "notes": "Sparse-material case validating draft behavior."
}
```

- [ ] **Step 4: Validate all case files parse as JSON**

Run:

```bash
python3 - <<'PY'
import json
from pathlib import Path
for path in sorted(Path("eval/skills/test-case-generator/cases").glob("*.json")):
    with path.open() as f:
        json.load(f)
    print(path)
PY
```

Expected: all three `case_00X.json` files print without traceback.

- [ ] **Step 5: Commit the case split**

Run:

```bash
git add eval/skills/test-case-generator/cases/case_001.json eval/skills/test-case-generator/cases/case_002.json eval/skills/test-case-generator/cases/case_003.json
git commit -m "test(eval): split test-case-generator eval cases"
```

Expected: a commit containing only the three case JSON files.

### Task 3: Remove Legacy Eval And Verify Final Structure

**Files:**
- Delete: `skills/test-case-generator/evals/evals.json`
- Verify: `eval/skills/test-case-generator/README.md`
- Verify: `eval/skills/test-case-generator/baseline.json`
- Verify: `eval/skills/test-case-generator/cases/case_001.json`
- Verify: `eval/skills/test-case-generator/cases/case_002.json`
- Verify: `eval/skills/test-case-generator/cases/case_003.json`

- [ ] **Step 1: Delete the legacy monolithic eval file**

Delete:

```text
skills/test-case-generator/evals/evals.json
```

Expected: the old skill-local eval file no longer exists.

- [ ] **Step 2: Verify the old path is gone and the new files exist**

Run:

```bash
test ! -f skills/test-case-generator/evals/evals.json
test -f eval/skills/test-case-generator/README.md
test -f eval/skills/test-case-generator/baseline.json
test -f eval/skills/test-case-generator/cases/case_001.json
test -f eval/skills/test-case-generator/cases/case_002.json
test -f eval/skills/test-case-generator/cases/case_003.json
echo "eval migration structure verified"
```

Expected:

```text
eval migration structure verified
```

- [ ] **Step 3: Verify final file tree**

Run:

```bash
find eval/skills/test-case-generator -maxdepth 2 -type f | sort
```

Expected:

```text
eval/skills/test-case-generator/README.md
eval/skills/test-case-generator/baseline.json
eval/skills/test-case-generator/cases/case_001.json
eval/skills/test-case-generator/cases/case_002.json
eval/skills/test-case-generator/cases/case_003.json
```

- [ ] **Step 4: Review git diff for migration scope**

Run:

```bash
git diff --stat -- eval/skills/test-case-generator skills/test-case-generator/evals/evals.json
```

Expected: only the new `eval/skills/test-case-generator/` files and deletion of `skills/test-case-generator/evals/evals.json` appear.

- [ ] **Step 5: Commit the final migration**

Run:

```bash
git add eval/skills/test-case-generator/README.md \
  eval/skills/test-case-generator/baseline.json \
  eval/skills/test-case-generator/cases/case_001.json \
  eval/skills/test-case-generator/cases/case_002.json \
  eval/skills/test-case-generator/cases/case_003.json \
  skills/test-case-generator/evals/evals.json
git commit -m "refactor(eval): migrate test-case-generator eval pack"
```

Expected: a commit capturing the completed migration and legacy file removal.

## Self-Review

- Spec coverage:
  - repository-level `eval/skills/<skill-name>/` structure is implemented in Task 1 and Task 3
  - `README.md`, `baseline.json`, and independent `cases/*.json` are created in Task 1 and Task 2
  - migration from legacy `evals.json` and its removal are handled in Task 2 and Task 3
  - `test-case-generator` is used as the first rollout target in all tasks
- Placeholder scan:
  - no `TBD`, `TODO`, or vague "implement later" steps remain
- Consistency:
  - all paths use the same `eval/skills/test-case-generator/` target
  - all case identifiers and filenames match across tasks
