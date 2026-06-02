# moviepilot-agent

`moviepilot-agent` 是一个面向 MoviePilot Agent Runtime 的结构化能力资产管理仓库。

它用于组织和维护影响 Agent 行为的可复用资产，包括技能、人格、长期规则、定时任务、自动化脚本与运维知识。项目目标是让 Agent Runtime 在不同 MoviePilot 环境中具备更好的可迁移性、可审计性、可恢复性与持续演进能力。

> 本仓库只保存 Agent 的可维护能力资产，不保存账号、密钥、Cookie、Token、数据库、日志、缓存或其他敏感运行数据。

## 它解决什么问题

MoviePilot Agent 会随着使用不断演进：技能会增加，人格会调整，工作流规则会被优化，定时任务会被创建，运维脚本也会逐渐积累。如果没有结构化仓库，这些资产很容易变得难以追踪、迁移、审计和恢复。

本仓库为 Agent 能力资产提供一个清晰的版本化来源，帮助你：

- 保持不同环境中的 Agent 行为一致
- 对技能、人格、长期规则、任务和脚本进行版本管理
- 在变更影响运行行为前进行审查
- 在迁移、重装或故障后恢复 Agent 能力资产
- 在可复用配置与敏感运行数据之间建立更安全的边界

## 项目定位

`moviepilot-agent` 不是 MoviePilot 主程序源码仓库，也不是完整的 MoviePilot 配置备份仓库。

它维护的是 Agent 能力资产：

- `skills/`：Agent 技能定义与工作流说明
- `runtime/personas/`：运行时人格定义
- `memory/`：长期规则、偏好、安全边界与工作流约束
- `jobs/`：定时任务定义与执行说明
- `scripts/`：维护脚本与自动化工具

## 推荐目录结构

```text
moviepilot-agent/
├── README.md
├── .gitignore
├── skills/
├── runtime/
│   └── personas/
├── memory/
├── jobs/
├── scripts/
```

## 安全边界

提交前必须确认仓库中不包含以下内容：

- API Token、Cookie、密码、私钥
- 站点、下载器、媒体服务器认证信息
- 数据库、日志、缓存、临时文件
- 下载记录中的敏感路径或个人隐私信息
- 任何不适合进入 Git 历史的凭据或运行态数据

推荐提交前检查：

```bash
git status
git diff --cached
```

必要时进行敏感关键词扫描：

```bash
grep -RniE "token|secret|password|cookie|apikey|api_key|authorization|private key" . \
  --exclude-dir=.git \
  --exclude-dir=runtime/cache \
  --exclude='*.log'
```

## 维护原则

- 只同步可复用、可审计、可迁移的 Agent 能力资产
- 不同步运行缓存、活动日志、数据库、密钥和环境绑定凭据
- 每次同步前先检查变更范围
- 重要变更使用清晰的 commit message
- 定时同步必须先做安全扫描，再提交和推送

## 推荐提交规范

```text
feat: add new agent skill
fix: update job execution command
docs: update runtime notes
chore: sync memory rules
refactor: reorganize agent scripts
```

## 恢复建议

在新环境恢复时，建议按以下顺序处理：

1. 安装并启动 MoviePilot
2. 备份新环境现有 `/config/agent`
3. 从本仓库同步需要的目录
4. 检查路径、权限和环境差异
5. 重启或刷新 Agent Runtime
6. 验证技能、人格、任务和规则是否正常加载

不要直接覆盖包含凭据、缓存或环境绑定信息的文件。

## 免责声明

本仓库仅用于维护 MoviePilot Agent 能力资产。使用者应自行确认提交内容不包含敏感信息，并根据自身环境调整路径、权限和同步策略。
