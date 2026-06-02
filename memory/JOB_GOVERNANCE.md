---
name: Job 治理
version: 1.0.0
last_updated: 2026-05-29
---

# Job 治理

## 目录规则
1. 每个 Job 单独目录。
2. Job 目录只放 `JOB.md`。
3. 可执行脚本统一放 `/config/agent/scripts/`。
4. Job 不存放缓存、临时文件、脚本或备份文件。

## 生命周期
1. `once` 任务成功后设置 `status: completed`。
2. `recurring` 任务成功后保持 `status: pending`。
3. 每次执行后更新 `last_run`。
4. 执行日志只写简洁结果，不写长过程。

## 安全规则
1. 自动清理类任务必须硬锁路径。
2. Job 不读取 `docs/` 作为运行态来源。
3. 失败时保留现场，不盲目重试。
4. 删除、迁移、清理类 Job 必须可验证影响范围。
