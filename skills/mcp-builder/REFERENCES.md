# MCP Builder Reference

本文件是 `mcp-builder` 的低频参考资料。常规 MCP 设计优先看 `SKILL.md`；需要项目结构、stdio 调试、部署或完整清单时再读取这里。

## Project Shape

TypeScript 常见结构：

```text
src/index.ts          # 注册 tools/resources/prompts
src/tools/            # 按能力拆分 handler
src/resources/        # 只读资源
src/lib/              # 客户端、鉴权、校验、错误封装
tests/
package.json
```

Python 常见结构：

```text
src/my_mcp_server/server.py
src/my_mcp_server/tools/
src/my_mcp_server/lib/
tests/
pyproject.toml
```

常用依赖：

- TypeScript：`@modelcontextprotocol/sdk` + `zod`
- Python：`mcp` + `pydantic`

## Stdio Debugging

MCP stdio transport 不能向 stdout 打普通日志，否则会污染协议流。

- 不用 `console.log` 打调试信息。
- TypeScript 可用 `console.error` 或 SDK logging。
- Python 可用 stderr / logging，并确保不写 stdout 协议外内容。

常见问题：

| 症状 | 常见原因 | 处理 |
|---|---|---|
| 启动无响应 | transport 未 connect | 检查初始化顺序 |
| Tool 不出现 | 注册发生在 connect 之后 | 先注册再连接 |
| AI 不调用工具 | 名称/描述不清晰 | 改名并补描述 |
| 参数反复错 | Schema 太宽或缺描述 | 加枚举、范围、说明 |
| 调用超时 | 外部服务慢 | 加超时、缓存、分页 |

## Deployment Notes

- npm 发布：提供 `bin` 入口和客户端配置 JSON 示例。
- pip 发布：提供 `[project.scripts]` 命令入口。
- Docker：适合复杂依赖或隔离场景。
- README 必须包含安装、配置、环境变量、权限范围、示例调用和故障排查。
- 遵循 semver；破坏性参数或输出变更要升级 major。

## Build Checklist

### Design

- Tools / Resources / Prompts 分工明确。
- Tool 名称和描述足够让 AI 正确选择。
- 参数简洁，默认值合理，危险操作有确认机制。

### Implementation

- 输入校验完整。
- 外部调用有超时和错误处理。
- 敏感信息不硬编码、不输出。
- stdio 不被普通日志污染。
- 生命周期支持初始化和优雅关闭。

### Verification

- 单元测试覆盖核心逻辑。
- 集成测试覆盖 MCP 调用。
- Inspector 手动验证工具展示和调用。
- README 配置示例可复现。
