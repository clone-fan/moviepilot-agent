# 原生 Agent 能力清单

> 详细能力、插件清单与命令目录统一归档在这里；`/config/agent/AGENT_SKILLS.md` 只保留主索引与自定义技能定义。

## 1. MoviePilot CLI 能力

| 分类 | 命令 |
|---|---|
| **媒体搜索** | `search_media`、`recognize_media`、`query_media_detail`、`get_recommendations`、`search_person`、`search_person_credits`、`query_episode_schedule` |
| **种子搜索** | `search_torrents`、`get_search_results` |
| **下载管理** | `add_download`、`query_download_tasks`、`delete_download`、`modify_download`、`delete_download_history`、`query_downloaders` |
| **订阅管理** | `add_subscribe`、`query_subscribes`、`update_subscribe`、`delete_subscribe`、`search_subscribe`、`query_subscribe_history`、`query_popular_subscribes`、`query_subscribe_shares` |
| **媒体库** | `query_library_exists`、`query_library_latest`、`transfer_file`、`scrape_metadata`、`query_transfer_history`、`delete_transfer_history` |
| **文件目录** | `list_directory`、`query_directory_settings` |
| **站点** | `query_sites`、`query_site_userdata`、`test_site`、`update_site`、`update_site_cookie` |
| **系统** | `query_schedulers`、`run_scheduler`、`query_workflows`、`run_workflow`、`query_rule_groups`、`send_message`、`send_voice_message`、`send_local_file` |
| **自定义识别词** | `query_custom_identifiers`、`update_custom_identifiers` |
| **浏览器** | `browse_webpage`（动态页面交互、表格提取） |

## 2. MoviePilot API 能力范围

| 类别 | 端点数 | 说明 |
|---|---|---|
| **媒体搜索** | 13 | 搜索/识别/刮削/分类/季集/分组 |
| **TMDB** | 8 | 详情/演职员/推荐/季集 |
| **Douban** | 5 | 详情/演职员/推荐 |
| **Bangumi** | 5 | 详情/演职员/推荐 |
| **搜索/种子** | 4 | 媒体搜索/标题/结果/推荐 |
| **下载** | 7 | 添加/启动/停止/删除/列表 |
| **订阅** | 28 | 增删改/状态/历史/搜索/分享 |
| **站点** | 24 | 增删改/CookieCloud/测试/统计 |
| **历史** | 5 | 下载历史/转移历史 |
| **媒体服务器** | 8 | 存在性/缺失集/播放/库 |
| **存储/文件** | 13 | 列目录/建删改/容量 |
| **转移** | 5 | 预览/队列/手动 |
| **Dashboard** | 16 | 统计/存储/进程/CPU/内存/网络 |
| **插件** | 22 | 安装/卸载/重载/配置/仪表板 |
| **工作流** | 16 | 增删改/运行/分享 |
| **系统** | 20 | 环境/设置/重启/模块/版本 |
| **Discover** | 6 | 探索源/Bangumi/Douban/TMDB |
| **Recommend** | 14 | 推荐/每日放送/Top250/周榜 |
| **其他** | 42 | 种子缓存/消息/用户/登录/MCP/Webhook/Servarr/CookieCloud |

## 3. 已安装插件（40个 / 运行中28个）

