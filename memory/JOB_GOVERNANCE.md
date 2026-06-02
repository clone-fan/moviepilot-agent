---
name: Job 治理
version: 2.0.0
last_updated: 2026-06-02
---

# Job 治理

1. Job 目录只放 `JOB.md`；脚本统一 `/config/agent/scripts/`。
2. `once` 成功后 `completed`；`recurring` 成功后保持 `pending`，更新 `last_run`。
3. 执行日志简洁记录结果，不写长过程。
4. 自动清理/同步必须硬锁路径、验证影响范围、失败即停。
5. `moviepilot-agent-weekly-sync` 每 7 天同步能力资产到 Git，推送前敏感扫描。
