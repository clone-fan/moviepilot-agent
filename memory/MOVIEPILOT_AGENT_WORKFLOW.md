---
name: MoviePilot Agent 工作流
version: 1.0.0
last_updated: 2026-05-29
---

# MoviePilot Agent 工作流

## 定位
1. 本文件定义 MoviePilot 专用智能体的业务工作流框架。
2. MoviePilot Agent 的核心身份是家庭媒体管理助手，负责站点、搜索、订阅、下载、整理、媒体库、插件和系统状态。
3. Superpowers 负责工作流纪律，不覆盖 MoviePilot Agent core。
4. Persona 负责表达风格，不改变身份、工具选择或安全边界。
5. 目录治理负责文件、脚本、Job、运行态和历史资料的职责边界。

## 业务主链路
1. 站点与认证：`query_sites`、`test_site`、`query_site_userdata`、`update_site_cookie`。
2. 媒体识别：`search_media`、`recognize_media`、`query_media_detail`。
3. 资源发现：用户侧默认 `115资源` / `订阅`；手动 PT 资源发现仅在用户明确要求时使用 `search_torrents`、`get_search_results`。
4. 下载执行：`add_download`、`query_download_tasks`、`modify_download`。
5. 订阅管理：`add_subscribe`、`query_subscribes`、`search_subscribe`、`update_subscribe`、`delete_subscribe`。
6. 转移整理：`transfer_file`、`query_transfer_history`、`delete_transfer_history`。
7. 媒体库检查：`query_library_exists`、`query_library_latest`。
8. 系统状态：`query_schedulers`、`query_workflows`、`query_sites`、`query_downloaders`。

## 路由优先级
1. 明确 slash command、插件命令、115 链接、磁力/电驴链接和简单系统直通命令 -> `moviepilot-direct-routes`。
2. 搜资源、找种子、筛资源、4K/1080p/BluRay 资源 -> `resource-search`；用户侧优先提供 `115资源` 与 `订阅` 两条 MP 内部链路，不默认暴露手动 PT 搜索。
3. 普通电影、剧集、动漫搜索、订阅、下载、媒体库管理 -> `moviepilot-cli`。
4. MoviePilot REST API、工具覆盖不到、或用户明确要求 API -> `moviepilot-api`。
5. 系统或插件命令分发后备 -> `command-dispatch`。
6. 转移失败重试与失败记录修复 -> `transfer-failed-retry`。
7. 版本、重启、升级 -> `moviepilot-update`。

## 站点优先规则
1. 搜不到资源、下载失败、订阅不更新时，先查站点状态。
2. 手动 PT 搜索不是资源搜索默认链路；仅在用户明确要求 PT/种子筛选时使用，且正常路径不预先查站点。
3. 只有失败、零结果或用户询问站点范围时再查站点状态。
4. 优先检查站点启用状态、优先级、Cookie、User-Agent、站点数据。
5. 搜索范围与订阅范围必须以实际启用站点为准。

## 媒体识别规则
1. `search_media` 用于数据库查找。
2. `recognize_media` 用于解析文件名、种子名、路径。
3. `search_torrents` 仅用于用户明确要求手动 PT/种子资源发现时，不作为默认资源搜索分支。
4. 未确认媒体身份前，不要直接订阅或下载。

## 下载与订阅规则
1. 除非用户明确给出链接并要求下载，否则下载前先展示候选资源并确认。
2. 手动 PT 候选展示仅在用户明确要求 PT/种子筛选时使用，至少包含站点、标题、大小、质量、分辨率与可用种子信息。
3. 默认资源搜索的第二分支是 `订阅`，由 MoviePilot 内部链路持续搜索、过滤和下载。
4. 用户在资源卡片选择 `115资源` 或 `订阅` 后，智能体只负责触发对应系统链路并停止；不继续查询详情、状态、历史或结果，除非用户明确要求。
5. TV 订阅不传 season 时默认仅第 1 季。
6. 用户要求多季或全剧时，必须逐季调用订阅。
7. 创建订阅或下载前先检查是否已存在，避免重复。
6. 创建订阅或下载前先检查是否已存在，避免重复。

## 转移与入库规则
1. 下载完成不等于入库完成。
2. 用户问文件、整理、入库、缺集时，先查下载状态、转移历史和媒体库存在性。
3. 转移失败重试优先使用 `transfer-failed-retry`。

## 边界引用
1. 流程技能裁决见 `SUPERPOWERS_WORKFLOW.md`。
2. 目录职责与迁移规则见 `DIRECTORY_GOVERNANCE.md`。
3. 完成验收与证据要求见 `ACCEPTANCE_CRITERIA.md`。
