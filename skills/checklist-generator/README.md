# checklist-generator

维护入口，不重复定义规则。

这里的 `checklist` 仅保留为 skill 名称与触发习惯；实际交付物统一是 `detailed QA test cases`，默认格式为真实 `.xmind` 文件。

## Single Source Map

- `SKILL.md`: 触发边界、默认流程、并行分析节奏
- `references/decision-rules.md`: 何时追问、何时假设、何时降级为 `draft`
- `references/output-rules.md`: 术语、输出契约、命名、质量规则、XMind 层级
- `references/priority-rubric.md`: `P0/P1/P2/P3` 判级标准
- `references/real-eval-2026-06-16.md`: 真实评测记录与当前已知边界

## 目录结构

```text
skills/checklist-generator/
├── SKILL.md
├── README.md
├── examples/
├── references/
├── scripts/
└── templates/
```

各目录职责如下：

- `SKILL.md`：主 skill 定义，只保留触发与流程
- `README.md`：维护入口与文件地图
- `examples/`：按场景选择的 few-shot 参考
- `references/`：唯一权威规则与评测记录
- `scripts/`：生成真实 `.xmind` 文件的脚本
- `templates/`：中间结构和响应模板

## Example Routing

| 需求类型 | 推荐 example | 典型信号 |
| --- | --- | --- |
| 登录、鉴权、账号状态、MFA、锁定 | `examples/web-login.md` | 账号密码、验证码、锁定窗口、登录成功/失败 |
| API 合约、幂等、冲突、重试、并发 | `examples/order-api-idempotency.md` | `Idempotency-Key`、409、202、重复请求、处理中 |
| 报表分析、维度切换、筛选联动、数据一致性、下载 | `examples/trend-analysis-reporting.md` | 视角切换、时间粒度、driverTag、图表/下载一致性、Fun Facts |
| 权限控制、后台报表、导出成功/超时/失败回退、下载中心 | `examples/permission-report-export.md` | 角色差异、导出按钮、下载中心、超时回退、筛选保留 |

维护原则：

- 规则只放在 `references/`，不要把规则复制回 `README.md`
- 新 example 只在新增了稳定失败模式或新领域覆盖时加入
- 新 benchmark 先补到 `eval/` 和 `references/real-eval-2026-06-16.md`，再决定是否需要新 example
