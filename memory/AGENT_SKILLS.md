---
name: Agent 技能表
version: 6.1.0
last_updated: 2026-05-23
---

# Agent 技能表

## 总线规则
1. 常用业务链路优先使用 MoviePilot 原生能力：`CLI工具` → `API` → `插件/调度器`
2. 浏览器、文件、命令行用于补证与回退
3. 只要某技能适用，就先读取再执行
4. 遇到问题先查根因，再做修正
5. 宣告完成前必须拿到验证证据
6. 复杂任务完成前默认做自检
7. 不覆盖官方/内置 skills；本地增强能力统一做成独立技能
8. MP 内置/插件 slash 指令直通统一走 `moviepilot-direct-routes`

## 核心能力映射
| 能力类别 | 工具 | 对应技能 |
|---|---|---|
| 媒体搜索与识别 | `search_media`、`recognize_media`、`query_media_detail`、`get_recommendations`、`query_episode_schedule` | moviepilot-cli |
| 种子搜索与下载 | `search_torrents`、`get_search_results`、`add_download` | moviepilot-cli |
| 订阅管理 | `add_subscribe`、`query_subscribes`、`update_subscribe`、`delete_subscribe`、`search_subscribe` | moviepilot-cli |
| 媒体库与整理 | `query_library_exists`、`transfer_file`、`query_transfer_history`、`delete_transfer_history` | moviepilot-cli |
| 系统与站点 | `query_sites`、`query_site_userdata`、`query_schedulers`、`query_workflows` | moviepilot-cli |
| 插件与命令 | `list_slash_commands`、`query_plugin_capabilities`、`run_slash_command` | moviepilot-direct-routes / command-dispatch |
| 文件与命令回退 | `read_file`、`write_file`、`edit_file`、`execute_command` | 回退链路 |
| 定时任务与唤醒 | `jobs/*`、`WAKE_FORMAT.md`、scheduler/workflow 查询工具 | jobs-system |

## superpowers 工作方式
1. `using-superpowers`：技能先于动作
2. `systematic-debugging`：根因先于修复
3. `verification-before-completion`：证据先于结论
4. `brainstorming`：设计先于实现
5. `writing-plans`：计划先于落地
6. `executing-plans`：按计划推进
7. `subagent-driven-development`：任务拆分与阶段评审
8. `requesting-code-review`：评审先于放行
9. `receiving-code-review`：反馈先验证再落地
10. `using-git-worktrees`：隔离式执行思路
11. `finishing-a-development-branch`：完成前测试与收尾

## MoviePilot 业务技能裁决
1. `moviepilot-direct-routes` 优先处理明确直通命令、插件命令、115 链接、磁力/电驴链接和简单系统命令。
2. `resource-search` 处理站点种子资源搜索与候选筛选。
3. `moviepilot-cli` 是媒体搜索、订阅、下载、媒体库管理通用主链路。
4. `moviepilot-api` 只在工具链覆盖不到或用户明确要求 API 时回退。
5. `command-dispatch` 只在 direct-routes 无法明确匹配时作为命令分发回退。
6. 详细边界见 `MOVIEPILOT_AGENT_WORKFLOW.md`。

## 已接入技能
1. `moviepilot-direct-routes`：MP 内置/插件 slash 指令直通统一入口；遇到原本 MP 指令能完成的事，不查媒体、不查库、不绕推理，直接转成 slash command 执行
2. `moviepilot-cli`：媒体搜索、下载、订阅、媒体库管理主链路
3. `moviepilot-api`：CLI 覆盖不到时的 API 回退
4. `command-dispatch`：系统与插件命令分发回退；仅在 direct routes 无法明确匹配时使用
5. `database-operation`：数据库查询与运维回退
6. `moviepilot-update`：版本更新、重启、升级
7. `generate-identifiers`：自定义识别词管理
8. `transfer-failed-retry`：转移失败重试
9. `work-completion-workflow`：任务收尾流程

## 自定义技能索引
| 技能 | 描述 | 文档 |
|---|---|---|
| moviepilot-direct-routes | MP 内置/插件 slash 指令直通统一入口 | `skills/moviepilot-direct-routes/SKILL.md` |
| moviepilot-cli | 电影/剧集/动漫搜索、下载、订阅、媒体库管理 | `skills/moviepilot-cli/SKILL.md` |
| moviepilot-api | 直接调用 MoviePilot REST API | `skills/moviepilot-api/SKILL.md` |
| command-dispatch | 执行系统/插件命令回退 | `skills/command-dispatch/SKILL.md` |
| database-operation | 数据库查询与维护 | `skills/database-operation/SKILL.md` |
| moviepilot-update | 系统重启与升级 | `skills/moviepilot-update/SKILL.md` |
| generate-identifiers | 生成/管理自定义识别词 | `skills/generate-identifiers/SKILL.md` |
| transfer-failed-retry | 转移失败重试 | `skills/transfer-failed-retry/SKILL.md` |
| work-completion-workflow | 工作完成标准流程 | `skills/work-completion-workflow/SKILL.md` |

## 已合并/停用的本地重叠技能
以下技能的职责已并入 `moviepilot-direct-routes`，不再作为主入口保留：

1. `instant-command-router`
2. `mp-direct-command-router`
3. `p115-resource-workflow` 中的 115 slash 指令直通部分

说明：`resource-search` 的站点种子搜索链路与 slash command 直通不同，已移出直通入口；如后续确认为重复，再单独整理。

## 定时任务
1. 任务目录：`/config/agent/jobs`
2. 长期任务通过统一调度执行
3. recurring 任务按状态与 `last_run` 续转
