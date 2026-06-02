---
name: Skill 治理
version: 2.1.0
last_updated: 2026-06-02
---

# Skill 治理

1. 不直接覆盖官方/内置 skills；本地增强独立成 skill 或脚本。
2. skill name matches directory：`SKILL.md` frontmatter `name` 应等于目录名；`allowed-tools` 收敛到实际需要。
3. 安装/修改后检查重名、描述、触发边界、职责重叠和自检。
4. 业务重叠按 `AGENT_SKILLS.md` 与 `MOVIEPILOT_AGENT_WORKFLOW.md` 路由。

## 自检锚点
frontmatter `name` 必须等于目录名。