| 插件ID | 名称 | 版本 | 状态 | 功能 |
|---|---|---|---|---|
| AutoSignIn | 站点自动签到 | 2.8.2 | ✅ | 自动模拟登录、签到站点 |
| P115SubFixer | 115订阅站点修复 | 1.0.1 | ❌ | 修复115网盘订阅追更插件导致的订阅站点被篡改问题 |
| SiteStatistic | 站点数据统计 | 1.9 | ✅ | 站点统计数据图表 |
| MediaCoverGenerator | Emby媒体库封面生成 | 0.9.5 | ✅ | 生成媒体库动态/静态封面，支持 Emby/Jellyfin |
| CategoryEditor | 二级分类策略 | 1.3 | ❌ | 编辑下载和整理时自动二级分类的目录规则 |
| TorrentRemover | 自动删种 | 2.2 | ✅ | 自动删除下载器中的下载任务 |
| RemoteIdentifiers | 共享识别词 | 2.4 | ✅ | 从Github、Etherpad远程文件中获取共享识别词并应用 |
| SubscribeAssistant | 订阅助手 | 2.7.5 | ✅ | 多场景管理订阅，实现订阅种子删除以及自动待定/暂停/洗版 |
| IdentifierHelper | 自定义识别词助手 | 1.0.2 | ❌ | 帮助管理自定义识别词，支持标签分类和可视化编辑 |
| MediaServerMsg | 媒体库服务器通知 | 1.8.2.2 | ✅ | 发送Emby/Jellyfin/Plex服务器的播放、入库等通知消息 |
| AutoBackup | 自动备份 | 2.1.4 | ✅ | 自动备份数据和配置文件 |
| IYUUAutoSeed | IYUU自动辅种 | 2.15 | ❌ | 基于IYUU官方Api实现自动辅种 |
| TorrentTransfer | 自动转移做种 | 1.10.3 | ❌ | 定期转移下载器中的做种任务到另一个下载器 |
| TrafficAssistant | 站点流量管理 | 1.5 | ❌ | 自动管理流量，保障站点分享率 |
| RssSubscribe | 自定义订阅 | 2.1 | ❌ | 定时刷新RSS报文，识别内容后添加订阅或直接下载 |
| SpanelHelper | Sun-Panel助手 | 1.1 | ✅ | 同步MP中已启用的站点到Sun-Panel指定分组 |
| EmbyReverseProxy | Emby 302 反向代理 | 0.2.2 | ✅ | 自动代理并跳转最终播放地址，支持外部播放器调用 |
| BrushFlowLowFreq | 站点刷流（低频版） | 4.3.1 | ✅ | 自动托管刷流，将会提高对应站点的访问频率 |
| ImdbSource | IMDb源 | 1.6.7 | ✅ | 让探索、推荐和媒体识别支持IMDb数据源 |
| MoviePilotUpdateNotify | MoviePilot更新推送 | 2.3.1 | ✅ | 推送release更新通知、自动重启 |
| IyuuAuth | IYUU站点绑定 | 1.2 | ❌ | 为IYUU账号绑定认证站点，以便用于用户认证和辅种 |
| IyuuMsg | IYUU消息通知 | 1.3 | ✅ | 支持使用IYUU发送消息通知 |
| SubscribeGroup | 订阅规则自动填充 | 2.8.7 | ✅ | 电视剧下载后自动添加官组等信息到订阅；添加订阅后根据二级分类名称自定义订阅规则 |
| PluginMarketsAutoUpdate | 插件库更新推送 | 2.0 | ✅ | 自动化添加插件库 |
| SubscribeReminder | 订阅提醒 | 1.5 | ✅ | 推送当天订阅更新内容 |
| SmartRename | 智能重命名 | 1.4 | ✅ | 自定义适配多场景重命名 |
| FFprobeNamingSupplement | ffprobe命名补充 | 0.1.5 | ✅ | 整理重命名时调用 ffprobe，补全命名模板中的 videoFormat、videoCodec、audioCodec、fps、effect |
| LogsClean | 日志清理vue | 2.1 | ✅ | 定时清理插件产生的日志 |
| HistoryClear | 历史记录清理 | 1.0 | - | 一键清理历史记录 |
| DownloaderHelper | 下载器助手 | 4.0.7 | ✅ | 自动标签、自动做种、自动删种 |
| PluginUnInstall | 插件彻底卸载 | 2.2 | ❌ | 删除数据库中已安装插件记录、清理插件文件 |
| BangumiDailyDiscover | Bangumi每日放送探索 | 1.0.7 | ✅ | 让探索支持Bangumi每日放送的数据浏览 |
| TrendingShow | 流行趋势轮播 | 1.3 | ✅ | 在仪表板中显示流行趋势海报轮播图 |
| CloudDriveDisk | CloudDrive2储存 | 0.2.5 | ✅ | CloudDrive2 原生存储支持，grpc 原生 API 操作 |
| P115Disk | 115网盘储存 | 0.2.9 | ✅ | 更快更强的115网盘存储模块 |
| BilibiliDiscover | 哔哩哔哩探索 | 1.0.5 | ✅ | 让探索支持哔哩哔哩的数据浏览 |
| TencentVideoDiscover | 腾讯视频探索 | 1.0.3 | ✅ | 让探索支持腾讯视频的数据浏览 |
| P115StrmHelper | 115网盘STRM助手 | 2.8.8 | ✅ | 115网盘STRM生成一条龙服务 |

## 4. 系统命令

