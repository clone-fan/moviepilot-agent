---
version: 3
name: mcp-builder
description: MCP 服务器构建方法论 — 系统化构建生产级 MCP 工具，让 AI 助手连接外部能力。仅在用户显式要求 MCP server / MCP 工具开发时调用，不要抢占 MoviePilot 主业务路线。
---

# MCP 服务器构建

## Trigger Boundary

这是显式触发型参考技能。仅当用户明确要求 MCP Server、MCP 工具开发、Tools / Resources / Prompts 设计、MCP Inspector 调试或 MCP 发布部署时使用。

不要让本技能抢占 MoviePilot 媒体、站点、下载、订阅、转移、插件管理、Agent Git 或系统排障路线。MoviePilot 内部能力优先使用现有 MCP 工具、slash command、插件 API 和 MoviePilot 专用技能。

## Core Principle

生产级 MCP Server 的目标是：工具可被 AI 正确选择、参数清晰、错误可恢复、权限最小、测试可证明、部署可复现。

MCP 原语选择：

- **Tools**：有动作或副作用，AI 主动调用，如搜索、创建、更新、删除。
- **Resources**：只读数据源，用 URI 标识，如 `users://{id}/profile`。
- **Prompts**：可复用交互模板，引导用户进入固定工作流。

判断口诀：执行操作用 Tool，读取数据用 Resource，引导流程用 Prompt。

## Tool Design

工具要让 AI 一眼选对：

- 名称：`snake_case`，动词开头，如 `search_issues`、`create_ticket`、`delete_file`。
- 描述：说明用途、返回内容、限制条件和副作用。
- 参数：有类型、范围、枚举和描述；避免模糊布尔值。
- 输出：优先结构化 JSON；给人读的摘要可用 Markdown。
- 副作用：写操作、删除、外部发布等必须有确认参数或上层确认流程。

示例描述：

```text
search_users: 根据姓名或邮箱搜索用户。返回 ID、姓名、邮箱。模糊匹配，最多 50 条，无副作用。
```

## Validation and Errors

- Schema 层用 Zod / Pydantic 校验类型、枚举、范围。
- Handler 开头做业务校验：权限、资源存在性、状态是否允许操作。
- 外部调用要有超时、try/catch 和可操作错误。
- 错误结果设置 `isError: true`，并说明用户或 AI 下一步能做什么。
- 错误分类至少区分：参数错误、权限不足、资源不存在、冲突状态、外部服务不可用、超时。

## Security Rules

- 最小权限：读写工具分离，危险操作显式确认。
- 密钥只走环境变量或安全配置，不硬编码、不写日志、不回显。
- SQL 使用参数化查询。
- 文件路径限制根目录，防止 `../` 路径穿越。
- 命令执行优先 `execFile` / 参数数组，避免 shell 注入。
- 返回数据脱敏，日志只记录必要上下文。
- 对网络、文件、并发和请求体大小设置限制。

## Testing Strategy

测试分三层：

1. **单元测试**：handler 内部业务逻辑与外部客户端封装。
2. **集成测试**：用 MCP SDK Client 调用真实 server transport。
3. **人工调试**：用 MCP Inspector 检查工具是否出现、参数是否清晰、输出是否可用。

每个 Tool 至少覆盖：正常路径、参数错误、权限错误、资源不存在、外部服务失败、超时或边界值。

## MoviePilot MCP Boundary

吸收 MCP 集成候选时保持显式触发：

- 不用新 MCP server 取代 MoviePilot 现有 MCP 工具、slash command、插件 API 或 Agent 工具。
- 只有用户明确要求 MCP，或 MoviePilot 原生路径不存在时才设计 MCP。
- 实现前定义 tool/resource/prompt 所有权、副作用、确认门禁和验证方式。
- 不通过 MCP 描述、日志、resources 或 prompts 暴露 MoviePilot token / credential。

项目结构、stdio 调试、部署说明和完整 build checklist 见同目录 `REFERENCES.md`。
## Plugin And Agent Tool Boundary

When a MoviePilot plugin, Agent tool, or MCP candidate overlaps, choose the native owner first:

- MoviePilot plugin feature -> local plugin implementation, command, service, UI, or workflow action.
- Agent operational capability -> MCP/Agent tool only if it cannot live cleanly in MoviePilot plugin APIs or existing tools.
- External integration tool -> MCP only when the user explicitly asks for MCP or the integration must be reused outside MoviePilot.

Do not build an MCP wrapper around a MoviePilot action that already has a stable MCP tool, slash command, plugin command, or direct Agent tool path.

## Output Contract

回答时只给与用户请求相关的 MCP 设计、实现、测试或部署建议，不要展开整套手册。若修改了 Agent 能力资产，完成后执行结构验证，并提醒是否需要同步仓库。
