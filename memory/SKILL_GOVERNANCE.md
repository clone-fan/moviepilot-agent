---
name: Skill 治理
version: 1.0.0
last_updated: 2026-05-29
---

# Skill 治理

## 安装规则
1. 官方/内置 skills 不直接改；本地增强独立成 skill 或脚本。
2. 技能 frontmatter `name` 必须等于目录名。
3. `allowed-tools` 应尽量收敛到实际需要。
4. 安装新技能后必须检查重名、描述、触发边界与职责重叠。

## 路由规则
1. Superpowers 是工作流纪律层，不是身份层。
2. MoviePilot skills 管业务执行。
3. 带“仅显式触发”的 skills 不自动抢占。
4. 业务技能重叠时按 `MOVIEPILOT_AGENT_WORKFLOW.md` 和 `SUPERPOWERS_WORKFLOW.md` 裁决。

## 安装后检查
- skill 数量。
- frontmatter name 与目录一致。
- 重复职责。
- 显式触发例外。
- 自检脚本通过。
