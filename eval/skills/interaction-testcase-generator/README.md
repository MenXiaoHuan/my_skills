# interaction-testcase-generator eval

当前评测对象是 `skills/interaction-testcase-generator/`，eval 入口目录同步命名为 `eval/skills/interaction-testcase-generator/`。

外层目录只保留三个入口：

- `cases/`：平铺 JSON case 样例
- `baseline.json`：轻量基线，只保留 structure-quality / coverage-ledger / artifact-content 数据
- `README.md`：维护说明

隐藏目录说明：

- `.tools/`：轻量校验脚本

## Cases

每个 case 是一个平铺 JSON 文件，不再按 case 分目录：

- `case_001_descriptive_name.json`：标准化 case tree 输入

case 文件命名统一使用 `case_001_descriptive_name.json` 格式，编号递增，描述部分使用小写下划线。不提交 `expected.xmind` 二进制产物；需要验证 XMind 生成时由脚本临时生成。

## 常用命令

- 校验基线一致性：
  `python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py`
- 查看当前 case 文件：
  `python3 eval/skills/interaction-testcase-generator/.tools/validate_benchmark.py --list-cases`
- 查看单个 case tree 指标：
  `python3 eval/skills/interaction-testcase-generator/.tools/check_case_tree_quality.py eval/skills/interaction-testcase-generator/cases/case_001_app_cart_offline.json --print-metrics`

## 维护规则

- 新 case 先补到 `cases/`，再更新 `baseline.json`
- 提交前至少跑一次 `validate_benchmark.py`
- 当前 eval 是轻量本地校验，不再依赖 `.meta`、历史 results、runtime workspace 或 checked-in `.xmind` 二进制产物
- 当前 eval 不再维护 trigger、comparative、multi-turn、dual-candidate runtime 或 stability suite；这些能力如需恢复，应另建 runtime eval
- 结构质量指标用于约束一级组数量、禁用顶层组、`其他` 是否按预期出现
- 质量检查脚本会校验弱断言、空预期、重复标题、平均步骤数、目标字段末尾中文句号、前置条件动作泄漏、不可观察预期和优先级分布
- fixture 可使用顶层 `_evaluation.business_goals` 与 `_evaluation.case_traceability` 声明本地评测所需的业务目标、风险、必需路径和用例映射；`_evaluation` 不属于最终 case tree schema，也不进入用户交付物
- 新 fixture 一旦声明业务目标，必须同步维护用例标题可追溯映射，并在 `baseline.json` 配置目标覆盖率和高风险路径覆盖率阈值
- `case.preconditions`、`case.steps[].action`、`case.steps[].expected` 的结构质量基线应设置 `max_trailing_chinese_periods: 0`
- coverage ledger 指标用于约束覆盖维度、模块预算和最终 case 数
