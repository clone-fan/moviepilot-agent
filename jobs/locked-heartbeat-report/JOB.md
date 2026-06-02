---
name: 固定模板心跳播报
description: 定时采集真实 MoviePilot 内部数据并按固定模板直发 Telegram；唯一执行命令：/opt/venv/bin/python /config/heartbeat_report.py；成功输出 OK；recurring 执行后保持 pending。
schedule: recurring
status: pending
last_run: "2026-06-01 13:54"
---
# 固定模板心跳播报任务

## 目标
将旧 `simple-heartbeat-report` 蒸馏为新的固定模板心跳 Job。

本 Job 只做一件事：在 `agent_heartbeat` 唤醒时，执行确定性脚本 `/config/heartbeat_report.py`，通过 MoviePilot 内部路径采集真实数据，并按固定模板直发 Telegram。

## 固定模板版本
`2026-05-29.fixed-v1-locked`

## 固定模板
```text
少爷，{时段}好。给你送上今天的心跳播报。

🕒 时间：{YYYY-MM-DD HH:mm:ss}

🤖 MoviePilot：
⦁ 版本：{FRONTEND_VERSION} / {APP_VERSION}，{版本状态}

📡 站点状态：
⦁ 今日快照：正常 {normal_count}｜过期 {stale_count}｜异常 {error_count}
{异常站点条目，可为空}

📈 站点增量：
{站点增量条目；无则：⦁ 无}

⬇️ 下载器：
{无正在下载时：⦁ 正在下载：无；有正在下载时：⦁ 正在下载：{downloading_count}；有真实速度时显示速度}
{当前任务条目，可为空}

📦 入库整理：
⦁ 今日成功：{success_count}｜失败：{failed_count}
{失败条目，可为空}
{今日入库条目；无则：⦁ 今日入库：无}

📺 订阅追新：
{今日追新条目；无则：⦁ 今日追新：无}

💾 存储空间：
{存储空间条目；无则：⦁ 未取到}

✅ 今日摘要：
⦁ 系统正常
⦁ 站点快照正常
⦁ 无失败转移
⦁ 下载器无异常
```

若存在异常、过期、失败、未取到或空间偏紧，最后一栏固定替换为：

```text
⚠️ 今日提醒：
{异常提醒条目，最多 5 条}
```

## 锁定规则
1. icon 不准改。
2. 标题文本不准改。
3. 栏目顺序不准改。
4. 排版不准改。
5. 只允许 `{}` 中的具体数据按真实状态变化。
6. 下载器栏目允许按“有效数据存在性”收敛：无正在下载时固定显示 `⦁ 正在下载：无`；不再显示状态、0 速度、可转移/做种占位。
7. 禁止 AI 幻想、推测、补全、改写心跳业务数据。
8. 禁止使用聊天上下文当作数据来源。
9. 禁止网页抓取或脆弱日志解析替代 MoviePilot 内部路径。

## 最短真实数据路径
- 时间：Python `datetime.now()` 本地时间。
- 版本：MoviePilot 本地 `version.APP_VERSION / FRONTEND_VERSION`。
- 站点状态：`SiteOper.list_active()` + `SiteOper.get_userdata_latest()`。
- 站点增量：`SiteOper.get_userdata_latest()` + `SiteOper.get_userdata_by_date()` 向前回溯最近基线。
- 下载器：`DownloadChain.downloading()`；无正在下载任务时直接显示 `⦁ 正在下载：无`，不显示速度或无法代表真实做种数的占位字段。
- 入库整理：`TransferHistoryOper.list_by_date(today 00:00:00)`。
- 订阅追新：`/config/agent/runtime/cache/subscribereminder_last_push.json` 当日缓存；无当日缓存时仅用 `SubscribeOper / TmdbChain / MediaChain` 内部回退。
- 存储空间：`shutil.disk_usage()` 只读检测已挂载路径。
- 通知发送：`ChainBase.post_message(Notification(... userid=已绑定 Telegram 用户ID))`。

## 执行方式
```bash
/opt/venv/bin/python /config/heartbeat_report.py
```

成功标准：脚本退出码为 `0` 且输出 `OK`。

## 执行规则
1. 只在系统 `agent_heartbeat` 实际唤醒时执行，不自行推导运行窗口。
2. 不读取聊天上下文生成数据。
3. 不让 AI 参与模板渲染。
4. recurring 任务执行后更新本 Job 的 `last_run`，状态保持 `pending`。
5. 失败时记录错误，保留现场，等待排查。

## 验证记录
- **2026-05-29 14:31** - 已验证 `/config/heartbeat_report.py` 可通过 `py_compile`，并能按锁定模板渲染真实内部数据。

## 执行日志
- **2026-05-29 16:04** - 按少爷要求执行全量心跳 Job 检查并手动触发一次：已清理脚本未用导入与审计字符串缩进等维护性障碍；通过 `py_compile`、三种下载器呈现模拟、栏目顺序断言、旧字段残留断言；随后实际运行 `/opt/venv/bin/python /config/heartbeat_report.py` 发送成功，脚本输出 `OK`；从本次通知日志提取已发送文本复核，确认下载器为 `⦁ 正在下载：无`，无乱码、无 0 速度、无可转移/做种字段，状态保持 pending。
- **2026-05-29 15:30** - 心跳触发执行 `/config/heartbeat_report.py` 成功；脚本退出码 0，输出 OK，固定模板播报已通过内部通知发送；状态保持 pending。
- **2026-05-29 15:10** - 心跳触发执行 `/config/heartbeat_report.py` 成功；脚本退出码 0，输出 OK，固定模板播报已通过内部通知发送；状态保持 pending。
- **2026-05-29 14:36** - 从旧 `simple-heartbeat-report` 蒸馏创建本 Job；固定模板、真实数据路径、执行规则已写入本 Job；后续心跳应以本 Job 为准。
- **2026-05-29 15:22** - 按少爷反馈优化下载器栏目：`TorrentStatus.TRANSFER` 只能代表可转移任务，不能当作真实做种数；无正在下载时下载器栏目直接显示 `⦁ 正在下载：无`，不再输出速度 0 或可转移/做种 0 这类垃圾信息。已通过 `py_compile` 与渲染验证。

- **2026-05-29 15:41** - 按少爷确认的展示口径调整下载器栏目：无任务时显示 `⦁ 正在下载：无`，有任务时显示 `⦁ 正在下载：{数量}`；继续隐藏 0 速度与不可真实确认的做种/可转移字段。已通过编译与渲染断言验证。
- **2026-06-01 13:31** - 误报：报告曾记录“未找到确定性脚本”，后复核脚本实际存在于 `/config/heartbeat_report.py`；根因为心跳 Agent 未按 JOB.md 的“执行方式”读取完整任务详情，只依赖注入摘要判断。
- **2026-06-01 13:54** - 修复调度文档：在 frontmatter description 中加入唯一执行命令；已实际执行 `/opt/venv/bin/python /config/heartbeat_report.py`，脚本退出码 0，输出 OK，固定模板播报已发送；状态保持 pending。
