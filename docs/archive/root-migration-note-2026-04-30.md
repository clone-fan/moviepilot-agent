# 2026-04-30 根层收口说明

本次修复按 superpowers 工作流执行，完成了以下收口：

1. 在 `/config/agent/` 根层补齐以下骨架文件：
   - `CURRENT_PERSONA.md`
   - `MEMORY.md`
   - `AGENT_PROFILE.md`
   - `AGENT_SKILLS.md`
   - `AGENT_WORKFLOW.md`
   - `AGENT_HOOKS.md`
   - `USER_PREFERENCES.md`
   - `WAKE_FORMAT.md`
2. 根层文件现作为主版本
3. 原 `memory/` 与 `docs/` 中的对应文件暂保留，作为迁移期参考副本，不立即删除，以避免未知链路断裂
4. 后续若确认所有唤醒/接管逻辑已切到根层，可再清理旧副本