| 命令 | 描述 | 类别 |
|---|---|---|
| `/cookiecloud` | 同步站点 | 站点 |
| `/sites` | 查询站点 | 站点 |
| `/site_cookie` | 更新站点Cookie | 站点 |
| `/site_statistic` | 站点数据统计 | 站点 |
| `/site_enable` | 启用站点 | 站点 |
| `/site_disable` | 禁用站点 | 站点 |
| `/mediaserver_sync` | 同步媒体服务器 | 管理 |
| `/subscribes` | 查询订阅 | 订阅 |
| `/subscribe_refresh` | 刷新订阅 | 订阅 |
| `/subscribe_search` | 搜索订阅 | 订阅 |
| `/subscribe_delete` | 删除订阅 | 订阅 |
| `/subscribe_tmdb` | 订阅元数据更新 | 订阅 |
| `/downloading` | 正在下载 | 管理 |
| `/transfer` | 下载文件整理 | 管理 |
| `/redo` | 手动整理 | 管理 |
| `/clear_cache` | 清理缓存 | 管理 |
| `/restart` | 重启系统 | 管理 |
| `/version` | 当前版本 | 管理 |
| `/clear_session` | 清除会话 | 管理 |
| `/stop_agent` | 停止推理 | 管理 |

## 5. 插件命令

| 命令 | 描述 | 插件 |
|---|---|---|
| `/update_covers` | 更新媒体库封面 | MediaCoverGenerator |
| `/subscribe_toggle` | 切换订阅状态 | SubscribeAssistant |
| `/p115_full_sync` | 全量同步115网盘文件 | P115StrmHelper |
| `/p115_inc_sync` | 增量同步115网盘文件 | P115StrmHelper |
| `/p115_add_share` | 转存分享到待整理目录 | P115StrmHelper |
| `/p115_share_strm` | 115分享链接交互生成STRM | P115StrmHelper |
| `/ol` | 添加离线下载任务，支持磁力 / `ed2k`；`ed2k` 推荐保留完整末尾 `|/` | P115StrmHelper |
| `/p115_strm` | 全量生成指定网盘目录STRM | P115StrmHelper |
| `/sh` | 搜索指定资源 | P115StrmHelper |
| `/hdhivechin` | 手动 HDHive 签到 | P115StrmHelper |

## 6. 插件定时服务

| 服务ID | 名称 | 触发时间 |
|---|---|---|
| AutoSignIn | 站点自动签到服务 | `00:30` |
| MoviePilotUpdateNotify | MoviePilot更新推送服务 | `每6小时` |
| AutoBackup | 自动备份服务 | `每天` |
| TorrentRemover | 自动删种服务 | `1,7,13,19:45` |
| RemoteIdentifiers | 获取远端识别词 | `04:30` |
| SpanelHelper | SunPanel同步服务 | `00:00-01:59` |
| ImdbSource | 刷新主屏幕组件 | `每6小时` |
| ImdbSource.StaffPicks.Now | 刷新主屏幕组件 | `date` |
| SubscribeAssistant | 订阅助手服务 | `每30分` |
| SubscribeReminder | 订阅提醒推送服务 | `08:00` |
| SmartRename | 智能重命名服务 | `每5分` |
| BrushFlowLowFreq | 站点刷流（低频版）服务 | `每10分` |
| BrushFlowLowFreqCheck | 站点刷流（低频版）检查服务 | `每5分` |
| PluginMarketsAutoUpdate | 定时扫描网页记录的插件库地址 | `每24小时` |
| DownloaderHelperTimerService | 下载器助手定时服务 | `每35分` |
| LogsClean | 日志清理服务 | `每天` |
| P115StrmHelper_offline_status | 监控115网盘离线下载进度 | `每2分` |
| P115StrmHelper_monitor_life_guard | 115生活事件线程守护 | `每分` |
| P115StrmHelper_main_cleaner | 定期清理115空间 | `每7小时` |
| P115StrmHelper_increment_sync_strm | 115网盘定期增量同步 | `每小时` |

## 7. 媒体发现来源

| 来源 | 类型 | 说明 |
|---|---|---|
| TMDB | 电影/剧集 | The Movie Database |
| Douban | 电影/剧集 | 豆瓣 |
| Bangumi | 动漫 | Bangumi 每日放送 |
| Bilibili | 动漫/纪录片 | 哔哩哔哩 |
| TencentVideo | 剧集 | 腾讯视频 |
| IMDb | 电影/剧集 | IMDb 数据源 |
| TrendingShow | 流行趋势 | 仪表板流行趋势轮播 |

## 8. MP系统信息

| 项目 | 值 |
|---|---|
| **当前版本** | v2.10.1 |
| **数据库** | PostgreSQL |
| **配置文件目录** | `/config` |
| **系统安装目录** | `/app` |
| **API端口** | 3001 |
