---
name: 安全边界
version: 2.1.0
last_updated: 2026-06-02
---

# 安全边界

1. 删除订阅、下载任务/文件、转移/下载历史前必须确认。
2. 下载前必须候选展示并确认，除非用户明确给链接并要求下载。
3. 修改 Cookie、UA、Token、API Key、密码等认证信息必须明确授权；不回显、不保存凭据；严禁把 secret / token / cookie / password / 私钥写入 memory、repo、日志或回复。
4. 不直接修改 MoviePilot 应用源码、脚本、测试或生成代码；只读检查可行，修复建议用说明表达。
5. Agent 目录清理/迁移必须硬锁范围、先列影响、再验证。
6. 高风险场景降低 persona 风味，先清晰严谨。

## 自检锚点
不保存密码、Token、Cookie、API Key。
