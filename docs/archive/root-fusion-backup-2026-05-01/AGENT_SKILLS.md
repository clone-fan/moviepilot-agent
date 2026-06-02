---
name: Agent 技能表
description: 基于 superpowers-5.0.7 完整重构后的技能索引与能力映射
version: 5.0.0
last_updated: 2026-04-23
---

# Agent 技能表

## 1. 总线规则
1. 常用业务链路默认收束到 MoviePilot：`CLI工具` → `API` → `插件/调度器`
2. 浏览器、文件、命令行仅作补证与回退
3. 只要某技能、流程、文档有适用概率，就必须先读再做
4. 遇到 bug 必须先走根因调查思路
5. 要宣告完成，必须先拿到本轮验证证据
6. 复杂任务完成前默认做评审式自检

## 2. 核心能力映射
| 能力类别 | 工具 | 对应技能 |
|---|---|---|
| 媒体搜索与识别 | `search_media`、`recognize_media`、`query_media_detail`、`get_recommendations`、`query_episode_schedule` | moviepilot-cli |
| 种子搜索与下载 | `search_torrents`、`get_search_results`、`add_download` | moviepilot-cli |
| 订阅管理 | `add_subscribe`、`query_subscribes`、`update_subscribe`、`delete_subscribe`、`search_subscribe` | moviepilot-cli |
| 媒体库与整理 | `query_library_exists`、`transfer_file`、`query_transfer_history`、`delete_transfer_history` | moviepilot-cli |
| 系统与站点 | `query_sites`、`query_site_userdata`、`query_schedulers`、`query_workflows` | moviepilot-cli |
| 插件与命令 | `list_slash_commands`、`query_plugin_capabilities`、`run_slash_command` | command-dispatch |
| 文件与命令回退 | `read_file`、`write_file`、`edit_file`、`execute_command` | 回退链路 |
| 定时任务与唤醒 | `jobs/*`、`WAKE_FORMAT.md`、scheduler/workflow 查询工具 | jobs-system |

## 3. 已吸收的 superpowers-5.0.7 核心技能
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
11. `finishing-a-development-branch`：完成前测试与收口

## 4. MoviePilot 官方技能接入
1. `moviepilot-cli`：媒体搜索、下载、订阅、媒体库管理主链路
2. `moviepilot-api`：CLI 覆盖不到时的官方 API 回退
3. `command-dispatch`：系统 / 插件 slash 命令分发
4. `database-operation`：数据库只读 / 运维查询回退
5. `moviepilot-update`：版本更新、重启、升级

## 5. 当前自定义技能索引
| 技能 | 描述 | 文档 |
|---|---|---|
| moviepilot-cli | 电影/剧集/动漫搜索、下载、订阅、媒体库管理 | `skills/moviepilot-cli/SKILL.md` |
| generate-identifiers | 生成/管理自定义识别词 | `skills/generate-identifiers/SKILL.md` |
| command-dispatch | 执行系统/插件命令 | `skills/command-dispatch/SKILL.md` |
| transfer-failed-retry | 转移失败重试 | `skills/transfer-failed-retry/SKILL.md` |
| moviepilot-update | 系统重启与升级 | `skills/moviepilot-update/SKILL.md` |
| moviepilot-api | 直接调用 MoviePilot REST API | `skills/moviepilot-api/SKILL.md` |
| work-completion-workflow | 工作完成标准流程 | `skills/work-completion-workflow/SKILL.md` |

## 6. 定时任务系统
1. 任务目录：`/config/agent/jobs`
2. 当前长期任务纳入统一调度与唤醒检查
3. recurring 任务按状态与 `last_run` 自动续转
4. 不再把长期任务逻辑散落到临时对话里

## 7. 说明
1. 后续以本重构版技能表为准
2. 旧的“只改局部规则、不动整体骨架”的思路已废弃
3. 现在的 Agent 以“技能前置 + 根因优先 + 验证优先 + 评审优先”为统一骨架
