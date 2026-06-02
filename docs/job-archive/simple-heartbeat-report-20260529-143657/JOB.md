---
name: 简单心跳播报
description: 定时采集系统数据并通过send_message直接发送到TG，绕过MP内部消息队列
schedule: recurring
status: cancelled
last_run: "2026-05-29 09:16"
---
# 简单心跳播报任务

> 已蒸馏为新 Job：`/config/agent/jobs/locked-heartbeat-report/JOB.md`。旧 Job 停用，避免双重心跳。

## 目标
定时采集MoviePilot系统数据，**直接调用send_message**发送到TG，避免MP内部消息队列不转发的问题，同时保持既有唤醒栏目完整，重点保证`📈 站点增量`不再漏掉。

## 触发源
- 调度器ID: `agent_heartbeat`
- 触发条件: 以系统配置 `AI_AGENT_JOB_CRON` / `AI_AGENT_JOB_INTERVAL` 为准；当前仅在调度器实际唤醒本任务时执行
- 运行窗口规则: 不在 `JOB.md` 内自行推导下一次执行时间，不根据 `query_schedulers` 的显示结果二次改写调度结论；只在本任务被实际心跳唤醒且 `last_run` 不是本次同一执行窗口时执行，避免与系统定时配置冲突。

## 执行步骤
### 1. 数据采集
- **当前时间**: 系统实时时间
- **系统版本**: 调用 `/api/v1/system/global` 获取 FRONTEND_VERSION/BACKEND_VERSION
- **站点增量**: 采用站点数据统计插件同源口径：基于 `SiteOper().get_userdata_latest()` 取各启用站点最新记录，仅当最新记录属于今日时参与本轮展示；再向前回溯最近可用基线计算上传/下载增量。无今日记录的站点不显示；上传与下载增量同时为 `0 B` 的站点不显示；有异常则明确汇报异常。
- **今日入库**: 调用 `query_transfer_history` 获取当日成功记录
- **今日追新**: 读取 `/config/agent/docs/subscribereminder_last_push.json` 当日结果
- **当前下载**: 调用 `query_download_tasks(status=downloading)` 获取下载任务

### 2. 消息格式化
```text
🕒 当前时间：{current_time}

🤖 MoviePilot：{frontend_version} / {backend_version}

📈 站点增量：
{站点上传/下载增量条目，格式为"⦁ 站点名：↑ 2.15 GB|↓ 0.87 GB"；无今日记录的站点不显示；上传与下载同时为 `0 B` 的站点不显示；异常站点写"⦁ 站点名：异常 - 原因"；若最终无可展示条目则写"无"}

📦 今日入库：
{今日入库条目，按剧名+年份分组，同季多集用'-'连接，不同季用','分隔}

📺 今日追新：
{今日追新条目，每行⦁ 订阅标题 (年份) SxxExx}

⬇️ 当前下载：
{当前下载条目，每行⦁ 下载任务标题，无则写"无"}
```

### 3. 直接发送
- **关键步骤**: 调用 `send_message(message=格式化后的消息内容)`
- **绕过MP内部队列**: 确保消息直达TG通知通道
- **错误处理**: 发送失败时记录日志，保持status: in_progress

## 执行规则
1. **调度结果优先**: 是否到点只以系统调度器实际触发 `agent_heartbeat` 为准；禁止把 `query_schedulers` 的剩余时间、列表可见性或人工估算当成跳过/执行依据。
2. **执行去重**: 同一调度窗口内若 `last_run` 已记录为本轮时间，则不重复发送，避免重复播报。
3. **直接工具调用**: 所有数据采集使用对应工具，不依赖MP内部API
4. **send_message优先**: 格式化后立即调用send_message，不经过其他消息通道
5. **字段容错**: 站点增量遵循当前偏好：有今日快照且能计算时正常显示；无今日记录不显示；上传与下载增量同时为 `0 B` 的站点不显示；有异常明确汇报；最终无可展示条目时写"无"。其它字段按各自规则保持消息完整性。
6. **状态维护**: recurring 任务执行后更新 `last_run` 并保持 `status: in_progress`
7. **日志记录**: 记录每次执行情况和send_message调用结果

## 验证要点
- ✅ send_message工具已验证工作（主动激活测试成功）
- ✅ 数据采集工具可用性已验证
- ❌ MP内部消息队列不转发定时任务消息（已确认问题）
- ✅ 直接调用send_message可绕过此限制

