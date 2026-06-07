---
name: MoviePilot Agent 工作流
version: 2.2.0
last_updated: 2026-06-07
---

# MoviePilot Agent 工作流

## 主链路
始终按 MoviePilot 主业务链路执行：站点/认证 → 媒体识别 → 资源发现 → 下载或订阅 → 转移整理 → 媒体库验证 → 状态/历史确认。

## 路由与判断
- 先看会影响当前动作的站点、媒体身份、媒体库和历史上下文。
- 具体业务路由按 `AGENT_SKILLS.md` 执行。
- `search_media` 查元数据，`recognize_media` 解析名称/路径，`query_library_exists` 避免重复。

## 关键业务规则
- 搜不到、下载失败、订阅不更新时先查站点启用、范围、认证与优先级。
- 除用户明确给链接并要求下载外，下载前先展示候选并确认。
- TV 订阅不传 season 时默认仅第 1 季；多季/全剧需逐季添加。
- 下载完成不等于入库完成；入库问题要继续查转移历史与媒体库。
