---
name: 心跳播报固定模板规则
version: 1.0.0
last_updated: 2026-05-29
---

# 心跳播报固定模板规则

## 用户硬性要求
1. 心跳播报模板必须固定，不准乱飘。
2. 当前模板形式必须长期保持：icon 保留、文本标题保留、排版保留、栏目顺序保留。
3. 只允许具体数据随真实状态变化。
4. 数据必须通过真实路径或内部指令获取。
5. 采用最短路径、最快方式获取真实数据。
6. 不准通过幻想、推测、自我 AI 总结、AI 参与生成业务数据。
7. 心跳播报应是确定性脚本/内部接口产物，不需要 AI 参与数据生成。
8. 下载器栏目禁止输出无意义空数据：没有正在下载时固定显示 `⦁ 正在下载：无`；不显示 0 速度；不显示无法真实确认的做种/可转移字段。

## 固定模板版本
`2026-05-29.fixed-v1`

## 固定栏目顺序
1. 问候行：`少爷，{时段}好。给你送上今天的心跳播报。`
2. `🕒 时间：{YYYY-MM-DD HH:mm:ss}`
3. `🤖 MoviePilot：`
4. `📡 站点状态：`
5. `📈 站点增量：`
6. `⬇️ 下载器：`
7. `📦 入库整理：`
8. `📺 订阅追新：`
9. `💾 存储空间：`
10. `✅ 今日摘要：` 或 `⚠️ 今日提醒：`

## 固定数据来源
- 版本：MoviePilot 内部 `version.APP_VERSION / FRONTEND_VERSION`；GitHub Release 只读校验。
- 站点：MoviePilot 内部 `SiteOper.list_active / get_userdata_latest / get_userdata_by_date`。
- 下载器：MoviePilot 内部 `DownloadChain.downloading`；无正在下载时显示 `⦁ 正在下载：无`；不使用 `TorrentStatus.TRANSFER` 冒充做种数。
- 入库：MoviePilot 内部 `TransferHistoryOper.list_by_date`。
- 追新：订阅提醒缓存；必要时仅用 MoviePilot 内部 `SubscribeOper / TmdbChain / MediaChain` 回退。
- 存储：容器本地只读 `shutil.disk_usage` 检测已挂载路径。
- 通知：MoviePilot 内部 `ChainBase.post_message` 直发已绑定 Telegram 用户。

## 禁止事项
1. 禁止 AI 改写模板文案、icon、排版或栏目顺序。
2. 禁止 AI 主观生成、猜测、补全心跳数据。
3. 禁止从聊天上下文、自然语言记忆、日志想象结果。
4. 禁止为了“好看”改变模板结构。
5. 禁止走网页抓取或脆弱文本解析来替代已有内部接口。

## 下载器显示规则补充
1. 下载器栏目禁止输出无实际价值的占位状态。
2. 没有正在下载任务时，固定显示 `⦁ 正在下载：无`，不显示速度。
3. 如果无法真实获取当前正在做种数量，不显示“可转移/做种”这类混淆字段。
4. 有正在下载任务时显示 `⦁ 正在下载：{数量}`，仅在真实速度非零时显示速度。
