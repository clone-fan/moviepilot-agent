---
name: Mihomo_Yaml 每日脱敏维护
description: 每日从 10.0.0.2 只读读取 /etc/mihomo/config.yaml，脱敏生成 Mihomo_Yaml 仓库的 mihomo_smart_config.yaml，校验 YAML 并扫描敏感信息；有变更时提交推送。
schedule: recurring
status: pending
last_run: "2026-06-09 21:07"
---
# 任务详情

## 目标
每日维护 `clone-fan/Mihomo_Yaml` 仓库中的脱敏 mihomo smart 配置模板。

## 执行命令

```bash
/opt/venv/bin/python /config/agent/scripts/maintain_mihomo_yaml_repo.py
```

## 执行频率
每日执行一次。执行成功后本 recurring 任务保持 `pending`，只更新 `last_run` 与执行日志。

## 安全边界
- 只读读取 `10.0.0.2:/etc/mihomo/config.yaml`。
- 真实配置仅保存到 `/config/agent/runtime/mihomo/config.raw.yaml`，不进入 Git。
- 提交前执行 YAML 校验和敏感信息扫描。
- 不提交真实订阅 URL、回家端口、密码、cipher、Token、Cookie、私钥。

## 成功判定
脚本输出以下之一即视为成功：

- `OK no_changes`
- `OK committed_and_pushed ...`
## 执行日志

- **2026-06-09 21:07** - 执行每日脱敏维护；结果：OK committed_and_pushed 0e81660；已提交并推送变更，任务保持 pending。
- **2026-06-07 15:23** - 执行每日脱敏维护；结果：OK no_changes；无仓库变更，任务保持 pending。
- **2026-06-03 01:28** - 手动继续执行每日脱敏维护；结果：`OK no_changes`，无仓库变更，任务保持 `pending`。
