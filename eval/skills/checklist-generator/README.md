# checklist-generator eval

外层目录只保留三个入口：

- `cases/`：样例输入和期望 `.xmind` 产物
- `baseline.json`：主基线，包含 trigger / boundary / comparative / multi-turn / artifact 五套数据
- `README.md`：维护说明

隐藏目录说明：

- `.tools/`：校验与运行脚本
- `.meta/`：锁文件、结果快照、历史对照文档
- `.runtime/`：运行态对照 workspace，按需生成

## Cases

每个 case 一个目录，统一放两类文件：

- `input.json`：标准化 case tree 输入
- `expected.xmind`：期望 benchmark 产物

## 常用命令

- 校验基线一致性：
  `python3 eval/skills/checklist-generator/.tools/validate_benchmark.py`
- 检查本机 runner：
  `python3 eval/skills/checklist-generator/.tools/check_runtime_runner.py`
- 生成运行态对照 workspace：
  `python3 eval/skills/checklist-generator/.tools/prepare_runtime_eval.py --force`
- 执行运行态对照：
  `python3 eval/skills/checklist-generator/.tools/execute_runtime_eval.py`

## 维护规则

- 新 case 先补到 `cases/`，再更新 `baseline.json`
- 改动 `baseline.json` 后，必须同步更新 `.meta/benchmark-lock.json`
- 提交前至少跑一次 `validate_benchmark.py`
- 运行态对照优先复用旧版本快照，不手写伪 baseline
- 评测结果仍统一沉淀到 `skills/checklist-generator/references/real-eval-2026-06-16.md`
