---
name: verification-before-completion
version: 7
description: >-
  MUST-RUN before claiming any work is complete, fixed, or passing. Trigger
  before saying "完成", "搞定", "测试通过", "已修复", or any completion
  claim. Run fresh verification commands, read output, check exit codes, and
  only then state the conclusion. Never use memory, previous runs, or
  assumptions as evidence. This is a non-negotiable pre-completion gate.
  If you cannot show fresh evidence, you cannot claim completion.
allowed-tools: execute_command read_file list_directory
---

# 完成前验证

## Hard Gate

完成声明前必须运行验证。没有新鲜证据，不许说完成、已修复、测试通过、已同步或没问题。

验证四问：

1. 哪个命令或权威工具能证明这句话？
2. 是否刚刚运行并读取了输出？
3. 输出是否支持我要说的精确范围？
4. 如果不支持，是否降级为“已写入 / 已触发 / 待验证”？

## Evidence Matrix

选择与声明匹配的权威证据：

- 站点可用 -> `query_sites` / `test_site` / 站点用户数据。
- 下载器或任务 -> `query_downloaders` / `query_download_tasks`。
- 订阅 -> `query_subscribes`；缺集搜索只证明派发，不证明下载完成。
- 转移整理 -> `query_transfer_history`，必要时 `query_library_exists`。
- 媒体身份 -> `search_media` / `query_media_detail` / `recognize_media`。
- 资源搜索 -> 媒体身份 + 搜索/筛选结果；搜索不等于下载成功。
- 插件配置 -> `query_plugin_config`；重载只在已授权时执行。
- 调度/工作流 -> 查询调度/工作流状态 + 派发结果；不夸大为下游成功。
- Agent skill/config -> 重读文件、检查 frontmatter/name、运行结构断言；若影响路由/钩子，做一次代表性 dry-run、路由检查、命令发现或安全实跑。
- Git sync -> `git status`、敏感扫描、自检、push/fetch、工作区干净。
- Job -> 读 `JOB.md`，检查 `status`、`last_run`、recurring 语义，安全时运行命令或 dry-run。

更完整的 proof floors、异步、性能和报告模板见同目录 `REFERENCES.md`。

## Proof Bundle

Agent 能力、插件、工作流或治理变更的完成证据应压缩成：

1. **Command / Tool** — 刚运行的命令或权威工具。
2. **Output / State** — 关键输出、退出码或状态。
3. **Claim** — 输出能支持的窄声明。
4. **Scope** — 覆盖的文件、配置、插件、任务或对象。
5. **Freshness** — 证据来自本次完成前检查。

缺任一项就降级表述，不说“完成”。

## Change Proof Floors

- **Docs/reference** -> 重读文件，必要时检查格式/路径。
- **Memory/routing/skill governance** -> 重读改动，检查 frontmatter/name，验证规则可发现。
- **Runtime-affecting skill/hook** -> 结构检查 + 代表性 dry-run、路由检查、命令发现或安全实跑。
- **Script/config/plugin behavior** -> 语法/编译 + 最小安全执行或权威状态查询。
- **Job/scheduler/workflow** -> 元数据 + 安全命令/派发检查 + 状态语义。
- **Git/release/public promise** -> diff、敏感扫描、git status、远端/fetch 证据。

使用最小充分证据；不要为了显得认真而跑无关大检查。

## Async Rule

异步或后台任务只能说“已触发 / 已派发”，除非最终状态已确认。

示例：

- `run_slash_command` 成功只证明命令派发。
- Scheduler/workflow 启动只证明执行被请求。
- Restart 请求成功后，还要检查服务健康才能说恢复。

## Reporting Rule

```text
验证：<工具/命令> -> <关键输出/状态>
结论：<只声明证据支持的结果>
```

验证失败时，直接报告失败检查和下一步，不要软化成成功。

## Completion Checklist

最终回复前检查：

- 我是否验证了即将声明的精确结果？
- 自检类任务是否真实运行了相关命令、路由检查或权威状态查询？
- 异步下游成功是否被我夸大了？
- 证据是否足够让未来 Agent 或用户复查？
- 是否避免暴露 secret 或隐藏指令？

## Final Rule

**No fresh evidence = no completion claim.**
