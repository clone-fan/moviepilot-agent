---
name: Skill 治理
version: 2.2.0
last_updated: 2026-06-07
---

# Skill 治理

1. 不直接覆盖官方/内置 skills；本地增强独立成 skill 或脚本。
2. skill name matches directory：`SKILL.md` frontmatter `name` 应等于目录名；`allowed-tools` 收敛到实际需要。
3. 安装/修改后检查重名、描述、触发边界、职责重叠和自检。
4. 业务重叠按 `AGENT_SKILLS.md` 与 `MOVIEPILOT_AGENT_WORKFLOW.md` 路由。
5. 发现某类经验属于特定任务的稳定流程、排障顺序、检查清单、命令模板时，应优先蒸馏进对应 skill；memory 只保留需要全局常驻的边界与原则。
6. skill 若依赖非敏感运行锚点（如仓库名、本地路径、Host 别名、公钥指纹），优先放 runtime 文件并在 skill 中引用，不要塞进长期记忆。

## 自检锚点
frontmatter `name` 必须等于目录名。