## 执行日志
- **2026-04-03 17:44** - 任务创建，等待首次执行
- **2026-04-03 17:50** - 心跳触发，但TG消息未收到（MP内部队列问题）
- **2026-04-03 17:55** - 任务逻辑更新，改为直接调用send_message
- **2026-04-03 17:56** - 等待下次心跳（18:08）验证修复效果
- **2026-04-03 20:49** - 心跳触发，成功调用send_message发送消息到TG
- **2026-04-04 01:11** - 手动续查并验证：任务已实际执行到send_message且返回“消息已发送”，心跳会话在01:12正常清理；已将任务状态从in_progress修正回pending，等待下次 `agent_heartbeat` 自动触发
- **2026-04-04 02:21** - 少爷确认下一轮 `agent_heartbeat` 自动触发成功，TG 已正常收到心跳播报；本次修复完成验收，当前链路稳定运行
- **2026-04-04 03:35** - 修正今日入库整合显示逻辑：按剧名+年份分组，同季多集用'-'连接，识别连贯集数合并为范围格式（E01-E12），不同季用','分隔
- **2026-04-04 23:47** - 修复唤醒播报缺失栏目：补回`📈 站点增量`，站点增量按今日快照对比昨日快照输出
- **2026-04-05 02:10** - 修复今日追新回退链路与字节格式函数残缺：`subscribereminder_last_push.json` 为空时已回退到订阅数据，站点增量正数不再显示`+`号；已通过 `py_compile`、运行时断言和手动触发 `agent_heartbeat` 验证
- **2026-04-06 23:20** - 旧规则曾依据 `query_schedulers` 的下一次执行时间自行判断“未到窗口”，后确认该做法会与系统真实调度配置冲突，已废弃
- **2026-04-07 01:09** - 旧巡检逻辑曾按距离上次执行时间人工估算是否运行，后确认不应覆盖系统 `AI_AGENT_JOB_CRON` / `AI_AGENT_JOB_INTERVAL`，已废弃
- **2026-04-07 01:10** - 旧巡检逻辑曾以 `agent_heartbeat` 剩余等待时间作为跳过依据，后确认口径错误，已废弃
- **2026-04-07 01:31** - 旧巡检逻辑曾以 `agent_heartbeat` 剩余等待时间作为跳过依据，后确认口径错误，已废弃
- **2026-04-07 02:00** - 旧巡检逻辑曾以 `agent_heartbeat` 剩余等待时间作为跳过依据，后确认口径错误，已废弃
- **2026-04-07 02:26** - 旧巡检逻辑曾以 `agent_heartbeat` 剩余等待时间作为跳过依据，后确认口径错误，已废弃
- **2026-04-07 02:35** - 旧巡检逻辑曾以 `agent_heartbeat` 剩余等待时间作为跳过依据，后确认口径错误，已废弃
- **2026-04-07 03:02** - 旧巡检逻辑曾以 `agent_heartbeat` 剩余等待时间作为跳过依据，后确认口径错误，已废弃
- **2026-04-07 11:00** - 旧巡检逻辑曾以调度列表可见性作为是否执行依据，后确认与真实调度链路不一致，已废弃
- **2026-04-19 13:20** - 已修正任务文档与工作流：心跳是否到点完全以系统配置 `AI_AGENT_JOB_CRON` / `AI_AGENT_JOB_INTERVAL` 和调度器实际唤醒为准，不再允许 `JOB.md` 自定义运行窗口覆盖系统设置
- **2026-04-07 15:06** - 直连执行 `/config/heartbeat_report.py` 成功，输出：OK
- **2026-04-10 08:25** - 心跳触发执行成功：已采集版本/入库/追新/下载数据并直接调用 `send_message` 发送；站点增量未取到，按规则如实播报
- **2026-04-13 05:23** - 心跳触发执行成功：已采集版本/站点增量/今日入库/当前下载数据并直接调用 `send_message` 发送；今日追新缓存非今日，按规则如实标记未取到
- **2026-04-14 05:23** - 心跳触发执行成功：已采集版本/站点增量/今日入库/当前下载数据并直接调用 `send_message` 发送；站点增量无昨日基线，今日入库无当日成功记录，今日追新缓存非今日，均按规则如实播报
- **2026-04-14 20:03** - 心跳触发执行成功：已采集版本/站点增量/今日入库/当前下载数据并直接调用 `send_message` 发送；馒头较昨日上传 49.88 GB；今日追新缓存非今日，按规则如实播报未取到
- **2026-04-14 20:14** - 修复心跳播报格式化逻辑：今日入库改为按 `type` 判断是否电视剧，避免电影误拼出 `S01E404` 这类伪季集；站点增量正数不再显示 `+` 号；已通过 `py_compile`、消息渲染和脚本实发验证
- **2026-04-16 20:01** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-14 20:23** - 修复TG不通知问题：定位到心跳脚本未指定 `userid`，消息走了非立即发送分支且管理员无绑定目标；现已改为读取已绑定 Telegram 用户并直发，脚本执行返回 `OK`，对照 `send_message` 测试已成功送达TG
- **2026-04-19 13:13** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-20 01:13** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-21 03:59** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-21 15:59** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-22 12:55** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-23 07:09** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-23 19:09** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-24 07:09** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-24 19:09** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-25 07:09** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-25 20:01** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-26 20:04** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-27 08:03** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-27 20:03** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-30 01:06** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-04-30 20:05** - 心跳触发执行成功：首次用系统默认 `python3` 执行失败，报错 `ModuleNotFoundError: No module named 'fastapi'`；已切换 `/opt/venv/bin/python` 重跑 `/config/heartbeat_report.py`，脚本返回 `OK`，本轮播报已发送；任务保持 pending 等待下次心跳
- **2026-05-01 14:26** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-02 02:26** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-02 14:26** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-03 02:26** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-03 14:26** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-04 02:26** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-04 20:02** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-05 20:02** - 心跳触发执行成功：已直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-07 06:38** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-07 18:38** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-08 06:38** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-08 20:29** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`，本轮播报已直接发送；任务保持 pending 等待下次心跳
- **2026-05-09 20:02** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0`；任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-10 20:01** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0`；任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-11 20:03** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0`；任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-12 20:05** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；本轮播报已直接发送，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-14 20:02** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0`；任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-16 02:32** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0`；任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-17 04:47** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0`；任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-17 16:46** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-22 20:03** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-24 17:50** - ~~架构升级（cron方案），已于 18:10 回退，回归 agent_heartbeat 原生唤醒~~
- **2026-05-24 18:10** - 按少爷指示移除 cron 方案（`/etc/cron.d/moviepilot-heartbeat`），回归 `agent_heartbeat` 原生唤醒链路；`AI_AGENT_JOB_INTERVAL = 12h`，下次自动唤醒约在明晨 05:17
- **2026-05-26 05:16** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-25 05:34** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-27 07:34** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-27 20:02** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-28 09:16** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-28 21:16** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-29 09:16** - 心跳触发执行成功：已使用 `/opt/venv/bin/python` 直连执行 `/config/heartbeat_report.py`，脚本退出码 `0` 且返回 `OK`；消息已直发通知通道，任务文档已更新 `last_run`，状态保持 pending，等待下次心跳
- **2026-05-29 14:19** - 按少爷要求优化心跳播报：新增站点状态、下载器状态、入库整理统计、存储空间、今日摘要/异常提醒；站点增量补充分享率与魔力；已通过 `py_compile` 与消息渲染验证，未触发实发，等待下次心跳自动发送
- **2026-05-29 14:23** - 固定新版模板为 `2026-05-29.fixed-v1`，栏目顺序锁定为 greeting/time/moviepilot/site_status/site_increment/downloader/transfer/subscribe/storage/summary；补充 `get_source_audit()` 获取路径审计，确认数据获取优先走 MoviePilot 内部模块/操作类：SiteOper、DownloadChain、TransferHistoryOper、SubscribeOper/TmdbChain/MediaChain、ChainBase.post_message；仅存储空间使用容器本地只读 `shutil.disk_usage`，不走外部网页或脆弱文本解析。已通过 `py_compile` 与渲染验证。
- **2026-05-29 14:30** - 按少爷硬性要求锁定心跳模板为 `2026-05-29.fixed-v1-locked`：icon、标题文本、栏目顺序、排版不再漂移，只允许具体数据变化；数据来源必须是确定性内部接口/操作类或本地只读系统调用，禁用 AI 推测与外部 Release 网络查询作为日常心跳路径；已将规则写入 `/config/agent/memory/HEARTBEAT_REPORT_RULES.md`，并通过 `py_compile` 与渲染验证。
- **2026-05-29 14:36** - 已按少爷要求停止旧 Job：本任务已蒸馏迁移到 `locked-heartbeat-report`，旧任务设为 `cancelled`，避免重复发送。
