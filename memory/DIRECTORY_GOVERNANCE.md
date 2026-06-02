---
name: Agent 目录治理
version: 2.0.0
last_updated: 2026-06-02
---

# Agent 目录治理

- `memory/`：长期稳定规则，仅直接 `.md` 被加载。
- `skills/`：技能定义与私有辅助文件。
- `jobs/`：每个 Job 一个目录，只放 `JOB.md`。
- `scripts/`：确定性维护脚本。
- `runtime/`：运行态、缓存、当前生效配置、密钥等，不进 Git 能力资产。
- `docs/`：历史资料、归档、说明，不作为运行态来源。
- `activity/`：自动活动日志，只读。

新增/迁移文件按“它是什么”放置；禁止把缓存放 memory/docs，禁止把脚本放 jobs，禁止把单次过程写长期记忆。
