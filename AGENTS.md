# Repository Guidelines

## Project Overview

本仓库用于维护可安装的 Skills，以及配套的规则、模板、示例、脚本和评测基线。

## Repository Structure

- `skills/`：生产 Skills 及其运行时资源
- `eval/skills/`：对应 Skills 的测试、fixture 和 benchmark
- `docs/`：设计决策与实施文档

## Change Rules

- 修改生产 Skill 的 schema、规则、质量算法或输出契约时，必须同步检查对应 eval
- 修改 eval 契约、fixture 或阈值时，必须反向核对生产 Skill
- 每类规则只保留一个权威来源，README、模板和示例不得重复定义规则
- 删除或重命名文件前，必须搜索运行时引用并更新所有调用方
- 不得提交缓存、临时文件、调试输出或可由工具重新生成的中间产物

## Verification

- 运行被修改 Skill 的单元测试及对应 eval
- 运行相关 artifact、benchmark 或端到端验证
- 删除全部 `__pycache__/` 与 `*.pyc`
- 运行 `git diff --check`

## Git Safety

- 提交仅包含当前任务相关改动
- 不得覆盖或提交用户已有的无关工作区改动
- 未经用户明确要求，不执行 `git push`、发布或部署

## Nested Instructions

进入具体 Skill 或 eval 子目录后，继续遵守距离目标文件最近的 `AGENTS.md`。子目录规则可补充或收紧本文件，但不应复制无关的全仓约束。
